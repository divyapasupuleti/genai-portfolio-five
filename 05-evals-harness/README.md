# Project 5 — Eval Harness (Golden Set)

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

## CI example

```yaml
- name: AI golden evals
  run: python genai-portfolio-five/05-evals-harness/run_evals.py
```

## Extend

- Add **LLM-as-judge** scoring 1–5 with rubric
- Import **RAGAS** for faithfulness / context recall
- Store results in **MLflow** or **Arize** experiments
