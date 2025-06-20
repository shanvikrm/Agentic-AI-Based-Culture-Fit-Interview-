"""Agent that generates interview questions."""

from typing import List

from .base import BaseAgent, CulturalCues, CandidateProfile


class QuestionGeneratorAgent(BaseAgent):
    """Generate culture-fit interview questions."""

    def generate(self, cues: CulturalCues, profile: CandidateProfile) -> List[str]:
        self.log("Generating questions")
        return []
