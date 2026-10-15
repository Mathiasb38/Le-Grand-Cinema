from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import get_current_user
from types import SimpleNamespace


def test_list_films(mock_film_routes) -> None:
    response = TestClient(app).get("/films")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_film_details(mock_film_routes) -> None:
    response = TestClient(app).get("/films/1")

    assert response.status_code == 200
    assert response.json()["seances"][0]["places_disponibles"] == 10


def test_film_seances(mock_film_routes) -> None:
    response = TestClient(app).get("/films/1/seances?date=2026-10-07")

    assert response.status_code == 200
    assert response.json()[0]["places_disponibles"] == 10


def test_admin_list_films(mock_admin_film_routes) -> None:
    response = TestClient(app).get("/admin/films")

    assert response.status_code == 200
    assert response.json()[0]["titre"] == "Film test"


def test_admin_create_film(mock_admin_film_routes) -> None:
    response = TestClient(app).post("/admin/films", json={
        "titre": "Film test",
        "duree_minutes": 120,
        "affiche_url": "https://example.com/film.jpg",
        "description": "Description du film test",
    })

    assert response.status_code == 201
    assert response.json()["id_film"] == 1
    assert response.json()["description"] == "Description du film test"


def test_admin_update_film(mock_admin_film_routes) -> None:
    response = TestClient(app).put("/admin/films/1", json={
        "titre": "Film modifié",
        "duree_minutes": 130,
        "affiche_url": "https://example.com/film-modifie.jpg",
        "description": "Nouvelle description",
    })

    assert response.status_code == 200
    assert response.json()["titre"] == "Film test"


def test_admin_create_seance(mock_admin_seance_route) -> None:
    response = TestClient(app).post("/admin/seances", json={
        "id_film": 1,
        "id_salle": 1,
        "date_heure_debut": "2027-01-01T20:00:00",
    })

    assert response.status_code == 201
    assert response.json()["id_seance"] == 1
    assert response.json()["nom_salle"] == "Salle principale"
    mock_admin_seance_route.assert_called_once()


def test_admin_create_seance_requires_admin(mock_admin_seance_route, monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).post("/admin/seances", json={
        "id_film": 1,
        "id_salle": 1,
        "date_heure_debut": "2027-01-01T20:00:00",
    })

    assert response.status_code == 403


def test_admin_list_salles(mock_admin_salles_route) -> None:
    response = TestClient(app).get("/admin/salles")

    assert response.status_code == 200
    assert response.json() == [{"id_salle": 1, "nom": "Salle principale", "numero": 1}]
    mock_admin_salles_route.assert_called_once()


def test_admin_list_salles_requires_admin(mock_admin_salles_route, monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).get("/admin/salles")

    assert response.status_code == 403


def test_admin_film_routes_require_admin(monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).get("/admin/films")

    assert response.status_code == 403


def test_admin_film_routes_require_authentication() -> None:
    response = TestClient(app).get("/admin/films")

    assert response.status_code == 401
