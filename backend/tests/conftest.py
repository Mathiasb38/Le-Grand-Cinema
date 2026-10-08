import os

from dotenv import load_dotenv
import pytest
from sqlalchemy.orm import Session

from app.database import get_engine

load_dotenv()
os.environ["DATABASE_URL"] = os.environ["DATABASE_URL_TEST"]


@pytest.fixture
def db_session():
    with Session(get_engine()) as session:
        yield session
