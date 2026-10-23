import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import FilmCard from '../components/groups/FilmCard.jsx'
import { getFilms, getAdminFilms } from '../services/filmService.js'
import { scrollCards } from '../utils/helpers.js'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default FilmCatalog

function FilmCatalog() {
  const { isAdmin, token } = useAuth()
  const [films, setFilms] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const cardsRef = useRef(null)

  useEffect(() => {
    setIsLoading(true)
    const request = isAdmin ? getAdminFilms(token) : getFilms()
    request.then(setFilms).catch(() => setFilms([])).finally(() => setIsLoading(false))
  }, [isAdmin, token])

  return (
    <main className="catalog">
      <section className="panel" aria-label="Catalogue des films">

        {isLoading ? (
          <p>Chargement des films...</p>
        ) : films.length > 0 && (
          <div className="panel__list">
            <button
              className="panel__arrow panel__arrow--left"
              type="button"
              aria-label="Films précédents"
              onClick={() => scrollCards(cardsRef, -1, 304)}
            >
              <ChevronLeft aria-hidden="true" />
            </button>
            <div className="panel__cards" ref={cardsRef}>
              {films.map((film) => <FilmCard key={film.id_film} film={film} />)}
            </div>
            <button
              className="panel__arrow panel__arrow--right"
              type="button"
              aria-label="Films suivants"
              onClick={() => scrollCards(cardsRef, 1, 304)}
            >
              <ChevronRight aria-hidden="true" />
            </button>
          </div>
        )}
        {isAdmin && (
          <div className="catalog__admin-action">
            <Link className="button-gold" to="/admin/films/nouveau">Ajouter un film</Link>
          </div>
        )}
      </section>
    </main>
  )
}
