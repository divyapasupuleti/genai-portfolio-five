#!/usr/bin/env python3
"""RAG API: retrieve chunks + optional OpenAI generation with citations."""

from __future__ import annotations

import os
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

CHROMA_PATH = Path(__file__).parent / ".chroma"
COLLECTION = "knowledge"

app = FastAPI(title="RAG Assistant", version="1.0.0")


class QueryIn(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(3, ge=1, le=10)


class Citation(BaseModel):
    source: str
    excerpt: str


class QueryOut(BaseModel):
    answer: str
    citations: list[Citation]


def get_collection():
    embed = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_collection(COLLECTION, embedding_function=embed)


def retrieve(question: str, top_k: int) -> list[Citation]:
    col = get_collection()
    res = col.query(query_texts=[question], n_results=top_k)
    cites: list[Citation] = []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        cites.append(Citation(source=meta.get("source", "unknown"), excerpt=doc[:500]))
    return cites


def generate_answer(question: str, cites: list[Citation]) -> str:
    context = "\n\n".join(f"[{c.source}] {c.excerpt}" for c in cites)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "Retrieval-only mode (set OPENAI_API_KEY for generation).\n\n"
            f"Based on retrieved context:\n{context[:1200]}"
        )
    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    msg = [
        {
            "role": "system",
            "content": "Answer using only the context. Cite sources by name. If unsure, say you don't know.",
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    r = client.chat.completions.create(model=model, messages=msg, temperature=0.2)
    return r.choices[0].message.content or ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryOut)
def query(body: QueryIn):
    cites = retrieve(body.question, body.top_k)
    answer = generate_answer(body.question, cites)
    return QueryOut(answer=answer, citations=cites)
