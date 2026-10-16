import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import FilmInfo from '../components/sections/FilmInfo.jsx'
import AdminFilmInfo from '../components/sections/AdminFilmInfo.jsx'

import { getFilmDetails, getAdminFilmDetails } from '../services/filmService.js'
import { useAuth } from '../context/AuthContext.jsx'

export default FilmDetail

function FilmDetail({ isNew = false }) {
  const { idFilm } = useParams()
  const { isAdmin, token } = useAuth()
  const [film, setFilm] = useState(null)

  useEffect(() => {
    if (isNew) return

    const request = isAdmin
      ? getAdminFilmDetails(idFilm, token)
      : getFilmDetails(idFilm)

    request
      .then(setFilm)
      .catch(() => setFilm(null))
  }, [idFilm, isAdmin, isNew, token])

  if ((!isNew && !film) || (isNew && !isAdmin)) {
    return null
  }

  return (
    <main className="film-detail">
      {isAdmin ? <AdminFilmInfo film={film} /> : <FilmInfo film={film} />}
    </main>
  )
}
