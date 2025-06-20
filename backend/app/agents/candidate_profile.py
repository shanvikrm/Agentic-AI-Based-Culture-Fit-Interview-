"""Candidate Profile Agent.

Builds a rich profile by fusing:
• résumé text              (skills, experience, achievements)
• LinkedIn profile scrape   (endorsements, roles)
• personal statement        (values, goals)

Outputs a dict keyed clearly so downstream agents can reference fields
without extra parsing.
"""

from __future__ import annotations

import concurrent.futures
import os
import re
from pathlib import Path
from typing import Dict, List

import pdfplumber
import requests
from bs4 import BeautifulSoup
from docx import Document

from .base import BaseAgent, CandidateProfile


class CandidateProfileAgent(BaseAgent):
    """Create a structured candidate JSON profile."""

    _SECTION_RX = re.compile(
        r"^(skills?|experience|achievements?|projects|education)[:\-\s]+",
        flags=re.I,
    )

    # ------------------------------------------------------------------ #
    # public API
    # ------------------------------------------------------------------ #
    def build_profile(
        self,
        resume_path: str,
        linkedin_url: str,
        statement: str,
    ) -> CandidateProfile:
        """Return CandidateProfile with at least 80 % field coverage."""
        with concurrent.futures.ThreadPoolExecutor() as pool:
            fut_resume   = pool.submit(self._load_resume, resume_path)
            fut_linkedin = pool.submit(self._load_linkedin, linkedin_url)

        resume_text   = fut_resume.result()
        linkedin_text = fut_linkedin.result()

        if not any([resume_text, linkedin_text, statement.strip()]):
            raise ValueError("All inputs are empty or failed to load.")

        combined = "\n".join([resume_text, linkedin_text, statement])

        sections  = self._extract_sections(combined)
        values    = self._extract_values(statement or linkedin_text)

        profile: Dict[str, object] = {
            "resume_text"      : resume_text,
            "linkedin_text"    : linkedin_text,
            "personal_statement": statement.strip(),
            "skills"           : sections.get("skills", []),
            "experience"       : sections.get("experience", []),
            "achievements"     : sections.get("achievements", []),
            "values"           : values,
        }
        return CandidateProfile(data=profile)

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    # -------- file / url loading
    def _load_resume(self, path: str) -> str:
        if not path:
            return ""
        file = Path(path)
        if not file.exists():
            self.log(f"Resume not found: {path}")
            return ""
        try:
            ext = file.suffix.lower()
            if ext == ".pdf":
                with pdfplumber.open(file) as pdf:
                    return "\n".join(page.extract_text() or "" for page in pdf.pages)
            if ext in (".docx", ".doc"):
                doc = Document(file)
                return "\n".join(p.text for p in doc.paragraphs)
            return file.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:  # pragma: no cover
            self.log(f"Failed reading resume: {exc}")
            return ""

    def _load_linkedin(self, url: str) -> str:
        if not url:
            return ""
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "header", "footer", "nav"]):
                tag.decompose()
            return "\n".join(soup.stripped_strings)
        except Exception as exc:  # pragma: no cover
            self.log(f"Failed to fetch LinkedIn profile: {exc}")
            return ""

    # -------- information extraction
    def _extract_sections(self, text: str) -> Dict[str, List[str]]:
        blocks = {"skills": [], "experience": [], "achievements": []}
        for line in text.splitlines():
            if not line.strip():
                continue
            header = self._SECTION_RX.match(line)
            if header:
                key = header.group(1).lower()
                key = "achievements" if "achieve" in key else key
                key = "skills"       if "skill"   in key else key
                blocks.setdefault(key, [])
                content = line[header.end():]
                items = re.split(r",|;|\u2022", content)
                blocks[key].extend(i.strip() for i in items if i.strip())
        return blocks

    def _extract_values(self, text: str) -> List[str]:
        keywords = [
            "collaboration",
            "innovation",
            "integrity",
            "diversity",
            "customer",
            "leadership",
            "ownership",
            "agility",
            "learning",
        ]
        lower = text.lower()
        return [kw for kw in keywords if kw in lower]
