"""
schemas.py
──────────
All Pydantic request/response models for the API layer.

Keeping schemas in one file:
  • Avoids circular imports between router.py and other modules.
  • Makes the API contract easy to audit at a glance.
  • Simplifies OpenAPI doc generation (FastAPI introspects these).
"""

from typing import Any
from pydantic import BaseModel, Field


# ── Requests ──────────────────────────────────────────────────────────────────

class QuestionRequest(BaseModel):
    """POST /ask — user question with optional conversation history."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural-language question to answer from the knowledge base",
        examples=["What is Retrieval-Augmented Generation?"],
    )
    conversation_history: list[dict[str, str]] = Field(
        default_factory=list,
        description=(
            "Prior conversation turns for follow-up question support. "
            "Format: [{\"role\": \"user\" | \"assistant\", \"content\": \"...\"}]. "
            "Maximum last 6 turns are used."
        ),
    )
    top_k: int | None = Field(
        default=None,
        ge=1,
        le=20,
        description="Override default retrieval_k for this request (optional)",
    )


# ── Responses ─────────────────────────────────────────────────────────────────

class SourceDocument(BaseModel):
    """One cited source document included in an answer."""
    filename: str = Field(description="Name of the source file")
    snippet: str = Field(description="Relevant excerpt from the document")
    similarity_score: float = Field(
        description="Cosine similarity score [0, 1] — higher = more relevant",
        ge=0.0,
        le=1.0,
    )
    start_index: int | None = Field(
        default=None,
        description="Character offset of this chunk in the original document",
    )


class QuestionResponse(BaseModel):
    """POST /ask — answer with grounded sources and retrieval metadata."""
    question: str
    answer: str
    sources: list[SourceDocument]
    chunks_retrieved: int = Field(
        description="Number of chunks that passed the similarity threshold"
    )


class HistoryEntry(BaseModel):
    """One persisted Q&A interaction."""
    timestamp: str
    question: str
    answer: str = ""
    sources: list[dict[str, Any]] = Field(default_factory=list)
    chunks_retrieved: int = 0
    error: str | None = None


class HistoryResponse(BaseModel):
    entries: list[HistoryEntry]
    total: int


class ClearHistoryResponse(BaseModel):
    removed: int
    message: str


class DeleteHistoryResponse(BaseModel):
    """DELETE /history/{index} — result of deleting one entry."""
    deleted: bool
    index: int
    message: str


class HealthResponse(BaseModel):
    """GET /health — system readiness."""
    status: str
    groq_model: str
    embedding_model: str
    vector_store_ready: bool
    total_vectors: int | None = Field(
        default=None,
        description="Total embeddings in the FAISS index (None if not loaded)",
    )
    chunk_size: int
    retrieval_k: int


class IngestResponse(BaseModel):
    """POST /ingest — ingestion result."""
    message: str
    documents_loaded: int | None = None
    chunks_indexed: int | None = None
