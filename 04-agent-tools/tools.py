"""Tool implementations for the demo agent."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone


def calculator(expression: str) -> str:
    allowed = {"sqrt": math.sqrt, "pi": math.pi}
    try:
        # Safe subset: numbers and + - * / only
        if not all(c in "0123456789+-*/(). " for c in expression):
            return "error: unsupported characters"
        return str(eval(expression, {"__builtins__": {}}, allowed))  # noqa: S307 demo only
    except Exception as e:
        return f"error: {e}"


def utc_time(_: str = "") -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def knowledge_lookup(query: str) -> str:
    kb = {
        "studx": "Studx: Azure OpenAI education platform, 20k+ students, RAG over 5k URLs.",
        "vocera": "Vocera: healthcare voice AI for Stryker with Datadog and Arize observability.",
    }
    q = query.lower()
    for k, v in kb.items():
        if k in q:
            return v
    return "No internal doc matched. Try studx or vocera."


TOOLS = {
    "calculator": {
        "description": "Evaluate a math expression. Input: expression string.",
        "fn": calculator,
    },
    "utc_time": {
        "description": "Return current UTC time. Input: empty string.",
        "fn": utc_time,
    },
    "knowledge_lookup": {
        "description": "Lookup internal project blurbs. Input: query string.",
        "fn": knowledge_lookup,
    },
}


def tool_schemas() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": meta["description"],
                "parameters": {
                    "type": "object",
                    "properties": {"input": {"type": "string"}},
                    "required": ["input"],
                },
            },
        }
        for name, meta in TOOLS.items()
    ]


def run_tool(name: str, arg: str) -> str:
    if name not in TOOLS:
        return f"unknown tool: {name}"
    return TOOLS[name]["fn"](arg)
