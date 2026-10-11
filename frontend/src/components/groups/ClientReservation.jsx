import { CalendarDays } from 'lucide-react'

export default ClientReservation

function ClientReservation({ reservation, onCancel }) {
  const date = new Date(reservation.date_heure_debut)

  return (
    <li className="client-reservation">
      <div className="client-reservation__film principal">
        <span>{reservation.titre_film}</span>
      </div>

      <span className="client-reservation__reference secondaire">
        {reservation.reference}
      </span>

      <div className="client-reservation__details petit">
        <CalendarDays aria-hidden="true" />
        <time dateTime={reservation.date_heure_debut}>
          {date.toLocaleDateString('fr-FR', {
            day: '2-digit',
            month: 'long',
            year: 'numeric',
          })}
          {' · '}
          {date.toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </time>
        <span className="client-reservation__room secondaire">
          {reservation.nom_salle} - Salle {reservation.numero_salle}
        </span>
      </div>
      {onCancel && (
        <button
          className="button-danger client-reservation__cancel"
          type="button"
          onClick={() => onCancel(reservation.reference)}
        >
          Annuler
        </button>
      )}
    </li>
  )
}
