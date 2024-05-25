from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, Table, Column, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from store.database.postgres.accessor import Base


class GameStatusEnum(Enum):
    victory = "victory"
    loss = "loss"
    progress = "progress"
    cancelled = "cancelled"


game_status_enum = ENUM("victory", "loss", "progress", "cancelled", name="gamestatusenum", metadata=Base.metadata)

association_table = Table(
    "user_game_session_association",
    Base.metadata,
    Column("user_tg_user_id", String, ForeignKey("users.tg_user_id"), primary_key=True),
    Column("game_session_id", ForeignKey("game_sessions.id"), primary_key=True),
)


class UserModel(Base):
    __tablename__ = "users"

    tg_user_id: Mapped[str] = mapped_column(init=False, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(unique=True, init=False, nullable=True)
    user_name: Mapped[str] = mapped_column(init=False, nullable=True)
    game_sessions: Mapped[List["GameSessionModel"]] = relationship(
        "GameSessionModel",
        secondary=association_table,
        back_populates="users",
        init=False
    )


class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    game_status: Mapped[ENUM] = mapped_column(game_status_enum, init=False)
    timeout: Mapped[int] = mapped_column(init=False)

    users: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary=association_table,
        back_populates="game_sessions",
        init=False
    )

