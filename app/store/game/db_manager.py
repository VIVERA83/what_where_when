from typing import Optional
from uuid import UUID

from store.database.postgres.accessor import PostgresAccessor

from store.game.models import (
    UserModel,
    user_game_session_association,
    GameStatusEnum,
    QuestionModel,
    question_game_session_association,
    UserAnswerModel,
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

    async def create_game_session(self) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
            insert into game.game_sessions (game_status, timeout) 
            values ('{GameStatusEnum.progress.value}', 60) 
            returning *;
        """
        )
        return (await self.query_execute(query)).mappings().first()

    async def add_user_to_game_session(
        self, game_session_id: str, user_id: str
    ) -> Optional[dict]:
        query = self.get_query_insert(
            model=user_game_session_association,
            user_id=user_id,
            game_session_id=game_session_id,
        ).returning("*")
        return (await self.query_execute(query)).mappings().first()

    async def add_question_to_game_session(
        self, game_session_id: str, question_id: str
    ) -> Optional[dict]:
        query = self.get_query_insert(
            model=question_game_session_association,
            question_id=question_id,
            game_session_id=game_session_id,
        ).returning("*")
        return (await self.query_execute(query)).mappings().first()

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

    async def get_user_id_by_tg_user_id(self, tg_user_id: str) -> UUID:
        query = self.get_query_from_text(
            f"""
                select id  
                from game.users u
                where u.tg_user_id = '{tg_user_id}'
                ;
            """
        )
        return (await self.query_execute(query)).scalar()

    async def get_number_questions_in_game_session(self, game_session_id: str) -> int:
        query = self.get_query_from_text(
            f"""
                select count(1) from game.questions q 
                join game.question_game_session_association qgsa on qgsa.question_id  = q.id 
                join game.game_sessions gs  on gs.id = qgsa.game_session_id 
                where gs.id ='{game_session_id}'
                ;
            """
        )
        return (await self.query_execute(query)).scalars().first()

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

    async def get_random_question(self) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
                select * from game.questions
                order by random()
                limit 1
            """
        )
        return (await self.query_execute(query)).mappings().first()

    async def get_question_by_title(self, title: str) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
                select * from game.questions
                where question = '{title}'
            """
        )
        return (await self.query_execute(query)).mappings().first()

    async def get_question_by_id(self, question_id: str) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
                select * from game.questions
                where id = '{question_id}'
            """
        )
        return (await self.query_execute(query)).mappings().first()

    async def add_answer(
        self, user_id: str, game_session_id: str, question_id: str, answer: str
    ) -> Optional[dict]:
        query = self.get_query_from_text(
            f"""
                insert into game.user_answers (is_correct, answer, game_session, question_id, user_id) 
                values (
                    (select 
                        case when lower(q.answer) = lower('{answer}')
                            then true 
                            else false  
                        end as is_correct 
                    from game.questions q  
                    where q.id  = '{question_id}'
                    ), lower('{answer}'), '{game_session_id}', '{question_id}','{user_id}'
                )
                returning *
            """
        )
        return (await self.query_execute(query)).mappings().first()
