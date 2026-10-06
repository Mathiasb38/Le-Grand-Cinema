from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Film
from app.schemas import FilmDetailsResponse, FilmResponse
from app.services.film_service import get_film_details, get_programmed_films


router = APIRouter()


@router.get("/films", response_model=list[FilmResponse])
def list_films(session: Session = Depends(get_db)) -> list[Film]:
    return get_programmed_films(session)


@router.get("/films/{id_film}", response_model=FilmDetailsResponse)
def film_details(id_film: int, session: Session = Depends(get_db)) -> dict:
    film, seances = get_film_details(session, id_film)

    if film is None:
        raise HTTPException(status_code=404, detail="Film introuvable")

    return {
        "id_film": film.id_film,
        "titre": film.titre,
        "duree_minutes": film.duree_minutes,
        "affiche_url": film.affiche_url,
        "seances": seances,
    }
