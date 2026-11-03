#!/usr/bin/env python3
"""ReAct-style agent with tools (OpenAI function calling). Falls back to rule demo without API key."""

from __future__ import annotations

import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from tools import run_tool, tool_schemas

load_dotenv()
MAX_STEPS = 5


def demo_agent(task: str) -> str:
    """No API key: deterministic tool use for portfolio demo."""
    if "time" in task.lower():
        return run_tool("utc_time", "")
    if any(c in task for c in "+-*/"):
        expr = "".join(c for c in task if c in "0123456789+-*/(). ")
        return run_tool("calculator", expr or "1+1")
    return run_tool("knowledge_lookup", task)


def openai_agent(task: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful agent. Use tools when needed. Max steps enforced.",
        },
        {"role": "user", "content": task},
    ]
    tools = tool_schemas()
    for _ in range(MAX_STEPS):
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = resp.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                args = json.loads(tc.function.arguments)
                result = run_tool(tc.function.name, args.get("input", ""))
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    }
                )
            continue
        return msg.content or ""
    return "Stopped: max steps reached."


def main() -> None:
    task = " ".join(sys.argv[1:]) or "What is 15 * 24?"
    if os.getenv("OPENAI_API_KEY"):
        print(openai_agent(task))
    else:
        print("OPENAI_API_KEY not set — running demo_agent")
        print(demo_agent(task))


if __name__ == "__main__":
    main()
