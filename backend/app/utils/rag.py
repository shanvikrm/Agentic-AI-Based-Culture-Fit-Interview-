"""
RAG helper – tiny in-memory vector store.

• Uses OpenAI embeddings if OPENAI_API_KEY set, else sentence-transformers.
• Stores (text, embedding) pairs in a global list.
• retrieve(query) → top-k (default 3) snippets concatenated.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import List, Tuple

_DOCS: List[Tuple[str, List[float]]] = []   # (text, embedding)

_OPENAI_KEY = os.getenv("OPENAI_API_KEY")


# --------------------------------------------------------------------- #
# embedding
# --------------------------------------------------------------------- #
def _embed(text: str) -> List[float]:
    text = text.replace("\n", " ")[:4096]
    if _OPENAI_KEY:
        import openai

        openai.api_key = _OPENAI_KEY
        vec = openai.Embedding.create(
            model="text-embedding-3-small",
            input=text,
        )["data"][0]["embedding"]
        return vec

    # fallback: local sentence-transformers (all-MiniLM)
    from sentence_transformers import SentenceTransformer

    _model = getattr(_embed, "_model", None)
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        _embed._model = _model  # type: ignore
    return _model.encode(text).tolist()


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-8)


# --------------------------------------------------------------------- #
# public API
# --------------------------------------------------------------------- #
def add_corpus(path: str | Path):
    """Index a UTF-8 text file or directory of .txt docs."""
    path = Path(path)
    if path.is_dir():
        for f in path.glob("*.txt"):
            add_corpus(f)
        return

    txt = Path(path).read_text(encoding="utf-8", errors="ignore")
    _DOCS.append((txt, _embed(txt)))


def retrieve(query: str, k: int = 3) -> str:
    """Return concatenated top-k snippets most similar to *query*."""
    if not _DOCS:
        return ""

    q_vec = _embed(query)
    scored = sorted(
        (( _cosine(q_vec, emb), txt) for txt, emb in _DOCS),
        key=lambda x: -x[0],
    )[:k]
    return "\n\n".join(t for _, t in scored)
