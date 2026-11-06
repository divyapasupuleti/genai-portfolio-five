#!/usr/bin/env python3
"""Capstone: guardrails → RAG mock → output check → optional eval subprocess."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "05-evals-harness" / "run_evals.py"

BLOCK_INPUT = re.compile(r"(ignore previous|system prompt|jailbreak|api_key)", re.I)
BLOCK_OUTPUT = re.compile(r"(password|ssn|credit card)", re.I)

KB = {
    "remote work": "Employees may work remotely up to three days per week with manager approval.",
    "gdpr": "All customer data must stay in EU regions for GDPR compliance.",
    "latency incident": "Page on-call if p95 latency exceeds 2 seconds for 5 minutes.",
}


def mock_rag_answer(query: str) -> str:
    q = query.lower()
    for k, v in KB.items():
        if k in q:
            return v
    return "I don't know."


def input_guard(user_message: str) -> tuple[bool, str]:
    msg = user_message.strip()
    if not msg:
        return False, "empty_input"
    if BLOCK_INPUT.search(msg):
        return False, "blocked_input_pattern"
    return True, msg


def output_guard(reply: str) -> tuple[bool, str]:
    if BLOCK_OUTPUT.search(reply):
        return False, "blocked_output_pattern"
    return True, reply


def orchestrate(user_message: str) -> dict:
    trace_id = str(uuid.uuid4())
    ok_in, payload = input_guard(user_message)
    if not ok_in:
        return {
            "trace_id": trace_id,
            "safe": False,
            "stage": "input_guard",
            "error": payload,
            "reply": None,
        }
    raw = mock_rag_answer(payload)
    ok_out, reply = output_guard(raw)
    if not ok_out:
        return {
            "trace_id": trace_id,
            "safe": False,
            "stage": "output_guard",
            "error": reply,
            "reply": None,
        }
    return {
        "trace_id": trace_id,
        "safe": True,
        "stage": "complete",
        "reply": reply,
        "sources": ["mock_kb"],
    }


def run_evals() -> int:
    if not EVALS.is_file():
        print(f"Missing eval script: {EVALS}", file=sys.stderr)
        return 1
    return subprocess.call([sys.executable, str(EVALS)])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="User question")
    parser.add_argument("--run-evals", action="store_true", help="Run 05-evals-harness (CI gate)")
    args = parser.parse_args()

    if args.run_evals:
        sys.exit(run_evals())

    if not args.query:
        parser.error("provide query or --run-evals")

    result = orchestrate(args.query)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("safe") else 1)


if __name__ == "__main__":
    main()
