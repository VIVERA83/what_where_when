from typing import Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, field_validator, Field

GAME_STATUS = Literal["victory", "loss", "progress", "cancelled"]


class User(BaseModel):
    id: UUID
    tg_user_id: str
    email: Optional[str] = None
    user_name: Optional[str] = None
    game_sessions: Optional[list["GameSession"]] = None

    @field_validator("game_sessions", mode="before")
    def str_to_date(cls, v: Optional[list[dict]]) -> Optional[list[dict]]:
        if isinstance(v, list):
            if not all(v[0].values()):
                return None
        return v


class GameSession(BaseModel):
    id: Optional[UUID]
    game_status: Optional[GAME_STATUS]
    timeout: Optional[int]
    users: Optional[list["User"]] = None
    questions: Optional[list["Question"]] = None

    @field_validator("users", "questions", mode="before")
    def str_to_date(cls, v: Optional[list[dict]]) -> Optional[list[dict]]:
        if isinstance(v, list):
            if not all(v[0].values()):
                return None
        return v


class Question(BaseModel):
    id: Optional[UUID]
    question: Optional[str]
    answer: Optional[str]
    game_sessions: Optional[list["GameSession"]] = None

    @field_validator("game_sessions", mode="before")
    def str_to_date(cls, v: Optional[list[dict]]) -> Optional[list[dict]]:
        if isinstance(v, list):
            if not all(v[0].values()):
                return None
        return v


class UserAnswer(BaseModel):
    id: Optional[UUID]
    is_correct: Optional[bool]
    answer: Optional[str]
    game_session: Optional[UUID] = None
    question_id: Optional[UUID] = None
    user_id: Optional[UUID] = None

    @field_validator("game_session", mode="before")
    def str_to_date(cls, v: Optional[dict]) -> Optional[dict]:
        if isinstance(v, dict):
            if not all(v.values()):
                return None
        return v
