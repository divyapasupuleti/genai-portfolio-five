# Project 4 — Tool-Using Agent

Part of the [agentic capstone](../00-capstone-agentic-rag) story (optional tool step after RAG).

**Detailed guide:** [PROJECT_EXPLANATION.md](./PROJECT_EXPLANATION.md) · [PROJECT_EXPLANATION.docx](./PROJECT_EXPLANATION.docx)

**Goal:** **Agent** that plans and **calls tools** (calculator, time, internal KB) — ReAct / function-calling pattern.

## What this demonstrates

- Tool **schemas** for LLM function calling
- Multi-step loop with **max steps** (production safety)
- Works **without API key** via `demo_agent` fallback

## Setup

```bash
cd 04-agent-tools
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional OPENAI_API_KEY
```

## Commands

```bash
# Demo mode (no key)
python agent.py "lookup studx"
python agent.py "sqrt(144)+10"

# With OpenAI
export OPENAI_API_KEY=sk-...
python agent.py "What time is UTC now and what is 20*30?"
```

## Interview talking points

- **Idempotent** tools, timeouts, allowlist
- **Observability**: log every tool call with trace id
- Prefer **LangGraph** when workflow has branches and HITL

## `.env.example`

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```
