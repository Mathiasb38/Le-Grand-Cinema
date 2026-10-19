import { ArrowRight, ArrowLeft } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate, useParams,Link } from 'react-router-dom'

import SeatReservation from '../components/groups/SeatReservation.jsx'
import Modal from '../components/sections/Modal.jsx'
import { useAuth } from '../context/AuthContext.jsx'
import { createReservation } from '../services/reservationService.js'
import { getSeancePlaces } from '../services/filmService.js'

export default Reservation

function Reservation() {
  const { idSeance } = useParams()
  const { state: session } = useLocation()
  const navigate = useNavigate()
  const { isAuthenticated, token } = useAuth()
  const [selectedPlaceIds, setSelectedPlaceIds] = useState([])
  const [modal, setModal] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [places, setPlaces] = useState([])
  const [placesError, setPlacesError] = useState(null)
  const [isLoadingPlaces, setIsLoadingPlaces] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/connexion')
    }
  }, [isAuthenticated, navigate])

  useEffect(() => {
    if (!isAuthenticated || !session) return

    getSeancePlaces(idSeance, token)
      .then(setPlaces)
      .catch((error) => setPlacesError(error.message))
      .finally(() => setIsLoadingPlaces(false))
  }, [idSeance, isAuthenticated, session, token])

  if (!session) {
    return null
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setIsLoading(true)

    try {
      await createReservation(idSeance, selectedPlaceIds, token)
      setSelectedPlaceIds([])
      try {
        setPlaces(await getSeancePlaces(idSeance, token))
      } catch {
        setModal({
          type: 'confirmation',
          message: 'Réservation confirmée, mais le plan n’a pas pu être actualisé. Rechargez la page.',
        })
        return
      }
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

  return (
    <main className="reservation-page">
      <section className="panel reservation-panel" aria-label="Réservation de places">
        {isLoadingPlaces ? (
          <p className="muted">Chargement des places...</p>
        ) : placesError ? (
          <p className="secondaire" role="alert">{placesError}</p>
        ) : (
          <SeatReservation
            film={{ titre: session.titreFilm }}
            session={session}
            places={places}
            selectedIds={selectedPlaceIds}
            onSelectionChange={setSelectedPlaceIds}
            isLoading={isLoading}
          >
            <form className="reservation-form" onSubmit={handleSubmit}>
              <button className="button-gold" type="submit" disabled={isLoading || selectedPlaceIds.length === 0}>
                {isLoading ? 'Validation...' : 'Valider la réservation'}
                <ArrowRight aria-hidden="true" />
              </button>
              <Link className="button-black" to={`/films/${session.idFilm}`}>
                <ArrowLeft aria-hidden="true" />
                Retour
              </Link>
            </form>
          </SeatReservation>
        )}
      </section>
      {modal && <Modal {...modal} onClose={() => setModal(null)} />}
    </main>
  )
}
