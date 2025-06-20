from copy import deepcopy
from fastapi import APIRouter
from bson import ObjectId

from ..agents.culture_retriever import CompanyCultureRetrieverAgent
from ..database import db
from ..schemas import CompanyInput, CompanyOutput

router = APIRouter()


def clean_bson(obj):
    if isinstance(obj, dict):
        return {k: clean_bson(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_bson(v) for v in obj]
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


@router.post("/company", response_model=CompanyOutput)
async def upload_company(data: CompanyInput) -> CompanyOutput:
    agent = CompanyCultureRetrieverAgent()
    cues = agent.retrieve(data.sources)

    cues_dict = deepcopy(clean_bson(cues.values))
    result = db.companies.insert_one(cues_dict)
    cues_dict.pop("_id", None)

    return CompanyOutput(id=str(result.inserted_id), cues=cues_dict)
