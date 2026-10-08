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
