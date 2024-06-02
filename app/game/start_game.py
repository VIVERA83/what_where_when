import asyncio

from icecream import ic

from game import BaseGameAccessor, str_to_user_state
from game.model import Question, GameSession


class StartSingleGame(BaseGameAccessor):
    id: str
    quiz_count: int
    user_id: str
    game_session: GameSession

    async def run(self, user_id: str, quiz_count: int):
        await self.initialize(user_id, quiz_count)
        await self.worker()

    async def initialize(self, user_id: str, quiz_count: int):
        # создаём игру
        self.user_id = user_id
        self.id = (await self.db.get_user_id_by_tg_user_id(user_id)).hex
        self.quiz_count = quiz_count
        self.game_session = await self.create_game_session()
        await self.db.add_user_to_game_session(self.game_session.id.hex, self.id)

        user_state = str_to_user_state(await self.cache.get(self.user_id))
        user_state.game_session_id = self.game_session.id.hex
        await self.cache.set(self.user_id, user_state.to_string(), 3600)

    async def get_random_question(self) -> Question:
        question_raw = await self.db.get_random_question()
        return Question(**question_raw)

    async def create_game_session(self) -> GameSession:
        game_session_raw = await self.db.create_game_session()
        return GameSession(**game_session_raw)

    async def worker(self):
        """Таймер ожидания окончания времени на ответ."""
        await asyncio.sleep(10)
        user_state = str_to_user_state(await self.cache.get(self.user_id))
        while (user_state
               and self.quiz_count > 0
               and user_state.position in ["start_game", "single_game"]
               and user_state.game_session_id == self.game_session.id.hex):
            user_state = str_to_user_state(await self.cache.get(self.user_id))
            question = await self.get_random_question()
            user_state.position = "single_game"
            user_state.current_question = question.question

            await self.db.add_question_to_game_session(self.game_session.id.hex, question.id.hex)
            await self.rabbit.send_message("kts_bot", user_state.to_bytes())
            await self.cache.set(self.user_id, user_state.to_string(), 3600)
            self.quiz_count -= 1
            await asyncio.sleep(10)
        # return

        user_state = str_to_user_state(await self.cache.get(self.user_id))
        if (user_state
                and self.quiz_count == 0
                and user_state.position in ["single_game_correct", "single_game_incorrect"]
                and user_state.game_session_id == self.game_session.id.hex):
            user_state.position = "single_game_end"
            await self.cache.set(self.user_id, user_state.to_string(), 3600)
            await self.rabbit.send_message("kts_bot", user_state.to_bytes())
        user_state.score = 0
        await self.cache.set(self.user_id, user_state.to_string(), 3600)
        # if (user_state
        #         and user_state.position == "start_game"
        #         and user_state.game_session_id == self.game_session.id.hex):

        ic(1)
        # await asyncio.sleep(10)
        # self.user_state.position = "single_game"
        # await self.rabbit.send_message("kts_bot", self.user_state.to_bytes())
        # for _ in range(self.quiz_count + 3):
        #     await asyncio.sleep(10)
        #     question = await self.get_random_question()
        #
        #     self.user_state.game_session_id = self.game_session.id.hex
        #     self.user_state.current_question = question.question
        #     user_state_raw = await self.cache.get(self.user_state.tg_user_id)
        #     new_user_state = str_to_user_state(user_state_raw)
        #     await self.rabbit.send_message("kts_bot", new_user_state.to_bytes())

    # async def start_game(self, user_state: UserState, *_, **__):
    #     user_state.position = "single_game"
    #     await self.rabbit.send_message("kts_bot", user_state.to_bytes())
