from game_www import BaseGameAccessor


class StartGame(BaseGameAccessor):
    async def create_game(
        self, users: set[str], timeout: int, questions_count: int, *_
    ) -> None:
        """Создаем игру."""
        self.logger.info(f"create_game: {users=}, {timeout=}, {questions_count=}")
        for user in users:
            await self.db.add_user({"user_name": user})
        await self.db.add_game_session(
            users=users, timeout=timeout, questions_count=questions_count
        )

    async def create_user(self, email: str, user_name: str = None) -> None:
        """Обработчик событий."""
        await self.db.add_user(email=email, user_name=user_name)
        self.logger.info(f"create_user: {user_name=}")
