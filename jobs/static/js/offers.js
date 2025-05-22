// js/offers.js
import { fetchAPI } from './api.js';

export async function loadOffers(containerId) {
  const container = document.getElementById(containerId);
  try {
    const offers = await fetchAPI('/joboffers/');
    if (offers.length === 0) {
      container.innerHTML = '<p>Aucune offre disponible.</p>';
    }

    offers.forEach(offer => {
      const div = document.createElement('div');
      div.className = 'offer-card';
      div.innerHTML = `
        <h3>${offer.title}</h3>
        <p>${offer.description.slice(0, 100)}...</p>
        <a href="offer_detail.html?id=${offer.id}" class="cta">Voir l’offre</a>
      `;
      container.appendChild(div);
    });
  } catch (e) {
    container.innerHTML = '<p>Erreur lors du chargement des offres.</p>';
  }
}
