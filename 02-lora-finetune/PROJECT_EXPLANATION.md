# Project 2 — LoRA Fine-Tuning: Detailed Explanation

## 1. Problem this solves

**Prompting** alone sometimes fails on a fixed format (e.g. always output `positive|negative|neutral`) or domain phrasing. **Supervised fine-tuning (SFT)** teaches the model from examples. **LoRA (Low-Rank Adaptation)** updates only small adapter matrices — cheaper than full fine-tune.

This project trains a **tiny** adapter on **distilgpt2** so it runs on **CPU** for demos. Swap the base model for Llama/Mistral when you have GPU.

---

## 2. Architecture

```
train.jsonl  ──►  format prompts  ──►  tokenize
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  distilgpt2 (frozen) │
                              │  + LoRA on c_attn    │
                              └──────────┬──────────┘
                                         │ Trainer
                                         ▼
                              checkpoints/lora_adapter/
                                         │
inference_lora.py ◄──────────────────────┘
```

| Piece | Meaning |
|-------|---------|
| **Base model** | Pre-trained weights (general language) |
| **LoRA adapters** | Small matrices injected into attention; only these train |
| **Adapter folder** | Saved weights you load at inference without copying full model |

---

## 3. Data format

Each line in `data/train.jsonl`:

```json
{"instruction": "...", "input": "...", "output": "..."}
```

Training text template:

```
### Instruction:
...
### Input:
...
### Response:
...
```

The model learns to continue after `### Response:` with the label you want.

---

## 4. Commands

```bash
cd 02-lora-finetune
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python train_lora.py          # writes checkpoints/lora_adapter/
python inference_lora.py      # sample generation
```

**First run:** downloads `distilgpt2` from Hugging Face (~350MB).

---

## 5. Hyperparameters (train_lora.py)

| Setting | Value | Note |
|---------|-------|------|
| `r` | 8 | LoRA rank — higher = more capacity, more VRAM |
| `lora_alpha` | 16 | Scaling |
| `epochs` | 30 | OK for 5 demo rows; use early stopping on real data |
| `learning_rate` | 2e-4 | Typical for LoRA |

---

## 6. When to use LoRA vs RAG vs prompts

| Approach | Best when |
|----------|-----------|
| **Prompting** | Few examples, behavior changes often |
| **RAG** | Knowledge changes, need citations |
| **LoRA/SFT** | Stable task format, fixed style/labels, enough labeled data |

Always keep a **hold-out eval set** (Project 5).

---

## 7. Interview talking points

- **PEFT** reduces cost vs full fine-tune; adapters versioned separately.  
- **QLoRA** = LoRA on quantized base for large models on one GPU.  
- **DPO/RLHF** = alignment after SFT (Anthropic-style stack).  
- Production: register adapter in **MLflow**; canary new adapter vs production.

---

## 8. Upgrade path

1. Replace data with 500+ real labeled examples  
2. Use `meta-llama/Llama-3.2-1B-Instruct` + GPU  
3. Add `eval` script comparing base vs LoRA on golden.jsonl  
4. Merge adapter for deployment or serve with PEFT runtime
