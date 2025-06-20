"""Company Culture Retriever Agent using Retrieval-Augmented Generation (RAG).

This agent loads company related material from a variety of sources
(PDF/DOCX/text files or web URLs), performs basic HTML/PDF/DOCX parsing,
filters obviously irrelevant lines and then attempts to extract cultural
information such as mission, vision and values.  The extracted text is then
passed through placeholder RAG utilities to simulate enrichment with
industry standard cultural frameworks.
"""

from __future__ import annotations

import os
from typing import Dict, List

import pdfplumber
import requests
from bs4 import BeautifulSoup
from docx import Document

from .base import BaseAgent, CulturalCues
from ..utils import llm, rag


class CompanyCultureRetrieverAgent(BaseAgent):
    """Extract cultural cues from company documents or URLs."""

    FILTER_TERMS = ["advertisement", "cookie policy", "all rights reserved"]

    def _load_source(self, source: str) -> str:
        """Return text from a file path or URL with basic parsing."""

        if source.startswith("http://") or source.startswith("https://"):
            self.log(f"Fetching URL: {source}")
            try:
                resp = requests.get(source, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["script", "style"]):
                    tag.decompose()
                return "\n".join(soup.stripped_strings)
            except Exception as exc:  # pragma: no cover - network errors
                self.log(f"Failed to fetch {source}: {exc}")
                return ""

        if not os.path.exists(source):
            self.log(f"Source not found: {source}")
            return ""

        ext = os.path.splitext(source)[1].lower()
        try:
            if ext == ".pdf":
                with pdfplumber.open(source) as pdf:
                    return "\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    )
            if ext in {".docx", ".doc"}:
                doc = Document(source)
                return "\n".join(p.text for p in doc.paragraphs)
            with open(source, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as exc:  # pragma: no cover - file errors
            self.log(f"Failed to read {source}: {exc}")
            return ""

    def _filter_text(self, text: str) -> str:
        """Remove lines containing obviously irrelevant content."""

        lines = [
            ln.strip()
            for ln in text.splitlines()
            if ln.strip() and not any(t in ln.lower() for t in self.FILTER_TERMS)
        ]
        return "\n".join(lines)

    def _extract_cues(self, text: str) -> Dict[str, str]:
        """Very small heuristic extractor for cultural elements."""

        lowered = text.lower()
        cues: Dict[str, str] = {}

        if "mission" in lowered:
            idx = lowered.find("mission")
            end = text.find(".", idx) + 1 or idx + 200
            cues["mission"] = text[idx:end].strip()

        if "vision" in lowered:
            idx = lowered.find("vision")
            end = text.find(".", idx) + 1 or idx + 200
            cues["vision"] = text[idx:end].strip()

        values = []
        for kw in ["collaboration", "innovation", "diversity", "integrity", "customer"]:
            if kw in lowered:
                values.append(kw)
        if "values" in lowered:
            idx = lowered.find("values")
            snippet = text[idx : idx + 200]
            values.append(snippet.strip())
        if values:
            cues["values"] = ", ".join(dict.fromkeys(values))

        return cues

    def _rag_enrich(self, cues: Dict[str, str]) -> Dict[str, str]:
        """Use placeholder RAG utilities and LLM to enrich cues."""

        query = " ".join(cues.values())
        retrieved = rag.retrieve(query)
        # The real implementation would call Gemini or another LLM.  Here we
        # simply simulate the call and include the API key check for completeness.
        if not os.getenv("GEMINI_API_KEY"):
            self.log("Warning: GEMINI_API_KEY not configured")
        summary = llm.generate(f"{query}\n{retrieved}")
        cues["rag_summary"] = summary
        return cues

    def retrieve(self, sources: List[str]) -> CulturalCues:
        """Retrieve cultural cues from the provided sources."""

        self.log(f"Retrieving culture from {sources}")
        raw = "\n".join(self._load_source(src) for src in sources)
        filtered = self._filter_text(raw)
        cues = self._extract_cues(filtered)
        enriched = self._rag_enrich(cues)
        return CulturalCues(values=enriched)
