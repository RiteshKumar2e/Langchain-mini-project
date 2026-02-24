"""
ingestor.py
───────────
Handles the offline indexing phase of the RAG pipeline:

  1. Load all .md / .txt documents from the configured documents folder.
  2. Split them into overlapping chunks with RecursiveCharacterTextSplitter.
  3. Embed chunks and persist them in a FAISS vector store on disk.

Run directly to rebuild the index:
    python ingestor.py
"""

import shutil
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import settings
from embeddings import get_embeddings
from logger import get_logger

log = get_logger(__name__)


def load_documents():
    """Load all Markdown and plain-text files from the documents directory."""
    docs_path = settings.docs_path

    if not docs_path.exists():
        raise FileNotFoundError(f"Documents directory not found: {docs_path}")

    # Load markdown files
    md_loader = DirectoryLoader(
        str(docs_path),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        use_multithreading=True,
    )
    # Load plain text files
    txt_loader = DirectoryLoader(
        str(docs_path),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        use_multithreading=True,
    )

    docs = md_loader.load() + txt_loader.load()
    log.info("Loaded %d raw document(s) from '%s'", len(docs), docs_path)
    return docs


def split_documents(docs):
    """Split documents into overlapping chunks suitable for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
        add_start_index=True,        # Adds metadata: start_index
    )
    chunks = splitter.split_documents(docs)
    log.info(
        "Split %d doc(s) into %d chunk(s) "
        "(chunk_size=%d, overlap=%d)",
        len(docs), len(chunks),
        settings.chunk_size, settings.chunk_overlap,
    )
    return chunks


def build_vector_store(chunks, force_rebuild: bool = False) -> FAISS:
    """Embed chunks and save/load a FAISS vector store."""
    store_path = settings.store_path

    if store_path.exists() and not force_rebuild:
        log.info("Vector store already exists at '%s'. Loading…", store_path)
        return FAISS.load_local(
            str(store_path),
            get_embeddings(),
            allow_dangerous_deserialization=True,
        )

    if store_path.exists():
        log.info("Force-rebuild requested — removing existing store.")
        shutil.rmtree(store_path)

    log.info("Building FAISS vector store — this may take a moment…")
    vectorstore = FAISS.from_documents(chunks, get_embeddings())
    store_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(store_path))
    log.info("Vector store saved to '%s' (%d vectors).", store_path, vectorstore.index.ntotal)
    return vectorstore


def ingest(force_rebuild: bool = False) -> FAISS:
    """Full ingestion pipeline: load → split → embed → store."""
    docs = load_documents()
    chunks = split_documents(docs)
    return build_vector_store(chunks, force_rebuild=force_rebuild)


# ── CLI entry point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build the RAG knowledge-base index.")
    parser.add_argument(
        "--force", action="store_true",
        help="Delete and rebuild the vector store even if it already exists."
    )
    args = parser.parse_args()

    try:
        ingest(force_rebuild=args.force)
        print("\n✅ Ingestion complete. You can now start the API server.")
    except Exception as exc:
        log.exception("Ingestion failed: %s", exc)
        raise SystemExit(1) from exc
