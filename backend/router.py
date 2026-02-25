"""
router.py
─────────
FastAPI APIRouter — HTTP edge layer only.

Each endpoint is intentionally thin:
  • Parse + validate the request (Pydantic does this automatically).
  • Delegate to the appropriate domain module (rag_pipeline, history, ingestor).
  • Map domain exceptions to appropriate HTTP status codes.
  • Return the response model (FastAPI serialises it to JSON).

No business logic lives here.
"""

from fastapi import APIRouter, HTTPException, Query, status

import history as hist
import rag_pipeline as rag
from config import settings
from logger import get_logger
from schemas import (
    ClearHistoryResponse,
    DeleteHistoryResponse,
    HealthResponse,
    HistoryResponse,
    IngestResponse,
    QuestionRequest,
    QuestionResponse,
    SourceDocument,
)

log = get_logger(__name__)
router = APIRouter()


# ══════════════════════════════════════════════════════════════════════════════
# POST /ask
# ══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/ask",
    response_model=QuestionResponse,
    summary="Ask a question",
    description=(
        "Submit a natural-language question. The RAG pipeline retrieves the most "
        "relevant context chunks from the knowledge base, injects them into the LLM "
        "prompt, and returns a grounded answer with source citations and similarity scores."
    ),
    tags=["RAG"],
)
async def ask_question(body: QuestionRequest) -> QuestionResponse:
    question = body.question.strip()
    log.info("POST /ask | question=%r | history_turns=%d", question[:80], len(body.conversation_history))

    # Allow per-request top_k override
    if body.top_k is not None:
        original_k = settings.retrieval_k
        settings.retrieval_k = body.top_k
        log.debug("top_k override: %d → %d", original_k, body.top_k)

    try:
        result = rag.ask(
            question=question,
            conversation_history=body.conversation_history or [],
        )
    except FileNotFoundError as exc:
        log.error("Vector store missing — user must run ingestor: %s", exc)
        hist.log_entry(question, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Knowledge base index not found. "
                "Call POST /api/ingest first or run `python ingestor.py` manually."
            ),
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        log.exception("Unhandled error in RAG pipeline: %s", exc)
        hist.log_entry(question, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Answer generation failed: {exc}",
        ) from exc
    finally:
        # Restore top_k if it was overridden
        if body.top_k is not None:
            settings.retrieval_k = original_k  # type: ignore[possibly-undefined]

    answer: str = result["answer"]
    raw_sources: list[dict] = result["sources"]
    chunks_retrieved: int = result["chunks_retrieved"]

    hist.log_entry(
        question,
        answer=answer,
        sources=raw_sources,
        chunks_retrieved=chunks_retrieved,
    )

    return QuestionResponse(
        question=question,
        answer=answer,
        sources=[SourceDocument(**s) for s in raw_sources],
        chunks_retrieved=chunks_retrieved,
    )


# ══════════════════════════════════════════════════════════════════════════════
# GET /health
# ══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health & readiness check",
    description="Returns system status, configuration metadata, and vector store readiness.",
    tags=["System"],
)
async def health_check() -> HealthResponse:
    vector_store_ready = settings.store_path.exists()
    total_vectors: int | None = None

    if vector_store_ready:
        try:
            from retriever import get_vector_store
            vs = get_vector_store()
            total_vectors = vs.index.ntotal
        except Exception:
            pass  # non-fatal — store path exists but index may be stale

    return HealthResponse(
        status="ok",
        groq_model=settings.groq_model,
        embedding_model=settings.embedding_model,
        vector_store_ready=vector_store_ready,
        total_vectors=total_vectors,
        chunk_size=settings.chunk_size,
        retrieval_k=settings.retrieval_k,
    )


# ══════════════════════════════════════════════════════════════════════════════
# POST /ingest
# ══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest and re-index documents",
    description=(
        "Triggers a full ingestion of the `documents/` folder: load → split → embed → "
        "persist FAISS index. Existing index is overwritten. Use when documents are added "
        "or updated. Returns counts of documents loaded and chunks indexed."
    ),
    tags=["RAG"],
)
async def ingest_documents(force: bool = Query(default=True, description="Force rebuild even if index exists")) -> IngestResponse:
    try:
        from ingestor import ingest
        vectorstore, doc_count = ingest(force_rebuild=force)

        # Invalidate the cached vector store so next /ask reloads the fresh index
        from retriever import invalidate_vector_store_cache
        invalidate_vector_store_cache()

        chunks_indexed: int = vectorstore.index.ntotal
        log.info("Ingestion complete — %d docs, %d chunks", doc_count, chunks_indexed)

        return IngestResponse(
            message=f"Ingestion complete. {doc_count} document(s) processed.",
            documents_loaded=doc_count,
            chunks_indexed=chunks_indexed,
        )
    except Exception as exc:
        log.exception("Ingestion failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {exc}",
        ) from exc


# ══════════════════════════════════════════════════════════════════════════════
# GET /history
# ══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="List recent Q&A interactions",
    tags=["System"],
)
async def get_history(
    limit: int = Query(default=10, ge=1, le=100, description="Max number of entries to return"),
) -> HistoryResponse:
    entries = hist.get_recent(n=limit)
    return HistoryResponse(entries=entries, total=len(entries))


# ══════════════════════════════════════════════════════════════════════════════
# POST /history/clear
# ══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/history/clear",
    response_model=ClearHistoryResponse,
    summary="Clear all conversation history",
    tags=["System"],
)
async def clear_history() -> ClearHistoryResponse:
    removed = hist.clear()
    return ClearHistoryResponse(
        removed=removed,
        message=f"Cleared {removed} history entry/entries.",
    )


# ══════════════════════════════════════════════════════════════════════════════
# DELETE /history/{index}
# ══════════════════════════════════════════════════════════════════════════════

@router.delete(
    "/history/{index}",
    response_model=DeleteHistoryResponse,
    summary="Delete a single history entry by its index",
    description=(
        "Deletes one entry from the history log by its 0-based position in the "
        "full chronological list. The index is assigned by the backend at fetch time."
    ),
    tags=["System"],
)
async def delete_history_entry(index: int) -> DeleteHistoryResponse:
    deleted = hist.delete_entry(index)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History entry at index {index} not found.",
        )
    return DeleteHistoryResponse(
        deleted=True,
        index=index,
        message=f"Entry {index} deleted successfully.",
    )
