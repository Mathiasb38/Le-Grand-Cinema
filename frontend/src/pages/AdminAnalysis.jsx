import { CalendarDays, Clock, Film, MapPin } from 'lucide-react'
import { useState } from 'react'
import Modal from '../components/sections/Modal.jsx'
import { useAuth } from '../context/AuthContext.jsx'
import { getAdminSeanceTaux } from '../services/filmService.js'

export default AdminAnalysis

function AdminAnalysis() {
  const { isAdmin, token } = useAuth()
  const [dateDebut, setDateDebut] = useState('')
  const [dateFin, setDateFin] = useState('')
  const [sessions, setSessions] = useState([])
  const [modal, setModal] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  if (!isAdmin) return null

  async function handleSearch(event) {
    event.preventDefault()
    setModal(null)
    setHasSearched(true)

    if (new Date(dateDebut) > new Date(dateFin)) {
      setSessions([])
      setHasSearched(false)
      setModal({ type: 'error', message: 'La date de début doit précéder la date de fin.' })
      return
    }

    setIsLoading(true)
    try {
      setSessions(await getAdminSeanceTaux(dateDebut, dateFin, token))
    } catch (loadError) {
      setSessions([])
      setHasSearched(false)
      setModal({ type: 'error', message: loadError.message })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="admin-analysis-page">
      <section className="panel admin-analysis" aria-label="Analyse du taux de remplissage">
        <form className="admin-analysis__filters" onSubmit={handleSearch}>
          <label className="admin-analysis__filter">
            <span>Date et heure de début</span>
            <input
              type="datetime-local"
              value={dateDebut}
              onChange={(event) => setDateDebut(event.target.value)}
              required
            />
          </label>
          <label className="admin-analysis__filter">
            <span>Date et heure de fin</span>
            <input
              type="datetime-local"
              value={dateFin}
              onChange={(event) => setDateFin(event.target.value)}
              required
            />
          </label>
          <button className="button-black" type="submit" disabled={isLoading}>
            {isLoading ? 'Recherche...' : 'Rechercher'}
          </button>
        </form>

        <ul className="admin-analysis__results" aria-label="Taux de remplissage des séances" aria-live="polite">
          {sessions.map((session) => {
            const date = new Date(session.date_heure_debut)
            const rate = Math.round(session.taux_remplissage)
            const color = rate >= 80 ? 'var(--color-danger)' : rate >= 50 ? 'var(--color-gold-primary)' : 'var(--color-success)'

            return (
              <li className="admin-analysis__row" key={session.id_seance}>
                <div className="admin-analysis__session">
                  <span className="admin-analysis__film"><Film aria-hidden="true" />{session.titre_film}</span>
                  <span className="admin-analysis__date">
                    <CalendarDays aria-hidden="true" />
                    <time dateTime={session.date_heure_debut}>
                      {date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}
                    </time>
                  </span>
                  <span>
                    <Clock aria-hidden="true" />
                    <time dateTime={session.date_heure_debut}>
                      {date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                    </time>
                  </span>
                  <span><MapPin aria-hidden="true" />Salle {session.numero_salle}</span>
                </div>
                <div className="admin-analysis__occupancy">
                  <div
                    className="admin-analysis__track"
                    role="meter"
                    aria-label={`Taux de remplissage de ${session.titre_film}, salle ${session.numero_salle}`}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-valuenow={rate}
                    aria-valuetext={`${rate} %`}
                  >
                    <span style={{ width: `${rate}%`, background: color }} />
                  </div>
                  <span className="petit">{rate} %</span>
                </div>
              </li>
            )
          })}
        </ul>
        {!isLoading && hasSearched && sessions.length === 0 && (
          <p className="secondaire" role="status">Aucune séance sur cette période.</p>
        )}
        {!hasSearched && <p className="secondaire" role="status">Sélectionnez une période pour consulter les taux de remplissage.</p>}
      </section>
      {modal && <Modal {...modal} onClose={() => setModal(null)} />}
    </main>
  )
}
