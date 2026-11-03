# Project 4 — Tool-Using Agent: Detailed Explanation

## 1. Problem this solves

Many tasks need **actions**, not only text: math, lookups, APIs. An **agent** loop lets the LLM decide **which tool** to call, run it, observe the result, and continue until it can answer.

This repo implements the **function-calling / ReAct** pattern with three tools and a **max-step** safety limit.

---

## 2. Architecture

```
                    ┌─────────────────┐
  task (CLI arg) ──►│    agent.py     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │ OPENAI_API_KEY set?         │
              └──────────────┬──────────────┘
                    yes      │      no
                     ▼       │       ▼
            openai_agent()   │   demo_agent()
                     │       │       │
                     └───────┴───────┘
                             │
                     loop ≤ MAX_STEPS (5)
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        calculator    utc_time    knowledge_lookup
              │              │              │
              └──────────────┴──────────────┘
                             │
                        final answer
```

| File | Role |
|------|------|
| `tools.py` | Tool implementations + OpenAI function schemas |
| `agent.py` | Orchestration loop |
| `.env.example` | Optional API key |

---

## 3. Tools explained

| Tool | Input | Output |
|------|-------|--------|
| **calculator** | Math expression (`+ - * / ()`) | Numeric result or error |
| **utc_time** | empty | ISO UTC timestamp |
| **knowledge_lookup** | query string | Short blurbs on `studx` / `vocera` |

**Production:** replace calculator `eval` with a safe math parser; add timeouts and auth on external APIs.

---

## 4. Commands

```bash
cd 04-agent-tools
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Demo mode (no API key)
python agent.py "lookup studx"
python agent.py "100/4+5"

# Full agent with OpenAI
export OPENAI_API_KEY=sk-...
python agent.py "What is UTC time and 17*23?"
```

---

## 5. OpenAI agent loop (when key is set)

1. Send user task + tool definitions to the model  
2. If model returns **tool_calls**, execute each via `run_tool()`  
3. Append tool results to messages  
4. Repeat until model returns text or **MAX_STEPS** reached  

This mirrors **LangGraph / Assistants** at a minimal level.

---

## 6. Interview talking points

- **Tool design:** JSON schema, idempotency, errors returned as strings for the model  
- **Multi-agent routing** (Studx): router agent → specialist agents  
- **HITL:** require approval before destructive tools  
- **Observability:** log every tool name, args hash, latency, trace_id  
- **Inference teams:** agent gateway is async I/O; GPU work stays on inference workers

---

## 7. Safety checklist

- [ ] Max steps enforced  
- [ ] Tool allowlist only  
- [ ] No raw SQL/shell from model without sandbox  
- [ ] Secrets never passed into tool args from user text  

---

## 8. Extensions

- Add LangGraph for branching and human-in-the-loop nodes  
- Wire tools to real RAG (Project 1) HTTP endpoint  
- Export trajectories to Project 5 eval format
