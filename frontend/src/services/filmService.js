import { apiRequest } from './api.js'

const API_URL = import.meta.env.VITE_API_URL

export async function getFilms() {
  const response = await fetch(`${API_URL}/films`)

  if (!response.ok) {
    throw new Error(`Erreur HTTP ${response.status}`)
  }

  return response.json()
}

export async function getFilmDetails(idFilm) {
  const response = await fetch(`${API_URL}/films/${idFilm}`)

  if (!response.ok) {
    throw new Error(`Erreur HTTP ${response.status}`)
  }

  return response.json()
}

export async function getFilmSessions(idFilm, date) {
  const response = await fetch(`${API_URL}/films/${idFilm}/seances?date=${date}`)

  if (!response.ok) {
    throw new Error(`Erreur HTTP ${response.status}`)
  }

  return response.json()
}

export async function getSeancePlaces(idSeance, token) {
  return apiRequest(`/seances/${idSeance}/places`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function getAdminFilms(token) {
  return apiRequest('/admin/films', {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function getAdminFilmDetails(idFilm, token) {
  return apiRequest(`/admin/films/${idFilm}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function getAdminSeanceTaux(dateDebut, dateFin, token) {
  const params = new URLSearchParams({ date_debut: dateDebut, date_fin: dateFin })
  return apiRequest(`/admin/remplissage?${params}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function createAdminFilm(film, token) {
  return apiRequest('/admin/films', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(film),
  })
}

export async function updateAdminFilm(idFilm, film, token) {
  return apiRequest(`/admin/films/${idFilm}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(film),
  })
}

export async function getAdminSalles(token) {
  return apiRequest('/admin/salles', {
    headers: { Authorization: `Bearer ${token}` },
  })
}

export async function createAdminSeance(seance, token) {
  return apiRequest('/admin/seances', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(seance),
  })
}

export async function updateAdminSeance(idSeance, seance, token) {
  return apiRequest(`/admin/seances/${idSeance}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(seance),
  })
}

export async function deleteAdminSeance(idSeance, token) {
  return apiRequest(`/admin/seances/${idSeance}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
}
