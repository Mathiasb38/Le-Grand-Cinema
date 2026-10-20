from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models import Billet, Place, Reservation, Seance, Utilisateur, Film, Salle
from app.schemas import (
    ReservationCreate,
    ReservationDetailsResponse,
    ReservationAdminResponse,
    BilletResponse,
    BilletCreate,
    BilletVenteResponse,
)


def create_reservation(
    session: Session,
    user: Utilisateur,
    reservation_data: ReservationCreate,
) -> list[Reservation]:
    try:
        seance = session.scalar(
            select(Seance)
            .where(Seance.id_seance == reservation_data.id_seance)
            .with_for_update()
        )

        if seance is None or seance.date_heure_debut <= datetime.now():
            raise HTTPException(status_code=404, detail="Séance introuvable")

        occupied_places = select(Billet.id_place).where(
            Billet.id_seance == seance.id_seance
        )
        reserved_places = select(Reservation.id_place).where(
            Reservation.id_seance == seance.id_seance,
            Reservation.is_cancelled.is_(False),
            Reservation.is_paid.is_(False),
        )
        places = session.scalars(
            select(Place)
            .where(
                Place.id_salle == seance.id_salle,
                Place.id_place.in_(reservation_data.id_places),
                Place.id_place.not_in(occupied_places),
                Place.id_place.not_in(reserved_places),
            )
        ).all()

        if len(places) != len(reservation_data.id_places):
            raise HTTPException(
                status_code=409,
                detail="Une ou plusieurs places sont indisponibles",
            )

        places_by_id = {place.id_place: place for place in places}
        reservations = [
            Reservation(
                reference=f"RES-{uuid4().hex[:12].upper()}",
                date_reservation=datetime.now(),
                id_seance=seance.id_seance,
                id_utilisateur=user.id_utilisateur,
                id_place=place.id_place,
            )
            for place in (places_by_id[place_id] for place_id in reservation_data.id_places)
        ]
        session.add_all(reservations)
        session.commit()

        return reservations
    except Exception:
        session.rollback()
        raise


def create_billet(
    session: Session,
    sale_data: BilletCreate,
) -> list[BilletVenteResponse]:
    try:
        seance = session.scalar(
            select(Seance)
            .where(Seance.id_seance == sale_data.id_seance)
            .with_for_update()
        )

        if seance is None or seance.date_heure_debut <= datetime.now():
            raise HTTPException(status_code=404, detail="Séance introuvable")

        reserved_places = select(Reservation.id_place).where(
            Reservation.id_seance == seance.id_seance,
            Reservation.is_cancelled.is_(False),
        )
        sold_places = select(Billet.id_place).where(
            Billet.id_seance == seance.id_seance
        )
        places = session.scalars(
            select(Place).where(
                Place.id_salle == seance.id_salle,
                Place.id_place.in_(sale_data.id_places),
                Place.id_place.not_in(reserved_places),
                Place.id_place.not_in(sold_places),
            )
        ).all()

        if len(places) != len(sale_data.id_places):
            raise HTTPException(
                status_code=409,
                detail="Une ou plusieurs places sont indisponibles",
            )

        billets = [
            Billet(
                code_billet=f"BIL-{uuid4().hex[:12].upper()}",
                date_emission=datetime.now(),
                id_place=place.id_place,
                id_seance=seance.id_seance,
                id_utilisateur=None,
            )
            for place in places
        ]
        session.add_all(billets)
        session.commit()
        return [BilletVenteResponse(code_billet=billet.code_billet) for billet in billets]
    except Exception:
        session.rollback()
        raise


def get_user_reservations(
    session: Session,
    user: Utilisateur,
) -> list[ReservationDetailsResponse]:
    statement = (
        select(
            Reservation.reference,
            Film.titre,
            Seance.date_heure_debut,
            Salle.nom,
            Salle.numero,
        )
        .join(Seance, Reservation.id_seance == Seance.id_seance)
        .join(Film, Seance.id_film == Film.id_film)
        .join(Salle, Seance.id_salle == Salle.id_salle)
        .where(
            Reservation.id_utilisateur == user.id_utilisateur,
            Reservation.is_paid.is_(False),
            Reservation.is_cancelled.is_(False),
        )
        .order_by(Seance.date_heure_debut)
    )

    return [
        ReservationDetailsResponse(
            reference=reference,
            titre_film=titre,
            date_heure_debut=date_heure_debut,
            nom_salle=nom_salle,
            numero_salle=numero_salle,
        )
        for reference, titre, date_heure_debut, nom_salle, numero_salle in session.execute(
            statement
        )
    ]


