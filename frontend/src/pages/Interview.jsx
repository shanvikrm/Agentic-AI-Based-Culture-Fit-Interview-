import React, { useState } from 'react';
import { post } from '../api.js';

export default function Interview({ onComplete }) {
  const [form, setForm] = useState({
    candidate_id: '',
    company_id: '',
    responses: '',
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      candidate_id: form.candidate_id,
      company_id: form.company_id,
      responses: form.responses
        .split('\n')
        .map((s) => s.trim())
        .filter(Boolean),
    };
    const data = await post('/interview', payload);
    setResult(data);
    if (onComplete) onComplete(data);
  };

  return (
    <section>
      <h2>Interview</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            name="candidate_id"
            placeholder="Candidate ID"
            value={form.candidate_id}
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            name="company_id"
            placeholder="Company ID"
            value={form.company_id}
            onChange={handleChange}
          />
        </div>
        <div>
          <textarea
            name="responses"
            placeholder="Candidate responses, one per line"
            value={form.responses}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Run Interview</button>
      </form>
      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </section>
  );
}
