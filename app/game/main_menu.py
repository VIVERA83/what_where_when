from game import BaseGameAccessor, check_cache, UserState


class MainMenuPosition(BaseGameAccessor):
    @check_cache
    async def new_game(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Новая игра"."""
        user_state.position = "question_count"
        return user_state

    @check_cache
    async def join_game(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Присоединится и гре"."""
        user_state.position = "join_game"
        return user_state

    @check_cache
    async def back_main(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Вернуться в главное меню"."""
        user_state.position = "main"
        return user_state
