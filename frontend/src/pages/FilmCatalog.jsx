import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import FilmCard from '../components/groups/FilmCard.jsx'
import { getFilms } from '../services/filmService.js'
import { scrollCards } from '../utils/helpers.js'

export default FilmCatalog

function FilmCatalog() {
  const [films, setFilms] = useState([])
  const cardsRef = useRef(null)

  useEffect(() => {
    getFilms()
      .then(setFilms)
  }, [])

  return (
    <main className="catalog">
      <section className="panel" aria-label="Catalogue des films">
        {films.length > 0 && (
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
      </section>
    </main>
  )
}
