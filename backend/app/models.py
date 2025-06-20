"""Pydantic models for MongoDB documents."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CandidateModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    profile: Dict[str, Any]


class CompanyModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    cues: Dict[str, Any]


class InterviewModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    candidate_id: str
    company_id: str
    questions: List[str]
    evaluation: Dict[str, Any]
    coaching: List[str]
