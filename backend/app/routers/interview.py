"""API routes for running interviews."""

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from ..agents.base import CandidateProfile, CulturalCues
from ..agents.question_generator import QuestionGeneratorAgent
from ..agents.response_coach import ResponseCoachingAgent
from ..agents.response_evaluator import ResponseEvaluatorAgent
from ..database import db
from ..schemas import InterviewInput, InterviewOutput


router = APIRouter()


@router.post("/interview", response_model=InterviewOutput)
async def start_interview(data: InterviewInput) -> InterviewOutput:
    """Run the interview process and store results."""
    candidate = db.candidates.find_one({"_id": ObjectId(data.candidate_id)})
    company = db.companies.find_one({"_id": ObjectId(data.company_id)})
    if not candidate or not company:
        raise HTTPException(status_code=404, detail="Candidate or company not found")

    profile = CandidateProfile(data=candidate)
    cues = CulturalCues(values=company)

    q_agent = QuestionGeneratorAgent()
    questions = q_agent.generate(cues, profile)

    evaluator = ResponseEvaluatorAgent()
    evaluation = evaluator.evaluate(data.responses, cues)

    coach = ResponseCoachingAgent()
    coaching = coach.coach(data.responses, evaluation, cues)

    doc = {
        "candidate_id": data.candidate_id,
        "company_id": data.company_id,
        "questions": questions,
        "evaluation": evaluation,
        "coaching": coaching,
    }
    result = db.interviews.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return InterviewOutput(**doc)
