from fastapi.testclient import TestClient

from app.main import app


def test_create_reservation(mock_reservation_route):
    response = TestClient(app).post(
        "/reservations",
        json={"id_seance": 1, "nombre_places": 1},
    )

    assert response.status_code == 201
    assert response.json()[0]["reference"] == "RES-TEST"


def test_create_reservation_requires_authentication():
    response = TestClient(app).post(
        "/reservations",
        json={"id_seance": 1, "nombre_places": 1},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentification requise"


def test_list_reservations(mock_reservation_list_route):
    response = TestClient(app).get("/reservations")

    assert response.status_code == 200
    assert response.json()[0]["reference"] == "RES-TEST"
    assert response.json()[0]["titre_film"] == "Film test"
    assert response.json()[0]["date_heure_debut"] == "2027-01-01T20:30:00"
    assert response.json()[0]["nom_salle"] == "test"
    assert response.json()[0]["numero_salle"] == 666
