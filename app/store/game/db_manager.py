from typing import Any

from sqlalchemy.orm import joinedload

from store.database.postgres.accessor import PostgresAccessor

from store.game.models import GameSessionModel, UserModel


class DataBaseManager(PostgresAccessor):

    async def add_user(
        self, tg_user_id: str, email: str = None, user_name: str = None
    ) -> UserModel:
        query = self.get_query_insert(
            UserModel, tg_user_id=tg_user_id, email=email, user_name=user_name
        )
        self.logger.info(f"add {UserModel.__name__} : {tg_user_id}")
        return (await self.query_execute(query)).unique().scalar()

    async def add_game_session(self, **data: dict[str, Any]):
        query = self.get_query_insert(GameSessionModel, **data)
        await self.query_execute(query)
        self.logger.info(f"add {GameSessionModel.__name__} : {data}")

    async def get_user_by_id(self, tg_user_id: str) -> UserModel | None:
        query = (
            self.get_query_select_by_field(UserModel, "tg_user_id", tg_user_id)
            .options(joinedload(UserModel.game_sessions))
            .where(UserModel.tg_user_id == tg_user_id)
        )
        return (await self.query_execute(query)).unique().scalar()


"""
print(select(address_table.c.email_address).select_from(user_table).join(address_table))
"""
# select_from(GameSessionModel).
# join(, UserModel.id == GameSessionModel.user_id))
# join_from(UserModel,GameSessionModel, ))
# select_from(GameSessionModel).
# join(UserModel, UserModel.id == GameSessionModel.))
# b1 = session.query(Book). \
#     options(joinedload(Book.authors)). \
#     where(Book.id == 1).one()
# print(b1.title)
