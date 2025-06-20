"""Agent that provides coaching feedback."""

from typing import Any, Dict, List

from .base import BaseAgent, CulturalCues


class ResponseCoachingAgent(BaseAgent):
    """Provide coaching feedback for responses."""

    def coach(
        self, responses: List[str], evaluation: Dict[str, Any], cues: CulturalCues
    ) -> List[str]:
        self.log("Coaching responses")
        return []
