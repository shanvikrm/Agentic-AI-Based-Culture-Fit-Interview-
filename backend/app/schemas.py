"""Pydantic request and response schemas."""

from typing import Any, Dict, List

from pydantic import BaseModel


class CandidateInput(BaseModel):
    resume_path: str
    linkedin_url: str
    personal_statement: str


class CandidateOutput(BaseModel):
    id: str
    profile: Dict[str, Any]


class CompanyInput(BaseModel):
    sources: List[str]


class CompanyOutput(BaseModel):
    id: str
    cues: Dict[str, Any]


class InterviewInput(BaseModel):
    candidate_id: str
    company_id: str
    responses: List[str]


class InterviewOutput(BaseModel):
    id: str
    questions: List[str]
    evaluation: Dict[str, Any]
    coaching: List[str]
