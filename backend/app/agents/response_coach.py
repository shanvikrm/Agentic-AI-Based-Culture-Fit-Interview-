"""Agent that provides coaching feedback."""

from typing import Any, Dict, List

from ..utils import gemini

from .base import BaseAgent, CulturalCues


class ResponseCoachingAgent(BaseAgent):
    """Provide coaching feedback for responses."""

    def coach(
        self, responses: List[str], evaluation: Dict[str, Any], cues: CulturalCues
    ) -> List[str]:
        self.log("Coaching responses")

        suggestions: List[str] = []
        eval_details = evaluation.get("responses", [])
        values = cues.values.get("values", "")

        for resp, detail in zip(responses, eval_details):
            prompt = (
                f"Company values: {values}. Candidate response: {resp}. "
                "Provide one actionable suggestion to improve this answer."
            )
            suggestions.append(gemini.generate(prompt).strip())

        return suggestions
