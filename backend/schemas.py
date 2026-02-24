"""
schemas.py
──────────
Pydantic request / response models shared between the router and tests.
Keeping schemas separate avoids circular imports and makes the API contract
easy to discover.
"""

from typing import Any
from pydantic import BaseModel, Field


# ── Request ──────────────────────────────────────────────────────────────────

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000, description="The user's question")
    conversation_history: list[dict[str, str]] = Field(
        default_factory=list,
        description="Optional prior turns: [{'role': 'user'|'assistant', 'content': '...'}]",
    )


# ── Response ─────────────────────────────────────────────────────────────────

class SourceDocument(BaseModel):
    filename: str
    snippet: str
    start_index: int | None = None


class QuestionResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
    question: str


class HistoryEntry(BaseModel):
    timestamp: str
    question: str
    answer: str
    sources: list[dict[str, Any]]
    error: str | None = None


class HistoryResponse(BaseModel):
    entries: list[HistoryEntry]
    total: int


class ClearHistoryResponse(BaseModel):
    removed: int
    message: str


class HealthResponse(BaseModel):
    status: str
    llm_provider: str
    embedding_provider: str
    vector_store_ready: bool


class IngestResponse(BaseModel):
    message: str
    chunks_indexed: int | None = None
