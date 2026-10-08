import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Utilisateur
from app.schemas import UtilisateurCreate


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
