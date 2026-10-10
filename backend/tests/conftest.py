import os

from dotenv import load_dotenv
import pytest
from sqlalchemy.orm import Session

from app.database import get_engine

load_dotenv()
os.environ["DATABASE_URL"] = os.environ["DATABASE_URL_TEST"]


@pytest.fixture
def db_session():
    with get_engine().connect() as connection:
        transaction = connection.begin()

        try:
            with Session(
                bind=connection,
                join_transaction_mode="create_savepoint",
            ) as session:
                yield session
        finally:
            transaction.rollback()
