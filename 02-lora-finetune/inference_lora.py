#!/usr/bin/env python3
"""Run inference with saved LoRA adapter."""

from __future__ import annotations

from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE = "distilgpt2"
ADAPTER = Path(__file__).parent / "checkpoints" / "lora_adapter"


def main() -> None:
    prompt = (
        "### Instruction:\nClassify sentiment.\n"
        "### Input:\nThis is amazing!\n"
        "### Response:\n"
    )
    tok = AutoTokenizer.from_pretrained(ADAPTER if ADAPTER.exists() else BASE)
    base = AutoModelForCausalLM.from_pretrained(BASE)
    if ADAPTER.exists():
        model = PeftModel.from_pretrained(base, ADAPTER)
    else:
        model = base
    model.eval()
    ids = tok.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=20, do_sample=False)
    print(tok.decode(out[0], skip_special_tokens=True))


if __name__ == "__main__":
    main()
