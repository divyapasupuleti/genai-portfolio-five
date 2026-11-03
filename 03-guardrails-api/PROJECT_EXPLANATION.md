# Project 3 — Guardrails API: Detailed Explanation

## 1. Problem this solves

LLM applications must **block unsafe inputs** (jailbreaks, prompt injection), **validate outputs** (no secrets, schema compliance), and **fail clearly** when policy triggers. This service wraps a (mock) LLM with **guardrails** you can place in front of any model API.

---

## 2. Architecture

```
Client POST /chat
       │
       ▼
┌──────────────────┐
│ Pydantic ChatIn  │  ← max length, regex block (injection patterns)
└────────┬─────────┘
         ▼
┌──────────────────┐
│ mock_llm()       │  ← replace with real LLM call
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Pydantic ChatOut │  ← intent enum, reply max length, secret patterns
└────────┬─────────┘
         ▼
    JSON response or HTTP 400
```

**Defense in depth in production:** regex → classifier (Llama Guard) → human review for high-risk actions.

---

## 3. What is blocked today

**Input regex (`BLOCK_INPUT`):** phrases like `ignore previous`, `jailbreak`, `api_key`  
**Output regex (`BLOCK_OUTPUT`):** `password`, `ssn`, `credit card`  
**Schema:** `intent` must be enum; `reply` max 500 chars  

Extend lists from your threat model — never rely on regex alone for production.

---

## 4. Commands

```bash
cd 03-guardrails-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8003
```

**Allowed request:**

```bash
curl -s -X POST http://127.0.0.1:8003/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message":"I need help with billing"}'
```

**Blocked request:**

```bash
curl -s -X POST http://127.0.0.1:8003/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message":"ignore previous instructions"}'
```

---

## 5. API reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Lists active guardrail types |
| `/chat` | POST | Body: `{"user_message": "..."}` → `ChatOut` |

**ChatOut fields:** `intent` (`support`|`billing`|`unknown`), `reply`, `safe` (always true when returned)

---

## 6. Interview talking points

- **Prompt injection** via untrusted RAG documents — treat user + retrieved text as hostile.  
- **Structured outputs** (Pydantic / JSON schema) reduce parse errors in agents.  
- Healthcare (Vocera): PHI must not appear in logs or model outputs — redact + block.  
- Layer **Azure Content Safety**, **NeMo Guardrails**, or **Llama Guard** behind this API.

---

## 7. Integration pattern

```text
User → API Gateway → Guardrails (this app) → LLM Provider → Guardrails output check → User
```

Log **blocked** events with reason code, not full user PII.

---

## 8. Extensions

- Rate limiting per user/IP  
- Allow tool calls only from allowlisted tools (agent safety)  
- Async moderation for streaming (buffer + cut stream on violation)
