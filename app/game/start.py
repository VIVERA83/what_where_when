from . import BaseGameAccessor, check_cache
from .dc import UserState, GameSettings


class StartPosition(BaseGameAccessor):

    def init(self):
        self.add_text_event_handler(self.start, "start")  # noqa

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
            settings=GameSettings(),
        )
        await self.cache.set(user.tg_user_id, user_state.to_string(), 3600)
        self.logger.info(f"start: {user.tg_user_id}")
        return user_state

    @check_cache
    async def main(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь в главном меню."""
        user_state.position = "main"
        return user_state
