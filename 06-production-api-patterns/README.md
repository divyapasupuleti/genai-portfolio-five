# Production API patterns (FastAPI)

Minimal **hire-ready** service showing patterns from real LLM deployments: validated I/O, **in-memory cache** (Redis-shaped interface), **trace id**, structured logs, **pytest**.

## Run

```bash
cd 06-production-api-patterns
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8080
```

```bash
curl -s http://127.0.0.1:8080/health | python -m json.tool
curl -s -X POST http://127.0.0.1:8080/v1/complete \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"hello","use_cache":true}' | python -m json.tool
pytest -q
```

## What interviewers notice

- **Pydantic** request/response models
- **Cache key** = hash of normalized prompt (swap dict → Redis in one line)
- **`X-Trace-Id`** header for log correlation (Datadog/Arize)
- Tests without standing up external LLM

## Pin on GitHub

Link from profile README as “production FastAPI patterns” alongside agentic capstone.
