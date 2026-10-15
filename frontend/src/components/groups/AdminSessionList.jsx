import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'
import { createAdminSeance, getAdminSalles } from '../../services/filmService.js'
import { scrollCards, getCurrentDateTime } from '../../utils/helpers.js'

export default AdminSessionList

function AdminSessionList({ idFilm, sessions }) {
  const { token } = useAuth()
  const cardsRef = useRef(null)
  const [selectedSessions, setSelectedSessions] = useState(sessions)
  const [salles, setSalles] = useState([])
  const [isSavingSession, setIsSavingSession] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    getAdminSalles(token)
      .then(setSalles)
      .catch((error) => setError(error.message))
  }, [token])

  useEffect(() => {
    setSelectedSessions(sessions)
  }, [sessions])

  async function handleSessionSubmit(event) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    setError(null)
    setIsSavingSession(true)

    try {
      const session = await createAdminSeance({
        id_film: idFilm,
        id_salle: Number(formData.get('id_salle')),
        date_heure_debut: formData.get('date_heure_debut'),
      }, token)
      setSelectedSessions((currentSessions) => [...currentSessions, session])
      form.reset()
    } catch (error) {
      setError(error.message)
    } finally {
      setIsSavingSession(false)
    }
  }

  return (
    <>
      <form className="admin-seance-form" onSubmit={handleSessionSubmit}>
        <label>
          Date et heure
          <input
            name="date_heure_debut"
            type="datetime-local"
            min={getCurrentDateTime()}
            required
          />
        </label>
        <label>
          Salle
          <select name="id_salle" required defaultValue="">
            <option value="" disabled>Choisir une salle</option>
            {salles.map((salle) => (
              <option key={salle.id_salle} value={salle.id_salle}>
                {salle.nom} - Salle {salle.numero}
              </option>
            ))}
          </select>
        </label>
        <button className="button-gold" type="submit" disabled={isSavingSession || !salles.length}>
          {isSavingSession ? 'Programmation...' : 'Valider'}
        </button>
      </form>

      {error && <p role="alert">{error}</p>}

      {selectedSessions.length === 0 ? (
        <p className="sessions__empty muted">Aucune séance programmée.</p>
      ) : (
        <div className="panel__list">
          <button
            className="panel__arrow panel__arrow--left"
            type="button"
            aria-label="Séances précédentes"
            onClick={() => scrollCards(cardsRef, -1, 332)}
          >
            <ChevronLeft aria-hidden="true" />
          </button>
          <div className="panel__cards" ref={cardsRef}>
            {selectedSessions.map((session) => (
              <article className="session-card" key={session.id_seance}>
                <span className="principal">
                  {new Date(session.date_heure_debut).toLocaleString('fr-FR', {
                    weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit',
                  })}
                </span>
                <span className="muted">
                  {session.nom_salle} - Salle {session.numero_salle}
                </span>
                <span className="petit session-places">
                  {session.places_disponibles} places disponibles
                </span>
              </article>
            ))}
          </div>
          <button
            className="panel__arrow panel__arrow--right"
            type="button"
            aria-label="Séances suivantes"
            onClick={() => scrollCards(cardsRef, 1, 332)}
          >
            <ChevronRight aria-hidden="true" />
          </button>
        </div>
      )}
    </>
  )
}

