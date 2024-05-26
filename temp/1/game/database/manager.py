from typing import Any

from .postgres import PostgresAccessor
from .models import GameSessionModel, UserModel


class DataBaseManager(PostgresAccessor):

    async def add_user(self, data: dict[str, Any]):
        query = self.get_query_insert(UserModel, **data)
        await self.query_execute(query)
        self.logger.info(f"add {UserModel.__name__} : {data}")

    async def add_game_session(self, data: dict[str, Any]):
        query = self.get_query_insert(GameSessionModel, **data)
        await self.query_execute(query)
        self.logger.info(f"add {GameSessionModel.__name__} : {data}")
