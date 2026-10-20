import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useRef } from 'react'
import { scrollCards } from '../../utils/helpers.js'

export default AdminSaleFilms

function AdminSaleFilms({ films, selectedFilmId, onSelectFilm }) {
  const cardsRef = useRef(null)

  return (
    <div className="panel__list">
      <button
        className="panel__arrow panel__arrow--left"
        type="button"
        aria-label="Films précédents"
        onClick={() => scrollCards(cardsRef, -1, 304)}
      >
        <ChevronLeft aria-hidden="true" />
      </button>
      <div className="panel__cards admin-sale__films" ref={cardsRef}>
        {films.map((film) => (
          <button
            className={`film-card admin-sale__film-card${selectedFilmId === film.id_film ? ' admin-sale__film-card--selected' : ''}`}
            key={film.id_film}
            type="button"
            onClick={() => onSelectFilm(film)}
          >
            <img className="film-card__poster" src={film.affiche_url} alt={`Affiche du film ${film.titre}`} />
            <h2 className="film-card__title">{film.titre}</h2>
          </button>
        ))}
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
  )
}
