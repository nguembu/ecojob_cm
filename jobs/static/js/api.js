// js/api.js
const API_BASE = 'http://localhost:8000/api';

export async function fetchAPI(endpoint, method = 'GET', data = null, auth = false) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (auth) {
    const token = localStorage.getItem('token');
    if (token) {
      options.headers['Authorization'] = `Token ${token}`;
    }
  }

  if (data) {
    options.body = JSON.stringify(data);
  }

  const res = await fetch(`${API_BASE}${endpoint}`, options);
  if (!res.ok) {
    throw new Error(`Erreur API: ${res.status}`);
  }

  return await res.json();
}
