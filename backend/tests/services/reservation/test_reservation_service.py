import pytest
from fastapi import HTTPException

from app.schemas import ReservationCreate
from app.services.reservation_service import create_reservation, get_user_reservations
from sqlalchemy import select
from app.models import Reservation


def test_create_reservation(reservation_data):
    db_session, user, seance, _ = reservation_data

    created = create_reservation(
        db_session,
        user,
        ReservationCreate(id_seance=seance.id_seance, nombre_places=2),
    )

    assert len(created) == 2
    assert all(item.id_seance == seance.id_seance for item in created)

    created_ids = {item.id_reservation for item in created}
    saved_ids = set(db_session.scalars(
        select(Reservation.id_reservation).where(
            Reservation.id_reservation.in_(created_ids)
        )
    ).all())

    assert saved_ids == created_ids


def test_create_reservation_rejects(reservation_data):
    db_session, user, seance, _ = reservation_data

    with pytest.raises(HTTPException) as error:
        create_reservation(
            db_session,
            user,
            ReservationCreate(id_seance=seance.id_seance, nombre_places=101),
        )

    assert error.value.status_code == 409


def test_get_user_reservations(reservations_data):
    db_session, user, seance, _ = reservations_data
    result = get_user_reservations(db_session, user)

    assert [item.reference for item in result] == ["RES-CLIENT"]
    assert result[0].titre_film == "Film test"
    assert result[0].date_heure_debut == seance.date_heure_debut
    assert result[0].nom_salle == "test"
    assert result[0].numero_salle == 666
