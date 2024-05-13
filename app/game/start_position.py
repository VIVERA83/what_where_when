from icecream import ic

from . import BaseGameAccessor, check_cache
from .dc import UserState


class StartPosition(BaseGameAccessor):

    def init(self):
        self.add_text_event_handler(self.start, "start")

    async def start(self, tg_user_id: str, *_, **__) -> UserState:
        """Стартовая позиция пользователя в игре.

        1. Проверяем зарегистрирован ли пользователь
            - нет: создаем пользователя
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """
        user = await self.db.get_user_by_id(tg_user_id) or await self.db.add_user(tg_user_id=tg_user_id)
        user_state = UserState(
            tg_user_id=user.tg_user_id,
            position="start",
            settings={},
        )
        await self.cache.set(user.tg_user_id, user_state.to_string(), 3600)
        self.logger.info(f"start: {user=}")
        return user_state

    @check_cache
    async def main(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь в главном меню."""
        user_state.position = "main"
        return user_state

    @check_cache
    async def new_game(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Новая игра"."""
        user_state.position = "new_game"
        return user_state
