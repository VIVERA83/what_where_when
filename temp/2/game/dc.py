from dataclasses import dataclass
from typing import Literal

GAME_STATUS = Literal["victory", "loss", "progress", "cancelled"]


@dataclass
class Game:
    id: str
    users: set[str]
    timeout: int
    questions: list["Question"]
    user_answers: list["UserAnswer"]
    game_status: GAME_STATUS


@dataclass
class Question:
    id: str
    text: str
    answer: str


@dataclass
class UserAnswer:
    user_id: str
    question_id: str
    answer: str


@dataclass
class UserState:
    user_id: str
    position: str
    settings: dict
