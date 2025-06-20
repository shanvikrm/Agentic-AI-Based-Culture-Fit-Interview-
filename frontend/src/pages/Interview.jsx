import React, { useState } from 'react';
import { post } from '../api.js';

export default function Interview({ onComplete }) {
  // Step 1: IDs to fetch questions
  const [ids, setIds] = useState({ candidate_id: '', company_id: '' });
  const [interviewId, setInterviewId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState('');
  const [result, setResult] = useState(null);

  const handleIdsChange = (e) =>
    setIds({ ...ids, [e.target.name]: e.target.value });

  const handleGetQuestions = async (e) => {
    e.preventDefault();
    const data = await post('/interview/questions', ids);
    setInterviewId(data.id);
    setQuestions(data.questions);
  };

  const handleSubmitAnswers = async (e) => {
    e.preventDefault();
    const payload = {
      id: interviewId,
      responses: responses
        .split('\n')
        .map((s) => s.trim())
        .filter(Boolean),
    };
    const data = await post('/interview/answers', payload);
    setResult(data);
    if (onComplete) onComplete(data);
  };

  return (
    <section>
      <h2>Interview</h2>

      {!questions.length && !result && (
        <form onSubmit={handleGetQuestions}>
          <div>
            <input
              name="candidate_id"
              placeholder="Candidate ID"
              value={ids.candidate_id}
              onChange={handleIdsChange}
            />
          </div>
          <div>
            <input
              name="company_id"
              placeholder="Company ID"
              value={ids.company_id}
              onChange={handleIdsChange}
            />
          </div>
          <button type="submit">Get Questions</button>
        </form>
      )}

      {questions.length > 0 && !result && (
        <form onSubmit={handleSubmitAnswers}>
          <ol>
            {questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
          <textarea
            name="responses"
            placeholder="Responses, one per line"
            value={responses}
            onChange={(e) => setResponses(e.target.value)}
          />
          <button type="submit">Submit Answers</button>
        </form>
      )}

      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </section>
  );
}
