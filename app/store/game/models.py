from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, Table, Column, String, text, UUID
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship, registry

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


# class Child(Base):
#     __tablename__ = "right_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     parents: Mapped[List[Parent]] = relationship(
#         secondary=association_table, back_populates="children"
#     )


"""


# class GameStatusEnum(Enum):
#     victory = "victory"
#     loss = "loss"
#     progress = "progress"
#     cancelled = "cancelled"
GameStatusEnum = ENUM("victory", "loss", "progress", "cancelled", name="gamestatusenum", metadata=Base.metadata)

association_table = Table(
    "association_table",
    Base.metadata,
    Column("id", UUID, primary_key=True, server_default=text("gen_random_uuid()"), nullable=True),
    Column("tg_user_id", String, ForeignKey("users.tg_user_id"), primary_key=True),
    Column("game_session_id", ForeignKey("game_sessions.id"), primary_key=True),
)


# class Association(Base):
#     __tablename__ = "association_table"
#
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"), primary_key=True, init=False
#     )
#     game_session_id: Mapped[int] = mapped_column(
#         ForeignKey("game_sessions.id"), primary_key=True, init=False
#     )


class UserModel(Base):
    __tablename__ = "users"

    tg_user_id: Mapped[str] = mapped_column(init=False, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(unique=True, init=False, nullable=True)
    user_name: Mapped[str] = mapped_column(init=False, nullable=True)
    game_sessions: Mapped[List["GameSessionModel"]] = relationship(
        secondary=association_table, back_populates="users", init=False, lazy="subquery"
    )


class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    game_status: Mapped[ENUM] = mapped_column(GameStatusEnum, init=False)
    timeout: Mapped[int] = mapped_column(init=False)

    users: Mapped[List["UserModel"]] = relationship(
        secondary=association_table, back_populates="game_sessions", init=False
    )

# class UserModel(Base):
#     __tablename__ = "users"
#
#     user_name: Mapped[str] = mapped_column(init=False)
#     game_sessions: Mapped[list["GameSessionModel"]] = relationship(
#         "GameSessionModel",
#         backref="user",
#         cascade="all, delete",
#         passive_deletes=True,
#         init=False,
#     )


#
# class UserModel(Base):
#     __tablename__ = "users"
#
#     user_name: Mapped[str] = mapped_column(init=False)
#     game_sessions: Mapped[list["GameSessionModel"]] = relationship(
#         "GameSessionModel",
#         backref="user",
#         cascade="all, delete",
#         passive_deletes=True,
#         init=False,
#     )
#
#
# class GameSessionModel(Base):
#     __tablename__ = "game_sessions"
#
#     users: Mapped[list["UserModel"]] = relationship(
#         "UserModel",
#         backref="game_session",
#         cascade="all, delete",
#         passive_deletes=True,
#         init=False,
#     )
#
#     timeout: Mapped[int] = mapped_column(init=False)
#     user_answers: list["UserAnswerModel"] = relationship(
#         "UserAnswerModel",
#         backref="game_session",
#         cascade="all, delete",
#         passive_deletes=True,
#         init=False,
#     )
#     game_status: Mapped[ENUM] = mapped_column(ENUM(GameStatusEnum), init=False)
#
#     user_id: Mapped[UUID] = mapped_column(
#         UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, init=False
#     )
#
#
# class QuestionModel(Base):
#     __tablename__ = "questions"
#
#     title: Mapped[str] = mapped_column(init=False)
#     answer: Mapped[str] = mapped_column(init=False)
#
#
# class UserAnswerModel(Base):
#     __tablename__ = "user_answers"
#
#     user_id: Mapped[UUID] = mapped_column(
#         UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, init=False
#     )
#     question_id: Mapped[UUID] = mapped_column(
#         UUID, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, init=False
#     )
#     game_session_id: Mapped[UUID] = mapped_column(
#         UUID,
#         ForeignKey("game_sessions.id", ondelete="CASCADE"),
#         nullable=False,
#         init=False,
#     )
#
#     answer: Mapped[str] = mapped_column(init=False)
#     is_correct: Mapped[bool] = mapped_column(init=False)
"""
