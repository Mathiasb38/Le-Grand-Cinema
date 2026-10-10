import { useState } from 'react'

import AuthPanel from '../components/groups/AuthPanel.jsx'
import Modal from '../components/sections/Modal.jsx'
import { useAuth } from '../context/AuthContext.jsx'

export default AdminLogin

function AdminLogin() {
  const [modal, setModal] = useState(null)
  const { adminLogin } = useAuth()

  async function handleSubmit({ email, password, clearForm }) {
    setModal(null)

    try {
      await adminLogin(email, password)
      clearForm()
    } catch (error) {
      setModal({ type: 'error', message: error.message })
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-page__hero hero">
        <h1 className="display-xl">BACK-OFFICE</h1>
      </section>

      <AuthPanel
        ariaLabel="Connexion back-office"
        onSubmit={handleSubmit}
        submitLabel="Connexion"
      />
      {modal && <Modal {...modal} onClose={() => setModal(null)} />}
    </main>
  )
}
