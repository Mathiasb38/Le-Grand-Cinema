import os
import pytest
from datetime import datetime, timedelta

from types import SimpleNamespace
from unittest.mock import Mock

from dotenv import load_dotenv

from sqlalchemy.orm import Session

from app.database import get_db, get_engine
from app.main import app
from app.models import Film, Salle, Seance


load_dotenv()
os.environ["DATABASE_URL"] = os.environ["DATABASE_URL_TEST"]

# Fixtures des routes
@pytest.fixture
def mock_routes(monkeypatch):
    film = SimpleNamespace(
        id_film=1,
        titre="Film test",
        duree_minutes=120,
        affiche_url="https://example.com/film.jpg",
    )
    seance = SimpleNamespace(
        id_seance=1,
        date_heure_debut=datetime.now() + timedelta(days=1),
        id_salle=1,
    )

    monkeypatch.setattr(
        "app.routes.films.get_programmed_films",
        Mock(return_value=[film]),
    )
    monkeypatch.setattr(
        "app.routes.films.get_film_details",
        Mock(return_value=(film, [seance])),
    )
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)


# Fixtures des services
@pytest.fixture
def db_session():
    with Session(get_engine()) as session:
        yield session


@pytest.fixture
def film_data(db_session):
    salle = Salle(numero=666, nom="test", capacite_max=10)
    past_film = Film(
        titre="Past",
        duree_minutes=120,
        affiche_url="https://xxx.com/past.jpg",
    )
    programmed_film = Film(
        titre="Futur",
        duree_minutes=120,
        affiche_url="https://xxx.com/futur.jpg",
    )
    db_session.add_all([salle, past_film, programmed_film])
    db_session.flush()

    now = datetime.now()
    past_session = Seance(
        date_heure_debut=now - timedelta(days=1),
        id_film=past_film.id_film,
        id_salle=salle.id_salle,
    )
    programmed_session = Seance(
        date_heure_debut=now + timedelta(days=1),
        id_film=programmed_film.id_film,
        id_salle=salle.id_salle,
    )
    db_session.add_all([past_session, programmed_session])

    return db_session, past_film, programmed_film, past_session, programmed_session


