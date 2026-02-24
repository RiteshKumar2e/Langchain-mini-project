"""
ingestor.py
───────────
Document ingestion pipeline:
  1. Load — read all .md / .txt / .pdf files from the documents folder.
  2. Split — RecursiveCharacterTextSplitter (chunk_size=500, overlap=50 by default).
  3. Embed — HuggingFace sentence-transformers (all-MiniLM-L6-v2, runs locally).
  4. Store — persist FAISS index to disk.

Returns the FAISS vectorstore + document count so the caller can report stats.

Run standalone:
    python ingestor.py

Or trigger via API:
    POST /api/ingest
"""

import sys
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_community.vectorstores import FAISS

from config import settings
from embeddings import get_embeddings
from logger import get_logger

log = get_logger(__name__)

# ── Loader registry ────────────────────────────────────────────────────────────
# Maps file extensions → loader class / kwargs.
# Add new formats here (e.g. PyPDFLoader) without touching the rest of the code.
LOADER_MAP = {
    "**/*.md":  (TextLoader, {"encoding": "utf-8", "autodetect_encoding": True}),
    "**/*.txt": (TextLoader, {"encoding": "utf-8", "autodetect_encoding": True}),
}

# PDF support is optional — only include if unstructured is available
try:
    from langchain_community.document_loaders import PyPDFLoader  # noqa: F401
    LOADER_MAP["**/*.pdf"] = (PyPDFLoader, {})
    log.debug("PDF loader available")
except ImportError:
    log.debug("PyPDFLoader not available — PDFs will be skipped")


def load_documents(docs_path: Path) -> list:
    """
    Load all supported documents from docs_path.
    Uses per-extension loaders so each file type is handled correctly.
    """
    if not docs_path.exists():
        raise FileNotFoundError(
            f"Documents directory '{docs_path}' not found. "
            "Create it and add your documents."
        )

    all_docs = []
    for glob_pattern, (loader_cls, loader_kwargs) in LOADER_MAP.items():
        loader = DirectoryLoader(
            str(docs_path),
            glob=glob_pattern,
            loader_cls=loader_cls,
            loader_kwargs=loader_kwargs if loader_kwargs else None,
            show_progress=False,
            use_multithreading=True,
            silent_errors=True,
        )
        docs = loader.load()
        if docs:
            log.info("Loaded %d file(s) via %s (pattern=%s)", len(docs), loader_cls.__name__, glob_pattern)
        all_docs.extend(docs)

    if not all_docs:
        raise ValueError(
            f"No documents found in '{docs_path}'. "
            "Add .md, .txt, or .pdf files and re-run ingestion."
        )

    log.info("Total documents loaded: %d", len(all_docs))
    return all_docs


def split_documents(documents: list) -> list:
    """
    Split documents into overlapping chunks optimised for RAG retrieval.

    chunk_size and chunk_overlap are read from settings so they can be
    adjusted via .env without touching code.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        add_start_index=True,      # persists character offset in metadata
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    log.info(
        "Split %d documents → %d chunks (size=%d, overlap=%d)",
        len(documents), len(chunks),
        settings.chunk_size, settings.chunk_overlap,
    )
    return chunks


def build_vector_store(chunks: list) -> FAISS:
    """Embed chunks and build the FAISS index."""
    log.info("Embedding %d chunks — this may take a moment…", len(chunks))
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    log.info("FAISS index built — %d vectors", vectorstore.index.ntotal)
    return vectorstore


def persist_vector_store(vectorstore: FAISS) -> None:
    """Save the FAISS index to disk."""
    store_path = settings.store_path
    store_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(store_path))
    log.info("Vector store persisted to '%s'", store_path)


def ingest(force_rebuild: bool = True) -> tuple:
    """
    Full ingestion pipeline. Called by `python ingestor.py` or POST /api/ingest.

    Returns:
        (vectorstore, document_count) — caller uses ntotal and count for API response.
    """
    log.info("=== Ingestion started (force_rebuild=%s) ===", force_rebuild)

    store_path = settings.store_path
    if not force_rebuild and store_path.exists():
        log.info("Index already exists and force_rebuild=False — skipping.")
        embeddings = get_embeddings()
        vs = FAISS.load_local(
            str(store_path), embeddings, allow_dangerous_deserialization=True
        )
        return vs, 0

    docs_path = settings.docs_path
    documents = load_documents(docs_path)
    chunks = split_documents(documents)
    vectorstore = build_vector_store(chunks)
    persist_vector_store(vectorstore)

    log.info("=== Ingestion complete: %d docs → %d chunks ===", len(documents), len(chunks))
    return vectorstore, len(documents)


# ── CLI entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    try:
        _vs, _doc_count = ingest(force_rebuild=True)
        print(f"[OK] Ingestion complete: {_doc_count} document(s), {_vs.index.ntotal} chunk(s) indexed.")
        sys.exit(0)
    except Exception as _exc:
        print(f"[ERROR] Ingestion failed: {_exc}", file=sys.stderr)
        sys.exit(1)
