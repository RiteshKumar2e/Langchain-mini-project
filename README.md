# LangChain RAG Platform

> A production-ready Retrieval-Augmented Generation (RAG) question-answering platform built with **LangChain**, **FastAPI**, **FAISS**, and a **React** frontend. Ask natural-language questions and receive grounded answers with source citations and similarity scores.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)  
2. [Tech Stack](#tech-stack)  
3. [Project Structure](#project-structure)  
4. [Quick Start (Local)](#quick-start-local)  
5. [API Reference](#api-reference)  
6. [Configuration Reference](#configuration-reference)  
7. [Sample Queries](#sample-queries)  
8. [Design Decisions](#design-decisions)  
9. [Future Scope Roadmap](#future-scope-roadmap)  

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         React Frontend                              │
│   WelcomeBanner → ChatInput → MessageBubble (Markdown + Citations)  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │  HTTP /api/*
┌───────────────────────────────▼─────────────────────────────────────┐
│                  FastAPI Backend (main.py)                          │
│                                                                     │
│  POST /api/ask ──► router.py ──► rag_pipeline.py (LLM generation)  │
│                                        └──► retriever.py           │
│                                               └──► FAISS index     │
│                                               └──► embeddings.py   │
│  POST /api/ingest ─► ingestor.py ─► split ─► embed ─► FAISS save  │
│  GET  /api/health ─► config + index stats                           │
│  GET  /api/history ─► history.jsonl                                 │
│                                                                     │
│  config.py ── logger.py ── schemas.py ── history.py                │
└─────────────────────────────────────────────────────────────────────┘
```

### RAG Flow (per user query)

```
User Query
    │
    ▼
[Embedding] → sentence-transformers/all-MiniLM-L6-v2 (local, free)
    │
    ▼
[FAISS Retrieval] → top-K similar chunks with L2 distance scores
    │
    ▼
[Score Filtering] → drop chunks below similarity threshold
    │
    ▼
[Context Building] → concatenate chunks with source filenames
    │
    ▼
[LLM Generation] → Groq (llama-3.3-70b-versatile)
    │              System prompt enforces grounding rules
    │              Conversation history injected for follow-ups
    ▼
[Response] → Answer + source citations with similarity scores
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Groq (llama-3.3-70b-versatile) | Ultra-fast inference, free tier |
| **Orchestration** | LangChain 0.3 | Message construction, splitters, loaders |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 | Local, free, 384-dim dense vectors |
| **Vector DB** | FAISS (flat L2) | Exact similarity search, file-persisted |
| **Backend** | FastAPI + Uvicorn | Async REST API, auto OpenAPI docs |
| **Validation** | Pydantic v2 + pydantic-settings | Request/response schemas, env config |
| **Frontend** | React 18 + Vite | Hot-reloading dev, optimised prod bundle |
| **Markdown** | react-markdown + remark-gfm | Renders LLM output with tables/code |
| **Styling** | CSS Modules | Scoped component styles, design system variables |

---

## Project Structure

```
langchain-rag-platform/
│
├── backend/
│   ├── documents/              # Knowledge base (14 Markdown files)
│   │   ├── python_intro.md
│   │   ├── machine_learning_basics.md
│   │   ├── langchain_overview.md
│   │   ├── rag_explained.md
│   │   ├── transformers_and_attention.md
│   │   └── ...                 # 14 topics total
│   │
│   ├── vector_store/           # FAISS index (auto-generated, git-ignored)
│   │
│   ├── config.py               # Pydantic-settings — single source of config
│   ├── logger.py               # Structured logging with UTF-8 output
│   ├── embeddings.py           # HuggingFace embedding model factory
│   ├── ingestor.py             # Load → Split → Embed → Persist pipeline
│   ├── retriever.py            # FAISS retrieval with similarity scores
│   ├── rag_pipeline.py         # LLM generation with conversation memory
│   ├── history.py              # Append-only JSONL interaction log
│   ├── schemas.py              # Pydantic request/response models
│   ├── router.py               # FastAPI route handlers (thin layer)
│   ├── main.py                 # App factory, CORS, lifespan hooks
│   │
│   ├── requirements.txt
│   ├── .env                    # Your secrets (git-ignored)
│   └── .env.example            # Template — copy to .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx / .module.css
│   │   │   ├── WelcomeBanner.jsx / .module.css
│   │   │   ├── MessageBubble.jsx / .module.css
│   │   │   ├── ChatInput.jsx / .module.css
│   │   │   └── HistoryPanel.jsx / .module.css
│   │   ├── hooks/
│   │   │   └── useChat.js      # Chat state + API calls + follow-up memory
│   │   ├── api.js              # Typed API client (all fetch calls here)
│   │   ├── App.jsx             # Root layout
│   │   └── index.css           # Design system (CSS variables + Markdown)
│   │
│   ├── vite.config.js          # Dev proxy: /api → localhost:8000
│   ├── index.html
│   └── package.json
│
├── start_backend.bat           # Windows one-click backend launcher
├── start_frontend.bat          # Windows one-click frontend launcher
└── README.md
```

---

## Quick Start (Local)

### Prerequisites

- Python 3.10+ with `pip`
- Node.js 18+
- A free **Groq API key** → [console.groq.com/keys](https://console.groq.com/keys)

### 1. Clone & configure

```bash
git clone <your-repo-url>
cd langchain-rag-platform
```

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and set: GROQ_API_KEY=gsk_your_key_here
```

### 2. Backend setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # macOS/Linux

pip install -r requirements.txt
```

### 3. Ingest documents (builds the FAISS index)

```bash
# Still in backend/ with venv active
python ingestor.py
# Output: [OK] Ingestion complete: 14 document(s), ~180 chunk(s) indexed.
```

### 4. Start the backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs: **http://localhost:8000/docs**

### 5. Start the frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

> **Windows one-click:** Double-click `start_backend.bat` and `start_frontend.bat` from the project root.

---

---

## API Reference

### `POST /api/ask`

Ask a natural-language question.

**Request:**
```json
{
  "question": "What is Retrieval-Augmented Generation?",
  "conversation_history": [
    { "role": "user", "content": "What is LangChain?" },
    { "role": "assistant", "content": "LangChain is a framework..." }
  ],
  "top_k": 5
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | string | ✅ | The question (1–2000 chars) |
| `conversation_history` | array | ❌ | Prior Q&A turns for follow-up support |
| `top_k` | int | ❌ | Override retrieval K for this request |

**Response:**
```json
{
  "question": "What is Retrieval-Augmented Generation?",
  "answer": "RAG is a technique that combines...",
  "chunks_retrieved": 5,
  "sources": [
    {
      "filename": "rag_explained.md",
      "snippet": "Retrieval-Augmented Generation (RAG) is...",
      "similarity_score": 0.87,
      "start_index": 0
    }
  ]
}
```

---

### `POST /api/ingest`

Trigger document ingestion and FAISS index rebuild.

```bash
curl -X POST http://localhost:8000/api/ingest
```

**Response:**
```json
{
  "message": "Ingestion complete. 14 document(s) processed.",
  "documents_loaded": 14,
  "chunks_indexed": 183
}
```

---

### `GET /api/health`

System readiness and configuration metadata.

**Response:**
```json
{
  "status": "ok",
  "groq_model": "llama-3.3-70b-versatile",
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "vector_store_ready": true,
  "total_vectors": 183,
  "chunk_size": 500,
  "retrieval_k": 5
}
```

---

### `GET /api/history?limit=10`

Last N interactions with full source + score metadata.

### `POST /api/history/clear`

Truncate the interaction log.

---

## Configuration Reference

All options set in `backend/.env`:

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | *(required)* | Your Groq API key |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | LLM model |
| `LLM_TEMPERATURE` | `0.2` | Sampling temperature (0=deterministic) |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `CHUNK_SIZE` | `500` | Characters per text chunk |
| `CHUNK_OVERLAP` | `50` | Overlap characters between chunks |
| `RETRIEVAL_K` | `5` | Top-K chunks to retrieve per query |
| `RETRIEVAL_SCORE_THRESHOLD` | `0.0` | Min similarity score to include a source |
| `ENABLE_CONVERSATION_MEMORY` | `true` | Pass history to LLM for follow-ups |
| `DOCUMENTS_PATH` | `./documents` | Source documents folder |
| `VECTOR_STORE_PATH` | `./vector_store` | FAISS persist directory |
| `CORS_ORIGINS` | `http://localhost:5173,...` | Allowed frontend origins |

---

## Sample Queries

Try these in the UI or via `curl -X POST localhost:8000/api/ask -d '{"question":"..."}'`:

```
1. What is Retrieval-Augmented Generation and how does it work?
2. Explain the Transformer attention mechanism step by step.
3. What are the main types of machine learning algorithms?
4. How does LangChain help build LLM applications?
5. Compare FAISS with other vector databases like Pinecone and Chroma.
6. What is the difference between supervised and unsupervised learning?
7. What are the key NLP techniques used in modern AI?
8. Explain the key features of FastAPI.
```

**Follow-up example:**
```
Q1: What is deep learning?
Q2: How does it differ from traditional machine learning? ← uses conversation history
```

---

## Design Decisions

### Why Groq instead of OpenAI?
Groq provides a **free tier** with extremely fast inference (up to 750 tokens/sec on llama-3.3-70b), making it ideal for prototypes and demos. The abstraction in `rag_pipeline.py` supports any `langchain_core.language_models.BaseChatModel`, so switching to OpenAI/Anthropic is a one-line config change.

### Why FAISS instead of Chroma/Pinecone?
FAISS is **zero-dependency**, file-persisted, and sufficient for corpora up to ~100k vectors. It requires no external service. The retrieval layer (`retriever.py`) is fully decoupled from the chain, so swapping to Chroma or Pinecone only requires changing `_load_vector_store()`.

### Why HuggingFace embeddings (local)?
`all-MiniLM-L6-v2` runs entirely locally with no API calls, no cost, and no latency beyond the first load. At 384 dimensions it offers excellent recall for English-language technical documents.

### Chunk size 500 / overlap 50
This was chosen after empirical testing on the document corpus:
- Chunks large enough to contain complete semantic units (paragraphs, definitions).
- Small enough to keep retrieval precision high (fewer irrelevant sentences in context).
- Overlap ensures sentences at chunk boundaries are not split mid-thought.

### Layered architecture (retriever.py separate from rag_pipeline.py)
LangChain's `RetrievalQA` chain hides similarity scores. We deliberately own the retrieval step (`retriever.py`) to:
1. Expose per-source similarity scores to the API consumer.
2. Apply configurable score thresholds.
3. Enable future reranking without touching LLM code.

### JSONL for history
Human-readable, grep-able, and zero-setup. Suitable for a local prototype. In production, replace with PostgreSQL or DynamoDB.

---

## Future Scope Roadmap

This section outlines planned enhancements that would evolve this prototype into a production-grade enterprise platform.

### 🔍 Advanced Retrieval

| Feature | Description | Priority |
|---|---|---|
| **Hybrid Retrieval (BM25 + Dense)** | Combine sparse keyword search (BM25) with dense vector search for better recall on factual and entity-heavy queries | High |
| **Multi-Query Expansion** | Use the LLM to rephrase the user question 3–5 ways, retrieve for each, and union the results | High |
| **Cross-Encoder Reranking** | After top-K retrieval, use a cross-encoder (e.g. `ms-marco-MiniLM-L-6-v2`) to reorder by actual relevance | High |
| **Configurable top-K per request** | Already partially implemented; expose in UI | Medium |
| **Semantic Caching** | Cache previous queries with high semantic similarity and return cached answers | Medium |
| **Parent Document Retriever** | Retrieve small chunks for precision, but pass larger parent context to the LLM | Low |

### 🤖 LLM & Generation

| Feature | Description | Priority |
|---|---|---|
| **Streaming Responses** | Use SSE/WebSockets to stream tokens to the frontend as they are generated | High |
| **Hallucination Detection** | Post-process answers to verify every factual claim is grounded in retrieved context | High |
| **Multi-LLM Router** | Route different query types (simple factual vs complex analytical) to different models by cost | Medium |
| **Custom System Prompts** | Allow per-deployment system prompts for domain-specific tone and behaviour | Medium |
| **Confidence Scores** | Estimate answer confidence from retrieval scores + LLM self-consistency sampling | Low |

### 📊 Evaluation & Observability

| Feature | Description | Priority |
|---|---|---|
| **RAGAS Evaluation** | Automated pipeline using RAGAS metrics: faithfulness, answer relevancy, context precision/recall | High |
| **LangSmith Tracing** | End-to-end trace every chain call for debugging and latency analysis | High |
| **Prometheus + Grafana** | Metrics: latency p50/p99, retrieval hit rate, LLM error rate | Medium |
| **A/B Testing Framework** | Compare retrieval strategies or models against offline evaluation datasets | Low |

### 🏗️ Platform & Scalability

| Feature | Description | Priority |
|---|---|---|
| **Background Ingestion Workers** | Async Celery/RQ workers for large document ingestion without blocking the API | High |
| **Document Versioning** | Track document changes with SHA hashes; auto re-index only changed files | High |
| **Multi-tenant Indexing** | Separate FAISS namespaces or Chroma collections per user/organisation | High |
| **Role-Based Access Control** | JWT authentication; restrict /ingest and /history/clear to admin roles | High |
| **Persistent Conversation Sessions** | Store conversation history in Redis or PostgreSQL by session_id | Medium |
| **PDF + Web Crawler Support** | Extend ingestor to crawl URLs and extract structured data from PDFs | Medium |

### ☁️ Cloud & Infrastructure

| Feature | Description | Priority |
|---|---|---|
| **Kubernetes Deployment** | Helm chart for horizontal scaling of the backend; separate embedding pod | High |
| **AWS Deployment** | ECS Fargate (backend) + S3 (vector store) + CloudFront (frontend) + RDS (history) | Medium |
| **GCP Deployment** | Cloud Run (backend) + Cloud Storage (index) + Vertex AI (managed embeddings) | Medium |
| **GPU Acceleration** | Use FAISS-GPU for 10–100× faster indexing on large corpora; vLLM for local LLM | Low |
| **Pinecone / Weaviate Migration** | Drop-in replacement of FAISS for fully managed, auto-scaling vector search | Low |
| **CDN-Cached Responses** | Cache GET /health and common queries at the CDN edge for global latency reduction | Low |

---

## License

This project was built for educational and evaluation purposes. All documents in the knowledge base are sourced from publicly available open-domain information.
