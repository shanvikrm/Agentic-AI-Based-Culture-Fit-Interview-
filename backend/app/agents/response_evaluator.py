"""Response Evaluator Agent.

Scores answers for cultural alignment, sentiment, and depth.
"""

import re
from typing import Any, Dict, List

from ..utils import gemini
from .base import BaseAgent, CulturalCues


class ResponseEvaluatorAgent(BaseAgent):
    """Produces per-answer scores + feedback and an overall score."""

    _POSITIVE = {"good", "great", "excellent", "love", "happy", "positive"}
    _NEGATIVE = {"bad", "poor", "hate", "angry", "negative", "terrible"}

    def evaluate(
        self,
        responses: List[str],
        cues: CulturalCues,
        questions: List[str] | None = None,
    ) -> Dict[str, Any]:
        self.log("Evaluating responses")

        values = [
            v.strip().lower() for v in cues.values.get("values", "").split(",") if v
        ]

        results: List[Dict[str, Any]] = []
        total = 0

        for resp in responses:
            lower = resp.lower()

            align = sum(1 for v in values if v in lower) / max(1, len(values))

            words = re.findall(r"\w+", lower)
            pos = sum(w in self._POSITIVE for w in words)
            neg = sum(w in self._NEGATIVE for w in words)
            sentiment = (pos - neg) / max(1, len(words))

            depth = min(1.0, len(words) / 120)
            if any(k in lower for k in ("for example", "such as", "i led", "i managed")):
                depth = min(1.0, depth + 0.2)

            score = int(70 * align + 20 * depth + 10 * ((sentiment + 1) / 2))
            total += score

            feedback_prompt = (
                f"Company values: {values}\n"
                f"Response: \"{resp}\"\n"
                "Give one sentence of feedback on cultural alignment—mention one "
                "strength and one area to improve."
            )
            feedback = gemini.generate(feedback_prompt).strip()
            if feedback.startswith("[stub-llm]"):
                feedback = feedback.replace("[stub-llm] →", "").strip()

            results.append({"response": resp, "score": score, "feedback": feedback})

        overall = int(total / max(1, len(responses)))
        return {"overall_score": overall, "responses": results}
