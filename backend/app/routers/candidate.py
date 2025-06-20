"""API routes for candidate data."""

from fastapi import APIRouter

from ..agents.candidate_profile import CandidateProfileAgent
from ..database import db
from ..schemas import CandidateInput, CandidateOutput


router = APIRouter()


@router.post("/candidate", response_model=CandidateOutput)
async def upload_candidate(data: CandidateInput) -> CandidateOutput:
    """Build a candidate profile and store it in MongoDB."""
    agent = CandidateProfileAgent()
    profile = agent.build_profile(
        data.resume_path, data.linkedin_url, data.personal_statement
    )
    result = db.candidates.insert_one(profile.data)
    return CandidateOutput(id=str(result.inserted_id), profile=profile.data)
