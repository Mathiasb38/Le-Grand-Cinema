from fastapi.testclient import TestClient

from app.main import app


def test_register_user(mock_auth_route) -> None:
    response = TestClient(app).post(
        "/auth/register",
        json={
            "email": "client@example.com",
            "mot_de_passe": "motdepasse123",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id_utilisateur": 1,
        "email": "client@example.com",
        "role": "client",
    }


def test_short_password(mock_auth_route) -> None:
    response = TestClient(app).post(
        "/auth/register",
        json={
            "email": "client@example.com",
            "mot_de_passe": "short",
        },
    )

    assert response.status_code == 422


def test_duplicate_email(mock_auth_route) -> None:
    mock_auth_route.return_value = None

    response = TestClient(app).post(
        "/auth/register",
        json={
            "email": "client@example.com",
            "mot_de_passe": "motdepasse123",
        },
    )

    assert response.status_code == 409
