from typing import Any

from store.database.postgres.accessor import PostgresAccessor

from store.manager.models import GameSessionModel, UserModel


class DataBaseManager(PostgresAccessor):

    async def add_user(self, **kwargs):
        query = self.get_query_insert(UserModel, **kwargs)
        await self.query_execute(query)
        self.logger.info(f"add {UserModel.__name__} : {kwargs}")

    async def add_game_session(self, **data: dict[str, Any]):
        query = self.get_query_insert(GameSessionModel, **data)
        await self.query_execute(query)
        self.logger.info(f"add {GameSessionModel.__name__} : {data}")
