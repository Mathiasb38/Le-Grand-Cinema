import { Link } from 'react-router-dom'

export default FilmCard

function FilmCard({ film }) {
  return (
    <article className="film-card">
      <img
        className="film-card__poster"
        src={film.affiche_url}
        alt={`Affiche du film ${film.titre}`}
      />
      <h2 className="film-card__title">{film.titre}</h2>
      <Link
        className="button-gold film-card__sessions"
        to={`/films/${film.id_film}`}
      >
        Voir les séances
      </Link>
    </article>
  )
}
