"""Base classes and data models for agents."""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CulturalCues:
    values: Dict[str, Any]


@dataclass
class CandidateProfile:
    data: Dict[str, Any]


class BaseAgent:
    """Common functionality for all agents."""

    def log(self, message: str) -> None:
        print(f"[Agent] {message}")
