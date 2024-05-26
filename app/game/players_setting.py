from icecream import ic

from game import BaseGameAccessor, UserState, check_cache
from game.model import GameSession


class PlayersSettingPosition(BaseGameAccessor):
    # Переход из главного меню, настройка меню игры.
    # Выбор количества вопросов в игре
    # переход в меню выбора количества вопросов

    @check_cache
    async def players_1(self, user_state: UserState, *_, **__) -> UserState:
        """Пользователь нажал кнопку "Игрок 1"."""
        user_state.settings.quantity_players = 1
        # создаём игру, и переходим в игру
        users_ids = await self.db.get_users_ids_by_tg_user_ids([user_state.tg_user_id])
        questions = await self.db.get_random_questions(
            user_state.settings.quantity_questions
        )
        game_session_raw = await self.db.create_game_session(
            [user_id.hex for user_id in users_ids],
            [question.id.hex for question in questions],
        )
        game_session = GameSession(**game_session_raw)
        user_state.position = "single_game"
        user_state.game_session_id = game_session.id.hex
        user_state.current_question = game_session.questions[0].question
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
