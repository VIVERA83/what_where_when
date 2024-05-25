from typing import Any

from icecream import ic
from sqlalchemy.orm import joinedload

from store.database.postgres.accessor import PostgresAccessor

from store.game.models import GameSessionModel, UserModel, association_table, GameStatusEnum


class DataBaseManager(PostgresAccessor):

    async def add_user(
            self, tg_user_id: str, email: str = None, user_name: str = None
    ) -> UserModel:
        query = self.get_query_insert(
            UserModel, tg_user_id=tg_user_id, email=email, user_name=user_name
        ).returning(UserModel)
        self.logger.info(f"add {UserModel.__name__} : {tg_user_id}")
        return (await self.query_execute(query)).unique().scalar()

    async def create_game_session(self, users: list[str]) -> str:
        query = self.get_query_insert(model=GameSessionModel,
                                      game_status=GameStatusEnum.progress.value,
                                      timeout=60).returning(GameSessionModel)
        game_session = (await self.query_execute(query)).unique().scalar()
        for user in users:
            query = self.get_query_insert(association_table, user_tg_user_id=user, game_session_id=game_session.id)
            await self.query_execute(query)
            self.logger.info(f"add {GameSessionModel.__name__}")
        return game_session.id

    async def get_user_by_id(self, tg_user_id: str) -> UserModel | None:
        query = (
            self.get_query_select_by_field(UserModel, "tg_user_id", tg_user_id)
            .options(joinedload(UserModel.game_sessions))

        )
        return (await self.query_execute(query)).unique().scalars().first()
