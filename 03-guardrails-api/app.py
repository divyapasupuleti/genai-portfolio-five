#!/usr/bin/env python3
"""Guardrails layer: input/output policy + structured response validation."""

from __future__ import annotations

import re
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Guardrails API", version="1.0.0")

BLOCK_INPUT = re.compile(r"(ignore previous|system prompt|jailbreak|api_key)", re.I)
BLOCK_OUTPUT = re.compile(r"(password|ssn|credit card)", re.I)


class Intent(str, Enum):
    support = "support"
    billing = "billing"
    unknown = "unknown"


class ChatIn(BaseModel):
    user_message: str = Field(..., min_length=1, max_length=2000)

    @field_validator("user_message")
    @classmethod
    def no_injection(cls, v: str) -> str:
        if BLOCK_INPUT.search(v):
            raise ValueError("blocked_input_pattern")
        return v.strip()


class ChatOut(BaseModel):
    intent: Intent
    reply: str = Field(..., max_length=500)
    safe: bool = True

    @field_validator("reply")
    @classmethod
    def no_secrets(cls, v: str) -> str:
        if BLOCK_OUTPUT.search(v):
            raise ValueError("blocked_output_pattern")
        return v


def mock_llm(message: str) -> ChatOut:
    low = message.lower()
    if "bill" in low or "invoice" in low:
        intent = Intent.billing
        reply = "I can help with billing. Please open ticket BILL-001."
    elif "help" in low:
        intent = Intent.support
        reply = "Support team will follow up within 24 hours."
    else:
        intent = Intent.unknown
        reply = "I am not sure. A human agent will assist you."
    return ChatOut(intent=intent, reply=reply)


@app.get("/health")
def health():
    return {"status": "ok", "guardrails": ["input_regex", "output_regex", "pydantic_schema"]}


@app.post("/chat", response_model=ChatOut)
def chat(body: ChatIn):
    try:
        return mock_llm(body.user_message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
