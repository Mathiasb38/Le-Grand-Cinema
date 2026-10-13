import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'
import { updateAdminFilm } from '../../services/filmService.js'

export default AdminFilmInfo

function AdminFilmInfo({ film }) {
  const { token } = useAuth()
  const [filmData, setFilmData] = useState(film)
  const [error, setError] = useState(null)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    setFilmData(film)
  }, [film])

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)
    setIsSaving(true)

    try {
      const updatedFilm = await updateAdminFilm(film.id_film, {
        titre: filmData.titre,
        duree_minutes: filmData.duree_minutes,
        affiche_url: filmData.affiche_url,
        description: filmData.description,
      }, token)
      setFilmData(updatedFilm)
    } catch (error) {
      setError(error.message)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <section className="panel" aria-label={`Détails du film ${film.titre}`}>
      <div className="film-info__summary">
        <div className="film-poster">
          <img src={filmData.affiche_url} alt={`Affiche du film ${filmData.titre}`} />
        </div>

        <form className="film-info__info" onSubmit={handleSubmit}>

          <div className="admin-film-info__form">
            <input className='admin-film-info__affiche petit'
              type="url"
              placeholder="URL de l’affiche"
              required
              value={filmData.affiche_url}
              onChange={(event) => setFilmData({ ...filmData, affiche_url: event.target.value })}
            />
            <input className="admin-film-info__titre display-l"
              maxLength="50"
              placeholder="Titre du film"
              required
              value={filmData.titre}
              onChange={(event) => setFilmData({ ...filmData, titre: event.target.value })}
            />
            <div className='admin-film-info__duree'>
            <input className="admin-film-info__number muted"
              type="number"
              min="1"
              required
              value={filmData.duree_minutes}
              onChange={(event) => setFilmData({ ...filmData, duree_minutes: Number(event.target.value) })}
            /> 
            <span className='admin-film-info__number muted'>min</span>  
            </div>

            <textarea className="admin-film-info__description principal"
              placeholder="Description du film"
              required
              value={filmData.description}
              onChange={(event) => setFilmData({ ...filmData, description: event.target.value })}
            />

          </div>

          {error && <p role="alert">{error}</p>}
          <button className="admin__film-action button-gold" type="submit" disabled={isSaving}>
            {isSaving ? 'Enregistrement...' : 'Sauvegarder'}
          </button>
        </form>

      </div>
    </section>
  )
}
