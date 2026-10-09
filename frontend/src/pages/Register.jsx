import { useState } from 'react'

import AuthPanel from '../components/groups/AuthPanel.jsx'
import Modal from '../components/organisms/Modal.jsx'
import { registerUser } from '../services/authService.js'

export default Register

function Register() {
  const [modal, setModal] = useState(null)

  async function handleSubmit({ email, password, clearForm }) {
    setModal(null)

    try {
      await registerUser(email, password)
      clearForm()
      setModal({ type: 'confirmation', message: 'Votre compte a été créé.' })
    } catch (error) {
      setModal({ type: 'error', message: error.message })
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-page__hero hero">
        <h1 className="display-xl">
          CRÉER UN<br />
          COMPTE
        </h1>
      </section>

      <AuthPanel
        ariaLabel="Créer un compte"
        onSubmit={handleSubmit}
        passwordMinLength={12}
        submitLabel="Créer le compte"
      />
      {modal && <Modal {...modal} onClose={() => setModal(null)} />}
    </main>
  )
}
