from app.services.film_service import (
    get_film_details,
    get_programmed_films,
    get_all_films,
    create_film,
    update_film,
)
from app.schemas import FilmWrite, SeanceCreate, SeanceUpdate
from app.services.film_service import create_seance, update_seance, delete_seance
from app.models import Salle, Seance
from sqlalchemy import select
from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException


def test_get_programmed_films(film_data) -> None:
    db_session, past_film, programmed_film, far_film, _, _, _ = film_data
    result = get_programmed_films(db_session)

    assert programmed_film in result
    assert past_film not in result
    assert far_film not in result


def test_get_film_details(film_data) -> None:
    db_session, _, film, _, past_seance, programmed_seance, far_seance = film_data
    result = get_film_details(
        db_session,
        film.id_film,
        programmed_seance.date_heure_debut.date(),
    )

    assert result.id_film == film.id_film
    assert result.seances[0].id_seance == programmed_seance.id_seance
    assert result.seances[0].nom_salle == "test"
    assert result.seances[0].numero_salle == 666
    assert result.seances[0].places_disponibles == 7
    result_ids = [seance.id_seance for seance in result.seances]
    assert past_seance.id_seance not in result_ids
    assert far_seance.id_seance not in result_ids


def test_get_all_films(film_data) -> None:
    db_session, past_film, programmed_film, far_film, *_ = film_data
    result = get_all_films(db_session)

    assert past_film in result
    assert programmed_film in result
    assert far_film in result


def test_create_seance(film_data) -> None:
    db_session, film, *_ = film_data
    salle = db_session.scalar(select(Salle))
    seance_data = SeanceCreate(
        id_film=film.id_film,
        id_salle=salle.id_salle,
        date_heure_debut=datetime.now() + timedelta(days=2),
    )

    seance = create_seance(db_session, seance_data)

    assert seance.id_seance is not None
    assert seance.date_heure_debut == seance_data.date_heure_debut
    assert seance.id_salle == salle.id_salle


def test_create_seance_rejects_past_date(film_data) -> None:
    db_session, film, *_ = film_data
    salle = db_session.scalar(select(Salle))
    seance_data = SeanceCreate(
        id_film=film.id_film,
        id_salle=salle.id_salle,
        date_heure_debut=datetime.now() - timedelta(minutes=1),
    )

    with pytest.raises(HTTPException) as error:
        create_seance(db_session, seance_data)

    assert error.value.status_code == 400


def test_create_seance_rejects_overlapping_session(film_data) -> None:
    db_session, film, _, _, _, existing_seance, _ = film_data
    seance_data = SeanceCreate(
        id_film=film.id_film,
        id_salle=existing_seance.id_salle,
        date_heure_debut=existing_seance.date_heure_debut + timedelta(minutes=30),
    )

    with pytest.raises(HTTPException) as error:
        create_seance(db_session, seance_data)

    assert error.value.status_code == 409


def test_update_seance(film_data) -> None:
    db_session, _, _, _, _, _, seance = film_data
    updated_data = SeanceUpdate(
        id_salle=seance.id_salle,
        date_heure_debut=datetime.now() + timedelta(days=9),
    )

    result = update_seance(db_session, seance.id_seance, updated_data)

    assert result.date_heure_debut == updated_data.date_heure_debut


def test_update_seance_rejects_past_session(film_data) -> None:
    db_session, _, _, _, past_seance, _, _ = film_data
    updated_data = SeanceUpdate(
        id_salle=past_seance.id_salle,
        date_heure_debut=datetime.now() + timedelta(days=1),
    )

    with pytest.raises(HTTPException) as error:
        update_seance(db_session, past_seance.id_seance, updated_data)

    assert error.value.status_code == 400


def test_update_seance_rejects_reserved_session(film_data) -> None:
    db_session, _, _, _, _, programmed_seance, _ = film_data
    updated_data = SeanceUpdate(
        id_salle=programmed_seance.id_salle,
        date_heure_debut=datetime.now() + timedelta(days=2),
    )

    with pytest.raises(HTTPException) as error:
        update_seance(db_session, programmed_seance.id_seance, updated_data)

    assert error.value.status_code == 409


def test_update_seance_rejects_occupied_room(film_data) -> None:
    db_session, _, _, _, _, _, far_seance = film_data
    other_seance = Seance(
        date_heure_debut=datetime.now() + timedelta(days=3),
        id_film=far_seance.id_film,
        id_salle=far_seance.id_salle,
    )
    db_session.add(other_seance)
    db_session.flush()
    updated_data = SeanceUpdate(
        id_salle=far_seance.id_salle,
        date_heure_debut=other_seance.date_heure_debut + timedelta(minutes=30),
    )

    with pytest.raises(HTTPException) as error:
        update_seance(db_session, far_seance.id_seance, updated_data)

    assert error.value.status_code == 409


def test_delete_seance(film_data) -> None:
    db_session, _, _, _, _, _, far_seance = film_data

    delete_seance(db_session, far_seance.id_seance)

    assert db_session.get(Seance, far_seance.id_seance) is None


def test_delete_seance_rejects_past_session(film_data) -> None:
    db_session, _, _, _, past_seance, _, _ = film_data

    with pytest.raises(HTTPException) as error:
        delete_seance(db_session, past_seance.id_seance)

    assert error.value.status_code == 400


def test_delete_seance_rejects_reserved_session(film_data) -> None:
    db_session, _, _, _, _, programmed_seance, _ = film_data

    with pytest.raises(HTTPException) as error:
        delete_seance(db_session, programmed_seance.id_seance)

    assert error.value.status_code == 409

def test_create_film(db_session) -> None:
    film_data = FilmWrite(
        titre="Nouveau film",
        duree_minutes=100,
        affiche_url="https://example.com/nouveau.jpg",
        description="Description du nouveau film",
    )

    film = create_film(db_session, film_data)

    assert film.id_film is not None
    assert film.titre == film_data.titre
    assert film.description == film_data.description


def test_update_film(film_data) -> None:
    db_session, film, *_ = film_data
    updated_data = FilmWrite(
        titre="Titre modifié",
        duree_minutes=130,
        affiche_url="https://example.com/modifie.jpg",
        description="Description modifiée",
    )

    updated_film = update_film(db_session, film.id_film, updated_data)

    assert updated_film.titre == updated_data.titre
    assert updated_film.duree_minutes == updated_data.duree_minutes
    assert updated_film.affiche_url == updated_data.affiche_url
    assert updated_film.description == updated_data.description


def test_update_film_not_found(db_session) -> None:
    updated_data = FilmWrite(
        titre="Titre modifié",
        duree_minutes=130,
        affiche_url="https://example.com/modifie.jpg",
        description="Description modifiée",
    )

    assert update_film(db_session, 999, updated_data) is None
