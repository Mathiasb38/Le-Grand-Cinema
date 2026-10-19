from datetime import datetime, timedelta, date, time

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Film, Seance, Reservation, Salle, Billet, Place
from app.schemas import FilmDetailsResponse, SeanceResponse, FilmWrite, SeanceCreate, SeanceUpdate, PlaceResponse
from fastapi import HTTPException


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
    session: Session, id_film: int, selected_date: date | None = None
) -> FilmDetailsResponse | None:
    film = session.get(Film, id_film)

    if film is None:
        return None

    seances = []
    for seance in get_film_seances(session, id_film, selected_date):
        salle = session.get(Salle, seance.id_salle)
        seances.append(
            SeanceResponse(
                id_seance=seance.id_seance,
                date_heure_debut=seance.date_heure_debut,
                id_salle=seance.id_salle,
                nom_salle=salle.nom,
                numero_salle=salle.numero,
                places_disponibles=get_available_places(session, seance),
            )
        )

    return FilmDetailsResponse(
        id_film=film.id_film,
        titre=film.titre,
        duree_minutes=film.duree_minutes,
        affiche_url=film.affiche_url,
        description=film.description,
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


def get_seance_places(
    session: Session,
    id_seance: int,
) -> list[PlaceResponse] | None:
    seance = session.get(Seance, id_seance)

    if seance is None:
        return None

    places = session.scalars(
        select(Place)
        .where(Place.id_salle == seance.id_salle)
        .order_by(Place.rangee, Place.numero)
    ).all()
    occupied_place_ids = set(session.scalars(
        select(Billet.id_place).where(Billet.id_seance == id_seance)
    ))
    reserved_place_ids = set(session.scalars(
        select(Reservation.id_place).where(
            Reservation.id_seance == id_seance,
            Reservation.is_cancelled.is_(False),
        )
    ))
    unavailable_place_ids = occupied_place_ids | reserved_place_ids

    return [
        PlaceResponse(
            id_place=place.id_place,
            rangee=place.rangee,
            numero=place.numero,
            disponible=place.id_place not in unavailable_place_ids,
        )
        for place in places
    ]


def get_film_seances(
    session: Session, id_film: int, selected_date: date | None
) -> list[Seance]:
    if selected_date is None:
        statement = (
            select(Seance)
            .where(
                Seance.id_film == id_film,
                Seance.date_heure_debut >= datetime.now(),
            )
            .order_by(Seance.date_heure_debut)
        )
        return list(session.scalars(statement))

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


def get_all_films(session: Session) -> list[Film]:
    return list(session.scalars(select(Film).order_by(Film.titre)))


def create_seance(session: Session, seance_data: SeanceCreate) -> SeanceResponse:
    if seance_data.date_heure_debut < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Date invalide",
        )

    film = session.get(Film, seance_data.id_film)
    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    salle = session.get(Salle, seance_data.id_salle)
    if salle is None:
        raise HTTPException(status_code=404, detail="Salle introuvable")

    start = seance_data.date_heure_debut
    end = start + timedelta(minutes=film.duree_minutes)
    if seance_conflict(session, salle.id_salle, start, end):
        raise HTTPException(
            status_code=409,
            detail="La salle est déjà occupée sur ce créneau",
        )

    seance = Seance(**seance_data.model_dump())
    session.add(seance)
    session.commit()
    session.refresh(seance)

    return SeanceResponse(
        id_seance=seance.id_seance,
        date_heure_debut=seance.date_heure_debut,
        id_salle=salle.id_salle,
        nom_salle=salle.nom,
        numero_salle=salle.numero,
        places_disponibles=get_available_places(session, seance),
    )


def update_seance(
    session: Session,
    id_seance: int,
    seance_data: SeanceUpdate,
) -> SeanceResponse:
    seance = session.get(Seance, id_seance)
    if seance is None:
        raise HTTPException(status_code=404, detail="Séance introuvable")

    check_reservation_billet(session, seance)

    if seance_data.date_heure_debut <= datetime.now():
        raise HTTPException(status_code=400, detail="Date invalide")

    salle = session.get(Salle, seance_data.id_salle)
    if salle is None:
        raise HTTPException(status_code=404, detail="Salle introuvable")

    film = session.get(Film, seance.id_film)
    end = seance_data.date_heure_debut + timedelta(minutes=film.duree_minutes)
    if seance_conflict(
        session,
        salle.id_salle,
        seance_data.date_heure_debut,
        end,
        excluded_id=seance.id_seance,
    ):
        raise HTTPException(
            status_code=409,
            detail="La salle est déjà occupée sur ce créneau",
        )

    seance.id_salle = salle.id_salle
    seance.date_heure_debut = seance_data.date_heure_debut
    session.commit()
    session.refresh(seance)

    return SeanceResponse(
        id_seance=seance.id_seance,
        date_heure_debut=seance.date_heure_debut,
        id_salle=salle.id_salle,
        nom_salle=salle.nom,
        numero_salle=salle.numero,
        places_disponibles=get_available_places(session, seance),
    )


def delete_seance(session: Session, id_seance: int) -> None:
    seance = session.get(Seance, id_seance)
    if seance is None:
        raise HTTPException(status_code=404, detail="Séance introuvable")

    check_reservation_billet(session, seance)
    session.delete(seance)
    session.commit()


def create_film(session: Session, film_data: FilmWrite) -> Film:
    film = Film(**film_data.model_dump())
    session.add(film)
    session.commit()
    session.refresh(film)
    return film


def update_film(
    session: Session, id_film: int, film_data: FilmWrite
) -> Film | None:
    film = session.get(Film, id_film)

    if film is None:
        return None

    film.titre = film_data.titre
    film.duree_minutes = film_data.duree_minutes
    film.affiche_url = film_data.affiche_url
    film.description = film_data.description

    session.commit()
    session.refresh(film)
    return film


def get_all_salles(session: Session) -> list[Salle]:
    return list(session.scalars(select(Salle).order_by(Salle.numero)))

def seance_conflict(
    session: Session,
    id_salle: int,
    start: datetime,
    end: datetime,
    excluded_id: int | None = None,
) -> bool:
    statement = (
        select(Seance.id_seance)
        .join(Film, Seance.id_film == Film.id_film)
        .where(
            Seance.id_salle == id_salle,
            Seance.date_heure_debut >= datetime.combine(start.date(), time.min) - timedelta(days=1),
            Seance.date_heure_debut < end,
            Seance.date_heure_debut
            + func.make_interval(0, 0, 0, 0, 0, Film.duree_minutes)
            > start,
        )
        .limit(1)
    )
    if excluded_id is not None:
        statement = statement.where(Seance.id_seance != excluded_id)

    return session.execute(statement).first() is not None


def check_reservation_billet(session: Session, seance: Seance) -> None:
    if seance.date_heure_debut <= datetime.now():
        raise HTTPException(status_code=400, detail="Séance passée")

    has_reservation = session.scalar(
        select(Reservation.id_reservation)
        .where(
            Reservation.id_seance == seance.id_seance,
            Reservation.is_cancelled.is_(False),
        )
        .limit(1)
    ) is not None
    has_ticket = session.scalar(
        select(Billet.id_billet)
        .where(Billet.id_seance == seance.id_seance)
        .limit(1)
    ) is not None

    if has_reservation or has_ticket:
        raise HTTPException(
            status_code=409,
            detail="Séance associée à une réservation ou un billet",
        )
