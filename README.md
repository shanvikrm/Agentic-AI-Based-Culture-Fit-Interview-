# Agentic AI-Based Culture Fit Interview Simulator

This repository aims to build an **Agentic AI-powered Culture Fit Interview Simulator**. The system uses a multi-agent architecture with Retrieval-Augmented Generation (RAG) to assess a candidate's cultural alignment and provide coaching feedback.

## Objectives
- Build a web platform for uploading candidate data (resume, LinkedIn, personal statement) and company cultural documents or URLs.
- Integrate an Agentic AI workflow in a single RAG-enabled agent for retrieving cultural cues.
- Implement multiple specialized agents to handle candidate profiling, question generation, response evaluation, and coaching.
- Store profiles, questions, evaluations, and feedback in a MongoDB database.
- Ensure explainable, unbiased scoring with sentiment analysis.

## System Architecture
1. **Company Culture Retriever Agent**
   - Uses RAG to extract cultural cues from documents or websites.
   - Accepts PDF, DOCX, text, or URLs and outputs structured JSON.
2. **Candidate Profile Agent**
   - Processes resumes, LinkedIn profiles, and personal statements to build a candidate profile.
   - Handles multiple input formats and outputs structured JSON.
3. **Question Generator Agent**
   - Generates adaptive culture-fit interview questions based on cultural cues and candidate profile.
4. **Response Evaluator Agent**
   - Scores candidate responses for alignment with company values and provides feedback.
5. **Response Coaching Agent**
   - Offers actionable suggestions to improve candidate answers.

## Example Flow
1. Upload company and candidate data via the frontend.
2. The Company Culture Retriever Agent produces cultural cues JSON.
3. The Candidate Profile Agent builds a candidate profile JSON.
4. The Question Generator Agent produces tailored interview questions.
5. The Response Evaluator Agent assesses responses and assigns scores.
6. The Response Coaching Agent provides feedback and suggestions.
7. The UI displays questions, evaluation scores, and coaching advice.

See the `docs/` directory for a detailed specification of each agent and acceptance criteria.

## Running the Backend

Ensure a MongoDB instance is accessible. Update `DATABASE_URL` in `.env` or copy
`.env.example` with the provided connection string. Install backend dependencies
using `pip`:

```bash
pip install -r backend/requirements.txt
```

Then run:

```bash
uvicorn backend.app.main:app --reload
```

## Running the Frontend

The frontend lives in the `frontend` directory and uses Vite with React. To
start the development server run:

```bash
cd frontend
npm install
npm run dev
```

For a production build execute:

```bash
npm run build
```
