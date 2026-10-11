import pytest
from fastapi import HTTPException

from app.schemas import ReservationCreate
from app.services.reservation_service import create_reservation
from sqlalchemy import select
from app.models import Reservation


def test_create_reservation(reservation_data):
    db_session, user, seance = reservation_data

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
    db_session, user, seance = reservation_data

    with pytest.raises(HTTPException) as error:
        create_reservation(
            db_session,
            user,
            ReservationCreate(id_seance=seance.id_seance, nombre_places=4),
        )

    assert error.value.status_code == 409
