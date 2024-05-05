from . import BaseGameAccessor


class StartPosition(BaseGameAccessor):
    async def start(self, tg_user_id: str, *_, **__):
        """Стартовая позиция пользователя в игре.

        1. Проверяем зарегистрирован ли пользователь
            - нет: создаем пользователя
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """
        user = await self.db.get_user_by_id(tg_user_id) or await self.db.add_user(tg_user_id=tg_user_id)
        self.logger.info(f"start: {user=}")
        return 0

    async def click_new_game(self, user_id: str, *_, **__):
        """Пользователь нажал кнопку "Новая игра".

        1. Проверяем позицию пользователя
            - не соответствует: отправляем на стартовую позицию
        2. Запоминаем позицию пользователя
        3. Направляем пользователю позицию в игре
        """
        return 0
