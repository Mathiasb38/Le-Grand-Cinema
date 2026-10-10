from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UtilisateurCreate, UtilisateurResponse, TokenResponse, UtilisateurLogin
from app.services.auth_service import create_user,authenticate_user, create_access_token

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UtilisateurResponse, status_code=201)
def register(
    user_data: UtilisateurCreate,
    session: Session = Depends(get_db),
) -> UtilisateurResponse:
    user = create_user(session, user_data)

    if user is None:
        raise HTTPException(status_code=409, detail="Cet e-mail est déjà utilisé")

    return user


@router.post("/login", response_model=TokenResponse)
def login(
    user_data: UtilisateurLogin,
    session: Session = Depends(get_db),
) -> TokenResponse:
    user = authenticate_user(session, user_data)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user),
        token_type="bearer",
    )
