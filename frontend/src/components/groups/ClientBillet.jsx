import { CalendarDays } from 'lucide-react'

export default ClientBillet

function ClientBillet({ billet }) {
  const date = new Date(billet.date_heure_debut)

  return (
    <li className="client-reservation client-billet">
      <div className="client-reservation__film principal">
        <span>{billet.titre_film}</span>
      </div>

      <span className="client-reservation__reference secondaire">
        {billet.code_billet}
      </span>

      <div className="client-reservation__details petit">
        <CalendarDays aria-hidden="true" />
        <time dateTime={billet.date_heure_debut}>
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
          {billet.nom_salle} - Salle {billet.numero_salle}
        </span>
      </div>

      <span className="status-badge button-black">Payée</span>
    </li>
  )
}
