"""
Light-weight LLM helper
=======================
Supports OpenAI Chat and Gemini-pro, otherwise falls back to a stub.

Usage:
    from backend.app.utils.llm import generate
    print(generate("Hello"))
"""

from __future__ import annotations

import functools
import os
from typing import Literal

import requests
from dotenv import load_dotenv

# ------------------------------------------------------------------ #
# env setup
# ------------------------------------------------------------------ #
load_dotenv()  # load .env if present

_PROVIDER: Literal["openai", "gemini", "stub"] = (
    os.getenv("LLM_PROVIDER", "").lower() or "stub"
)
_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
_GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if _PROVIDER == "openai" and not _OPENAI_KEY:
    _PROVIDER = "stub"
if _PROVIDER == "gemini" and not _GEMINI_KEY:
    _PROVIDER = "stub"


# ------------------------------------------------------------------ #
# internal callers
# ------------------------------------------------------------------ #
def _call_openai(prompt: str) -> str:
    import openai

    openai.api_key = _OPENAI_KEY
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        timeout=20,
    )
    return resp.choices[0].message.content.strip()


def _call_gemini(prompt: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-pro:generateContent?key=" + _GEMINI_KEY
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=payload, timeout=20)
    if not r.ok:
        print("Gemini HTTP error:", r.status_code, r.text[:120])
    r.raise_for_status()
    data = r.json()
    return (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
        .strip()
    )


# ------------------------------------------------------------------ #
# public API
# ------------------------------------------------------------------ #
@functools.lru_cache(maxsize=256)
def generate(prompt: str) -> str:
    """Return LLM response (cached). Falls back to stub on error."""
    if _PROVIDER == "openai":
        try:
            return _call_openai(prompt)
        except Exception as exc:
            print("OpenAI call failed:", exc)

    if _PROVIDER == "gemini":
        try:
            return _call_gemini(prompt)
        except Exception as exc:
            print("Gemini call failed:", exc)

    return f"[stub-llm] → {prompt[:120]}..."
