import asyncio

from game import BaseGameAccessor, UserState, check_cache

from game.start_game import StartSingleGame


class PlayersSettingPosition(BaseGameAccessor):
    tasks: dict[str, asyncio.Task]

    @check_cache
    async def players_1(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 1"."""
        # создаём игру, и переходим в игру
        user_state.settings.quantity_players = 1
        user_state.position = "start_game"
        self.add_task(
            asyncio.create_task(
                StartSingleGame(self.db, self.cache, self.rabbit, self.logger).run(
                    user_state.tg_user_id, user_state.settings.quantity_questions
                )
            ),
            user_state.tg_user_id,
        )
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

    def add_task(self, task: asyncio.Task, user_id: str):
        if not getattr(self, "tasks", None):
            self.tasks = {}
        self.tasks[user_id] = task
        for key, t in self.tasks.items():
            if t.done():
                self.tasks.pop(key)
