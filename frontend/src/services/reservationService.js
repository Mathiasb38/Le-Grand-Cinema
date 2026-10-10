const API_URL = import.meta.env.VITE_API_URL

export async function createReservation(idSeance, nombrePlaces, token) {
  const response = await fetch(`${API_URL}/reservations`, {
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

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      Array.isArray(data.detail)
        ? data.detail.map((error) => error.msg).join(', ')
        : data.detail || `Erreur HTTP ${response.status}`,
    )
  }

  return data
}
