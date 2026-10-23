from datetime import datetime, timedelta

import pytest

from app.models import Film, Place, Reservation, Salle, Seance, Utilisateur


@pytest.fixture
def reservation_data(db_session):
    salle = Salle(numero=666, nom="test", capacite_max=100)
    film = Film(
        titre="Film test",
        duree_minutes=120,
        affiche_url="https://example.com/film.jpg",
        description="Description du film test",
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
        for number in range(1, 101)
    ]
    seance = Seance(
        date_heure_debut=datetime.now() + timedelta(days=1),
        id_film=film.id_film,
        id_salle=salle.id_salle,
    )
    db_session.add_all([*places, seance])
    db_session.flush()

    return db_session, user, seance, places


@pytest.fixture
def reservations_data(reservation_data):
    db_session, user, seance, places = reservation_data
    other_user = Utilisateur(
        email="other@example.com",
        mot_de_passe_hash="hash",
        role="client",
    )
    db_session.add(other_user)
    db_session.flush()
    db_session.add_all([
        Reservation(
            reference="RES-CLIENT",
            date_reservation=datetime.now(),
            id_seance=seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=places[0].id_place,
        ),
        Reservation(
            reference="RES-PAID",
            date_reservation=datetime.now(),
            is_paid=True,
            id_seance=seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=places[1].id_place,
        ),
        Reservation(
            reference="RES-CANCELLED",
            date_reservation=datetime.now(),
            is_cancelled=True,
            id_seance=seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=places[2].id_place,
        ),
        Reservation(
            reference="RES-OTHER",
            date_reservation=datetime.now(),
            id_seance=seance.id_seance,
            id_utilisateur=other_user.id_utilisateur,
            id_place=places[3].id_place,
        ),
    ])
    db_session.flush()

    return db_session, user, seance, places
