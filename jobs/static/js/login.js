// js/login.js
import { login } from './auth.js';

document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = e.target.username.value;
  const password = e.target.password.value;

  try {
    await login(username, password);
    alert('Connexion réussie !');
    window.location.href = 'offers.html';
  } catch (e) {
    alert('Échec de la connexion. Vérifie tes identifiants.');
  }
});
