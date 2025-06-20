import React from 'react';
import UploadCompany from './pages/UploadCompany.jsx';
import UploadCandidate from './pages/UploadCandidate.jsx';
import Interview from './pages/Interview.jsx';

export default function App() {
  return (
    <div>
      <h1>Culture Fit Interview</h1>
      <UploadCompany />
      <UploadCandidate />
      <Interview />
    </div>
  );
}
