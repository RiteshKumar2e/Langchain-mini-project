"""
retriever.py
────────────
Retrieval orchestration layer — sits between the vector store and the LLM chain.

Responsibilities:
  • Load the persisted FAISS index.
  • Perform similarity_search_with_score so callers get relevance scores.
  • Apply the configurable score threshold to filter low-relevance chunks.
  • Deduplicate sources so we never cite the same file twice.
  • Return both the context string (for the prompt) and structured SourceDocument
    metadata (for the API response).

This module deliberately does NOT call the LLM — that is rag_pipeline.py's job.
Keeping retrieval separate makes it trivially testable and swappable (e.g. Chroma,
Pinecone, hybrid BM25+dense) without touching chain logic.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from langchain_community.vectorstores import FAISS

from config import settings
from embeddings import get_embeddings
from logger import get_logger

log = get_logger(__name__)


@dataclass
class RetrievedChunk:
    """Structured representation of one retrieved document chunk."""
    content: str
    filename: str
    source_path: str
    similarity_score: float
    start_index: int | None


@lru_cache(maxsize=1)
def _load_vector_store() -> FAISS:
    """Load and cache the FAISS index from disk (loads only once per process)."""
    store_path = settings.store_path
    if not store_path.exists():
        raise FileNotFoundError(
            f"Vector store not found at '{store_path}'. "
            "Run `python ingestor.py` to build the index first."
        )
    log.info("Loading FAISS index from '%s'", store_path)
    vs = FAISS.load_local(
        str(store_path),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )
    log.info("FAISS index loaded — %d vectors total", vs.index.ntotal)
    return vs


def get_vector_store() -> FAISS:
    """Public accessor for the cached vector store."""
    return _load_vector_store()


def invalidate_vector_store_cache() -> None:
    """Clear the lru_cache after a re-ingestion so the new index is loaded."""
    _load_vector_store.cache_clear()
    log.info("Vector store cache invalidated — will reload on next request")


def retrieve(query: str) -> list[RetrievedChunk]:
    """
    Embed the query, search FAISS, apply threshold filtering, and return
    a list of RetrievedChunk objects ordered by similarity (highest first).

    Args:
        query: The natural-language question from the user.

    Returns:
        List of RetrievedChunk, filtered by settings.retrieval_score_threshold.
    """
    vs = get_vector_store()
    raw: list[tuple[Any, float]] = vs.similarity_search_with_score(
        query, k=settings.retrieval_k
    )

    chunks: list[RetrievedChunk] = []
    for doc, raw_score in raw:
        # FAISS returns L2 distance (lower = better); convert to [0,1] similarity
        # using a simple inversion so 0 distance → 1.0 similarity.
        similarity = float(max(0.0, 1.0 - raw_score / 2.0))

        if similarity < settings.retrieval_score_threshold:
            log.debug(
                "Filtered chunk (score %.3f < threshold %.3f): %s",
                similarity, settings.retrieval_score_threshold,
                doc.metadata.get("source", "?")[:60],
            )
            continue

        meta = doc.metadata or {}
        source_path: str = meta.get("source", "unknown")
        filename = source_path.replace("\\", "/").split("/")[-1]

        chunks.append(RetrievedChunk(
            content=doc.page_content,
            filename=filename,
            source_path=source_path,
            similarity_score=round(similarity, 4),
            start_index=meta.get("start_index"),
        ))

    log.info(
        "Retrieved %d/%d chunks for query %r (threshold=%.2f)",
        len(chunks), len(raw),
        query[:60],
        settings.retrieval_score_threshold,
    )
    return chunks


def build_context(chunks: list[RetrievedChunk]) -> str:
    """
    Concatenate chunk contents into a single context block for the prompt.
    Each chunk is prefixed with its source filename for transparency.
    """
    if not chunks:
        return "No relevant context found in the knowledge base."
    parts = [
        f"[Source: {c.filename}]\n{c.content}"
        for c in chunks
    ]
    return "\n\n---\n\n".join(parts)


def deduplicate_sources(chunks: list[RetrievedChunk]) -> list[dict]:
    """
    Collapse multiple chunks from the same file into one source citation.
    Returns the highest-scoring chunk per file for the citation.
    """
    seen: dict[str, RetrievedChunk] = {}
    for chunk in chunks:
        if chunk.filename not in seen or chunk.similarity_score > seen[chunk.filename].similarity_score:
            seen[chunk.filename] = chunk

    return [
        {
            "filename": c.filename,
            "snippet": c.content[:350].strip() + ("…" if len(c.content) > 350 else ""),
            "similarity_score": c.similarity_score,
            "start_index": c.start_index,
        }
        for c in seen.values()
    ]
