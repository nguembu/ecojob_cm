// js/auth.js
import { fetchAPI } from './api.js';

export async function login(username, password) {
  const data = await fetchAPI('/auth/login/', 'POST', { username, password });
  localStorage.setItem('token', data.token);
  return data;
}

export async function register(username, email, password) {
  return await fetchAPI('/auth/register/', 'POST', { username, email, password });
}

export function logout() {
  localStorage.removeItem('token');
}

export function isAuthenticated() {
  return !!localStorage.getItem('token');
}
