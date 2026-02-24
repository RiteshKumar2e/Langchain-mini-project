"""
rag_pipeline.py
───────────────
Core RAG pipeline using Groq as the LLM and FAISS as the vector store.

Exposes a single `ask()` function used by the API layer.
"""

from typing import Any

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

from config import settings
from embeddings import get_embeddings
from logger import get_logger

log = get_logger(__name__)

# ── Prompt ───────────────────────────────────────────────────────────────────
RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful and knowledgeable AI assistant.
Use ONLY the context below to answer the user's question.
If the context does not contain enough information to fully answer the question,
say so clearly — do not make up information.

Context:
{context}

Question: {question}

Answer:""",
)


def get_llm() -> ChatGroq:
    """Return a Groq LLM instance (reads key fresh from settings each call)."""
    if not settings.groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Add it to backend/.env and restart the server."
        )
    log.info("Initialising Groq LLM — model: %s", settings.groq_model)
    return ChatGroq(
        model=settings.groq_model,
        groq_api_key=settings.groq_api_key,
        temperature=0.2,
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
    log.info("QA chain built (retrieval_k=%d, model=%s)", settings.retrieval_k, settings.groq_model)
    return chain


def format_sources(source_docs: list) -> list[dict[str, Any]]:
    """Extract citation-friendly metadata from retrieved documents."""
    seen: set[str] = set()
    sources: list[dict] = []

    for doc in source_docs:
        meta = doc.metadata or {}
        source_file = meta.get("source", "Unknown")
        filename = source_file.replace("\\", "/").split("/")[-1]

        if filename in seen:
            continue
        seen.add(filename)

        sources.append({
            "filename": filename,
            "snippet": doc.page_content[:300].strip() + "…",
            "start_index": meta.get("start_index"),
        })

    return sources


# ── Module-level singletons (lazily initialised on first request) ────────────
_vectorstore: FAISS | None = None
_qa_chain: RetrievalQA | None = None


def get_qa_chain(force_rebuild: bool = False) -> RetrievalQA:
    """Return the (lazily initialised) singleton QA chain."""
    global _vectorstore, _qa_chain
    if _qa_chain is None or force_rebuild:
        _vectorstore = load_vector_store()
        _qa_chain = build_qa_chain(_vectorstore)
    return _qa_chain


def ask(question: str) -> dict[str, Any]:
    """
    Main RAG entry point.
    Returns {"answer": str, "sources": [{"filename", "snippet", ...}]}
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
