from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM, UUID

from store.database import Base


class GameStatusEnum(Enum):
    victory = "victory"
    loss = "loss"
    progress = "progress"
    cancelled = "cancelled"


class UserModel(Base):
    __tablename__ = "users"

    user_name: Mapped[str] = mapped_column(init=False)
    game_sessions: Mapped[list["GameSessionModel"]] = relationship(
        "GameSessionModel",
        backref="user",
        cascade="all, delete",
        passive_deletes=True,
        init=False,
    )


class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        backref="game_session",
        cascade="all, delete",
        passive_deletes=True,
        init=False,
    )

    timeout: Mapped[int] = mapped_column(init=False)
    user_answers: list["UserAnswerModel"] = relationship(
        "UserAnswerModel",
        backref="game_session",
        cascade="all, delete",
        passive_deletes=True,
        init=False,
    )
    game_status: Mapped[ENUM] = mapped_column(ENUM(GameStatusEnum), init=False)

    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, init=False
    )


class QuestionModel(Base):
    __tablename__ = "questions"

    title: Mapped[str] = mapped_column(init=False)
    answer: Mapped[str] = mapped_column(init=False)


class UserAnswerModel(Base):
    __tablename__ = "user_answers"

    user_id: Mapped[str] = mapped_column(init=False)
    question_id: Mapped[str] = mapped_column(init=False)
    game_session_id: Mapped[str] = mapped_column(init=False)

    answer: Mapped[str] = mapped_column(init=False)
    is_correct: Mapped[bool] = mapped_column(init=False)
