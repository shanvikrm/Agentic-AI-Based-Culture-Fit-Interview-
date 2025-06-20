import React from 'react';

export default function Dashboard({ data }) {
  if (!data) return (
    <section>
      <h2>Dashboard</h2>
      <p>No interview run yet.</p>
    </section>
  );

  return (
    <section>
      <h2>Dashboard</h2>
      <div>
        <h3>Questions</h3>
        <ol>
          {data.questions.map((q, i) => (
            <li key={i}>{q}</li>
          ))}
        </ol>
      </div>
      <div>
        <h3>Evaluation</h3>
        <pre>{JSON.stringify(data.evaluation, null, 2)}</pre>
      </div>
      <div>
        <h3>Coaching Feedback</h3>
        <ul>
          {data.coaching.map((c, i) => (
            <li key={i}>{c}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
