from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.database import get_db
from app.main import app


@pytest.fixture
def mock_routes(monkeypatch):
    seance = SimpleNamespace(
        id_seance=1,
        date_heure_debut=datetime.now() + timedelta(days=1),
        id_salle=1,
        places_disponibles=10,
    )
    film = SimpleNamespace(
        id_film=1,
        titre="Film test",
        duree_minutes=120,
        affiche_url="https://example.com/film.jpg",
        seances=[seance],
    )

    monkeypatch.setattr(
        "app.routes.films.get_programmed_films",
        Mock(return_value=[film]),
    )
    monkeypatch.setattr(
        "app.routes.films.get_film_details",
        Mock(return_value=film),
    )
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

