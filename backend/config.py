"""
config.py
─────────
Centralised settings loaded from environment variables via pydantic-settings.
Every other module imports from here — no scattered os.getenv calls.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── LLM (Groq) ───────────────────────────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # ── Embeddings (HuggingFace — free, local) ───────────────────────────
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ── Paths ────────────────────────────────────────────────────────────
    documents_path: str = "./documents"
    vector_store_path: str = "./vector_store"

    # ── Chunking ─────────────────────────────────────────────────────────
    chunk_size: int = 800
    chunk_overlap: int = 100

    # ── Retrieval ────────────────────────────────────────────────────────
    retrieval_k: int = 5

    # ── CORS ─────────────────────────────────────────────────────────────
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.replace(" ", ",").split(",") if o.strip()]

    @property
    def docs_path(self) -> Path:
        return Path(self.documents_path)

    @property
    def store_path(self) -> Path:
        return Path(self.vector_store_path)


# Single shared instance used by the whole application
settings = Settings()
