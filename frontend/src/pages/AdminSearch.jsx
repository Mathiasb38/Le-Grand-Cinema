import { Search, Check } from 'lucide-react'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext.jsx'
import { searchAdminReservations, validateAdminPayment } from '../services/reservationService.js'
import Modal from '../components/sections/Modal.jsx'

export default AdminSearch

function AdminSearch() {
  const { isAdmin, token } = useAuth()
  const [reservations, setReservations] = useState([])
  const [query, setQuery] = useState('')
  const [search, setSearch] = useState('')
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [confirmation, setConfirmation] = useState(null)
  const [isPaymentLoading, setIsPaymentLoading] = useState(false)

  async function handleSearch(event) {
    event.preventDefault()
    const value = query.trim()
    setSearch(value)
    setError(null)

    if (!value) {
      setReservations([])
      return
    }

    setIsLoading(true)
    try {
      setReservations(await searchAdminReservations(value, token))
    } catch (error) {
      setError(error.message)
      setReservations([])
    } finally {
      setIsLoading(false)
    }
  }

  async function handlePayment() {
    setIsPaymentLoading(true)
    setError(null)

    try {
      await validateAdminPayment(confirmation, token)
      setReservations((items) => items.map((item) => (
        item.reference === confirmation ? { ...item, is_paid: true } : item
      )))
      setConfirmation(null)
    } catch (error) {
      setError(error.message)
    } finally {
      setIsPaymentLoading(false)
    }
  }

  if (!isAdmin) {
    return null
  }

  return (
    <main className="admin-search-page">
      <section className="panel admin-search" aria-label="Recherche de réservation ou de billet">
        <form className="admin-search__form" role="search" onSubmit={handleSearch}>
          <label className="auth-field__control admin-search__field">
            <Search aria-hidden="true" />
            <input
              type="search"
              aria-label="Référence ou e-mail"
              placeholder="Référence ou e-mail"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </label>
          <button className="button-black" type="submit">Rechercher</button>
        </form>

        <div className="admin-search__results" aria-live="polite">
          {error && <p className="secondaire" role="alert">{error}</p>}
          {!search && !error && (
            <p className="secondaire">Saisissez une référence ou un e-mail.</p>
          )}
          {isLoading && <p className="secondaire">Recherche en cours...</p>}
          {search && !isLoading && !error && reservations.length === 0 && (
            <p className="secondaire">Aucun résultat trouvé.</p>
          )}
          {reservations.map((reservation) => {
            const date = new Date(reservation.date_heure_debut)
            const status = reservation.is_cancelled
              ? 'Annulée'
              : reservation.is_paid
                ? 'Payée'
                : 'Réservée'

            return (
              <article
                className="admin-search__result"
                key={reservation.reference}
                aria-label={`Réservation ${reservation.reference}`}
              >
                <div className="admin-search__details">
                  <p className="titre">{reservation.titre_film}</p>
                  <p className="principal">Référence : {reservation.reference}</p>
                  <p className="petit">Client : {reservation.email}</p>
                  <p className="secondaire">
                    Séance : <time dateTime={reservation.date_heure_debut}>
                      {date.toLocaleDateString('fr-FR')} à {date.toLocaleTimeString('fr-FR', {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </time>
                  </p>
                  <p className="secondaire">
                    Salle : {reservation.nom_salle} - Salle {reservation.numero_salle}
                  </p>
                </div>
                <div className="admin-search__actions">
                  <span className={`admin-search__status button-black${reservation.is_cancelled ? ' admin-search__status--cancelled' : ''}`}>
                    {status}
                  </span>
                  {!reservation.is_paid && !reservation.is_cancelled && (
                    <button
                      className="button-gold admin-search__payment"
                      type="button"
                      onClick={() => setConfirmation(reservation.reference)}
                      disabled={date <= new Date()}
                    >
                      Valider le paiement
                      <Check aria-hidden="true" />
                    </button>
                  )}
                </div>
              </article>
            )
          })}
        </div>
      </section>
      {confirmation && (
        <Modal
          type="validation"
          message={`Valider le paiement de ${confirmation} ?`}
          onConfirm={handlePayment}
          onCancel={() => setConfirmation(null)}
          onClose={() => setConfirmation(null)}
          isLoading={isPaymentLoading}
        />
      )}
    </main>
  )
}
