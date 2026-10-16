from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Film, Salle
from app.schemas import FilmDetailsResponse, FilmResponse, SeanceResponse, FilmWrite, SeanceCreate, SalleResponse, SeanceUpdate
from app.services.film_service import (
    get_film_details,
    get_programmed_films,
    get_all_films,
    create_film,
    update_film,
    create_seance,
    get_all_salles,
    update_seance,
    delete_seance,
)
from app.services.auth_service import require_admin

router = APIRouter()


@router.get("/films", response_model=list[FilmResponse])
def list_films(session: Session = Depends(get_db)) -> list[Film]:
    return get_programmed_films(session)


@router.get("/films/{id_film}", response_model=FilmDetailsResponse)
def film_details(id_film: int, session: Session = Depends(get_db)) -> FilmDetailsResponse:
    film = get_film_details(session, id_film, date.today())

    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    return film


@router.get("/films/{id_film}/seances", response_model=list[SeanceResponse])
def film_seances(id_film: int, date: date, session: Session = Depends(get_db)) -> list[SeanceResponse]:
    film = get_film_details(session, id_film, date)

    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    return film.seances


@router.get("/admin/films", response_model=list[FilmResponse], dependencies=[Depends(require_admin)])
def admin_list_films(session: Session = Depends(get_db)) -> list[Film]:
    return get_all_films(session)


@router.get("/admin/films/{id_film}", response_model=FilmDetailsResponse, dependencies=[Depends(require_admin)])
def admin_film_details(id_film: int, session: Session = Depends(get_db)) -> FilmDetailsResponse:
    film = get_film_details(session, id_film)

    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    return film


@router.post("/admin/films", response_model=FilmResponse, status_code=201, dependencies=[Depends(require_admin)])
def admin_create_film(film_data: FilmWrite, session: Session = Depends(get_db)) -> Film:
    return create_film(session, film_data)


@router.put("/admin/films/{id_film}", response_model=FilmResponse, dependencies=[Depends(require_admin)])
def admin_update_film(id_film: int, film_data: FilmWrite, session: Session = Depends(get_db)) -> Film:
    film = update_film(session, id_film, film_data)

    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    return film


@router.post("/admin/seances", response_model=SeanceResponse, status_code=201, dependencies=[Depends(require_admin)])
def admin_create_seance(seance_data: SeanceCreate, session: Session = Depends(get_db)) -> SeanceResponse:
    return create_seance(session, seance_data)


@router.put("/admin/seances/{id_seance}", response_model=SeanceResponse, dependencies=[Depends(require_admin)])
def admin_update_seance(
    id_seance: int,
    seance_data: SeanceUpdate,
    session: Session = Depends(get_db),
) -> SeanceResponse:
    return update_seance(session, id_seance, seance_data)


@router.delete("/admin/seances/{id_seance}", status_code=204, dependencies=[Depends(require_admin)])
def admin_delete_seance(id_seance: int, session: Session = Depends(get_db)) -> None:
    delete_seance(session, id_seance)


@router.get("/admin/salles", response_model=list[SalleResponse], dependencies=[Depends(require_admin)])
def admin_list_salles(session: Session = Depends(get_db)) -> list[Salle]:
    return get_all_salles(session)


