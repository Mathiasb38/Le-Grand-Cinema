import pytest
from fastapi import HTTPException

from app.schemas import ReservationCreate
from app.services.reservation_service import (
    create_reservation,
    get_user_reservations,
    cancel_reservation,
)
from sqlalchemy import select
from app.models import Reservation
from datetime import datetime


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
    saved_ids = set(
        db_session.scalars(
            select(Reservation.id_reservation).where(
                Reservation.id_reservation.in_(created_ids)
            )
        ).all()
    )

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


def test_cancel_reservation_frees_place(reservations_data):
    db_session, user, seance, places = reservations_data
    reservation = db_session.scalar(
        select(Reservation).where(Reservation.reference == "RES-CLIENT")
    )

    cancel_reservation(db_session, user, reservation.reference)
    created = create_reservation(
        db_session,
        user,
        ReservationCreate(id_seance=seance.id_seance, nombre_places=1),
    )

    assert reservation.is_cancelled is True
    assert created[0].id_place == places[0].id_place


@pytest.mark.parametrize(
    ("reference", "status_code"),
    [("RES-PAID", 409), ("RES-CANCELLED", 409), ("RES-OTHER", 404)],
)
def test_cancel_reservation_rejects_ineligible(
    reservations_data, reference, status_code
):
    db_session, user, _, _ = reservations_data

    with pytest.raises(HTTPException) as error:
        cancel_reservation(db_session, user, reference)

    assert error.value.status_code == status_code


def test_cancel_reservation_rejects_past_session(reservations_data):
    db_session, user, seance, _ = reservations_data
    seance.date_heure_debut = datetime.now()
    db_session.flush()

    with pytest.raises(HTTPException) as error:
        cancel_reservation(db_session, user, "RES-CLIENT")

    assert error.value.status_code == 409
