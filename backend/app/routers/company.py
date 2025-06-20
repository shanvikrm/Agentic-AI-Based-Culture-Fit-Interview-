"""API routes for company data."""

from fastapi import APIRouter

from ..agents.culture_retriever import CompanyCultureRetrieverAgent
from ..database import db
from ..schemas import CompanyInput, CompanyOutput


router = APIRouter()


@router.post("/company", response_model=CompanyOutput)
async def upload_company(data: CompanyInput) -> CompanyOutput:
    """Extract cultural cues and store them in MongoDB."""
    agent = CompanyCultureRetrieverAgent()
    cues = agent.retrieve(data.sources)
    result = db.companies.insert_one(cues.values)
    return CompanyOutput(id=str(result.inserted_id), cues=cues.values)
