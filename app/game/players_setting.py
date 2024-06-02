import asyncio

from icecream import ic

from game import BaseGameAccessor, UserState, check_cache, str_to_user_state
from game.model import GameSession, Question
from game.start_game import StartSingleGame


class PlayersSettingPosition(BaseGameAccessor):
    tasks: dict[str, asyncio.Task]

    # Переход из главного меню, настройка меню игры.
    # Выбор количества вопросов в игре
    # переход в меню выбора количества вопросов

    def add_task(self, task: asyncio.Task, user_id: str):
        if not getattr(self, "tasks", None):
            self.tasks = {}
        self.tasks[user_id] = task
        for key, t in self.tasks.items():
            if t.done():
                self.tasks.pop(key)

    @check_cache
    async def players_1(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 1"."""
        user_state.settings.quantity_players = 1
        # создаём игру, и переходим в игру
        # question = await self.get_random_question()
        # user_id = await self.db.get_user_id_by_tg_user_id(user_state.tg_user_id)
        # game_session = await self.create_single_game_session(
        #     user_id.hex, question.id.hex
        # )
        #
        # user_state.game_session_id = game_session.id.hex
        # user_state.current_question = question.question
        user_state.position = "start_game"
        self.add_task(asyncio.create_task(StartSingleGame(
            self.db,
            self.cache,
            self.rabbit,
            self.logger
        ).run(user_state.tg_user_id, user_state.settings.quantity_questions)), user_state.tg_user_id)
        # self.add_task(asyncio.create_task(self.timer(user_state)), user_state.tg_user_id)
        return user_state

    @check_cache
    async def players_2(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 2"."""
        user_state.settings.quantity_players = 2
        user_state.position = "wait_players"
        return user_state

    @check_cache
    async def players_3(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 3"."""
        user_state.settings.quantity_players = 3
        user_state.position = "wait_players"
        return user_state

    @check_cache
    async def players_4(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 4"."""
        user_state.settings.quantity_players = 4
        user_state.position = "wait_players"
        return user_state

    # async def get_random_question(self) -> Question:
    #     question_raw = await self.db.get_random_question()
    #     return Question(**question_raw)
    #
    # async def create_game_session(self) -> GameSession:
    #     game_session_raw = await self.db.create_game_session()
    #     return GameSession(**game_session_raw)
    #
    # async def create_single_game_session(
    #         self,
    #         user_id: str,
    #         question_id: str,
    # ) -> GameSession:
    #     game_session = await self.create_game_session()
    #
    #     await self.db.add_question_to_game_session(game_session.id.hex, question_id)
    #     await self.db.add_user_to_game_session(game_session.id.hex, user_id)
    #     await self.db.get_number_questions_in_game_session(game_session.id.hex)
    #
    #     return game_session
    #
    # async def timer(self, user_state: UserState, *_, **__):
    #     """Таймер ожидания окончания времени на ответ."""
    #     await asyncio.sleep(10)
    #     # user_state.position = "single_game"
    #     # await self.rabbit.send_message("kts_bot", user_state.to_bytes())
    #     await asyncio.sleep(10)
    #     user_state_raw = await self.cache.get(user_state.tg_user_id)
    #     new_user_state = str_to_user_state(user_state_raw)
    #     if new_user_state.position == "single_game":
    #         user_state.position = "time_out"
    #         await self.rabbit.send_message("kts_bot", user_state.to_bytes())
