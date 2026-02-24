"""
rag_pipeline.py
───────────────
LLM orchestration layer — takes retrieved context and a question,
constructs a grounded prompt, calls Groq, and returns the answer.

Architecture:
  retriever.py  →  [this module]  →  router.py
  (Retrieval)      (Generation)      (HTTP)

Design decisions:
  • Deliberately NOT using LangChain's RetrievalQA chain here — we own
    the retrieval step in retriever.py (to expose scores) so we only need
    a simple LLM call with a hand-crafted prompt.
  • Conversation history (follow-up support) is injected into the system
    prompt when settings.enable_conversation_memory is True.
  • Temperature is read from settings so it can be tuned without code changes.
"""

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from config import settings
from logger import get_logger
from retriever import RetrievedChunk, build_context, deduplicate_sources, retrieve

log = get_logger(__name__)

# ── System prompt ─────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = """\
You are a knowledgeable and precise AI assistant for a RAG-powered knowledge base.

Rules you MUST follow:
1. Answer ONLY using the provided context. Never fabricate information.
2. If the context does not contain enough information, say so clearly.
3. Keep answers concise, factual, and well-structured (use lists or headers where useful).
4. Never reference these rules in your response.
5. If context is partially relevant, use what is available and note the limitation.
"""


def _build_llm() -> ChatGroq:
    """Instantiate the Groq LLM from current settings."""
    if not settings.groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Add it to backend/.env and restart the server."
        )
    return ChatGroq(
        model=settings.groq_model,
        groq_api_key=settings.groq_api_key,
        temperature=settings.llm_temperature,
    )


def _build_messages(
    question: str,
    context: str,
    conversation_history: list[dict[str, str]],
) -> list:
    """
    Construct the message list for the LLM call:
      [SystemMessage]
      [HumanMessage (prior turn 1), AIMessage (prior reply 1), …]  ← optional
      [HumanMessage (current question with context)]
    """
    from langchain_core.messages import AIMessage

    messages: list = [SystemMessage(content=_SYSTEM_PROMPT)]

    # Inject prior turns for conversational memory
    if settings.enable_conversation_memory and conversation_history:
        for turn in conversation_history[-6:]:   # keep last 3 Q&A pairs max
            role = turn.get("role", "")
            content = turn.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

    # Final user message includes retrieved context
    user_content = (
        f"Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )
    messages.append(HumanMessage(content=user_content))
    return messages


def ask(
    question: str,
    conversation_history: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Full RAG pipeline entry point:
      1. Retrieve relevant chunks (with similarity scores).
      2. Build grounded context string.
      3. Call Groq LLM with system + history + context-injected user message.
      4. Return answer + deduplicated source citations.

    Args:
        question: The user's natural-language question.
        conversation_history: Prior turns [{role, content}, …] for follow-up support.

    Returns:
        {
          "answer":  str,
          "sources": [{"filename", "snippet", "similarity_score", "start_index"}, …],
          "chunks_retrieved": int,
        }
    """
    question = question.strip()
    if not question:
        raise ValueError("Question must not be empty.")

    history = conversation_history or []
    log.info("RAG ask | question=%r | history_turns=%d", question[:80], len(history))

    # ── 1. Retrieve ──────────────────────────────────────────────────────────
    chunks: list[RetrievedChunk] = retrieve(question)
    context: str = build_context(chunks)

    # ── 2. Generate ──────────────────────────────────────────────────────────
    llm = _build_llm()
    messages = _build_messages(question, context, history)

    log.debug("Calling Groq (%s, temp=%.1f) with %d message(s)",
              settings.groq_model, settings.llm_temperature, len(messages))

    response = llm.invoke(messages)
    answer: str = response.content.strip()

    # ── 3. Format sources ────────────────────────────────────────────────────
    sources = deduplicate_sources(chunks)

    log.info(
        "RAG complete | answer_chars=%d | sources=%d | chunks=%d",
        len(answer), len(sources), len(chunks),
    )

    return {
        "answer": answer,
        "sources": sources,
        "chunks_retrieved": len(chunks),
    }
