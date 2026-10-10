import bcrypt
import os
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Utilisateur
from app.schemas import UtilisateurCreate, UtilisateurLogin


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
    session: Session, user_data: UtilisateurLogin
) -> Utilisateur | None:
    user = session.scalar(
        select(Utilisateur).where(Utilisateur.email == user_data.email)
    )

    if user is None or not bcrypt.checkpw(
        user_data.mot_de_passe.encode(), user.mot_de_passe_hash.encode()
    ):
        return None

    return user


def create_access_token(user: Utilisateur) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")

    payload = {
        "sub": str(user.id_utilisateur),
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")
