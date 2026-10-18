import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'
import { getUserReservations, cancelReservation, getUserBillets } from '../services/reservationService.js'
import ClientReservation from '../components/groups/ClientReservation.jsx'
import Modal from '../components/sections/Modal.jsx'
import ClientBillet from '../components/groups/ClientBillet.jsx'

export default ClientAccount

function ClientAccount() {
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()
  const [reservations, setReservations] = useState([])
  const [billets, setBillets] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isCancelling, setIsCancelling] = useState(false)
  const [modal, setModal] = useState(null)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/connexion')
      return
    }

    async function loadReservations() {
      try {
        const [userReservations, userBillets] = await Promise.all([
          getUserReservations(token),
          getUserBillets(token),
        ])
        setReservations(userReservations)
        setBillets(userBillets)
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

  function handleCancel(reference) {
    setModal({
      type: 'validation',
      message: 'Voulez-vous vraiment annuler cette réservation ?',
      reference,
    })
  }

  async function confirmCancellation() {
    setIsCancelling(true)
    try {
      await cancelReservation(modal.reference, token)
      setReservations((current) => current.filter(
        (reservation) => reservation.reference !== modal.reference,
      ))
      setModal({ type: 'confirmation', message: 'Votre réservation a été annulée.' })
    } catch (error) {
      setModal({ type: 'error', message: error.message })
    } finally {
      setIsCancelling(false)
    }
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
                <ClientReservation
                  key={reservation.reference}
                  reservation={reservation}
                  onCancel={handleCancel}
                />
              ))}
            </ul>
          ) : (
            <p className="client-reservations__message principal">
              Vous n'avez aucune réservation en cours.{' '}
              <Link to="/films">Découvrir les films</Link>
            </p>
          )}
        </section>

        {!isLoading && !error && (
          <section className="client-billets" aria-labelledby="billets-title">
            <h2 className="titre" id="billets-title">Billets</h2>
            {billets.length ? (
              <ul className="client-reservations__list">
                {billets.map((billet) => (
                  <ClientBillet key={billet.code_billet} billet={billet} />
                ))}
              </ul>
            ) : (
              <p className="client-reservations__message principal">
                Vous n'avez aucun billet.
              </p>
            )}
          </section>
        )}
      </section>
      {modal && (
        <Modal
          {...modal}
          onClose={() => setModal(null)}
          onConfirm={confirmCancellation}
          onCancel={() => setModal(null)}
          isLoading={isCancelling}
        />
      )}
    </main>
  )
}
