from copy import deepcopy
from bson import ObjectId
from fastapi import APIRouter, HTTPException

from ..agents.base import CandidateProfile, CulturalCues
from ..agents.question_generator   import QuestionGeneratorAgent
from ..agents.response_evaluator   import ResponseEvaluatorAgent
from ..agents.response_coach       import ResponseCoachingAgent
from ..database import db
from ..schemas  import (
    InterviewInput,            # still used for answers
    InterviewOutput,
    QuestionsRequest,          # <-- new Pydantic models
    QuestionsResponse,
)

router = APIRouter()


@router.post("/interview/questions", response_model=QuestionsResponse)
async def get_questions(req: QuestionsRequest) -> QuestionsResponse:
    """Phase 1 – generate questions only."""
    cand = db.candidates.find_one({"_id": ObjectId(req.candidate_id)})
    comp = db.companies .find_one({"_id": ObjectId(req.company_id)})
    if not cand or not comp:
        raise HTTPException(404, "Candidate or company not found")

    q_agent   = QuestionGeneratorAgent()
    questions = q_agent.generate(
        CulturalCues(values=deepcopy(comp)),
        CandidateProfile(data=deepcopy(cand)),
    )

    # Persist draft interview doc (status: pending answers)
    doc = {
        "candidate_id": req.candidate_id,
        "company_id"  : req.company_id,
        "questions"   : questions,
        "evaluation"  : None,
        "coaching"    : None,
    }
    interview_id = str(db.interviews.insert_one(doc).inserted_id)
    return QuestionsResponse(id=interview_id, questions=questions)


@router.post("/interview/answers", response_model=InterviewOutput)
async def submit_answers(data: InterviewInput) -> InterviewOutput:
    """Phase 2 – evaluate answers and coach."""
    interview = db.interviews.find_one({"_id": ObjectId(data.id)})
    if not interview:
        raise HTTPException(404, "Interview not found")

    comp = db.companies .find_one({"_id": ObjectId(interview["company_id"])})
    cues = CulturalCues(values=deepcopy(comp))

    evaluator  = ResponseEvaluatorAgent()
    evaluation = evaluator.evaluate(data.responses, cues, interview["questions"])

    coach      = ResponseCoachingAgent()
    coaching   = coach.coach(data.responses, evaluation, cues)

    # update and return
    db.interviews.update_one(
        {"_id": interview["_id"]},
        {"$set": {"evaluation": evaluation, "coaching": coaching}},
    )
    interview.update({"evaluation": evaluation, "coaching": coaching})
    interview["id"] = str(interview["_id"])
    interview.pop("_id")
    return InterviewOutput(**interview)
