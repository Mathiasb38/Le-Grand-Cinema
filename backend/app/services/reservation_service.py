from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Billet, Place, Reservation, Seance, Utilisateur
from app.schemas import ReservationCreate


def create_reservation(
    session: Session,
    user: Utilisateur,
    reservation_data: ReservationCreate,
) -> list[Reservation]:
    seance = session.get(Seance, reservation_data.id_seance)

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
            Place.id_place.not_in(occupied_places),
            Place.id_place.not_in(reserved_places),
        )
        .order_by(Place.id_place)
        .limit(reservation_data.nombre_places)
    ).all()

    if len(places) < reservation_data.nombre_places:
        raise HTTPException(
            status_code=409,
            detail="Nombre de places indisponible",
        )

    reservations = [
        Reservation(
            reference=f"RES-{uuid4().hex[:12].upper()}",
            date_reservation=datetime.now(),
            id_seance=seance.id_seance,
            id_utilisateur=user.id_utilisateur,
            id_place=place.id_place,
        )
        for place in places
    ]
    session.add_all(reservations)
    session.commit()

    return reservations
