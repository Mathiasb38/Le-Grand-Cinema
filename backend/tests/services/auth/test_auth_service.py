import bcrypt

from app.services.auth_service import create_user


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
