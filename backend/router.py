"""
router.py
─────────
FastAPI APIRouter with all RAG-related endpoints.

Routes:
  POST /ask           — Ask a question, get an answer + sources
  GET  /health        — Liveness / readiness probe
  GET  /history       — Last 10 interactions
  POST /history/clear — Wipe history
  POST /ingest        — Re-index documents (admin use)
"""

from fastapi import APIRouter, HTTPException, status

import history as hist
import rag_pipeline as rag
from config import settings
from logger import get_logger
from schemas import (
    ClearHistoryResponse,
    HealthResponse,
    HistoryResponse,
    IngestResponse,
    QuestionRequest,
    QuestionResponse,
    SourceDocument,
)

log = get_logger(__name__)
router = APIRouter()


# ── POST /ask ────────────────────────────────────────────────────────────────

@router.post(
    "/ask",
    response_model=QuestionResponse,
    summary="Ask a question",
    description="Submit a natural-language question. The RAG pipeline retrieves relevant context "
                "from the knowledge base and returns a grounded answer with source citations.",
)
async def ask_question(body: QuestionRequest) -> QuestionResponse:
    question = body.question.strip()
    log.info("Received question: %r", question[:120])

    try:
        result = rag.ask(question)
    except FileNotFoundError as exc:
        # Vector store not yet built
        log.error("Vector store missing: %s", exc)
        hist.log_entry(question, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Knowledge base not ready. Run `python ingestor.py` first.",
        ) from exc
    except Exception as exc:
        log.exception("Error during RAG pipeline: %s", exc)
        hist.log_entry(question, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating the answer: {exc}",
        ) from exc

    answer: str = result["answer"]
    raw_sources: list[dict] = result["sources"]

    # Persist to history
    hist.log_entry(question, answer=answer, sources=raw_sources)

    return QuestionResponse(
        question=question,
        answer=answer,
        sources=[SourceDocument(**s) for s in raw_sources],
    )


# ── GET /health ──────────────────────────────────────────────────────────────

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
async def health_check() -> HealthResponse:
    vector_store_ready = settings.store_path.exists()
    return HealthResponse(
        status="ok",
        llm_provider=settings.llm_provider,
        embedding_provider=settings.embedding_provider,
        vector_store_ready=vector_store_ready,
    )


# ── GET /history ─────────────────────────────────────────────────────────────

@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Retrieve recent Q&A history",
)
async def get_history(limit: int = 10) -> HistoryResponse:
    entries = hist.get_recent(n=max(1, min(limit, 100)))
    return HistoryResponse(entries=entries, total=len(entries))


# ── POST /history/clear ──────────────────────────────────────────────────────

@router.post(
    "/history/clear",
    response_model=ClearHistoryResponse,
    summary="Clear all history",
)
async def clear_history() -> ClearHistoryResponse:
    removed = hist.clear()
    return ClearHistoryResponse(
        removed=removed,
        message=f"Cleared {removed} history entry/entries.",
    )


# ── POST /ingest ─────────────────────────────────────────────────────────────

@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Re-index documents (admin)",
    description="Triggers a full re-ingestion of the documents folder and rebuilds the FAISS index.",
)
async def ingest_documents(force: bool = True) -> IngestResponse:
    try:
        from ingestor import ingest
        vectorstore = ingest(force_rebuild=force)

        # Invalidate the cached QA chain so it reloads with the new index
        import rag_pipeline
        rag_pipeline._vectorstore = None
        rag_pipeline._qa_chain = None

        return IngestResponse(
            message="Ingestion complete. Index rebuilt successfully.",
            chunks_indexed=vectorstore.index.ntotal,
        )
    except Exception as exc:
        log.exception("Ingestion failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {exc}",
        ) from exc
