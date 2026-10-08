from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Film
from app.schemas import FilmDetailsResponse, FilmResponse, SeanceResponse
from app.services.film_service import get_film_details, get_programmed_films

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
