import { ArrowRight, CalendarDays, ChevronLeft, ChevronRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useRef, useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'
import { getFilmSessions } from '../../services/filmService.js'
import { scrollCards } from '../../utils/helpers.js'

export default SessionList

function SessionList({ idFilm, sessions }) {
  const cardsRef = useRef(null)
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const today = getDateKey(new Date())
  const [selectedDate, setSelectedDate] = useState(today)
  const [selectedSessions, setSelectedSessions] = useState(sessions)
  const [isLoading, setIsLoading] = useState(false)
  const dates = getNextDates()

  function handleDateChange(date) {
    setSelectedDate(date)
    setSelectedSessions([])
    setIsLoading(true)
    getFilmSessions(idFilm, date)
      .then(setSelectedSessions)
      .catch(() => setSelectedSessions([]))
      .finally(() => setIsLoading(false))
  }

  function handleReservation(session) {
    if (!isAuthenticated) {
      navigate('/connexion')
      return
    }

    navigate(`/reservation/${session.id_seance}`, { state: session })
  }

  return (
    <div className="sessions">
      <div className="sessions__dates" aria-label="Filtrer les séances par date">
        {dates.map((date) => (
          <button
            className={selectedDate === date ? 'button-gold' : 'button-black'}
            type="button"
            aria-pressed={selectedDate === date}
            key={date}
            onClick={() => handleDateChange(date)}
          >
            {formatDate(date)}
          </button>
        ))}
      </div>

      {isLoading ? (
        <p className="sessions__empty muted">
          Chargement des séances...
        </p>
      ) : selectedSessions.length === 0 ? (
        <p className="sessions__empty muted">
          Aucune séance n'est programmée pour cette date.
        </p>
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
          {selectedSessions.map((session) => {
            const date = new Date(session.date_heure_debut)
            const time = date.toLocaleTimeString('fr-FR', {
              hour: '2-digit',
              minute: '2-digit',
            })
            const isAvailable = session.places_disponibles > 0

            return (
              <article className="session-card" key={session.id_seance}>
                <span className="principal">
                  {time}
                </span>
                <span className="muted">Salle {session.id_salle}</span>
                <button
                  className="button-gold reserve-button"
                  type="button"
                  disabled={!isAvailable}
                  onClick={() => handleReservation(session)}
                >
                  <CalendarDays aria-hidden="true" />
                  <span>{isAvailable ? 'Réserver' : 'Complet'}</span>
                  <ArrowRight aria-hidden="true" />
                </button>
                <span className="petit session-places">
                  {session.places_disponibles} places disponibles
                </span>
              </article>
            )
          })}
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
    </div>
  )
}

function getDateKey(date) {
  return date.toLocaleDateString('sv-SE')
}

function getNextDates() {
  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date()
    date.setDate(date.getDate() + index)
    return getDateKey(date)
  })
}

function formatDate(date) {
  return new Date(`${date}T12:00:00`).toLocaleDateString('fr-FR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  })
}
