import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'
import { getUserReservations } from '../services/reservationService.js'
import ClientReservation from '../components/groups/ClientReservation.jsx'

export default ClientAccount

function ClientAccount() {
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()
  const [reservations, setReservations] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/connexion')
      return
    }

    async function loadReservations() {
      try {
        setReservations(await getUserReservations(token))
      } catch (error) {
        setError(error.message)
      } finally {
        setIsLoading(false)
      }
    }

    loadReservations()
  }, [isAuthenticated, navigate, token])

  if (!isAuthenticated) {
    return null
  }

  return (
    <main className="client-account-page">
      <section className="client-account panel">

        <section className="client-reservations" aria-labelledby="reservations-title">
          <h2 className="titre" id="reservations-title">
            Réservations
          </h2>
          {isLoading ? (
            <p>Chargement des réservations...</p>
          ) : error ? (
            <p className="client-reservations__message principal" role="alert">{error}</p>
          ) : reservations.length ? (
            <ul className="client-reservations__list">
              {reservations.map((reservation) => (
                <ClientReservation key={reservation.reference} reservation={reservation} />
              ))}
            </ul>
          ) : (
            <p className="client-reservations__message principal">
              Vous n'avez aucune réservation en cours.{' '}
              <Link to="/films">Découvrir les films</Link>
            </p>
          )}
        </section>
      </section>
    </main>
  )
}
