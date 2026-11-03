#!/usr/bin/env python3
"""Generate PROJECT_EXPLANATION.docx from PROJECT_EXPLANATION.md in each project."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("Install: pip install python-docx")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "01-rag-assistant",
    "02-lora-finetune",
    "03-guardrails-api",
    "04-agent-tools",
    "05-evals-harness",
]


def md_to_docx(md_path: Path, docx_path: Path) -> None:
    doc = Document()
    text = md_path.read_text(encoding="utf-8")
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if line.startswith("# "):
            doc.add_heading(line[2:].strip(), level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=2)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=3)
        elif line.startswith("|") and "---" not in line:
            doc.add_paragraph(line)
        elif line.strip().startswith("- "):
            doc.add_paragraph(line.strip()[2:], style="List Bullet")
        elif line.strip():
            p = doc.add_paragraph()
            parts = re.split(r"(\*\*.+?\*\*)", line)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    p.add_run(part[2:-2]).bold = True
                else:
                    p.add_run(part)
        elif not in_code:
            doc.add_paragraph("")
    doc.save(docx_path)


def main() -> None:
    for name in PROJECTS:
        folder = ROOT / name
        md = folder / "PROJECT_EXPLANATION.md"
        if not md.exists():
            print("Skip (no md):", name)
            continue
        out = folder / "PROJECT_EXPLANATION.docx"
        md_to_docx(md, out)
        print("Wrote", out)
    print("Done.")


if __name__ == "__main__":
    main()
