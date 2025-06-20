const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export async function post(path, data) {
  const url = BASE_URL + path;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}
