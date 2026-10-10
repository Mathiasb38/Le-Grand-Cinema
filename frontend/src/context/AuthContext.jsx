import { createContext, useContext, useState } from 'react'
import { loginUser } from '../services/authService.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('access_token'))

  async function login(email, password) {
    const { access_token: accessToken } = await loginUser(email, password)
    localStorage.setItem('access_token', accessToken)
    setToken(accessToken)
  }

  function logout() {
    localStorage.removeItem('access_token')
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{
      token,
      isAuthenticated: Boolean(token),
      login,
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
