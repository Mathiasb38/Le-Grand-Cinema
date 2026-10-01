import os
from collections.abc import Generator
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


load_dotenv()


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL n'est pas configurée.")

    return create_engine(database_url)


def get_db() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session
