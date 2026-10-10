from fastapi.testclient import TestClient

from app.main import app


def test_create_reservation(mock_reservation_route):
    response = TestClient(app).post(
        "/reservations",
        json={"id_seance": 1, "nombre_places": 1},
    )

    assert response.status_code == 201
    assert response.json()[0]["reference"] == "RES-TEST"
