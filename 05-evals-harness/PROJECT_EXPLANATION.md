# Project 5 — Eval Harness: Detailed Explanation

## 1. Problem this solves

LLM and RAG systems **regress silently** when you change prompts, models, or indexes. An **eval harness** runs a fixed **golden set** before every release and **fails CI** if quality drops.

This project uses simple **must_contain / must_not_contain** rules — the same idea as golden tests in **deepeval**, **RAGAS**, or custom LLM-as-judge pipelines.

---

## 2. Architecture

```
golden.jsonl  ──►  run_evals.py  ──►  for each case:
                           │              mock_rag_answer(input)
                           │              score vs must_contain / must_not
                           ▼
                    PASS/FAIL per id
                           │
                           ▼
                    exit 0 or 1 (CI gate)
```

Replace `mock_rag_answer()` with:

- HTTP POST to **01-rag-assistant** `/query`  
- Or your production pipeline function  

---

## 3. Golden file format

Each line in `golden.jsonl` is one JSON object:

```json
{
  "id": "1",
  "input": "remote work",
  "must_contain": ["three days", "remote"],
  "must_not_contain": ["password"]
}
```

| Field | Meaning |
|-------|---------|
| `input` | Question or query passed to the system |
| `must_contain` | All phrases must appear in answer (case-insensitive) |
| `must_not_contain` | Forbidden phrases (safety/regression) |

Version this file in git; tag with model + index version.

---

## 4. Commands

```bash
cd 05-evals-harness
python3 run_evals.py
echo $?   # 0 = all passed, 1 = failure
```

Example output:

```text
[PASS] id=1 input='remote work'
[PASS] id=2 input='GDPR'
...
Summary: 3/3 passed
```

---

## 5. CI integration

```yaml
# .github/workflows/evals.yml (example)
- name: Golden AI evals
  run: python 05-evals-harness/run_evals.py
```

Block merge on non-zero exit — same pattern as unit tests.

---

## 6. Interview talking points

- **Golden set** size: start 20–50 real user questions; refresh monthly  
- **LLM-as-judge** for subjective quality; calibrate vs human labels  
- **RAGAS:** faithfulness, context precision/recall for retrieval  
- **Arize / LangSmith:** store eval runs over time  
- Anthropic-style: eval before **canary** model rollout  

---

## 7. Scoring extensions

| Level | Method |
|-------|--------|
| L1 | Keyword rules (this repo) |
| L2 | Embedding similarity to reference answer |
| L3 | LLM judge with rubric |
| L4 | Human labeling queue for edge cases |

---

## 8. Link to other projects

1. After changing **01-rag-assistant** ingest or prompts → run evals  
2. After **02-lora-finetune** adapter → add cases for fine-tuned behavior  
3. After **03-guardrails** → add cases that must return HTTP 400  
4. After **04-agent-tools** → add trajectories expected to call specific tools

---

## 9. Operational cadence

| When | Action |
|------|--------|
| Every PR | Run golden set |
| Weekly | Add failures from production logs (redacted) |
| Model swap | Full eval + canary traffic compare |
