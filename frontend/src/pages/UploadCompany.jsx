import React, { useState } from 'react';
import { post } from '../api.js';

export default function UploadCompany() {
  const [sources, setSources] = useState('');
  const [companyId, setCompanyId] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const list = sources
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean);
    const data = await post('/company', { sources: list });
    setCompanyId(data.id);
  };

  return (
    <section>
      <h2>Upload Company Data</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={sources}
          onChange={(e) => setSources(e.target.value)}
          placeholder="Enter document paths or URLs, one per line"
        />
        <button type="submit">Submit</button>
      </form>
      {companyId && <p>Company saved with id: {companyId}</p>}
    </section>
  );
}
