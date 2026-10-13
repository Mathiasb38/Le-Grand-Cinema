import { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { loginAdminUser, loginUser } from '../services/authService.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(getStoredToken)
  const isAdmin = getTokenPayload(token)?.role === 'admin'

  async function saveToken(loginRequest) {
    const { access_token: accessToken } = await loginRequest
    localStorage.setItem('access_token', accessToken)
    setToken(accessToken)
  }

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    setToken(null)
  }, [])

  useEffect(() => {
    const { exp } = getTokenPayload(token) || {}
    if (!token) return
    if (!Number.isFinite(exp)) {
      logout()
      return
    }

    const delay = exp * 1000 - Date.now()
    if (delay <= 0) {
      logout()
      return
    }

    const timeout = setTimeout(logout, delay)
    return () => clearTimeout(timeout)
  }, [token, logout])

  return (
    <AuthContext.Provider value={{
      token,
      isAuthenticated: Boolean(token),
      isAdmin,
      login: (email, password) => saveToken(loginUser(email, password)),
      adminLogin: (email, password) => saveToken(loginAdminUser(email, password)),
      logout,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth doit être utilisé dans AuthProvider')
  }

  return context
}

function getTokenPayload(token) {
  if (!token) return null

  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    return JSON.parse(atob(payload))
  } catch {
    return null
  }
}

function getStoredToken() {
  const token = localStorage.getItem('access_token')
  const { exp } = getTokenPayload(token) || {}

  if (token && (!Number.isFinite(exp) || exp * 1000 <= Date.now())) {
    localStorage.removeItem('access_token')
    return null
  }

  return token
}
