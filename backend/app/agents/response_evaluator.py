"""Agent that evaluates interview responses."""

from typing import Any, Dict, List

from .base import BaseAgent, CulturalCues


class ResponseEvaluatorAgent(BaseAgent):
    """Evaluate candidate responses."""

    def evaluate(self, responses: List[str], cues: CulturalCues) -> Dict[str, Any]:
        self.log("Evaluating responses")
        return {}
