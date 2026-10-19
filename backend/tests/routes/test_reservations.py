from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import get_current_user
from types import SimpleNamespace


def test_create_reservation(mock_reservation_route):
    create_reservation = mock_reservation_route
    response = TestClient(app).post(
        "/reservations",
        json={"id_seance": 1, "id_places": [1]},
    )

    assert response.status_code == 201
    assert response.json()[0]["reference"] == "RES-TEST"
    assert create_reservation.call_args.args[2].id_places == [1]


def test_create_reservation_requires_authentication():
    response = TestClient(app).post(
        "/reservations",
        json={"id_seance": 1, "id_places": [1]},
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


def test_list_billets(mock_billet_list_route):
    response = TestClient(app).get("/billets")

    assert response.status_code == 200
    assert response.json()[0]["code_billet"] == "BIL-TEST"
    assert response.json()[0]["titre_film"] == "Film test"
    assert response.json()[0]["nom_salle"] == "Salle principale"
    assert response.json()[0]["numero_salle"] == 1
    mock_billet_list_route.assert_called_once()


def test_list_billets_requires_authentication():
    response = TestClient(app).get("/billets")

    assert response.status_code == 401

def test_admin_reservation_search_by_reference(mock_admin_reservation_route):
    response = TestClient(app).get("/admin/recherche?search=RES-TEST")

    assert response.status_code == 200
    assert response.json()[0]["reference"] == "RES-TEST"
    assert response.json()[0]["email"] == "client@example.com"
    assert response.json()[0]["nom_salle"] == "Salle principale"
    assert response.json()[0]["numero_salle"] == 1
    mock_admin_reservation_route.assert_called_once_with(None, "RES-TEST")


def test_admin_reservation_search_by_email(mock_admin_reservation_route):
    response = TestClient(app).get("/admin/recherche?search=client%40example.com")

    assert response.status_code == 200
    assert response.json()[0]["email"] == "client@example.com"


def test_admin_reservation_search_requires_admin(mock_admin_reservation_route, monkeypatch):
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).get("/admin/recherche?search=RES-TEST")

    assert response.status_code == 403


def test_admin_validate_payment(mock_validate_payment_route):
    response = TestClient(app).put(
        "/admin/reservations/RES-TEST/paiement"
    )

    assert response.status_code == 204
    mock_validate_payment_route.assert_called_once_with(None, "RES-TEST")


def test_admin_validate_payment_requires_admin(mock_validate_payment_route, monkeypatch):
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).put(
        "/admin/reservations/RES-TEST/paiement"
    )

    assert response.status_code == 403


def test_cancel_reservation(mock_cancel_reservation_route):
    cancel_reservation, _ = mock_cancel_reservation_route
    response = TestClient(app).delete("/reservations/RES-TEST")

    assert response.status_code == 204
    cancel_reservation.assert_called_once()

def test_cancel_reservation_requires_authentication():
    response = TestClient(app).delete("/reservations/RES-TEST")

    assert response.status_code == 401
