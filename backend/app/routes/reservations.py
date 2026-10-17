from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Utilisateur
from app.schemas import (
    ReservationCreate,
    ReservationResponse,
    ReservationDetailsResponse,
    ReservationAdminResponse,
)
from app.services.auth_service import get_current_user, require_admin
from app.services.reservation_service import (
    create_reservation,
    get_user_reservations,
    cancel_reservation,
    search_reservations,
)

router = APIRouter()


@router.get(
    "/admin/recherche",
    response_model=list[ReservationAdminResponse],
    dependencies=[Depends(require_admin)],
)
def admin_search(
    search: str,
    session: Session = Depends(get_db),
) -> list[ReservationAdminResponse]:
    return search_reservations(session, search)


@router.get("/reservations", response_model=list[ReservationDetailsResponse])
def list_reservations(
    current_user: Utilisateur = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[ReservationDetailsResponse]:
    if current_user.role != "client":
        raise HTTPException(
            status_code=403, detail="Réservations réservées aux clients"
        )

    return get_user_reservations(session, current_user)


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


@router.delete("/reservations/{reference}", status_code=204)
def cancel_user_reservation(
    reference: str,
    current_user: Utilisateur = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> None:
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Annulation réservée aux clients")

    cancel_reservation(session, current_user, reference)
