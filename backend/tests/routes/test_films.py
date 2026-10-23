from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import get_current_user
from types import SimpleNamespace
from unittest.mock import Mock


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


def test_seance_places(mock_seance_places_route) -> None:
    response = TestClient(app).get("/seances/1/places")

    assert response.status_code == 200
    assert response.json() == [
        {"id_place": 1, "rangee": "A", "numero": 1, "disponible": True},
        {"id_place": 2, "rangee": "A", "numero": 2, "disponible": False},
    ]
    mock_seance_places_route.assert_called_once_with(None, 1)


def test_seance_places_allows_admin(mock_seance_places_route, monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="admin"),
    )

    response = TestClient(app).get("/seances/1/places")

    assert response.status_code == 200
    mock_seance_places_route.assert_called_once_with(None, 1)


def test_admin_list_films(mock_admin_film_routes) -> None:
    response = TestClient(app).get("/admin/films")

    assert response.status_code == 200
    assert response.json()[0]["titre"] == "Film test"


def test_admin_film_details(mock_film_routes, monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="admin"),
    )
    response = TestClient(app).get("/admin/films/1")

    assert response.status_code == 200
    assert response.json()["seances"][0]["places_disponibles"] == 10


def test_admin_seance_taux_datetime(monkeypatch, mock_admin_route) -> None:
    seances = [SimpleNamespace(
        id_film=2,
        titre_film="Film test",
        id_seance=1,
        date_heure_debut="2026-10-19T20:00:00",
        id_salle=3,
        nom_salle="Salle principale",
        numero_salle=1,
        taux_remplissage=30,
    )]
    get_taux = Mock(return_value=seances)
    monkeypatch.setattr("app.routes.films.get_seance_taux", get_taux)

    response = TestClient(app).get(
        "/admin/remplissage?date_debut=2026-10-19T12:30:00&date_fin=2026-10-20T14:45:00&id_film=2&id_salle=3"
    )

    assert response.status_code == 200
    assert response.json()[0]["taux_remplissage"] == 30
    assert response.json()[0]["id_film"] == 2
    assert response.json()[0]["titre_film"] == "Film test"
    assert response.json()[0]["id_salle"] == 3
    assert get_taux.call_args.args[0] is None
    assert get_taux.call_args.args[1].isoformat() == "2026-10-19T12:30:00"
    assert get_taux.call_args.args[2].isoformat() == "2026-10-20T14:45:00"
    assert get_taux.call_args.args[3:] == (2, 3)


def test_admin_seance_taux_requires_filter(mock_admin_route) -> None:
    response = TestClient(app).get("/admin/remplissage")

    assert response.status_code == 422


def test_admin_seance_taux_requires_both_dates(mock_admin_route) -> None:
    response = TestClient(app).get(
        "/admin/remplissage?date_debut=2026-10-19T12:30:00&id_film=2"
    )

    assert response.status_code == 422


def test_admin_seance_taux_requires_admin(monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )

    response = TestClient(app).get(
        "/admin/remplissage?date_debut=2026-10-19T12:30:00&date_fin=2026-10-20T14:45:00"
    )

    assert response.status_code == 403

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


def test_admin_update_seance(mock_admin_update_seance_route) -> None:
    response = TestClient(app).put("/admin/seances/1", json={
        "id_salle": 2,
        "date_heure_debut": "2027-01-02T20:00:00",
    })

    assert response.status_code == 200
    assert response.json()["id_seance"] == 1
    assert response.json()["id_salle"] == 2
    mock_admin_update_seance_route.assert_called_once()
    assert mock_admin_update_seance_route.call_args.args[1] == 1
    assert mock_admin_update_seance_route.call_args.args[2].id_salle == 2


def test_admin_update_seance_requires_admin(mock_admin_update_seance_route, monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).put("/admin/seances/1", json={
        "id_salle": 2,
        "date_heure_debut": "2027-01-02T20:00:00",
    })

    assert response.status_code == 403


def test_admin_delete_seance(mock_admin_delete_seance_route) -> None:
    response = TestClient(app).delete("/admin/seances/1")

    assert response.status_code == 204
    assert response.content == b""
    mock_admin_delete_seance_route.assert_called_once()
    assert mock_admin_delete_seance_route.call_args.args[1] == 1


def test_admin_delete_seance_requires_admin(mock_admin_delete_seance_route, monkeypatch) -> None:
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(role="client"),
    )
    response = TestClient(app).delete("/admin/seances/1")

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
