"""
embeddings.py
─────────────
Returns a cached HuggingFace embedding model (all-MiniLM-L6-v2).
Completely free and runs locally — no API key needed.
"""

from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from config import settings
from logger import get_logger

log = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Return a cached HuggingFace sentence-transformer embedding model."""
    log.info("Initialising embeddings — model: %s", settings.embedding_model)
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
