"""Agent that builds candidate profiles."""

from .base import BaseAgent, CandidateProfile


class CandidateProfileAgent(BaseAgent):
    """Build a candidate profile from uploaded data."""

    def build_profile(self, resume_path: str, linkedin_url: str, statement: str) -> CandidateProfile:
        self.log("Building profile")
        return CandidateProfile(data={})
