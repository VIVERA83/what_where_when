import json
from dataclasses import dataclass, asdict
from typing import Literal, Optional

GAME_STATUS = Literal["victory", "loss", "progress", "cancelled"]


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
    id: str
    tg_user_id: str
    position: str
    settings: "GameSettings"
    current_question: Optional[str] = None
    game_session_id: Optional[str] = None
    correct_answer: str = None
    user_answer: str = None
    score: int = 0

    def to_string(self):
        return json.dumps(asdict(self))

    def to_bytes(self):
        return bytes(self.to_string(), "utf-8")

    def to_dict(self):
        return asdict(self)

@dataclass
class GameSettings:
    quantity_players: int = 1
    quantity_questions: int = 1


@dataclass
class GameSession:
    id: str
    users: set[str]
    timeout: int
    questions: list["Question"]
    user_answers: list["UserAnswer"]
    game_status: GAME_STATUS
