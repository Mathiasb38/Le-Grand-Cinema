import bcrypt
import jwt

from app.schemas import UtilisateurLogin
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user,
)


def test_create_user_hashes_password(db_session, user_data) -> None:
    user = create_user(db_session, user_data)

    try:
        assert user.email == user_data.email
        assert user.role == "client"
        assert bcrypt.checkpw(
            user_data.mot_de_passe.encode(),
            user.mot_de_passe_hash.encode(),
        )
    finally:
        db_session.delete(user)
        db_session.commit()


def test_create_user_rejects_duplicate_email(db_session, user_data) -> None:
    user = create_user(db_session, user_data)

    try:
        duplicate_user = create_user(db_session, user_data)

        assert duplicate_user is None
    finally:
        db_session.delete(user)
        db_session.commit()


def test_authenticate_user(db_session, user_data) -> None:
    user = create_user(db_session, user_data)

    try:
        authenticated_user = authenticate_user(
            db_session,
            UtilisateurLogin(
                email=user_data.email,
                mot_de_passe=user_data.mot_de_passe,
            ),
        )

        assert authenticated_user.id_utilisateur == user.id_utilisateur
    finally:
        db_session.delete(user)
        db_session.commit()


def test_authenticate_user_rejects_invalid_password(db_session, user_data) -> None:
    user = create_user(db_session, user_data)

    try:
        authenticated_user = authenticate_user(
            db_session,
            UtilisateurLogin(email=user_data.email, mot_de_passe="wrong-password"),
        )

        assert authenticated_user is None
    finally:
        db_session.delete(user)
        db_session.commit()


def test_create_access_token(monkeypatch, db_session, user_data) -> None:
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-characters-long-key")
    user = create_user(db_session, user_data)

    try:
        token = create_access_token(user)
        payload = jwt.decode(
            token,
            "test-secret-32-characters-long-key",
            algorithms=["HS256"],
        )

        assert payload["sub"] == str(user.id_utilisateur)
        assert payload["email"] == user.email
        assert payload["role"] == "client"
    finally:
        db_session.delete(user)
        db_session.commit()
