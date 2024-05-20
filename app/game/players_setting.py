from game import BaseGameAccessor, UserState, check_cache


class PlayersSettingPosition(BaseGameAccessor):
    # Переход из главного меню, настройка меню игры.
    # Выбор количества вопросов в игре
    # переход в меню выбора количества вопросов

    @check_cache
    async def players_1(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 1"."""
        user_state.settings.quantity_players = 1
        # создаём игру, и переходим в игру
        user_state.position = "меню игры"
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
