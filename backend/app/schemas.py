from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field



class FilmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_film: int
    titre: str
    duree_minutes: int
    affiche_url: str
    description: str


class FilmWrite(BaseModel):
    titre: str = Field(min_length=1, max_length=50)
    duree_minutes: int = Field(gt=0, le=32767)
    affiche_url: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1)


class SeanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_seance: int
    date_heure_debut: datetime
    id_salle: int
    nom_salle: str
    numero_salle: int
    places_disponibles: int


class SeanceCreate(BaseModel):
    id_film: int
    id_salle: int
    date_heure_debut: datetime


class SeanceUpdate(BaseModel):
    id_salle: int
    date_heure_debut: datetime


class SalleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_salle: int
    nom: str
    numero: int


class FilmDetailsResponse(FilmResponse):
    seances: list[SeanceResponse]


class UtilisateurCreate(BaseModel):
    email: EmailStr
    mot_de_passe: str = Field(min_length=12)


class UtilisateurLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str


class UtilisateurResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_utilisateur: int
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class ReservationCreate(BaseModel):
    id_seance: int
    nombre_places: int = Field(gt=0)


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reference: str
    date_reservation: datetime
    id_seance: int
    id_place: int


class ReservationDetailsResponse(BaseModel):
    reference: str
    titre_film: str
    date_heure_debut: datetime
    nom_salle: str
    numero_salle: int


class ReservationAdminResponse(BaseModel):
    reference: str
    email: EmailStr
    titre_film: str
    date_heure_debut: datetime
    nom_salle: str
    numero_salle: int
    is_paid: bool
    is_cancelled: bool
