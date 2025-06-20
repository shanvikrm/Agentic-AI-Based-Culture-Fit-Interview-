"""FastAPI application for the culture fit interview backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import candidate, company, interview


app = FastAPI(title="Culture Fit Interview API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate.router)
app.include_router(company.router)
app.include_router(interview.router)

