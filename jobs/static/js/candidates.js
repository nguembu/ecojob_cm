// js/candidates.js
import { fetchAPI } from './api.js';

export async function loadCandidates(containerId) {
  const container = document.getElementById(containerId);

  try {
    const candidates = await fetchAPI('/candidates/', 'GET', null, true);
    if (candidates.length === 0) {
      container.innerHTML = "<p>Aucun candidat trouvé.</p>";
    }

    candidates.forEach(candidate => {
      const div = document.createElement('div');
      div.className = 'candidate-card';
      div.innerHTML = `
        <h4>${candidate.name}</h4>
        <p>Email : ${candidate.email}</p>
        <p>Compétences : ${candidate.skills}</p>
      `;
      container.appendChild(div);
    });
  } catch (e) {
    container.innerHTML = '<p>Erreur lors du chargement des candidats.</p>';
  }
}
