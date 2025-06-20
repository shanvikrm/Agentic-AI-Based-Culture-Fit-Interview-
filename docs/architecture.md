# Agentic AI-Based Culture Fit Interview Simulator

This document outlines the architecture and agent responsibilities for the culture fit interview simulator.

## Agents and Responsibilities

### 1. Company Culture Retriever Agent
- **Function**: Extract cultural cues and values from company documents or URLs.
- **Input**: PDF, DOCX, text files, or website URLs.
- **Output**: Structured JSON with labeled cultural elements.
- **Acceptance Criteria**:
  - Extract at least 80% of relevant cultural information.
  - Handle multiple input formats and filter irrelevant content.
  - Process inputs in under one minute.

### 2. Candidate Profile Agent
- **Function**: Build a candidate profile from resume, LinkedIn, and personal statement.
- **Input**: Resume (PDF/DOCX), LinkedIn URL, personal statement text.
- **Output**: Structured JSON with skills, experience, achievements, and values.
- **Acceptance Criteria**:
  - Extract at least 80% of relevant fields.
  - Handle multiple input formats and remove noise.
  - Process five profiles in under two minutes.

### 3. Question Generator Agent
- **Function**: Generate adaptive interview questions aligned with company culture and candidate profile.
- **Input**: Cultural cues JSON and candidate profile JSON.
- **Output**: At least five tailored questions.

### 4. Response Evaluator Agent
- **Function**: Score candidate responses for alignment, sentiment, and relevance.
- **Input**: Candidate responses, cultural cues JSON, and questions.
- **Output**: Evaluation report with a numeric score and specific feedback.

### 5. Response Coaching Agent
- **Function**: Provide real-time suggestions to improve candidate answers.
- **Input**: Candidate responses, evaluation report, and cultural cues JSON.
- **Output**: Actionable coaching feedback.

## Data Storage
All candidate profiles, questions, evaluations, and coaching feedback are stored in MongoDB for transparency and review.

## Testing Considerations
The project includes tests for cultural cue extraction, question relevance, evaluation consistency, and coaching effectiveness. Sample documents and candidate data should be used to validate the system.
