import app.models

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, get_engine
from app.routes.films import router as films_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    Base.metadata.create_all(bind=get_engine())
    yield

app = FastAPI(
    title="Le-Grand-Cinema API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://le-grand-cinema-frontend.onrender.com"

    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(films_router)
