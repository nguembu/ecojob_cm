// js/register.js
import { register } from './auth.js';

document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = e.target.username.value;
  const email = e.target.email.value;
  const password = e.target.password.value;

  try {
    await register(username, email, password);
    alert('Inscription réussie ! Vous pouvez maintenant vous connecter.');
    window.location.href = 'login.html';
  } catch (e) {
    alert('Erreur lors de l’inscription. Vérifiez les informations.');
  }
});
