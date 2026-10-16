import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'
import { createAdminSeance, getAdminSalles, updateAdminSeance, deleteAdminSeance } from '../../services/filmService.js'
import { scrollCards, getCurrentDateTime, getDateTimeInputValue } from '../../utils/helpers.js'
import Modal from '../sections/Modal.jsx'

export default AdminSessionList

function AdminSessionList({ idFilm, sessions }) {
  const { token } = useAuth()
  const cardsRef = useRef(null)
  const [selectedSessions, setSelectedSessions] = useState(sessions)
  const [salles, setSalles] = useState([])
  const [isSavingSession, setIsSavingSession] = useState(false)
  const [editingSessionId, setEditingSessionId] = useState(null)
  const [modal, setModal] = useState(null)

  useEffect(() => {
    getAdminSalles(token)
      .then(setSalles)
      .catch((error) => setModal({ type: 'error', message: error.message }))
  }, [token])

  useEffect(() => {
    setSelectedSessions(sessions)
  }, [sessions])

  async function handleSessionSubmit(event) {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
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
      setModal({ type: 'error', message: error.message })
    } finally {
      setIsSavingSession(false)
    }
  }

  async function handleSessionUpdate(event, idSeance) {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    setIsSavingSession(true)

    try {
      const session = await updateAdminSeance(idSeance, {
        id_salle: Number(formData.get('id_salle')),
        date_heure_debut: formData.get('date_heure_debut'),
      }, token)
      setSelectedSessions((currentSessions) => currentSessions.map((currentSession) => (
        currentSession.id_seance === idSeance ? session : currentSession
      )))
      setEditingSessionId(null)
    } catch (error) {
      setModal({ type: 'error', message: error.message })
    } finally {
      setIsSavingSession(false)
    }
  }

  function handleDeleteSession(idSeance) {
    setModal({
      type: 'validation',
      message: 'Voulez-vous vraiment supprimer cette séance ?',
      idSeance,
    })
  }

  async function confirmDeleteSession() {
    setIsSavingSession(true)

    try {
      await deleteAdminSeance(modal.idSeance, token)
      setSelectedSessions((currentSessions) => currentSessions.filter(
        (session) => session.id_seance !== modal.idSeance,
      ))
      setModal({ type: 'confirmation', message: 'La séance a été supprimée.' })
    } catch (error) {
      setModal({ type: 'error', message: error.message })
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
              editingSessionId === session.id_seance ? (
                <form
                  className="session-card session-card--admin session-card--editing"
                  key={session.id_seance}
                  onSubmit={(event) => handleSessionUpdate(event, session.id_seance)}
                >
                  <label>
                    Date et heure
                    <input
                      name="date_heure_debut"
                      type="datetime-local"
                      min={getCurrentDateTime()}
                      defaultValue={getDateTimeInputValue(session.date_heure_debut)}
                      required
                    />
                  </label>
                  <label>
                    Salle
                    <select name="id_salle" defaultValue={session.id_salle} required>
                      {salles.map((salle) => (
                        <option key={salle.id_salle} value={salle.id_salle}>
                          {salle.nom} - Salle {salle.numero}
                        </option>
                      ))}
                    </select>
                  </label>
                  <div className="session-card__actions">
                    <button className="button-gold" type="submit" disabled={isSavingSession}>
                      Valider
                    </button>
                    <button
                      className="button-black"
                      type="button"
                      onClick={() => setEditingSessionId(null)}
                    >
                      Annuler
                    </button>
                  </div>
                </form>
              ) : (
                <article className="session-card session-card--admin" key={session.id_seance}>
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
                  <div className="session-card__actions">
                    <button
                      className="button-black"
                      type="button"
                      onClick={() => setEditingSessionId(session.id_seance)}
                    >
                      Modifier
                    </button>
                    <button
                      className="button-danger"
                      type="button"
                      onClick={() => handleDeleteSession(session.id_seance)}
                    >
                      Supprimer
                    </button>
                  </div>
                </article>
              )
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
      {modal && (
        <Modal
          {...modal}
          onClose={() => setModal(null)}
          onConfirm={confirmDeleteSession}
          onCancel={() => setModal(null)}
          isLoading={isSavingSession}
        />
      )}
    </>
  )
}

