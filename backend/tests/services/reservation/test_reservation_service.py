import pytest
from fastapi import HTTPException

from app.schemas import ReservationCreate
from app.services.reservation_service import create_reservation


def test_create_reservation(reservation_data):
    db_session, user, seance = reservation_data

    reservations = create_reservation(
        db_session,
        user,
        ReservationCreate(id_seance=seance.id_seance, nombre_places=2),
    )

    assert len(reservations) == 2
    assert all(reservation.id_seance == seance.id_seance for reservation in reservations)


def test_create_reservation_rejects(reservation_data):
    db_session, user, seance = reservation_data

    with pytest.raises(HTTPException) as error:
        create_reservation(
            db_session,
            user,
            ReservationCreate(id_seance=seance.id_seance, nombre_places=4),
        )

    assert error.value.status_code == 409
