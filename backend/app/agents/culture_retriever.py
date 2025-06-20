"""Agent that extracts company cultural cues."""

from typing import List

from .base import BaseAgent, CulturalCues
from ..utils import rag


class CompanyCultureRetrieverAgent(BaseAgent):
    """Extract cultural cues from company documents or URLs."""

    def retrieve(self, sources: List[str]) -> CulturalCues:
        self.log(f"Retrieving culture from {sources}")
        _ = rag.retrieve(" ".join(sources))
        return CulturalCues(values={})
