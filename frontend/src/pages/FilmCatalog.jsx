import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import FilmCard from '../components/groups/FilmCard.jsx'
import { getFilms } from '../services/filmService.js'

export default FilmCatalog

function FilmCatalog() {
  const [films, setFilms] = useState([])
  const cardsRef = useRef(null)

  useEffect(() => {
    getFilms()
      .then(setFilms)
  }, [])

  function scrollCards(direction) {
    cardsRef.current?.scrollBy({ left: direction * 304, behavior: 'smooth' })
  }

  return (
    <main className="catalog">
      <section className="panel" aria-label="Catalogue des films">
        {films.length > 0 && (
          <div className="panel__list">
            <button
              className="panel__arrow panel__arrow--left"
              type="button"
              aria-label="Films précédents"
              onClick={() => scrollCards(-1)}
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
              onClick={() => scrollCards(1)}
            >
              <ChevronRight aria-hidden="true" />
            </button>
          </div>
        )}
      </section>
    </main>
  )
}
