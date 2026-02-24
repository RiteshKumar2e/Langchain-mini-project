"""
rag_pipeline.py
───────────────
Core RAG (Retrieval-Augmented Generation) pipeline.

Responsibilities:
  • Initialise / cache the LLM based on the configured provider.
  • Build a retrieval-augmented QA chain with source attribution.
  • Expose a single `ask()` function used by the API layer.
"""

from functools import lru_cache
from typing import Any

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.language_models import BaseLanguageModel

from config import settings
from embeddings import get_embeddings
from logger import get_logger

log = get_logger(__name__)

# ── Prompt template ──────────────────────────────────────────────────────────
RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful and knowledgeable AI assistant.
Use ONLY the context below to answer the user's question.
If the context does not contain enough information to fully answer the question,
say so clearly and do not make up information.

Context:
{context}

Question: {question}

Answer:""",
)


@lru_cache(maxsize=1)
def get_llm() -> BaseLanguageModel:
    """Return a cached LLM instance based on the configured provider."""
    provider = settings.llm_provider.lower()
    log.info("Initialising LLM — provider: %s", provider)

    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set when llm_provider=openai")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.2,
        )

    if provider == "groq":
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY must be set when llm_provider=groq")
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=settings.groq_model,
            groq_api_key=settings.groq_api_key,
            temperature=0.2,
        )

    raise ValueError(
        f"Unknown llm_provider='{provider}'. Choose 'openai' or 'groq'."
    )


def load_vector_store() -> FAISS:
    """Load the persisted FAISS index from disk."""
    store_path = settings.store_path
    if not store_path.exists():
        raise FileNotFoundError(
            f"Vector store not found at '{store_path}'. "
            "Run `python ingestor.py` first to build the index."
        )
    log.info("Loading vector store from '%s'", store_path)
    return FAISS.load_local(
        str(store_path),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def build_qa_chain(vectorstore: FAISS) -> RetrievalQA:
    """Compose the retrieval + generation chain."""
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retrieval_k},
    )
    chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": RAG_PROMPT},
    )
    log.info("QA chain built (retrieval_k=%d)", settings.retrieval_k)
    return chain


def format_sources(source_docs: list) -> list[dict[str, Any]]:
    """Extract citation-friendly metadata from retrieved documents."""
    seen: set[str] = set()
    sources: list[dict] = []

    for doc in source_docs:
        meta = doc.metadata or {}
        source_file = meta.get("source", "Unknown")
        # Normalise path separators and extract filename
        filename = source_file.replace("\\", "/").split("/")[-1]

        # Deduplicate by filename
        if filename in seen:
            continue
        seen.add(filename)

        sources.append(
            {
                "filename": filename,
                "snippet": doc.page_content[:300].strip() + "…",
                "start_index": meta.get("start_index"),
            }
        )

    return sources


# ── Module-level singletons initialised lazily on first request ──────────────
_vectorstore: FAISS | None = None
_qa_chain: RetrievalQA | None = None


def get_qa_chain() -> RetrievalQA:
    """Return the (lazily initialised) singleton QA chain."""
    global _vectorstore, _qa_chain
    if _qa_chain is None:
        _vectorstore = load_vector_store()
        _qa_chain = build_qa_chain(_vectorstore)
    return _qa_chain


def ask(question: str) -> dict[str, Any]:
    """
    Main entry point for the RAG pipeline.

    Returns:
        {
          "answer": str,
          "sources": [{"filename": str, "snippet": str, ...}]
        }
    """
    if not question.strip():
        raise ValueError("Question must not be empty.")

    log.info("Processing question: %r", question[:120])
    chain = get_qa_chain()
    result = chain.invoke({"query": question})

    answer = result.get("result", "").strip()
    sources = format_sources(result.get("source_documents", []))

    log.info("Answer generated (%d chars, %d source(s))", len(answer), len(sources))
    return {"answer": answer, "sources": sources}
