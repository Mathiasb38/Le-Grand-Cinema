import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import FilmInfo from '../components/sections/FilmInfo.jsx'
import { getFilmDetails } from '../services/filmService.js'

export default FilmDetail

function FilmDetail() {
  const { idFilm } = useParams()
  const [film, setFilm] = useState(null)

  useEffect(() => {
    getFilmDetails(idFilm)
      .then(setFilm)
      .catch(() => setFilm(null))
  }, [idFilm])

  if (!film) {
    return null
  }

  return (
    <main className="film-detail">
      <FilmInfo film={film} />
    </main>
  )
}
