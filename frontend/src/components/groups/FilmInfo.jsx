import SessionList from '../sections/SessionList.jsx'

export default FilmInfo

function FilmInfo({ film }) {
  return (
    <section className="panel" aria-label={`Détails du film ${film.titre}`}>
      <div className="film-info__summary">
        <div className="film-poster">
          <img src={film.affiche_url} alt={`Affiche du film ${film.titre}`} />
        </div>
        <div className="film-info__info">
          <h1 className="display-l">{film.titre}</h1>
          <p className="principal">Description du film</p>
          <p className="muted">{film.duree_minutes} min</p>
        </div>
      </div>

      <SessionList sessions={film.seances} />
    </section>
  )
}
