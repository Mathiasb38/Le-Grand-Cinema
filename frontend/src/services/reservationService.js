import { apiRequest } from './api.js'

export async function getUserReservations(token) {
  return apiRequest('/reservations', {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function createReservation(idSeance, nombrePlaces, token) {
  return apiRequest('/reservations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      id_seance: Number(idSeance),
      nombre_places: nombrePlaces,
    }),
  })
}

export async function cancelReservation(reference, token) {
  return apiRequest(`/reservations/${reference}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function searchAdminReservations(search, token) {
  return apiRequest(`/admin/recherche?search=${encodeURIComponent(search)}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function validateAdminPayment(reference, token) {
  return apiRequest(`/admin/reservations/${encodeURIComponent(reference)}/paiement`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}` },
  })
}
