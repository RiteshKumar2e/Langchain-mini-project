"""
main.py
───────
FastAPI application entry point.

Startup sequence:
  1. Configure CORS.
  2. Attempt to pre-warm the RAG pipeline (non-fatal if index missing).
  3. Mount all routes via the router module.

Run with:
    uvicorn main:app --reload --port 8000
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
    """Pre-warm the QA chain on startup so the first request is fast."""
    log.info("═══════════════════════════════════════════")
    log.info("  LangChain RAG API — starting up")
    log.info("  LLM provider   : %s", settings.llm_provider)
    log.info("  Embeddings     : %s", settings.embedding_provider)
    log.info("  Vector store   : %s", settings.store_path)
    log.info("═══════════════════════════════════════════")

    try:
        from rag_pipeline import get_qa_chain
        get_qa_chain()
        log.info("QA chain pre-warmed successfully.")
    except FileNotFoundError:
        log.warning(
            "Vector store not found — run `python ingestor.py` to build the index. "
            "The /ask endpoint will return 503 until then."
        )
    except Exception as exc:
        log.warning("Could not pre-warm QA chain: %s", exc)

    yield  # Application is running

    log.info("LangChain RAG API — shutting down.")


app = FastAPI(
    title="LangChain RAG API",
    description=(
        "A Retrieval-Augmented Generation (RAG) API built with LangChain and FastAPI. "
        "Submit questions and receive answers grounded in a curated knowledge base."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ───────────────────────────────────────────────────────────────────
app.include_router(router, prefix="/api")


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "LangChain RAG API is running.",
        "docs": "/docs",
        "health": "/api/health",
    }
