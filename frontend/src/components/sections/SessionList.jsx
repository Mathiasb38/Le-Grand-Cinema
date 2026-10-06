import { ArrowRight, CalendarDays, ChevronLeft, ChevronRight } from 'lucide-react'
import { useRef } from 'react'
import { scrollCards } from '../../utils/helpers.js'

export default SessionList

function SessionList({ sessions }) {
  const cardsRef = useRef(null)

  return (
    <div className="sessions">

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
            const time = date.toLocaleTimeString('fr-FR', {
              hour: '2-digit',
              minute: '2-digit',
            })
            const formattedDate = date.toLocaleDateString('fr-FR')

            return (
              <article className="session-card" key={session.id_seance}>
                <span className="principal">
                  {time}
                </span>
                <span className="muted">Salle {session.id_salle}</span>
                <button className="button-gold reserve-button" type="button">
                  <CalendarDays aria-hidden="true" />
                  <span>Réserver</span>
                  <ArrowRight aria-hidden="true" />
                </button>
                <span className="principal session-date">
                  {formattedDate}
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
    </div>
  )
}
