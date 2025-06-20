"""API routes for running interviews."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/interview")
async def start_interview() -> dict:
    return {"questions": []}
