from . import BaseGameAccessor, check_cache
from .dc import UserState, GameSettings
from .model import User


class StartPosition(BaseGameAccessor):

    def init(self):
        self.add_text_event_handler(self.start, "start")  # noqa

    @check_cache
    async def start(self, user_state: UserState, *_, **__) -> UserState:
        """Стартовая позиция пользователя в игре.

        1. Проверяем зарегистрирован ли пользователь
            - нет: создаем пользователя
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """
        user_state.position = "start"
        return user_state

    @check_cache
    async def main(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь в главном меню."""
        user_state.position = "main"
        return user_state
