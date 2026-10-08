from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FilmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_film: int
    titre: str
    duree_minutes: int
    affiche_url: str


class SeanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_seance: int
    date_heure_debut: datetime
    id_salle: int
    places_disponibles: int


class FilmDetailsResponse(FilmResponse):
    seances: list[SeanceResponse]
