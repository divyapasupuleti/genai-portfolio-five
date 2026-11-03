# Project 1 — RAG Assistant: Detailed Explanation

## 1. Problem this solves

Companies have answers scattered in PDFs, wikis, and policies. Users ask natural-language questions; a **Retrieval-Augmented Generation (RAG)** system:

1. Finds the right passages in your corpus  
2. Grounds the LLM answer in those passages  
3. Returns **citations** so users can verify  

This demo uses **local embeddings** (no API required for retrieval) and **optional OpenAI** for fluent answers.

---

## 2. Architecture

```
┌─────────────┐     ingest.py      ┌──────────────┐
│ data/*.txt  │ ─────────────────► │   ChromaDB   │
└─────────────┘   chunk + embed    │  (.chroma/)  │
                                   └──────┬───────┘
                                          │ top_k similarity
┌─────────────┐     POST /query         │
│   Client    │ ───────────────────────►│  app.py      │
└─────────────┘                         │  retrieve    │
       ▲                                │  + optional  │
       │ citations + answer             │  OpenAI gen  │
       └────────────────────────────────┘
```

| Component | Role |
|-----------|------|
| **ingest.py** | Reads `.txt`/`.md`, splits into overlapping chunks, embeds with `all-MiniLM-L6-v2`, stores in Chroma |
| **app.py** | FastAPI: query → retrieve → build prompt with context → return answer + citations |
| **Chroma** | Persistent vector store on disk (`.chroma/`) |

---

## 3. How retrieval works (simple)

- Your question is embedded with the **same model** as the documents.  
- Chroma finds **cosine-similar** chunks (approximate nearest neighbors).  
- Top **k** chunks (default 3) become **context** for the LLM.  
- If `OPENAI_API_KEY` is missing, the API still returns **retrieved excerpts** (retrieval-only mode).

**Chunking:** words are grouped (~400 words, ~80 overlap) so sentences at boundaries are not lost.

---

## 4. File-by-file

| File | Purpose |
|------|---------|
| `data/sample_policy.txt` | Example corpus — replace with your docs |
| `ingest.py` | One-off or scheduled indexing job |
| `app.py` | Online serving |
| `requirements.txt` | Python dependencies |
| `.env.example` | `OPENAI_API_KEY`, `OPENAI_MODEL` |

---

## 5. Commands (operate the project)

```bash
cd 01-rag-assistant
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # optional: add OPENAI_API_KEY

python ingest.py        # build index
uvicorn app:app --reload --port 8001

curl -s -X POST http://127.0.0.1:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How many remote days are allowed?","top_k":3}'
```

**Health check:** `GET http://127.0.0.1:8001/health`

**Re-index after doc changes:** run `python ingest.py` again (drops and recreates collection).

---

## 6. Configuration

| Variable | Default | Meaning |
|----------|---------|---------|
| `OPENAI_API_KEY` | empty | If set, generates natural-language answers |
| `OPENAI_MODEL` | `gpt-4o-mini` | Chat model for generation |

---

## 7. Interview & resume talking points

- End-to-end **ingest → index → retrieve → generate** (Studx/EPAM-style pipelines).  
- **Hybrid search** next step: add BM25 + vector (Azure AI Search pattern).  
- **Multi-tenant:** add `tenant_id` in chunk metadata and filter at query time.  
- **Eval:** hook `/query` outputs into Project 5 golden set.  
- **Production:** rate limits, auth, trace IDs, p95 latency on retrieve vs generate.

---

## 8. Common failures

| Symptom | Fix |
|---------|-----|
| Empty retrieval | Run `ingest.py`; check `data/` has `.txt`/`.md` |
| Slow first query | Embedding model downloads on first run (~80MB) |
| Hallucination | Lower temperature; tighten system prompt; add reranker |
| Stale answers | Re-ingest; version indexes per release |

---

## 9. Extensions (portfolio v2)

- Reranker (cross-encoder) after retrieval  
- PDF ingest (Unstructured, Azure Document Intelligence)  
- Streaming SSE responses for long answers  
- OpenTelemetry spans: `retrieve_ms`, `generate_ms`, `tokens`
