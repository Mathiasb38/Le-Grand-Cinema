from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.database import get_db
from app.main import app
from app.services.auth_service import get_current_user


@pytest.fixture
def mock_film_routes(monkeypatch):
    seance = SimpleNamespace(
        id_seance=1,
        date_heure_debut=datetime.now() + timedelta(days=1),
        id_salle=1,
        nom_salle="Salle principale",
        numero_salle=1,
        places_disponibles=10,
    )
    film = SimpleNamespace(
        id_film=1,
        titre="Film test",
        duree_minutes=120,
        affiche_url="https://example.com/film.jpg",
        description="Description du film test",
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


@pytest.fixture
def mock_auth_route(monkeypatch):
    user = SimpleNamespace(
        id_utilisateur=1,
        email="client@example.com",
        role="client",
    )
    create_user = Mock(return_value=user)

    monkeypatch.setattr("app.routes.auth.create_user", create_user)
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return create_user


@pytest.fixture
def mock_login_route(monkeypatch):
    authenticate_user = Mock(return_value={
        "access_token": "token-test",
        "token_type": "bearer",
    })

    monkeypatch.setattr("app.routes.auth.authenticate_user", authenticate_user)
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return authenticate_user


@pytest.fixture
def mock_reservation_route(monkeypatch):
    user = SimpleNamespace(id_utilisateur=1, role="client")
    reservations = [
        SimpleNamespace(
            reference="RES-TEST",
            date_reservation=datetime.now(),
            id_seance=1,
            id_place=1,
        )
    ]
    create_reservation = Mock(return_value=reservations)

    monkeypatch.setattr(
        "app.routes.reservations.create_reservation",
        create_reservation,
    )
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: user,
    )
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return create_reservation


@pytest.fixture
def mock_reservation_list_route(monkeypatch):
    user = SimpleNamespace(id_utilisateur=1, role="client")
    reservations = [
        SimpleNamespace(
            reference="RES-TEST",
            titre_film="Film test",
            date_heure_debut=datetime(2027, 1, 1, 20, 30),
            nom_salle="test",
            numero_salle=666,
        )
    ]
    get_user_reservations = Mock(return_value=reservations)

    monkeypatch.setattr(
        "app.routes.reservations.get_user_reservations",
        get_user_reservations,
    )
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: user,
    )
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return get_user_reservations


@pytest.fixture
def mock_cancel_reservation_route(monkeypatch):
    user = SimpleNamespace(id_utilisateur=1, role="client")
    cancel_reservation = Mock()

    monkeypatch.setattr(
        "app.routes.reservations.cancel_reservation",
        cancel_reservation,
    )
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: user,
    )
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return cancel_reservation, user

@pytest.fixture
def mock_admin_film_routes(monkeypatch):
    user = SimpleNamespace(id_utilisateur=1, role="admin")
    film = SimpleNamespace(
        id_film=1,
        titre="Film test",
        duree_minutes=120,
        affiche_url="https://example.com/film.jpg",
        description="Description du film test",
    )
    get_all_films = Mock(return_value=[film])
    create_film = Mock(return_value=film)
    update_film = Mock(return_value=film)

    monkeypatch.setattr("app.routes.films.get_all_films", get_all_films)
    monkeypatch.setattr("app.routes.films.create_film", create_film)
    monkeypatch.setattr("app.routes.films.update_film", update_film)
    monkeypatch.setitem(app.dependency_overrides, get_current_user, lambda: user)
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return get_all_films, create_film, update_film


@pytest.fixture
def mock_admin_seance_route(monkeypatch):
    user = SimpleNamespace(id_utilisateur=1, role="admin")
    seance = SimpleNamespace(
        id_seance=1,
        date_heure_debut=datetime(2027, 1, 1, 20),
        id_salle=1,
        nom_salle="Salle principale",
        numero_salle=1,
        places_disponibles=100,
    )
    create_seance = Mock(return_value=seance)

    monkeypatch.setattr("app.routes.films.create_seance", create_seance)
    monkeypatch.setitem(app.dependency_overrides, get_current_user, lambda: user)
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return create_seance


@pytest.fixture
def mock_admin_salles_route(monkeypatch):
    salles = [
        SimpleNamespace(id_salle=1, nom="Salle principale", numero=1),
    ]
    get_all_salles = Mock(return_value=salles)

    monkeypatch.setattr("app.routes.films.get_all_salles", get_all_salles)
    monkeypatch.setitem(
        app.dependency_overrides,
        get_current_user,
        lambda: SimpleNamespace(id_utilisateur=1, role="admin"),
    )
    monkeypatch.setitem(app.dependency_overrides, get_db, lambda: None)

    return get_all_salles



