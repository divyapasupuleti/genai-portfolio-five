#!/usr/bin/env python3
"""Golden-set eval harness — run before promoting RAG/prompt changes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

GOLDEN = Path(__file__).parent / "golden.jsonl"


def mock_rag_answer(query: str) -> str:
    """Replace with HTTP call to 01-rag-assistant or your pipeline."""
    kb = {
        "remote work": "Employees may work remotely up to three days per week with manager approval.",
        "gdpr": "All customer data must stay in EU regions for GDPR compliance.",
        "latency incident": "Page on-call if p95 latency exceeds 2 seconds for 5 minutes.",
    }
    q = query.lower()
    for k, v in kb.items():
        if k in q:
            return v
    return "I don't know."


def score_case(row: dict, answer: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    ans_l = answer.lower()
    for phrase in row.get("must_contain", []):
        if phrase.lower() not in ans_l:
            errors.append(f"missing required phrase: {phrase!r}")
    for phrase in row.get("must_not_contain", []):
        if phrase.lower() in ans_l:
            errors.append(f"forbidden phrase present: {phrase!r}")
    return (len(errors) == 0, errors)


def main() -> None:
    rows = [json.loads(l) for l in GOLDEN.read_text(encoding="utf-8").splitlines() if l.strip()]
    passed = 0
    for row in rows:
        ans = mock_rag_answer(row["input"])
        ok, errs = score_case(row, ans)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] id={row['id']} input={row['input']!r}")
        if errs:
            for e in errs:
                print(f"       - {e}")
        if ok:
            passed += 1
    print(f"\nSummary: {passed}/{len(rows)} passed")
    sys.exit(0 if passed == len(rows) else 1)


if __name__ == "__main__":
    main()
