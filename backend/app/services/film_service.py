from datetime import datetime, timedelta, date, time

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Film, Seance, Reservation, Salle, Billet
from app.schemas import FilmDetailsResponse, SeanceResponse


def get_programmed_films(session: Session) -> list[Film]:
    now = datetime.now()
    end = datetime.combine(date.today() + timedelta(days=7), time.min)
    statement = (
        select(Film)
        .join(Seance)
        .where(
            Seance.date_heure_debut >= now,
            Seance.date_heure_debut < end,
        )
        .distinct()
        .order_by(Film.titre)
    )
    return list(session.scalars(statement))


def get_film_details(
    session: Session, id_film: int, selected_date: date
) -> FilmDetailsResponse | None:
    film = session.get(Film, id_film)

    if film is None:
        return None

    seances = [
        SeanceResponse(
            id_seance=seance.id_seance,
            date_heure_debut=seance.date_heure_debut,
            id_salle=seance.id_salle,
            places_disponibles=get_available_places(session, seance),
        )
        for seance in get_film_seances(session, id_film, selected_date)
    ]

    return FilmDetailsResponse(
        id_film=film.id_film,
        titre=film.titre,
        duree_minutes=film.duree_minutes,
        affiche_url=film.affiche_url,
        seances=seances,
    )


def get_available_places(session: Session, seance: Seance) -> int:
    occupied_places = (
        select(func.count(Billet.id_billet))
        .where(Billet.id_seance == seance.id_seance)
        .scalar_subquery()
    )
    reserved_places = (
        select(func.count(Reservation.id_reservation))
        .where(
            Reservation.id_seance == seance.id_seance,
            Reservation.is_cancelled.is_(False),
            Reservation.is_paid.is_(False),
        )
        .scalar_subquery()
    )
    statement = select(
        Salle.capacite_max,
        occupied_places,
        reserved_places,
    ).where(Salle.id_salle == seance.id_salle)

    capacity, occupied_places, reserved_places = session.execute(statement).one()
    return max(capacity - occupied_places - reserved_places, 0)


def get_film_seances(
    session: Session, id_film: int, selected_date: date
) -> list[Seance]:
    today = date.today()
    if not today <= selected_date <= today + timedelta(days=6):
        return []

    start = datetime.combine(selected_date, time.min)
    end = start + timedelta(days=1)

    if selected_date == today:
        start = max(start, datetime.now())

    statement = (
        select(Seance)
        .where(
            Seance.id_film == id_film,
            Seance.date_heure_debut >= start,
            Seance.date_heure_debut < end,
        )
        .order_by(Seance.date_heure_debut)
    )

    return list(session.scalars(statement))
