#!/usr/bin/env python3
"""Ingest text files into Chroma with local embeddings."""

from __future__ import annotations

import argparse
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

DATA_DIR = Path(__file__).parent / "data"
CHROMA_PATH = Path(__file__).parent / ".chroma"
COLLECTION = "knowledge"


def chunk_text(text: str, size: int = 400, overlap: int = 80) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    i = 0
    while i < len(words):
        piece = words[i : i + size]
        chunks.append(" ".join(piece))
        i += max(1, size - overlap)
    return chunks or [text]


def ingest(data_dir: Path) -> int:
    embed = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION, embedding_function=embed)

    ids, docs, metas = [], [], []
    n = 0
    for path in sorted(data_dir.glob("**/*")):
        if path.suffix.lower() not in {".txt", ".md"}:
            continue
        text = path.read_text(encoding="utf-8")
        for j, ch in enumerate(chunk_text(text)):
            cid = f"{path.stem}-{j}"
            ids.append(cid)
            docs.append(ch)
            metas.append({"source": str(path.name), "chunk": j})
            n += 1
    if ids:
        col.add(ids=ids, documents=docs, metadatas=metas)
    return n


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=Path, default=DATA_DIR)
    args = p.parse_args()
    count = ingest(args.data)
    print(f"Ingested {count} chunks into {CHROMA_PATH}")


if __name__ == "__main__":
    main()
