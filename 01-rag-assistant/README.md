# Project 1 — RAG Assistant with Citations

**Detailed guide:** [PROJECT_EXPLANATION.md](./PROJECT_EXPLANATION.md) · [PROJECT_EXPLANATION.docx](./PROJECT_EXPLANATION.docx)

**Goal:** Internal knowledge Q&A — ingest documents, retrieve relevant chunks, generate grounded answers with **source citations**.

## What this demonstrates (interviews)

- Chunking → **embeddings** (MiniLM) → **vector store** (Chroma)
- **Hybrid-ready** pattern (swap Chroma for Azure AI Search / pgvector)
- **FastAPI** serving path; optional **OpenAI** for generation layer

## Prerequisites

- Python 3.10+
- Optional: `OPENAI_API_KEY` for LLM answers (works in retrieval-only mode without it)

## Setup

```bash
cd 01-rag-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add OPENAI_API_KEY if you have one
```

## Commands

```bash
# 1) Ingest sample docs (add your own .txt/.md under data/)
python ingest.py

# 2) Run API
uvicorn app:app --reload --port 8001

# 3) Query (new terminal)
curl -s -X POST http://127.0.0.1:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the remote work policy?","top_k":3}' | python -m json.tool
```

## Project layout

| File | Purpose |
|------|---------|
| `ingest.py` | Chunk + index into Chroma |
| `app.py` | `/query` retrieval + optional generation |
| `data/` | Source documents |

## Extend for portfolio

- Add **reranker** step after retrieval
- Add **tenant_id** metadata filter for multi-tenant RAG
- Log traces to **OpenTelemetry** or export eval cases to Project 5
