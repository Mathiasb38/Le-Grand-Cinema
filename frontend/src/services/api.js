const API_URL = import.meta.env.VITE_API_URL

export async function apiRequest(path, options) {
  const response = await fetch(`${API_URL}${path}`, options)

  if (response.status === 401) {
    localStorage.removeItem('access_token')
    window.location.href = window.location.pathname.startsWith('/admin')
      ? '/admin/connexion'
      : '/connexion'
    throw new Error('Session expirée')
  }

  const data = response.status === 204 ? null : await response.json()

  if (!response.ok) {
    throw new Error(
      Array.isArray(data.detail)
        ? data.detail.map((error) => error.msg).join(', ')
        : data.detail || `Erreur HTTP ${response.status}`,
    )
  }

  return data
}
