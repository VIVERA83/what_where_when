import re

from icecream import ic

from game import BaseGameAccessor, UserState, check_cache
from game.model import Question, UserAnswer


class TextAccessor(BaseGameAccessor):
    def init(self):
        self.add_text_event_handler(self.start, "start")  # noqa
        self.add_regex_text_event_handler(self.text_handler, re.compile(r".*"))

    @check_cache
    async def text_handler(self, user_state: UserState, *_, **kwargs) -> UserState:
        """Обработчик всех текстовых сообщений которые приходят в игру."""
        if user_state.position == "single_game":
            return await self.handler_text_single_game_state(user_state, **kwargs)
        raise ValueError(
            "На текущей позиции пользователя нет обработчика текстового события"
        )

    async def handler_text_single_game_state(
        self, user_state: UserState, text: str, *_, **__
    ) -> UserState:
        """Обработка ответа полученного из позиции игрока в одиночной игре.

        Предполагается что пользователь ввел ответ и нужно проверить его соответствие с правильным ответом.
        """
        question = Question(
            **await self.db.get_question_by_title(user_state.current_question)
        )
        user_answer = UserAnswer(
            **await self.db.add_answer(
                user_state.id, user_state.game_session_id, question.id.hex, text
            )
        )

        if user_answer.is_correct:
            user_state.position = "single_game_correct"
            user_state.score += 1
        else:
            user_state.position = "single_game_incorrect"

        user_state.correct_answer = question.answer
        user_state.user_answer = text
        return user_state
