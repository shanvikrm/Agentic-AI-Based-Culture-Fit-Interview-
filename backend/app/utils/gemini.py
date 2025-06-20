import os
import requests

from . import llm


def generate(prompt: str) -> str:
    """Generate text using the Gemini API if configured."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return llm.generate(prompt)

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        f"?key={api_key}"
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # naive extraction of the first candidate text
        return (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
    except Exception:  # pragma: no cover - network issues
        return llm.generate(prompt)
