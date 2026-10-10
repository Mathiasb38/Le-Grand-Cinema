from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Utilisateur
from app.schemas import ReservationCreate, ReservationResponse
from app.services.auth_service import get_current_user
from app.services.reservation_service import create_reservation

router = APIRouter()


@router.post(
    "/reservations",
    response_model=list[ReservationResponse],
    status_code=201,
)
def reserve_places(
    reservation_data: ReservationCreate,
    current_user: Utilisateur = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[ReservationResponse]:
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Réservation réservée aux clients")

    return create_reservation(session, current_user, reservation_data)
