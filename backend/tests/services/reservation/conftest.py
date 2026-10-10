from datetime import datetime, timedelta

import pytest

from app.models import Film, Place, Salle, Seance, Utilisateur


@pytest.fixture
def reservation_data(db_session):
    salle = Salle(numero=777, nom="test", capacite_max=3)
    film = Film(
        titre="Film test",
        duree_minutes=120,
        affiche_url="https://example.com/film.jpg",
    )
    user = Utilisateur(
        email="reservation@example.com",
        mot_de_passe_hash="hash",
        role="client",
    )
    db_session.add_all([salle, film, user])
    db_session.flush()

    places = [
        Place(id_salle=salle.id_salle, rangee="A", numero=number)
        for number in range(1, 4)
    ]
    seance = Seance(
        date_heure_debut=datetime.now() + timedelta(days=1),
        id_film=film.id_film,
        id_salle=salle.id_salle,
    )
    db_session.add_all([*places, seance])
    db_session.flush()

    return db_session, user, seance