def get_user_billets(
    session: Session,
    user: Utilisateur,
) -> list[BilletResponse]:
    statement = (
        select(
            Billet.code_billet,
            Film.titre,
            Seance.date_heure_debut,
            Salle.nom,
            Salle.numero,
        )
        .join(Seance, Billet.id_seance == Seance.id_seance)
        .join(Film, Seance.id_film == Film.id_film)
        .join(Salle, Seance.id_salle == Salle.id_salle)
        .where(
            Billet.id_utilisateur == user.id_utilisateur,
        )
        .order_by(Seance.date_heure_debut)
    )

    return [
        BilletResponse(
            code_billet=code_billet,
            titre_film=titre,
            date_heure_debut=date_heure_debut,
            nom_salle=nom_salle,
            numero_salle=numero_salle,
        )
        for code_billet, titre, date_heure_debut, nom_salle, numero_salle in session.execute(statement)
    ]


def search_reservations(
    session: Session,
    search: str,
) -> list[ReservationAdminResponse]:
    statement = (
        select(
            Reservation.reference,
            Utilisateur.email,
            Film.titre,
            Seance.date_heure_debut,
            Salle.nom,
            Salle.numero,
            Reservation.is_paid,
            Reservation.is_cancelled,
        )
        .join(Seance, Reservation.id_seance == Seance.id_seance)
        .join(Film, Seance.id_film == Film.id_film)
        .join(Utilisateur, Reservation.id_utilisateur == Utilisateur.id_utilisateur)
        .join(Salle, Seance.id_salle == Salle.id_salle)
        .where(
            or_(
                Reservation.reference.ilike(f"%{search}%"),
                Utilisateur.email.ilike(f"%{search}%"),
            )
        )
        .order_by(Seance.date_heure_debut)
    )
    reservations = []
    for result in session.execute(statement):
        (
            reference,
            email,
            titre,
            date_heure_debut,
            nom_salle,
            numero_salle,
            is_paid,
            is_cancelled,
        ) = result
        reservations.append(
            ReservationAdminResponse(
                reference=reference,
                email=email,
                titre_film=titre,
                date_heure_debut=date_heure_debut,
                nom_salle=nom_salle,
                numero_salle=numero_salle,
                is_paid=is_paid,
                is_cancelled=is_cancelled,
            )
        )

    return reservations


def validate_payment(session: Session, reference: str) -> None:
    reservation = session.scalar(
        select(Reservation).where(Reservation.reference == reference)
    )

    if reservation is None:
        raise HTTPException(status_code=404, detail="Réservation introuvable")

    if reservation.is_paid or reservation.is_cancelled:
        raise HTTPException(
            status_code=409,
            detail="Paiement impossible",
        )

    seance = session.get(Seance, reservation.id_seance)
    if seance.date_heure_debut <= datetime.now():
        raise HTTPException(
            status_code=409,
            detail="Paiement impossible",
        )

    billet = Billet(
        code_billet=f"BIL-{uuid4().hex[:12].upper()}",
        date_emission=datetime.now(),
        id_place=reservation.id_place,
        id_seance=reservation.id_seance,
        id_utilisateur=reservation.id_utilisateur,
    )
    reservation.is_paid = True
    session.add(billet)
    session.commit()


def cancel_reservation(session: Session, user: Utilisateur, reference: str) -> None:
    statement = (
        select(Reservation, Seance.date_heure_debut)
        .join(Seance, Reservation.id_seance == Seance.id_seance)
        .where(
            Reservation.reference == reference,
            Reservation.id_utilisateur == user.id_utilisateur,
        )
    )

    reservation_and_date = session.execute(statement).one_or_none()

    if reservation_and_date is None:
        raise HTTPException(status_code=404, detail="Réservation introuvable")

    reservation, date_heure_debut = reservation_and_date
    if (
        reservation.is_paid
        or reservation.is_cancelled
        or date_heure_debut <= datetime.now()
    ):
        raise HTTPException(
            status_code=409,
            detail="Cette réservation ne peut plus être annulée",
        )

    reservation.is_cancelled = True
    session.commit()
