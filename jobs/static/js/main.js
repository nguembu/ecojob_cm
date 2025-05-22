document.addEventListener('DOMContentLoaded', () => {
  // Récupération des éléments du DOM
  const signupForm = document.getElementById('signup-form');
  const loginForm = document.getElementById('login-form');
  const signupTab = document.getElementById('signup-tab');
  const loginTab = document.getElementById('login-tab');
   const logoutBtn = document.getElementById('logout-btn');

  // Fonction pour activer l'onglet Inscription
  function activateSignup() {
    signupTab.classList.add('active');
    loginTab.classList.remove('active');
    signupForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
  }

  // Fonction pour activer l'onglet Connexion
  function activateLogin() {
    loginTab.classList.add('active');
    signupTab.classList.remove('active');
    loginForm.classList.remove('hidden');
    signupForm.classList.add('hidden');
  }

  // Événements clic pour changer d'onglet
  signupTab.addEventListener('click', activateSignup);
  loginTab.addEventListener('click', activateLogin);

  // Par défaut, activer l'onglet connexion (ou inscription selon besoin)
  activateLogin();

  // Gestion de l'inscription
  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = signupForm.querySelector('input[name="name"]').value.trim();
    const email = signupForm.querySelector('input[name="email"]').value.trim();
    const password = signupForm.querySelector('input[name="password"]').value;
    const password2 = signupForm.querySelector('input[name="password2"]').value;

    const roleInput = signupForm.querySelector('input[name="role"]:checked');
    const role = roleInput ? roleInput.value : null;

    if (!role) {
      alert('Veuillez sélectionner un rôle.');
      return;
    }

    if (password !== password2) {
      alert('Les mots de passe ne correspondent pas.');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, password2, role })
      });

      const text = await response.text();

      try {
        const data = JSON.parse(text);
        if (!response.ok) {
          let msg = '';
          if (data.password) msg = data.password;
          else if (data.email) msg = data.email;
          else if (data.detail) msg = data.detail;
          else msg = JSON.stringify(data);
          throw new Error(msg);
        }
        alert("Inscription réussie. Veuillez vous connecter.");
        signupForm.reset();
        activateLogin();
      } catch (e) {
        throw new Error("Réponse non JSON : " + text);
      }
    } catch (err) {
      alert('Erreur lors de l’inscription : ' + err.message);
    }
  });

  // Gestion de la connexion
  document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const res = await fetch('/api/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (data.access) {
        localStorage.setItem('access_token', data.access);

        const profile = await fetch('/api/user/me/', {
            headers: { 'Authorization': 'Bearer ' + data.access }
        });
        const user = await profile.json();

        if (user.role === 'collecteur') {
            window.location.href = '/collecteur/dashboard.html';
        } else if (user.role === 'recruteur') {
            window.location.href = '/recruteur/dashboard.html';
        } else if (user.role === 'acheteur') {
            window.location.href = '/acheteur/dashboard.html';
        }
    } else {
        alert("Identifiants incorrects !");
    }
});


  // Fonction de redirection selon rôle utilisateur
  function redirectToRolePage(role) {
    switch (role.toLowerCase()) {
      case 'collector':
        window.location.href = 'collecteur/dashboard.html';
        break;
      case 'recruiter':
        window.location.href = 'recruteur/dashboard.html';
        break;
      case 'buyer':
        window.location.href = 'acheteur/dashboard.html';
        break;
      default:
        alert('Rôle non reconnu');
    }
  }

  // Gestion de la déconnexion si bouton présent

  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = 'api/login/';
    });
  }
});


document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const role = document.querySelector('input[name="role"]:checked').value;

    const response = await fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, password, role })
    });

    if (response.ok) {
        window.location.href = '/login.html';
    } else {
        alert("Erreur lors de l'inscription");
    }
});


const res = await fetch('/api/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
});
const data = await res.json();

if (data.access) {
    // Stocker le token
    localStorage.setItem('access_token', data.access);
    
    const profile = await fetch('api/user/me/', {
        headers: { 'Authorization': 'Bearer ' + data.access }
    });
    const user = await profile.json();

    // Redirection selon rôle
    if (user.role === 'collector') {
        window.location.href = '/collecteur/dashboard.html';
    } else if (user.role === 'recruiter') {
        window.location.href = '/recruteur/dashboard.html';
    } else if (user.role === 'buyer') {
        window.location.href = '/acheteur/dashboard.html';
    }
}
