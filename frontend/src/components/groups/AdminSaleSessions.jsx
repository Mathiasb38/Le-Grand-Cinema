import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useRef } from 'react'
import { scrollCards } from '../../utils/helpers.js'

export default AdminSaleSessions

function AdminSaleSessions({ sessions, selectedSessionId, onSelectSession }) {
  const cardsRef = useRef(null)

  return (
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
        {sessions.map((session) => {
          const date = new Date(session.date_heure_debut)
          const isAvailable = session.places_disponibles > 0
          const isSelected = selectedSessionId === session.id_seance

          return (
            <button
              className={`session-card admin-sale__session-card${isSelected ? ' admin-sale__session-card--selected' : ''}`}
              key={session.id_seance}
              type="button"
              disabled={!isAvailable}
              aria-pressed={isSelected}
              onClick={() => onSelectSession(session)}
            >
              <span className="principal">
                {date.toLocaleString('fr-FR', {
                  weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit',
                })}
              </span>
              <span className="muted">{session.nom_salle} - Salle {session.numero_salle}</span>
              <span className="petit session-places">
                {isAvailable ? `${session.places_disponibles} places disponibles` : 'Complet'}
              </span>
            </button>
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
  )
}
