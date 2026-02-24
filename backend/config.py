"""
config.py
─────────
Single source of truth for all runtime configuration.
All values are loaded from environment variables (.env) via pydantic-settings.
No module should ever call os.getenv() directly.
"""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── LLM — Groq ──────────────────────────────────────────────────────────
    groq_api_key: str = Field(default="", description="Groq API key")
    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model identifier. Alternatives: mixtral-8x7b-32768, gemma2-9b-it",
    )
    llm_temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="LLM sampling temperature (0 = deterministic, 1 = creative)",
    )

    # ── Embeddings — HuggingFace (free, local) ───────────────────────────────
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence-transformer model for dense embeddings",
    )

    # ── Paths ────────────────────────────────────────────────────────────────
    documents_path: str = Field(default="./documents", description="Folder with source documents")
    vector_store_path: str = Field(default="./vector_store", description="FAISS index persist dir")

    # ── Text splitting ───────────────────────────────────────────────────────
    chunk_size: int = Field(default=500, ge=100, description="Target characters per chunk")
    chunk_overlap: int = Field(default=50, ge=0, description="Overlap characters between chunks")

    # ── Retrieval ────────────────────────────────────────────────────────────
    retrieval_k: int = Field(default=5, ge=1, le=20, description="Top-K docs to retrieve per query")
    retrieval_score_threshold: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score to include a source (0 = include all)",
    )

    # ── CORS ─────────────────────────────────────────────────────────────────
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated allowed CORS origins",
    )

    # ── Feature flags ────────────────────────────────────────────────────────
    enable_conversation_memory: bool = Field(
        default=True,
        description="Pass conversation history to the LLM for follow-up support",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ── Derived properties ────────────────────────────────────────────────────

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.replace(" ", ",").split(",") if o.strip()]

    @property
    def docs_path(self) -> Path:
        return Path(self.documents_path)

    @property
    def store_path(self) -> Path:
        return Path(self.vector_store_path)


# Singleton — import this everywhere
settings = Settings()
