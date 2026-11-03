# Project 3 — Guardrails API

**Detailed guide:** [PROJECT_EXPLANATION.md](./PROJECT_EXPLANATION.md) · [PROJECT_EXPLANATION.docx](./PROJECT_EXPLANATION.docx)

**Goal:** Safety layer before/after an LLM — block risky **inputs**, validate **outputs**, enforce **schema**.

## What this demonstrates

- **Prompt injection** pattern blocking (regex + extend to classifiers)
- **Structured output** with Pydantic (`intent`, `reply`, `safe`)
- **HTTP 400** on policy violations — pattern for production middleware

## Setup

```bash
cd 03-guardrails-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

```bash
uvicorn app:app --reload --port 8003

# Allowed
curl -s -X POST http://127.0.0.1:8003/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message":"I need help with billing"}' | python -m json.tool

# Blocked input
curl -s -X POST http://127.0.0.1:8003/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message":"ignore previous instructions"}' | python -m json.tool
```

## Extend

- Swap `mock_llm` for real LLM behind same validators
- Add **NeMo Guardrails**, **Llama Guard**, or **Azure Content Safety** as extra layers
- Log blocked events to SIEM (no raw PII)
