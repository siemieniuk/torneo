from datetime import datetime
from typing import List

from core.database import Base
from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

user_discipline_association_table = Table(
    "user_disciplines",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("discipline_id", ForeignKey("disciplines.id"), primary_key=True),
)

tournament_assignment = Table(
    "tournament_assignments",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tournament_id", ForeignKey("tournaments.id"), primary_key=True),
    Column("ranking", Integer, nullable=False),
    Column("licence_number", String(16), nullable=False),
)


class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    users: Mapped[List["User"]] = relationship(
        secondary="user_disciplines",
        back_populates="favourite_disciplines",
    )
    tournaments: Mapped[List["Tournament"]] = relationship(back_populates="discipline")


# TODO: Constraint TournamentAssignments
class Result(Base):
    __tablename__ = "results"

    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournaments.id"), primary_key=True
    )
    match_id: Mapped[int] = mapped_column(primary_key=True)
    selected_winner_1: Mapped[int | None] = mapped_column(Integer)
    selected_winner_2: Mapped[int | None] = mapped_column(Integer)


# TODO: location - geometry
class Tournament(Base):
    __tablename__ = "tournaments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    time_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    time_finish: Mapped[datetime] = mapped_column(DateTime)
    max_number_of_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    players: Mapped[List["User"]] = relationship(
        secondary="tournament_assignments", back_populates="tournaments"
    )
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    discipline: Mapped["Discipline"] = relationship(back_populates="tournaments")
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organizer: Mapped["User"] = relationship(back_populates="organized_tournaments")


class Sponsor(Base):
    __tablename__ = "sponsors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    img_path: Mapped[str | None] = mapped_column(String(256))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    organized_tournaments: Mapped[List["Tournament"]] = relationship(
        back_populates="organizer"
    )
    favourite_disciplines: Mapped[List["Discipline"]] = relationship(
        secondary="user_disciplines",
        back_populates="users",
    )
    tournaments: Mapped[List["Tournament"]] = relationship(
        secondary="tournament_assignments",
        back_populates="players",
    )
