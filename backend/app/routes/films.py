from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Film
from app.schemas import FilmDetailsResponse, FilmResponse, SeanceResponse, FilmWrite
from app.services.film_service import (
    get_film_details,
    get_programmed_films,
    get_all_films,
    create_film,
    update_film,
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


@router.post("/admin/films", response_model=FilmResponse, status_code=201, dependencies=[Depends(require_admin)])
def admin_create_film(film_data: FilmWrite, session: Session = Depends(get_db)) -> Film:
    return create_film(session, film_data)


@router.put("/admin/films/{id_film}", response_model=FilmResponse, dependencies=[Depends(require_admin)])
def admin_update_film(id_film: int, film_data: FilmWrite, session: Session = Depends(get_db)) -> Film:
    film = update_film(session, id_film, film_data)

    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    return film


