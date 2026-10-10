import bcrypt
import jwt
import pytest
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.schemas import UtilisateurLogin
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user,
    decode_access_token,
    require_admin,
)


def test_create_user_hashes_password(db_session, user_data) -> None:
    user = create_user(db_session, user_data)

    assert user.email == user_data.email
    assert user.role == "client"
    assert bcrypt.checkpw(
        user_data.mot_de_passe.encode(),
        user.mot_de_passe_hash.encode(),
    )


def test_create_user_rejects_duplicate_email(db_session, user_data) -> None:
    create_user(db_session, user_data)

    assert create_user(db_session, user_data) is None


def test_authenticate_user(db_session, user_data, monkeypatch) -> None:
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-characters-long-key")
    create_user(db_session, user_data)

    token = authenticate_user(
        db_session,
        UtilisateurLogin(
            email=user_data.email,
            mot_de_passe=user_data.mot_de_passe,
        ),
        "client",
    )

    assert token.token_type == "bearer"


def test_authenticate_user_rejects_invalid_password(db_session, user_data) -> None:
    create_user(db_session, user_data)

    with pytest.raises(HTTPException) as error:
        authenticate_user(
            db_session,
            UtilisateurLogin(email=user_data.email, mot_de_passe="wrong-password"),
            "client",
        )

    assert error.value.status_code == 401


def test_create_access_token(monkeypatch, db_session, user_data) -> None:
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-32-characters-long-key")
    user = create_user(db_session, user_data)

    token = create_access_token(user)
    payload = jwt.decode(
        token,
        "test-secret-32-characters-long-key",
        algorithms=["HS256"],
    )

    assert payload["sub"] == str(user.id_utilisateur)
    assert "exp" in payload


def test_decode_access_token_rejects_expired_token(monkeypatch) -> None:
    secret_key = "test-secret-32-characters-long-key"
    monkeypatch.setenv("JWT_SECRET_KEY", secret_key)
    token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        secret_key,
        algorithm="HS256",
    )

    assert decode_access_token(token) is None


def test_require_admin() -> None:
    admin = SimpleNamespace(role="admin")
    client = SimpleNamespace(role="client")

    assert require_admin(admin) is admin

    with pytest.raises(HTTPException) as error:
        require_admin(client)

    assert error.value.status_code == 403
