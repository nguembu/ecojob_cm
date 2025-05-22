// js/offer_detail.js
import { fetchAPI } from './api.js';

export async function loadOfferDetail(containerId) {
  const container = document.getElementById(containerId);
  const urlParams = new URLSearchParams(window.location.search);
  const offerId = urlParams.get('id');

  if (!offerId) {
    container.innerHTML = "<p>Offre non spécifiée.</p>";
    return;
  }

  try {
    const offer = await fetchAPI(`/joboffers/${offerId}/`);
    container.innerHTML = `
      <h2>${offer.title}</h2>
      <p><strong>Description:</strong> ${offer.description}</p>
      <p><strong>Compétences:</strong> ${offer.skills}</p>
      <p><strong>Lieu:</strong> ${offer.location}</p>
      <p><strong>Salaire:</strong> ${offer.salary} FCFA</p>
      <p><strong>Entreprise:</strong> ${offer.company.name}</p>
    `;
  } catch (e) {
    container.innerHTML = '<p>Erreur lors du chargement de l’offre.</p>';
  }
}
