from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field



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


class UtilisateurCreate(BaseModel):
    email: EmailStr
    mot_de_passe: str = Field(min_length=12)


class UtilisateurResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_utilisateur: int
    email: EmailStr
    role: str