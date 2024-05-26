from enum import Enum
from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey, Table, Column, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from store.database.postgres.accessor import Base


class GameStatusEnum(Enum):
    victory = "victory"
    loss = "loss"
    progress = "progress"
    cancelled = "cancelled"


game_status_enum = ENUM(
    "victory",
    "loss",
    "progress",
    "cancelled",
    name="gamestatusenum",
    metadata=Base.metadata,
)

user_game_session_association = Table(
    "user_game_session_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("game_session_id", ForeignKey("game_sessions.id"), primary_key=True),
)

question_game_session_association = Table(
    "question_game_session_association",
    Base.metadata,
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
    Column("game_session_id", ForeignKey("game_sessions.id"), primary_key=True),
)


class UserModel(Base):
    __tablename__ = "users"

    tg_user_id: Mapped[str] = mapped_column(init=False, unique=True)
    email: Mapped[str] = mapped_column(init=False, nullable=True)
    user_name: Mapped[str] = mapped_column(init=False, nullable=True)
    game_sessions: Mapped[List["GameSessionModel"]] = relationship(
        "GameSessionModel",
        secondary=user_game_session_association,
        back_populates="users",
        init=False,
    )


class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    game_status: Mapped[ENUM] = mapped_column(game_status_enum, init=False)
    timeout: Mapped[int] = mapped_column(init=False)

    users: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        secondary=user_game_session_association,
        back_populates="game_sessions",
        init=False,
    )
    questions: Mapped[List["QuestionModel"]] = relationship(
        "QuestionModel",
        secondary=question_game_session_association,
        back_populates="game_session",
        init=False,
    )
    user_answers: Mapped[List["UserAnswerModel"]] = relationship(
        "UserAnswerModel",
        back_populates="game_session",
        init=False,
    )


class QuestionModel(Base):
    __tablename__ = "questions"

    question: Mapped[str] = mapped_column(init=False)
    answer: Mapped[str] = mapped_column(init=False)

    game_sessions: Mapped[List["GameSessionModel"]] = relationship(
        "GameSessionModel",
        secondary=question_game_session_association,
        back_populates="questions",
        init=False,
    )


class UserAnswerModel(Base):
    __tablename__ = "user_answers"

    answer: Mapped[str] = mapped_column(init=False)

    is_correct: Mapped[bool] = mapped_column(init=False)

    game_session: Mapped[UUID] = mapped_column(
        ForeignKey("game_sessions.id"), init=False
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), init=False)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"), init=False)
