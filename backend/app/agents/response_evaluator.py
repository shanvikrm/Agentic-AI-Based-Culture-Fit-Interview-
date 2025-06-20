"""Agent that evaluates interview responses."""

import re
from typing import Any, Dict, List

from ..utils import gemini
from .base import BaseAgent, CulturalCues


class ResponseEvaluatorAgent(BaseAgent):
    """Evaluate candidate responses."""

    def evaluate(self, responses: List[str], cues: CulturalCues) -> Dict[str, Any]:
        self.log("Evaluating responses")

        values = [v.strip().lower() for v in cues.values.get("values", "").split(",") if v]
        results = []
        total = 0

        positive = {"good", "great", "excellent", "positive", "happy", "love"}
        negative = {"bad", "poor", "negative", "hate", "angry"}

        for resp in responses:
            lower = resp.lower()
            align = sum(1 for v in values if v in lower) / max(1, len(values))
            words = re.findall(r"\w+", lower)
            pos = sum(w in positive for w in words)
            neg = sum(w in negative for w in words)
            sentiment = (pos - neg) / max(1, len(words))

            align_score = int(align * 70)
            sentiment_score = int(((sentiment + 1) / 2) * 30)
            score = align_score + sentiment_score
            total += score

            feedback_prompt = (
                f"Company values: {values}. Response: '{resp}'. "
                "Provide one sentence of feedback on cultural alignment."
            )
            feedback = gemini.generate(feedback_prompt).strip()

            results.append({"response": resp, "score": score, "feedback": feedback})

        overall = int(total / max(1, len(responses)))
        return {"overall_score": overall, "responses": results}
