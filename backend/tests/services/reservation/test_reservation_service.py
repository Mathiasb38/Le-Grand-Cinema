import pytest
from fastapi import HTTPException

from app.schemas import ReservationCreate
from app.services.reservation_service import (
    create_reservation,
    get_user_reservations,
    cancel_reservation,
    search_reservations,
    validate_payment,
    get_user_billets,
)
from sqlalchemy import select
from app.models import Billet, Reservation
from datetime import datetime


def test_create_reservation(reservation_data):
    db_session, user, seance, places = reservation_data

    created = create_reservation(
        db_session,
        user,
        ReservationCreate(
            id_seance=seance.id_seance,
            id_places=[places[0].id_place, places[1].id_place],
        ),
    )

    assert len(created) == 2
    assert all(item.id_seance == seance.id_seance for item in created)
    assert {item.id_place for item in created} == {
        places[0].id_place,
        places[1].id_place,
    }

    created_ids = {item.id_reservation for item in created}
    assert len({item.reference for item in created}) == 2
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
            ReservationCreate(id_seance=seance.id_seance, id_places=[101]),
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


def test_get_user_billets_returns_only_user_paid_tickets(reservations_data):
    db_session, user, seance, places = reservations_data
    other_reservation = db_session.scalar(
        select(Reservation).where(Reservation.reference == "RES-OTHER")
    )
    other_reservation.is_paid = True
    db_session.add_all([
        Billet(
            code_billet="BIL-CLIENT",
            date_emission=datetime.now(),
            id_seance=seance.id_seance,
            id_place=places[1].id_place,
            id_utilisateur=user.id_utilisateur,
        ),
        Billet(
            code_billet="BIL-OTHER",
            date_emission=datetime.now(),
            id_seance=seance.id_seance,
            id_place=places[3].id_place,
            id_utilisateur=other_reservation.id_utilisateur,
        ),
    ])
    db_session.flush()

    result = get_user_billets(db_session, user)

    assert len(result) == 1
    assert result[0].code_billet == "BIL-CLIENT"
    assert result[0].titre_film == "Film test"
    assert result[0].date_heure_debut == seance.date_heure_debut
    assert result[0].nom_salle == "test"
    assert result[0].numero_salle == 666


def test_search_reservations_by_reference(reservations_data):
    db_session, _, seance, _ = reservations_data

    result = search_reservations(db_session, "CLIENT")

    assert len(result) == 1
    assert result[0].reference == "RES-CLIENT"
    assert result[0].email == "reservation@example.com"
    assert result[0].titre_film == "Film test"
    assert result[0].date_heure_debut == seance.date_heure_debut
    assert result[0].nom_salle == "test"
    assert result[0].numero_salle == 666
    assert result[0].is_paid is False
    assert result[0].is_cancelled is False


@pytest.mark.parametrize(
    ("reference", "is_paid", "is_cancelled"),
    [("RES-PAID", True, False), ("RES-CANCELLED", False, True)],
)
def test_search_reservations_by_reference_status(
    reservations_data,
    reference,
    is_paid,
    is_cancelled,
):
    db_session, _, _, _ = reservations_data

    result = search_reservations(db_session, reference)

    assert result[0].is_paid is is_paid
    assert result[0].is_cancelled is is_cancelled


def test_search_reservations_by_email(reservations_data):
    db_session, _, _, _ = reservations_data

    result = search_reservations(db_session, "reservation@")

    assert {reservation.reference for reservation in result} == {
        "RES-CLIENT",
        "RES-PAID",
        "RES-CANCELLED",
    }


def test_validate_payment_marks_reservation_paid_and_creates_ticket(reservations_data):
    db_session, _, _, _ = reservations_data

    validate_payment(db_session, "RES-CLIENT")

    reservation = db_session.scalar(
        select(Reservation).where(Reservation.reference == "RES-CLIENT")
    )
    billet = db_session.scalar(
        select(Billet).where(
            Billet.id_place == reservation.id_place,
            Billet.id_seance == reservation.id_seance,
        )
    )

    assert reservation.is_paid is True
    assert billet is not None
    assert billet.code_billet.startswith("BIL-")


@pytest.mark.parametrize(
    ("reference", "status_code"),
    [("RES-PAID", 409), ("RES-CANCELLED", 409), ("RES-UNKNOWN", 404)],
)
def test_validate_payment_rejects_ineligible_reservation(
    reservations_data, reference, status_code
):
    db_session, _, _, _ = reservations_data

    with pytest.raises(HTTPException) as error:
        validate_payment(db_session, reference)

    assert error.value.status_code == status_code


def test_validate_payment_rejects_past_session(reservations_data):
    db_session, _, seance, _ = reservations_data
    seance.date_heure_debut = datetime.now()
    db_session.flush()

    with pytest.raises(HTTPException) as error:
        validate_payment(db_session, "RES-CLIENT")

    assert error.value.status_code == 409


def test_cancel_reservation_frees_place(reservations_data):
    db_session, user, seance, places = reservations_data
    reservation = db_session.scalar(
        select(Reservation).where(Reservation.reference == "RES-CLIENT")
    )

    cancel_reservation(db_session, user, reservation.reference)
    created = create_reservation(
        db_session,
        user,
        ReservationCreate(id_seance=seance.id_seance, id_places=[places[0].id_place]),
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
