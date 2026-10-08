from datetime import datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.database import get_engine
from app.models import Billet, Film, Place, Reservation, Salle, Seance, Utilisateur


@pytest.fixture
def db_session():
    with Session(get_engine()) as session:
        yield session


@pytest.fixture
def film_data(db_session):
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
    far_film = Film(
        titre="8 Days Later",
        duree_minutes=120,
        affiche_url="https://xxx.com/far.jpg",
    )
    db_session.add_all([salle, past_film, programmed_film, far_film])
    db_session.flush()

    places = [
        Place(id_salle=salle.id_salle, rangee="A", numero=number)
        for number in range(1, 6)
    ]
    user = Utilisateur(
        email="test@example.com",
        mot_de_passe_hash="hash",
        role="client",
    )
    db_session.add_all([*places, user])
    db_session.flush()

    now = datetime.now()
    past_seance = Seance(
        date_heure_debut=now - timedelta(days=1),
        id_film=past_film.id_film,
        id_salle=salle.id_salle,
    )
    programmed_seance = Seance(
        date_heure_debut=now + timedelta(hours=1),
        id_film=programmed_film.id_film,
        id_salle=salle.id_salle,
    )
    far_seance = Seance(
        date_heure_debut=now + timedelta(days=8),
        id_film=far_film.id_film,
        id_salle=salle.id_salle,
    )
    db_session.add_all([past_seance, programmed_seance, far_seance])
    db_session.flush()

    db_session.add_all([
        Billet(
            code_billet="TEST-1",
            date_emission=now,
            id_place=places[0].id_place,
            id_seance=programmed_seance.id_seance,
        ),
        Billet(
            code_billet="TEST-2",
            date_emission=now,
            id_place=places[1].id_place,
            id_seance=programmed_seance.id_seance,
        ),
        Reservation(
            reference="RES-1",
            date_reservation=now,
            is_paid=False,
            is_cancelled=False,
            id_seance=programmed_seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=places[2].id_place,
        ),
        Reservation(
            reference="RES-2",
            date_reservation=now,
            is_paid=True,
            is_cancelled=False,
            id_seance=programmed_seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=places[3].id_place,
        ),
        Reservation(
            reference="RES-3",
            date_reservation=now,
            is_paid=False,
            is_cancelled=True,
            id_seance=programmed_seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=places[4].id_place,
        ),
    ])

    return (
        db_session,
        past_film,
        programmed_film,
        far_film,
        past_seance,
        programmed_seance,
        far_seance,
    )
