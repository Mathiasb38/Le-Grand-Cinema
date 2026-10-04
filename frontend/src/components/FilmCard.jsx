export default FilmCard

function FilmCard({ film, onViewSessions }) {
  return (
    <article className="film-card">
      <img
        className="film-card__poster"
        src={film.affiche_url}
        alt={`Affiche du film ${film.titre}`}
      />
      <h2 className="film-card__title">{film.titre}</h2>
      <button
        className="button-gold film-card__sessions"
        type="button"
        onClick={() => onViewSessions?.(film.id_film)}
      >
        Voir les séances
      </button>
    </article>
  )
}
