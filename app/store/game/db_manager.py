from typing import Optional
from uuid import UUID

from store.database.postgres.accessor import PostgresAccessor

from store.game.models import (
    UserModel,
    user_game_session_association,
    GameStatusEnum,
    QuestionModel,
    question_game_session_association,
)

from icecream import ic

ic.includeContext = True


class DataBaseManager(PostgresAccessor):

    async def add_user(
        self, tg_user_id: str, email: str = None, user_name: str = None
    ) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
            insert into game.users (tg_user_id, email, user_name) 
            values ('{tg_user_id}', '{email}', '{user_name}') 
            returning *;
        """
        )
        self.logger.debug(f"add {UserModel.__name__} : {tg_user_id}")
        return (await self.query_execute(query)).mappings().first()

    async def create_game_session(
        self, users_ids: list[str], questions_ids: list[str]
    ) -> Optional[dict]:
        query_session = self.get_query_from_text(
            f"""
            insert into game.game_sessions (game_status, timeout) 
            values ('{GameStatusEnum.progress.value}', 60) 
            returning id;
        """
        )
        game_session_id, *_ = (await self.query_execute(query_session)).first()
        for user_id in users_ids:
            query = self.get_query_insert(
                model=user_game_session_association,
                user_id=user_id,
                game_session_id=game_session_id,
            )
            await self.query_execute(query)
        for question_id in questions_ids:
            query = self.get_query_insert(
                model=question_game_session_association,
                question_id=question_id,
                game_session_id=game_session_id,
            )
            await self.query_execute(query)

        return await self.get_game_session_by_id(game_session_id)

    async def get_user_by_id(self, tg_user_id: str) -> dict:
        query = self.get_query_from_text(
            f"""
                select 
                jsonb_build_object( 'id', u.id,
                                    'tg_user_id', u.tg_user_id, 
                                    'email', u.email, 
                                    'user_name', u.user_name,
                                    'game_sessions', json_agg(jsonb_build_object(
                                                'id', gs.id, 
                                                'game_status', gs.game_status, 
                                                'timeout', gs.timeout))
                                    ) as data 
                from game.users u
                left join game.user_game_session_association ugsa on ugsa.user_id = u.id 
                left join game.game_sessions gs on gs.id = ugsa.game_session_id
                where u.tg_user_id='{tg_user_id}'
                group by u.id, u.tg_user_id, u.email, u.user_name
                ;
            """
        )
        return (await self.query_execute(query)).scalar()

    async def get_users_ids_by_tg_user_ids(self, tg_user_ids: list[str]) -> list[UUID]:
        query = self.get_query_from_text(
            f"""
                select id  
                from game.users u
                where u.tg_user_id in ({"".join(f"'{tg_user_id}'" for tg_user_id in tg_user_ids)})
                ;
            """
        )
        return (await self.query_execute(query)).scalars().all()  # type: ignore

    async def get_game_session_by_id(self, game_session_id: str) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
                select 
                jsonb_build_object('id', gs.id, 
                                   'game_status', gs.game_status, 
                                   'timeout', gs.timeout, 
                                   'users', json_agg(jsonb_build_object('id', u.id,
                                                                        'tg_user_id', u.tg_user_id,
                                                                        'email', u.email, 
                                                                        'user_name', u.user_name)),
                                   'questions', json_agg(jsonb_build_object('id', q.id, 
                                                                            'question', q.question,
                                                                            'answer', q.answer))
                                    ) as data_1 
                from game.game_sessions gs
                left join game.user_game_session_association ugsa on ugsa.game_session_id = gs.id 
                left join game.users u on u.id = ugsa.user_id
                left join game.question_game_session_association qgsa on qgsa.game_session_id = gs.id
                left join game.questions q on q.id = qgsa.question_id
                where gs.id='{game_session_id}'
                group by gs.id, u.tg_user_id, u.email, u.user_name
                ;
        """
        )
        return (await self.query_execute(query)).scalar()

    async def get_random_questions(self, count: int) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
                select * from game.questions
                order by random()
                limit {count}
            """
        )
        return (await self.query_execute(query)).mappings().all()
