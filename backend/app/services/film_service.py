from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Film, Seance


def get_programmed_films(session: Session) -> list[Film]:
    statement = (
        select(Film)
        .join(Seance)
        .where(Seance.date_heure_debut >= datetime.now())
        .distinct()
        .order_by(Film.titre)
    )
    return list(session.scalars(statement))
