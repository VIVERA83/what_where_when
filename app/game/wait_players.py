from game import BaseGameAccessor, UserState, check_cache


class WaitPlayersPosition(BaseGameAccessor):
    # Переход из главного меню, ожидание игроков после настройки игры.
    # Выбор количества вопросов в игре
    # переход в меню выбора количества вопросов

    @check_cache
    async def wait_players(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь перешел после выборка количества игроков."""
        # если кол-во игроков достаточно, то мы переходим в игровой процесс

        user_state.position = "question_count"
        return user_state
