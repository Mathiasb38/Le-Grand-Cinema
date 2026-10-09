from uuid import uuid4

import pytest

from app.schemas import UtilisateurCreate


@pytest.fixture
def user_data():
    return UtilisateurCreate(
        email=f"auth-{uuid4()}@example.com",
        mot_de_passe="motdepasse123",
    )
