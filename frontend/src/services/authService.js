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

export async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      mot_de_passe: password,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    const message = Array.isArray(error.detail)
      ? error.detail.map(e =>
        e.type === 'value_error'
          ? 'Adresse email invalide'
          : e.msg
      ).join(', ')
      : error.detail
    throw new Error(message || `Erreur HTTP ${response.status}`)
  }

  return response.json()
}

export async function loginAdminUser(email, password) {
  const response = await fetch(`${API_URL}/auth/admin/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      mot_de_passe: password,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    const message = Array.isArray(error.detail)
      ? error.detail.map(e =>
        e.type === 'value_error'
          ? 'Adresse email invalide'
          : e.msg
      ).join(', ')
      : error.detail
    throw new Error(message || `Erreur HTTP ${response.status}`)
  }

  return response.json()
}
