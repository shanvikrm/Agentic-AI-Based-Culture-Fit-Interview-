import React, { useState } from 'react';
import UploadCompany from './pages/UploadCompany.jsx';
import UploadCandidate from './pages/UploadCandidate.jsx';
import Interview from './pages/Interview.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Preferences from './pages/Preferences.jsx';

/**
 * Simple single page navigation. This avoids the need for
 * react-router which is not included in this minimal setup.
 */

const PAGES = {
  uploadCompany: 'Upload Company',
  uploadCandidate: 'Upload Candidate',
  interview: 'Interview',
  dashboard: 'Dashboard',
  preferences: 'Preferences',
};

export default function App() {
  const [page, setPage] = useState(PAGES.uploadCompany);
  const [interviewResult, setInterviewResult] = useState(null);

  let content = null;
  if (page === PAGES.uploadCompany) content = <UploadCompany />;
  if (page === PAGES.uploadCandidate) content = <UploadCandidate />;
  if (page === PAGES.interview)
    content = (
      <Interview
        onComplete={(data) => {
          setInterviewResult(data);
          setPage(PAGES.dashboard);
        }}
      />
    );
  if (page === PAGES.dashboard)
    content = <Dashboard data={interviewResult} />;
  if (page === PAGES.preferences) content = <Preferences />;

  return (
    <div>
      <h1>Culture Fit Interview</h1>
      <nav>
        {Object.entries(PAGES).map(([key, label]) => (
          <button key={key} onClick={() => setPage(label)} disabled={page === label}>
            {label}
          </button>
        ))}
      </nav>
      <hr />
      {content}
    </div>
  );
}
