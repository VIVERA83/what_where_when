from game import BaseGameAccessor, check_cache, UserState


class QuestionsSettingPosition(BaseGameAccessor):
    # Переход из "новая игра" (выбор количества игроков)
    # Выбор количества вопросов в игре, переход в меню ожидания игроков

    @check_cache
    async def questions_1(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "В игре 1 вопрос"."""
        user_state.settings.quantity_questions = 1
        user_state.position = "new_game"
        return user_state

    @check_cache
    async def questions_2(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "В игре 2 вопрос"."""
        user_state.settings.quantity_questions = 2
        user_state.position = "new_game"
        return user_state

    @check_cache
    async def questions_3(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "В игре 3 вопрос"."""
        user_state.settings.quantity_questions = 3
        user_state.position = "new_game"
        return user_state

    @check_cache
    async def back_new_game(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Вернуться главное меню"."""
        user_state.position = "question_count"
        return user_state
