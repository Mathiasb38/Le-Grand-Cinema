import { useState } from 'react'

import AuthPanel from '../components/groups/AuthPanel.jsx'
import Modal from '../components/sections/Modal.jsx'
import { loginUser } from '../services/authService.js'

export default Login

function Login() {
  const [modal, setModal] = useState(null)

  async function handleSubmit({ email, password, clearForm }) {
    setModal(null)

    try {
      const { access_token: accessToken } = await loginUser(email, password)
      localStorage.setItem('access_token', accessToken)
      clearForm()
      setModal({ type: 'confirmation', message: 'Connexion réussie.' })
    } catch (error) {
      setModal({ type: 'error', message: error.message })
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-page__hero hero">
        <h1 className="display-xl">CONNEXION</h1>
      </section>

      <AuthPanel
        ariaLabel="Connexion"
        linkLabel="Créer un compte"
        linkTo="/inscription"
        onSubmit={handleSubmit}
        submitLabel="Connexion"
      />
      {modal && <Modal {...modal} onClose={() => setModal(null)} />}
    </main>
  )
}
