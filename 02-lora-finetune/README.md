# Project 2 — LoRA Fine-Tuning (PEFT)

**Detailed guide:** [PROJECT_EXPLANATION.md](./PROJECT_EXPLANATION.md) · [PROJECT_EXPLANATION.docx](./PROJECT_EXPLANATION.docx)

**Goal:** Show you can **adapt an open model** for a specific task cheaper than prompt-only — using **LoRA** on a small LM.

## What this demonstrates

- **SFT** data format (instruction / input / output)
- **PEFT / LoRA** trainable parameters << full model
- Save **adapter** weights separately from base model

## Setup

```bash
cd 02-lora-finetune
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

```bash
# Train (CPU works; GPU faster) — ~1–3 min on CPU for this tiny set
python train_lora.py

# Inference
python inference_lora.py
```

## Data

Edit `data/train.jsonl` — one JSON object per line with keys `instruction`, `input`, `output`.

## Interview talking points

- When **LoRA** vs **RAG** vs **prompting**
- **Eval** on hold-out set before promoting adapter (link to Project 5)
- Production: store adapter version in **MLflow** / model registry

## Note

`distilgpt2` is a **demo** only. For real portfolios, swap to `meta-llama/Llama-3.2-1B` with GPU and more data.
