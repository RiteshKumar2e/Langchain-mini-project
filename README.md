# RAG Knowledge Assistant

A production-quality **Retrieval-Augmented Generation (RAG)** question-answering system built with **LangChain**, **FastAPI**, and **React**. Ask questions in natural language and receive grounded, cited answers from a curated knowledge base.

---

## ✨ Features

| Feature | Details |
|---|---|
| **RAG Pipeline** | LangChain · FAISS · Sentence-Transformers / OpenAI Embeddings |
| **LLM Providers** | Groq (free, fast) or OpenAI — swappable via `.env` |
| **Source Citations** | Every answer cites the source documents it was retrieved from |
| **Follow-up Questions** | Conversation history is maintained for multi-turn dialogue |
| **History Persistence** | All interactions logged to `history.jsonl`, viewable in the UI |
| **Light Theme UI** | Clean React app with Vite, CSS Modules, and react-markdown |
| **Modular Backend** | Config → Embeddings → Ingestor → RAG Chain → Router → FastAPI |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                                     │
│                                                                          │
│  INDEXING (offline)          RETRIEVAL + GENERATION (online)             │
│  ─────────────────           ─────────────────────────────               │
│  documents/                  User Question                               │
│      ↓                           ↓                                       │
│  DirectoryLoader             Embed Question                              │
│      ↓                           ↓                                       │
│  RecursiveCharacter          FAISS Similarity Search                     │
│  TextSplitter                    ↓                                       │
│      ↓                       Top-K Chunks                                │
│  Embeddings                      ↓                                       │
│  (MiniLM / OpenAI)           RAG Prompt (context + question)            │
│      ↓                           ↓                                       │
│  FAISS VectorStore  ────────► LLM (Groq / OpenAI)                        │
│      ↓                           ↓                                       │
│  Saved to disk               Answer + Sources                            │
└────────────────────────────────────────────────────────────────────────┘
```

### Folder Structure

```
Langchain mini project/
├── backend/
│   ├── documents/              # 10+ knowledge-base Markdown files
│   │   ├── python_intro.md
│   │   ├── machine_learning_basics.md
│   │   ├── langchain_overview.md
│   │   ├── artificial_intelligence.md
│   │   ├── deep_learning.md
│   │   ├── nlp_overview.md
│   │   ├── vector_databases.md
│   │   ├── rag_explained.md
│   │   ├── transformers_and_attention.md
│   │   ├── fastapi_overview.md
│   │   ├── git_version_control.md
│   │   ├── docker_containerization.md
│   │   ├── react_overview.md
│   │   └── cloud_computing.md
│   ├── vector_store/           # Auto-generated FAISS index (gitignored)
│   ├── config.py               # All settings via pydantic-settings
│   ├── logger.py               # Shared logging setup
│   ├── embeddings.py           # Embedding model factory (cached)
│   ├── ingestor.py             # Document load → split → embed → store
│   ├── rag_pipeline.py         # LLM factory + RetrievalQA chain + ask()
│   ├── history.py              # JSONL history persistence
│   ├── schemas.py              # Pydantic request/response models
│   ├── router.py               # FastAPI route handlers
│   ├── main.py                 # App factory, CORS, lifespan
│   ├── history.jsonl           # Auto-generated per-run (gitignored)
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Header.jsx / .module.css
    │   │   ├── MessageBubble.jsx / .module.css
    │   │   ├── ChatInput.jsx / .module.css
    │   │   └── HistoryPanel.jsx / .module.css
    │   ├── hooks/
    │   │   └── useChat.js      # Chat state + follow-up history
    │   ├── api.js              # Backend API client
    │   ├── App.jsx / .module.css
    │   ├── index.css           # Global design system
    │   └── main.jsx
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- A **Groq API key** (free at [console.groq.com](https://console.groq.com)) **OR** an OpenAI key

---

### 1 — Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env         # Windows
# cp .env.example .env         # macOS/Linux
```

Edit `.env` and set your API key:

```env
# For Groq (free, recommended)
GROQ_API_KEY=gsk_...
LLM_PROVIDER=groq

# For OpenAI
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai

# Embeddings (huggingface = free & local, no key needed)
EMBEDDING_PROVIDER=huggingface
```

### 2 — Build the Knowledge Base Index

```bash
python ingestor.py
# → Loads 14 documents, splits into ~300 chunks, builds FAISS index
# → Saves to ./vector_store/
```

To force a rebuild if you add new documents:

```bash
python ingestor.py --force
```

### 3 — Start the Backend API

```bash
uvicorn main:app --reload --port 8000
```

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

---

### 4 — Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ask` | Submit a question, receive answer + sources |
| `GET`  | `/api/health` | Check readiness |
| `GET`  | `/api/history` | Retrieve recent interactions |
| `POST` | `/api/history/clear` | Clear all history |
| `POST` | `/api/ingest` | Rebuild the FAISS index |

### Example Request

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG and how does it work?"}'
```

### Example Response

```json
{
  "question": "What is RAG and how does it work?",
  "answer": "RAG (Retrieval-Augmented Generation) is an AI architecture that enhances LLM responses...",
  "sources": [
    {
      "filename": "rag_explained.md",
      "snippet": "RAG is a technique that combines retrieval with generation...",
      "start_index": 0
    }
  ]
}
```

---

## 📚 Knowledge Base Documents

The assistant is pre-loaded with 14 curated documents covering:

- Python programming fundamentals
- Machine learning concepts
- Deep learning and neural networks
- Natural language processing
- Transformer architecture and attention
- RAG (Retrieval-Augmented Generation)
- LangChain framework
- Vector databases (FAISS, Chroma, Pinecone, etc.)
- FastAPI
- React.js
- Git & version control
- Docker & containerization
- Cloud computing
- Artificial intelligence overview

---

## 🔧 Configuration Reference

All settings live in `backend/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `groq` | `groq` or `openai` |
| `GROQ_API_KEY` | — | Required if provider=groq |
| `OPENAI_API_KEY` | — | Required if provider=openai |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model name |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `EMBEDDING_PROVIDER` | `huggingface` | `huggingface` or `openai` |
| `CHUNK_SIZE` | `800` | Characters per document chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between chunks |
| `RETRIEVAL_K` | `5` | Documents to retrieve per query |

---

## 🧪 Adding New Documents

1. Drop any `.md` or `.txt` file into `backend/documents/`
2. Rebuild the index: `python ingestor.py --force`
3. Or use the API: `POST /api/ingest`

No code changes required.

---

## 📄 License

This project is for evaluation purposes only.
