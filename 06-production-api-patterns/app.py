"""Production-style FastAPI skeleton for LLM gateway demos."""

from __future__ import annotations

import hashlib
import logging
import uuid
from typing import Any

from fastapi import FastAPI, Header, Request
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("llm-gateway")

app = FastAPI(title="LLM Gateway Patterns", version="1.0.0")

_cache: dict[str, dict[str, Any]] = {}


class CompleteIn(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    use_cache: bool = True


class CompleteOut(BaseModel):
    trace_id: str
    text: str
    cached: bool


def cache_key(prompt: str) -> str:
    normalized = " ".join(prompt.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()


def mock_llm(prompt: str) -> str:
    return f"Echo (demo): {prompt[:200]}"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/complete", response_model=CompleteOut)
def complete(
    body: CompleteIn,
    request: Request,
    x_trace_id: str | None = Header(default=None, alias="X-Trace-Id"),
) -> CompleteOut:
    trace_id = x_trace_id or str(uuid.uuid4())
    key = cache_key(body.prompt)
    if body.use_cache and key in _cache:
        log.info('{"trace_id":"%s","event":"cache_hit"}', trace_id)
        hit = _cache[key]
        return CompleteOut(trace_id=trace_id, text=hit["text"], cached=True)

    text = mock_llm(body.prompt)
    _cache[key] = {"text": text}
    log.info(
        '{"trace_id":"%s","event":"inference","path":"%s"}',
        trace_id,
        request.url.path,
    )
    return CompleteOut(trace_id=trace_id, text=text, cached=False)
