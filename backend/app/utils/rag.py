"""Retrieval-augmented generation utilities."""


def retrieve(query: str) -> str:
    """Return placeholder retrieval results."""
    return f"Retrieved docs for: {query}"
