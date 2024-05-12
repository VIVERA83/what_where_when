from icecream import ic

from . import BaseGameAccessor
from .dc import UserState


class StartPosition(BaseGameAccessor):
    async def start(self, tg_user_id: str, *_, **__) -> bytes:
        """Стартовая позиция пользователя в игре.

        1. Проверяем зарегистрирован ли пользователь
            - нет: создаем пользователя
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """
        user = await self.db.get_user_by_id(tg_user_id) or await self.db.add_user(tg_user_id=tg_user_id)
        user_state = UserState(
            tg_user_id=user.tg_user_id,
            position="main",
            settings={},
        )
        await self.cache.set(user.tg_user_id, user_state.to_string(), 3600)
        self.logger.info(f"start: {user=}")
        return user_state.to_bytes()

    async def main(self, tg_user_id: str, *_, **__) -> bytes:
        """Пользователь в главном меню.

        1. Проверяем позицию пользователя
            - нет: отправляем на стартовую позицию
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """

    async def new_game(self, tg_user_id: str, *_, **__):
        """Пользователь нажал кнопку "Новая игра".

        1. Проверяем позицию пользователя
            - не соответствует: отправляем на стартовую позицию
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """
        return UserState(tg_user_id=tg_user_id,position="new_game", settings={}).to_bytes()
