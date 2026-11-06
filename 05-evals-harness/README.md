# Project 5 — Eval Harness (Golden Set)

![Golden evals CI](https://github.com/divyapasupuleti/genai-portfolio-five/actions/workflows/golden-evals.yml/badge.svg)

**Detailed guide:** [PROJECT_EXPLANATION.md](./PROJECT_EXPLANATION.md) · [PROJECT_EXPLANATION.docx](./PROJECT_EXPLANATION.docx)

**Goal:** **Regression tests** for AI quality before each release — same idea as **RAGAS/deepeval/CI gates**.

## What this demonstrates

- Versioned **golden.jsonl** (input + must_contain / must_not_contain)
- **Exit code 1** on failure → plug into GitHub Actions
- Swap `mock_rag_answer` for real RAG API or LLM judge

## Setup

```bash
cd 05-evals-harness
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # optional deps only if you extend
```

## Commands

```bash
python run_evals.py
echo $?   # 0 = all pass
```

## CI

Runs on every push via [`.github/workflows/golden-evals.yml`](../.github/workflows/golden-evals.yml):

```bash
python 05-evals-harness/run_evals.py
python 00-capstone-agentic-rag/orchestrate.py --run-evals   # same gate from capstone
```

## Extend

- Add **LLM-as-judge** scoring 1–5 with rubric
- Import **RAGAS** for faithfulness / context recall
- Store results in **MLflow** or **Arize** experiments
