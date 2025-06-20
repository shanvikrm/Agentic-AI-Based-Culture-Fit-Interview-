"""Agent that builds candidate profiles."""

from __future__ import annotations

import os
import re
from typing import Dict, List

import pdfplumber
import requests
from bs4 import BeautifulSoup
from docx import Document

from .base import BaseAgent, CandidateProfile


class CandidateProfileAgent(BaseAgent):
    """Build a candidate profile from uploaded data."""

    def _load_resume(self, path: str) -> str:
        """Return plain text from a resume file."""

        if not os.path.exists(path):
            self.log(f"Resume not found: {path}")
            return ""

        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".pdf":
                with pdfplumber.open(path) as pdf:
                    return "\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    )
            if ext in {".docx", ".doc"}:
                doc = Document(path)
                return "\n".join(p.text for p in doc.paragraphs)
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as exc:  # pragma: no cover - file errors
            self.log(f"Failed to read resume: {exc}")
            return ""

    def _load_linkedin(self, url: str) -> str:
        """Fetch a LinkedIn profile and return visible text."""

        if not url:
            return ""
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            return "\n".join(soup.stripped_strings)
        except Exception as exc:  # pragma: no cover - network errors
            self.log(f"Failed to fetch LinkedIn profile: {exc}")
            return ""

    @staticmethod
    def _extract_sections(text: str) -> Dict[str, List[str]]:
        """Very small heuristic extractor for skills, experience and achievements."""

        skills: List[str] = []
        experience: List[str] = []
        achievements: List[str] = []
        for line in text.splitlines():
            line = line.strip()
            lower = line.lower()
            if not line:
                continue
            if re.search(r"^skills?[:\-]", lower):
                skills_line = re.split(r"[:\-]", line, 1)[-1]
                skills.extend(re.split(r",|;", skills_line))
            elif "experience" in lower:
                experience.append(line)
            elif "achievement" in lower or "accomplish" in lower:
                achievements.append(line)
        return {
            "skills": [s.strip() for s in skills if s.strip()],
            "experience": experience,
            "achievements": achievements,
        }

    @staticmethod
    def _extract_values(statement: str) -> List[str]:
        """Extract value keywords from a personal statement."""

        keywords = ["collaboration", "innovation", "integrity", "diversity", "customer"]
        lowered = statement.lower()
        return [kw for kw in keywords if kw in lowered]

    def build_profile(self, resume_path: str, linkedin_url: str, statement: str) -> CandidateProfile:
        """Create a structured candidate profile."""

        self.log("Building profile")

        resume_text = self._load_resume(resume_path)
        linkedin_text = self._load_linkedin(linkedin_url)

        combined = "\n".join([resume_text, linkedin_text, statement])
        sections = self._extract_sections(combined)
        values = self._extract_values(statement)

        data: Dict[str, object] = {
            "resume_text": resume_text,
            "linkedin_text": linkedin_text,
            "personal_statement": statement.strip(),
            "skills": sections.get("skills", []),
            "experience": sections.get("experience", []),
            "achievements": sections.get("achievements", []),
            "values": values,
        }

        return CandidateProfile(data=data)
