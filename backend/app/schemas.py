from pydantic import BaseModel, ConfigDict


class FilmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_film: int
    titre: str
    duree_minutes: int
    affiche_url: str
