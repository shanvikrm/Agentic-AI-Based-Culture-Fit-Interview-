"""API routes for candidate data."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/candidate")
async def upload_candidate() -> dict:
    return {"status": "received"}
