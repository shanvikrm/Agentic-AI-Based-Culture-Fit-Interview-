import React, { useState, useEffect } from 'react';

/**
 * Simple user control panel for evaluation preferences. For now the
 * preferences are stored in localStorage so they persist between reloads.
 */
export default function Preferences() {
  const [threshold, setThreshold] = useState(0.5);

  useEffect(() => {
    const saved = localStorage.getItem('evaluationThreshold');
    if (saved) setThreshold(parseFloat(saved));
  }, []);

  const handleChange = (e) => {
    const val = parseFloat(e.target.value);
    setThreshold(val);
    localStorage.setItem('evaluationThreshold', val);
  };

  return (
    <section>
      <h2>Evaluation Preferences</h2>
      <label>
        Passing score threshold: {threshold}
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={threshold}
          onChange={handleChange}
        />
      </label>
    </section>
  );
}
