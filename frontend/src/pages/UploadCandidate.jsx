import React, { useState } from 'react';
import { post } from '../api.js';

export default function UploadCandidate() {
  const [form, setForm] = useState({
    resume_path: '',
    linkedin_url: '',
    personal_statement: '',
  });
  const [candidateId, setCandidateId] = useState(null);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await post('/candidate', form);
    setCandidateId(data.id);
  };

  return (
    <section>
      <h2>Upload Candidate Data</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            name="resume_path"
            placeholder="Resume file path"
            value={form.resume_path}
            onChange={handleChange}
          />
        </div>
        <div>
          <input
            name="linkedin_url"
            placeholder="LinkedIn URL"
            value={form.linkedin_url}
            onChange={handleChange}
          />
        </div>
        <div>
          <textarea
            name="personal_statement"
            placeholder="Personal statement"
            value={form.personal_statement}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {candidateId && <p>Candidate saved with id: {candidateId}</p>}
    </section>
  );
}
