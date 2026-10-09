const API_URL = import.meta.env.VITE_API_URL

export async function registerUser(email, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      mot_de_passe: password,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `Erreur HTTP ${response.status}`)
  }

  return response.json()
}
