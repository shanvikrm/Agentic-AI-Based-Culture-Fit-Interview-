"""FastAPI application for the culture fit interview backend."""

from fastapi import FastAPI

from .routers import candidate, company, interview


app = FastAPI(title="Culture Fit Interview API")

app.include_router(candidate.router)
app.include_router(company.router)
app.include_router(interview.router)

