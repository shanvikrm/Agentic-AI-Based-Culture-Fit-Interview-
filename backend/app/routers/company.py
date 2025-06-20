"""API routes for company data."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/company")
async def upload_company() -> dict:
    return {"status": "received"}
