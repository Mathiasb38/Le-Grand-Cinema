import bcrypt
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Utilisateur
from app.schemas import UtilisateurCreate, UtilisateurLogin,TokenResponse

bearer_scheme = HTTPBearer(auto_error=False)


def create_user(session: Session, user_data: UtilisateurCreate) -> Utilisateur | None:
    existing_user = session.scalar(
        select(Utilisateur).where(Utilisateur.email == user_data.email)
    )
    if existing_user is not None:
        return None

    user = Utilisateur(
        email=user_data.email,
        mot_de_passe_hash=bcrypt.hashpw(
            user_data.mot_de_passe.encode(), bcrypt.gensalt()
        ).decode(),
        role="client",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(
    session: Session,
    user_data: UtilisateurLogin,
    role: str,
) -> TokenResponse:
    user = session.scalar(
        select(Utilisateur).where(Utilisateur.email == user_data.email)
    )

    if (
        user is None
        or not bcrypt.checkpw(
            user_data.mot_de_passe.encode(), user.mot_de_passe_hash.encode()
        )
        or user.role != role
    ):
        raise HTTPException(
            status_code=401,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user),
        token_type="bearer",
    )


def create_access_token(user: Utilisateur) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")

    payload = {
        "sub": str(user.id_utilisateur),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: Session = Depends(get_db),
) -> Utilisateur:
    if credentials is None:
        raise _unauthorized("Authentification requise")

    payload = decode_access_token(credentials.credentials)

    if payload is None:
        raise _unauthorized("Token invalide ou expiré")

    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise _unauthorized("Token invalide ou expiré")

    user = session.get(Utilisateur, user_id)

    if user is None:
        raise _unauthorized("Utilisateur introuvable")

    return user


def decode_access_token(token: str) -> dict | None:
    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        return None

    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None




def require_admin(current_user: Utilisateur = Depends(get_current_user)) -> Utilisateur:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")

    return current_user


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )    
