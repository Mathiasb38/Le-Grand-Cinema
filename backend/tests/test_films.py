from fastapi.testclient import TestClient

from app.main import app


def test_list_programmed_films() -> None:
    response = TestClient(app).get("/films")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(
        {"id_film", "titre", "duree_minutes", "affiche_url"}.issubset(film)
        for film in response.json()
    )
