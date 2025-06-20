"""Agent that generates interview questions."""

from typing import List

from ..utils import gemini

from .base import BaseAgent, CulturalCues, CandidateProfile


class QuestionGeneratorAgent(BaseAgent):
    """Generate culture-fit interview questions."""

    def generate(self, cues: CulturalCues, profile: CandidateProfile) -> List[str]:
        self.log("Generating questions")

        prompt = (
            "Generate five culture-fit interview questions based on the following "
            "company cultural cues and candidate profile."
            " Return each question on a new line.\n"
            f"Cues: {cues.values}\nProfile: {profile.data}"
        )

        raw = gemini.generate(prompt)
        questions = [q.strip("- ") for q in raw.splitlines() if q.strip()]
        return questions[:5]
