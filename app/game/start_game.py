import asyncio

from game import BaseGameAccessor, str_to_user_state
from game.model import Question, GameSession


class StartSingleGame(BaseGameAccessor):
    """Класс для запуска одиночной  игры."""

    # id - идентификатор игрока в базе данных
    id: str
    # quiz_count - количество вопросов в игре
    quiz_count: int
    # user_id - идентификатор пользователя в телеграм
    user_id: str
    # game_session - сессия игры
    game_session: GameSession

    async def run(self, user_id: str, quiz_count: int):
        """Запуск одиночной игры."""
        self.logger.info(f"Start single game: {user_id=}, {quiz_count=}")
        self.user_id = user_id
        self.id = (await self.db.get_user_id_by_tg_user_id(user_id)).hex
        self.quiz_count = quiz_count
        await self.initialize()
        await self.worker()

    async def initialize(self):
        """Инициализация одиночной игры."""
        self.game_session = await self.create_game_session()
        await self.db.add_user_to_game_session(self.game_session.id.hex, self.id)

        user_state = str_to_user_state(await self.cache.get(self.user_id))
        user_state.game_session_id = self.game_session.id.hex

        await self.cache.set(self.user_id, user_state.to_string(), 3600)
        self.logger.info("Initialize single game completed.")

    async def get_random_question(self) -> Question:
        """Получение случайного вопроса."""
        self.logger.info(f"Get random question.")
        question_raw = await self.db.get_random_question()
        return Question(**question_raw)

    async def create_game_session(self) -> GameSession:
        """Создание сессии игры."""
        game_session_raw = await self.db.create_game_session()
        self.logger.info(f"Create game session.")
        return GameSession(**game_session_raw)

    async def worker(self):
        """Запуск одиночной игры."""

        await asyncio.sleep(10)
        user_state = str_to_user_state(await self.cache.get(self.user_id))
        while (
                user_state
                and self.quiz_count > 0
                and user_state.position in ["start_game", "single_game"]
                and user_state.game_session_id == self.game_session.id.hex
        ):
            user_state = str_to_user_state(await self.cache.get(self.user_id))

            counter = 20
            while counter:
                counter -= 1
                question = await self.get_random_question()
                try:
                    await self.db.add_question_to_game_session(self.game_session.id.hex, question.id.hex)
                except Exception:
                    self.logger.warning(f"Can't add question to game session {counter}")
                    continue
                user_state.position = "single_game"
                user_state.current_question = question.question
                counter = 0
                await self.rabbit.send_message("kts_bot", user_state.to_bytes())
                await self.cache.set(self.user_id, user_state.to_string(), 3600)
                self.quiz_count -= 1
                await asyncio.sleep(10)

        user_state = str_to_user_state(await self.cache.get(self.user_id))
        if (
                user_state
                and self.quiz_count == 0
                and user_state.position in ["single_game_correct", "single_game_incorrect"]
                and user_state.game_session_id == self.game_session.id.hex
        ):
            user_state.position = "single_game_end"
            await self.cache.set(self.user_id, user_state.to_string(), 3600)
            await self.rabbit.send_message("kts_bot", user_state.to_bytes())
        user_state.score = 0
        await self.cache.set(self.user_id, user_state.to_string(), 3600)
