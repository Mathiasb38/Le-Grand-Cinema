from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Film, Seance


def get_programmed_films(session: Session) -> list[Film]:
    now = datetime.now()
    statement = (
        select(Film)
        .join(Seance)
        .where(
            Seance.date_heure_debut >= now,
            Seance.date_heure_debut <= now + timedelta(days=7),
        )
        .distinct()
        .order_by(Film.titre)
    )
    return list(session.scalars(statement))


def get_film_details(session: Session, id_film: int) -> tuple[Film | None, list[Seance]]:
    film = session.get(Film, id_film)

    if film is None:
        return None, []

    now = datetime.now()
    statement = (
        select(Seance)
        .where(
            Seance.id_film == id_film,
            Seance.date_heure_debut >= now,
            Seance.date_heure_debut <= now + timedelta(days=7),
        )
        .order_by(Seance.date_heure_debut)
    )
    return film, list(session.scalars(statement))
