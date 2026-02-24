"""
embeddings.py
─────────────
Factory that returns the configured embedding model.

Supported providers:
  • "huggingface"  → sentence-transformers/all-MiniLM-L6-v2 (free, local)
  • "openai"       → text-embedding-3-small (requires OPENAI_API_KEY)
"""

from functools import lru_cache

from langchain_core.embeddings import Embeddings

from config import settings
from logger import get_logger

log = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:
    """Return a cached embedding model based on the configured provider."""

    provider = settings.embedding_provider.lower()
    log.info("Initialising embeddings — provider: %s", provider)

    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when embedding_provider=openai")
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.openai_api_key,
        )

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    raise ValueError(
        f"Unknown embedding_provider='{provider}'. Choose 'openai' or 'huggingface'."
    )
