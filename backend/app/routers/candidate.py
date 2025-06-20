from copy import deepcopy
from fastapi import APIRouter, HTTPException
from bson import ObjectId
import logging

from ..agents.candidate_profile import CandidateProfileAgent
from ..database import db
from ..schemas import CandidateInput, CandidateOutput

router = APIRouter()
log = logging.getLogger("uvicorn.error")


def clean_bson(obj):
    if isinstance(obj, dict):
        return {k: clean_bson(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_bson(v) for v in obj]
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


@router.post("/candidate", response_model=CandidateOutput)
async def upload_candidate(data: CandidateInput) -> CandidateOutput:
    agent = CandidateProfileAgent()

    linkedin = data.linkedin_url.strip()
    if linkedin and not linkedin.startswith(("http://", "https://")):
        linkedin = "https://" + linkedin

    try:
        profile = agent.build_profile(
            data.resume_path, linkedin, data.personal_statement
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    profile_dict = deepcopy(clean_bson(profile.data))
    result = db.candidates.insert_one(profile_dict)
    profile_dict.pop("_id", None)

    return CandidateOutput(id=str(result.inserted_id), profile=profile_dict)
