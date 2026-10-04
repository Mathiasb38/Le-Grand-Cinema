from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
    Index,
    text
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Utilisateur(Base):

    __tablename__ = "UTILISATEUR"

    id_utilisateur: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20))


class Salle(Base):

    __tablename__ = "SALLE"

    id_salle: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[int] = mapped_column(SmallInteger, unique=True)
    nom: Mapped[str | None] = mapped_column(String(50))
    capacite_max: Mapped[int] = mapped_column(SmallInteger)


class Film(Base):

    __tablename__ = "FILM"

    id_film: Mapped[int] = mapped_column(Integer, primary_key=True)
    titre: Mapped[str] = mapped_column(String(50))
    duree_minutes: Mapped[int] = mapped_column(SmallInteger)
    affiche_url: Mapped[str] = mapped_column(String(500))

class Seance(Base):

    __tablename__ = "SEANCE"

    id_seance: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_heure_debut: Mapped[datetime] = mapped_column(DateTime)
    id_film: Mapped[int] = mapped_column(ForeignKey("FILM.id_film"))
    id_salle: Mapped[int] = mapped_column(ForeignKey("SALLE.id_salle"))


class Place(Base):

    __tablename__ = "PLACE"
    __table_args__ = (UniqueConstraint("id_salle", "rangee", "numero"),)

    id_place: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_salle: Mapped[int] = mapped_column(ForeignKey("SALLE.id_salle"))
    rangee: Mapped[str] = mapped_column(String(2))
    numero: Mapped[int] = mapped_column(SmallInteger)


class Reservation(Base):

    __tablename__ = "RESERVATION"

    __table_args__ = (
        Index(
            "uq_reservation_seance_place_active",
            "id_seance",
            "id_place",
            unique=True,
            postgresql_where=text("is_cancelled = false"),
        ),
    )

    id_reservation: Mapped[int] = mapped_column(Integer, primary_key=True)
    reference: Mapped[str] = mapped_column(String(50), unique=True)
    date_reservation: Mapped[datetime] = mapped_column(DateTime)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    id_seance: Mapped[int] = mapped_column(ForeignKey("SEANCE.id_seance"))
    id_utilisateur: Mapped[int] = mapped_column(ForeignKey("UTILISATEUR.id_utilisateur"))
    id_place: Mapped[int] = mapped_column(ForeignKey("PLACE.id_place"))


class Billet(Base):
    
    __tablename__ = "BILLET"
    __table_args__ = (UniqueConstraint("id_seance", "id_place"),)

    id_billet: Mapped[int] = mapped_column(Integer, primary_key=True)
    code_billet: Mapped[str] = mapped_column(String(255), unique=True)
    date_emission: Mapped[datetime] = mapped_column(DateTime)
    id_place: Mapped[int] = mapped_column(ForeignKey("PLACE.id_place"))
    id_seance: Mapped[int] = mapped_column(ForeignKey("SEANCE.id_seance"))
