from fastapi.testclient import TestClient

from app.main import app


def test_list_films(mock_routes) -> None:
    response = TestClient(app).get("/films")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_film_details(mock_routes) -> None:
    response = TestClient(app).get("/films/1")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
