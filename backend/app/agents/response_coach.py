"""Response Coaching Agent.

Provides short actionable improvements for each answer.
"""

from typing import Any, Dict, List

from ..utils import gemini
from .base import BaseAgent, CulturalCues


class ResponseCoachingAgent(BaseAgent):
    """One concise suggestion per response."""

    def coach(
        self,
        responses: List[str],
        evaluation: Dict[str, Any],
        cues: CulturalCues,
    ) -> List[str]:
        self.log("Coaching responses")

        suggestions: List[str] = []
        values = cues.values.get("values", "")
        for resp, detail in zip(responses, evaluation.get("responses", [])):
            prompt = (
                f"Company values: {values}\n"
                f"Candidate response: {resp}\n"
                f"Evaluator feedback: {detail.get('feedback','')}\n"
                "Provide ONE actionable suggestion (max 25 words) to improve the "
                "response and better align it with the company culture."
            )
            suggestion = gemini.generate(prompt).strip()
            if suggestion.startswith("[stub-llm]"):
                suggestion = suggestion.replace("[stub-llm] →", "").strip()
            suggestions.append(suggestion)

        return suggestions
