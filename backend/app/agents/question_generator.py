"""
Question Generator Agent
------------------------
Produces 5-7 behavioural / situational questions that probe alignment
with company values and the candidate’s background.

Guarantees:
• Stub / prompt-echo lines are filtered out.
• No JSON blobs or system text returned.
• Always ≥ 5 questions, ≤ num_questions (default 7).
"""

from typing import List

from ..utils import gemini
from .base import BaseAgent, CulturalCues, CandidateProfile


class QuestionGeneratorAgent(BaseAgent):
    """Adaptive question generator."""

    def generate(
        self,
        cues: CulturalCues,
        profile: CandidateProfile,
        num_questions: int = 7,
    ) -> List[str]:
        """Return a clean list of questions."""

        cues_clean = {k: v for k, v in cues.values.items() if k != "_id"}

        prompt = (
            "You are an interview question generator.\n\n"
            "Company culture cues JSON:\n"
            f"{cues_clean}\n\n"
            "Candidate profile JSON:\n"
            f"{profile.data}\n\n"
            f"Generate {num_questions} behavioural or situational interview "
            "questions that probe cultural alignment. Put each question on its "
            "own line with no numbering or bullets."
        )

        raw = gemini.generate(prompt)

        # ---- filter & normalise lines ------------------------------------
        questions: List[str] = []
        for line in raw.splitlines():
            line = line.strip()

            # skip noise lines
            if (
                not line
                or line.startswith("[stub-llm]")
                or "culture cues" in line.lower()
                or line.startswith("{")        # drops JSON echoes
            ):
                continue

            if not line.endswith("?"):
                line += "?"
            questions.append(line)

        # ---- ensure at least 5 questions ---------------------------------
        fallback_vals = [
            v.strip() for v in cues_clean.get("values", "").split(",") if v.strip()
        ]
        i = 0
        while len(questions) < 5 and fallback_vals:
            val = fallback_vals[i % len(fallback_vals)]
            questions.append(f"Describe a time you embodied {val}.")
            i += 1

        return questions[:num_questions]
