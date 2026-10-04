from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Film
from app.schemas import FilmResponse
from app.services.film_service import get_programmed_films


router = APIRouter()


@router.get("/films", response_model=list[FilmResponse])
def list_films(session: Session = Depends(get_db)) -> list[Film]:
    return get_programmed_films(session)
