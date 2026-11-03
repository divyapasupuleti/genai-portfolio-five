# GenAI Portfolio — 5 Hire-Ready Projects

Five small, production-style demos aligned with common **2025–2026 AI portfolio** reels (RAG, fine-tuning, guardrails, agents, evals). Each folder is self-contained with its own **README** and **run commands**.

| # | Project | Folder | One-line |
|---|---------|--------|----------|
| 1 | **RAG** with citations | [01-rag-assistant](./01-rag-assistant) | Ingest docs → retrieve → answer with sources |
| 2 | **LoRA fine-tuning** | [02-lora-finetune](./02-lora-finetune) | PEFT fine-tune a small LM on a custom JSONL task |
| 3 | **Guardrails** | [03-guardrails-api](./03-guardrails-api) | Block unsafe I/O + validate structured responses |
| 4 | **Tool-using agent** | [04-agent-tools](./04-agent-tools) | Plan → call tools → answer (OpenAI optional) |
| 5 | **Eval harness** | [05-evals-harness](./05-evals-harness) | Golden-set regression tests before release |

## Quick start (all projects)

```bash
cd genai-portfolio-five
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
```

Then open each project README for `pip install -r requirements.txt` and run commands.

## Author

**Divya Pasupuleti** — [GitHub](https://github.com/divyapasupuleti) · [LinkedIn](https://linkedin.com/in/divya-pasupuleti-97a342161)

## Note on the Instagram reel

Reel `De2Dm18xdia` could not be fetched programmatically; these five match the usual “get hired in AI” set (RAG, fine-tune, guardrails, agents, evals). Swap or extend folders if your reel lists different titles.
