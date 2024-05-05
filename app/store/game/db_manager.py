from typing import Any

from store.database.postgres.accessor import PostgresAccessor

from store.game.models import GameSessionModel, UserModel


class DataBaseManager(PostgresAccessor):

    async def add_user(self, **kwargs):
        query = self.get_query_insert(UserModel, **kwargs)
        await self.query_execute(query)
        self.logger.info(f"add {UserModel.__name__} : {kwargs}")

    async def add_game_session(self, **data: dict[str, Any]):
        query = self.get_query_insert(GameSessionModel, **data)
        await self.query_execute(query)
        self.logger.info(f"add {GameSessionModel.__name__} : {data}")

    async def get_user_by_id(self, tg_user_id: str) -> Any:
        query = self.get_query_select_by_field(UserModel, "tg_user_id", tg_user_id)
        return await self.query_execute(query)
