from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from store.database.postgres.accessor import Base


class GameStatusEnum(Enum):
    victory = "victory"
    loss = "loss"
    progress = "progress"
    cancelled = "cancelled"


class Association(Base):
    __tablename__ = "association_table"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True, init=False
    )
    game_session_id: Mapped[int] = mapped_column(
        ForeignKey("game_sessions.id"), primary_key=True, init=False
    )


class UserModel(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, init=False)
    user_name: Mapped[str] = mapped_column(init=False)

    game_sessions: Mapped[list["GameSessionModel"]] = relationship(
        secondary=Association, back_populates="user", init=False
    )


class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    game_status: Mapped[ENUM] = mapped_column(ENUM(GameStatusEnum), init=False)
    timeout: Mapped[int] = mapped_column(init=False)

    users: Mapped[list["UserModel"]] = relationship(
        secondary=Association, back_populates="game_session", init=False
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
