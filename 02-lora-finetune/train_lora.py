#!/usr/bin/env python3
"""Minimal LoRA SFT on distilgpt2 (CPU-friendly demo)."""

from __future__ import annotations

import json
from pathlib import Path

from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

MODEL = "distilgpt2"
OUT = Path(__file__).parent / "checkpoints"
DATA = Path(__file__).parent / "data" / "train.jsonl"


def load_rows() -> list[dict]:
    rows = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def format_example(row: dict) -> str:
    return (
        f"### Instruction:\n{row['instruction']}\n"
        f"### Input:\n{row['input']}\n"
        f"### Response:\n{row['output']}"
    )


def main() -> None:
    rows = load_rows()
    texts = [format_example(r) for r in rows]
    ds = Dataset.from_dict({"text": texts})

    tok = AutoTokenizer.from_pretrained(MODEL)
    tok.pad_token = tok.eos_token

    def tokenize(batch):
        return tok(batch["text"], truncation=True, max_length=256, padding="max_length")

    ds = ds.map(tokenize, batched=True)
    ds = ds.remove_columns(["text"])

    base = AutoModelForCausalLM.from_pretrained(MODEL)
    lora = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["c_attn"],
    )
    model = get_peft_model(base, lora)
    model.print_trainable_parameters()

    args = TrainingArguments(
        output_dir=str(OUT),
        num_train_epochs=30,
        per_device_train_batch_size=2,
        learning_rate=2e-4,
        logging_steps=5,
        save_strategy="no",
        report_to=[],
    )
    trainer = Trainer(model=model, args=args, train_dataset=ds)
    trainer.train()
    model.save_pretrained(OUT / "lora_adapter")
    tok.save_pretrained(OUT / "lora_adapter")
    print(f"Saved adapter to {OUT / 'lora_adapter'}")


if __name__ == "__main__":
    main()
