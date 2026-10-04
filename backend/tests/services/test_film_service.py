from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import get_engine
from app.models import Film, Salle, Seance
from app.services.film_service import get_programmed_films


def test_list_programmed_films_excludes_past_sessions() -> None:
    with Session(get_engine()) as session:
        salle = Salle(numero=666, nom="test", capacite_max=10)
        past_film = Film(
            titre="Past",
            duree_minutes=120,
            affiche_url="https://xxx.com/past.jpg",
        )
        programmed_film = Film(
            titre="Futur",
            duree_minutes=120,
            affiche_url="https://xxx.com/futur.jpg",
        )
        session.add_all([salle, past_film, programmed_film])
        session.flush()

        past_session = Seance(
            date_heure_debut=datetime.now() - timedelta(days=1),
            id_film=past_film.id_film,
            id_salle=salle.id_salle,
        )
        programmed_session = Seance(
            date_heure_debut=datetime.now() + timedelta(days=1),
            id_film=programmed_film.id_film,
            id_salle=salle.id_salle,
        )
        session.add_all([past_session, programmed_session])

        result = get_programmed_films(session)

        assert programmed_film in result
        assert past_film not in result
