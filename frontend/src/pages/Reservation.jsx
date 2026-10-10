import { ArrowRight } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate, useParams } from 'react-router-dom'

import Modal from '../components/sections/Modal.jsx'
import { useAuth } from '../context/AuthContext.jsx'
import { createReservation } from '../services/reservationService.js'

export default Reservation

function Reservation() {
  const { idSeance } = useParams()
  const { state: session } = useLocation()
  const navigate = useNavigate()
  const { isAuthenticated, token } = useAuth()
  const [nombrePlaces, setNombrePlaces] = useState(1)
  const [modal, setModal] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/connexion')
    }
  }, [isAuthenticated, navigate])

  if (!session) {
    return null
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setIsLoading(true)

    try {
      await createReservation(idSeance, nombrePlaces, token)
      setModal({
        type: 'confirmation',
        message: 'Votre réservation a été confirmée.',
      })
    } catch (error) {
      setModal({ type: 'error', message: error.message })
    } finally {
      setIsLoading(false)
    }
  }

  const date = new Date(session.date_heure_debut)

  return (
    <main className="reservation-page">
      <section className="panel reservation-panel" aria-label="Réservation de places">
        <div className="reservation-panel__header">
          <h1 className="display-l">Réserver une séance</h1>
          <p className="principal">
            {date.toLocaleDateString('fr-FR')} à {date.toLocaleTimeString('fr-FR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
          <p className="muted">Salle {session.id_salle}</p>
        </div>

        <form className="reservation-form" onSubmit={handleSubmit}>
          <label className="reservation-form__field petit" htmlFor="nombre-places">
            Nombre de places
            <input className="principal"
              id="nombre-places"
              type="number"
              min="1"
              max={session.places_disponibles}
              value={nombrePlaces}
              onChange={(event) => setNombrePlaces(Number(event.target.value))}
              required
            />
          </label>
          <p className="muted">
            {session.places_disponibles} places disponibles
          </p>
          <button className="button-gold" type="submit" disabled={isLoading}>
            {isLoading ? 'Validation...' : 'Valider la réservation'}
            <ArrowRight aria-hidden="true" />
          </button>
        </form>
      </section>
      {modal && <Modal {...modal} onClose={() => setModal(null)} />}
    </main>
  )
}
