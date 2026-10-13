import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext.jsx'
import { updateAdminFilm, createAdminFilm } from '../../services/filmService.js'
import { useNavigate } from 'react-router-dom'

const emptyFilm = { titre: '', duree_minutes: '', affiche_url: '', description: '' }

export default AdminFilmInfo

function AdminFilmInfo({ film = null }) {
  const { token } = useAuth()
  const navigate = useNavigate()
  const [filmData, setFilmData] = useState(film || emptyFilm)
  const [error, setError] = useState(null)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    setFilmData(film || emptyFilm)
  }, [film])

  function handleChange(event) {
    const { name, value, type } = event.target
    setFilmData({ ...filmData, [name]: type === 'number' ? Number(value) : value })
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError(null)
    setIsSaving(true)

    try {
      const filmToSave = {
        titre: filmData.titre,
        duree_minutes: Number(filmData.duree_minutes),
        affiche_url: filmData.affiche_url,
        description: filmData.description,
      }
      const savedFilm = film
        ? await updateAdminFilm(film.id_film, filmToSave, token)
        : await createAdminFilm(filmToSave, token)

      if (film) setFilmData(savedFilm)
      else navigate(`/films/${savedFilm.id_film}`)
    } catch (error) {
      setError(error.message)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <section className="panel" >
      <div className="film-info__summary">
        <div className="film-poster">
          {filmData.affiche_url && <img src={filmData.affiche_url} />}
        </div>

        <form className="film-info__info" onSubmit={handleSubmit}>

          <div className="admin-film-info__form">
            <input className='admin-film-info__affiche petit'
              name="affiche_url"
              type="url"
              placeholder="URL de l’affiche"
              required
              value={filmData.affiche_url}
              onChange={handleChange}
            />
            <input className="admin-film-info__titre display-l"
              name="titre"
              maxLength="50"
              placeholder="Titre du film"
              required
              value={filmData.titre}
              onChange={handleChange}
            />
            <div className='admin-film-info__duree'>
            <input className="admin-film-info__number muted"
              name="duree_minutes"
              type="number"
              min="1"
              required
              value={filmData.duree_minutes}
              onChange={handleChange}
            /> 
            <span className='admin-film-info__number muted'>min</span>  
            </div>

            <textarea className="admin-film-info__description principal"
              name="description"
              placeholder="Description du film"
              required
              value={filmData.description}
              onChange={handleChange}
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
