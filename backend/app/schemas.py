from typing import Any, Dict, List
from pydantic import BaseModel
from bson import ObjectId


class ConfigObjectId:
    json_encoders = {ObjectId: lambda v: str(v)}


class CandidateInput(BaseModel):
    resume_path: str
    linkedin_url: str
    personal_statement: str


class CandidateOutput(BaseModel, ConfigObjectId):
    id: str
    profile: Dict[str, Any]


class CompanyInput(BaseModel):
    sources: List[str]


class CompanyOutput(BaseModel, ConfigObjectId):
    id: str
    cues: Dict[str, Any]


class InterviewInput(BaseModel):
    candidate_id: str
    company_id: str
    responses: List[str]


class InterviewOutput(BaseModel, ConfigObjectId):
    id: str
    questions: List[str]
    evaluation: Dict[str, Any]
    coaching: List[str]

class QuestionsRequest(BaseModel):
    candidate_id: str
    company_id: str

class QuestionsResponse(BaseModel):
    id: str
    questions: List[str]

class InterviewInput(BaseModel):
    id: str                # interview document id
    responses: List[str]
