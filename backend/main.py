"""
main.py
───────
FastAPI application factory and startup lifecycle.

Architecture overview:
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  HTTP Clients  →  FastAPI (main.py)                                      │
  │                      └─ /api/* → router.py                              │
  │                            ├─ rag_pipeline.py  (LLM generation)         │
  │                            │    └─ retriever.py (FAISS retrieval)       │
  │                            │         └─ embeddings.py                   │
  │                            ├─ ingestor.py       (document indexing)     │
  │                            └─ history.py        (JSONL persistence)     │
  └──────────────────────────────────────────────────────────────────────────┘

Run locally:
    uvicorn main:app --reload --port 8000

Interactive docs:
    http://localhost:8000/docs    (Swagger UI)
    http://localhost:8000/redoc  (ReDoc)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from logger import get_logger
from router import router

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: log configuration summary and pre-warm the retrieval layer
    so the first user request is fast.
    Shutdown: no cleanup needed (FAISS is file-based, no connections to close).
    """
    log.info("═" * 55)
    log.info("  LangChain RAG Platform  —  starting up")
    log.info("  LLM model     : %s", settings.groq_model)
    log.info("  Embedding     : %s", settings.embedding_model)
    log.info("  Temperature   : %.1f", settings.llm_temperature)
    log.info("  Chunk size    : %d (overlap %d)", settings.chunk_size, settings.chunk_overlap)
    log.info("  Retrieval K   : %d", settings.retrieval_k)
    log.info("  Memory        : %s", "enabled" if settings.enable_conversation_memory else "disabled")
    log.info("  Vector store  : %s", settings.store_path)
    log.info("═" * 55)

    # Pre-warm: attempt to load the vector store into cache on startup
    if settings.store_path.exists():
        try:
            from retriever import get_vector_store
            vs = get_vector_store()
            log.info("Vector store ready — %d embeddings pre-loaded", vs.index.ntotal)
        except Exception as exc:
            log.warning("Could not pre-load vector store: %s", exc)
    else:
        log.warning(
            "Vector store not found at '%s'. "
            "Call POST /api/ingest or run `python ingestor.py` before querying.",
            settings.store_path,
        )

    yield  # Application is live

    log.info("LangChain RAG Platform — shutdown complete")


# ── Application ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="LangChain RAG Platform",
    description=(
        "Production-ready Retrieval-Augmented Generation API built with "
        "LangChain, FAISS, and Groq. Submit natural-language questions and "
        "receive grounded answers with source citations and similarity scores."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "RAG", "description": "Retrieval-Augmented Generation endpoints"},
        {"name": "System", "description": "Health, history, and management endpoints"},
    ],
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────────────
app.include_router(router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    """Redirect hint — point users to the docs."""
    return {
        "message": "LangChain RAG Platform API is running.",
        "docs": "/docs",
        "health": "/api/health",
    }
