import asyncio
import logging
from typing import Literal

from game_www.manager import DataBaseManager

EVENT = Literal["create_game"]


class GameAccessor:
    def __init__(self, database: DataBaseManager, logger=logging.getLogger(__name__)):
        self.db = database
        self.logger = logger

    async def event_handler(
        self, event: EVENT, timeout: int = None, users: set[str] = None, **kwargs
    ) -> None:
        """Обработчик событий."""
        handler = getattr(self, event)
        return await handler(timeout=timeout, users=users, **kwargs)

    async def create_game(self, users: set[str], timeout: int, questions_count: int):
        """Создаем игру."""
        await self.event_handler(event="create_game", timeout=timeout)
        await self.db.create_game_session({})

    async def start(self):
        queue = asyncio.Queue(1)
        self.logger.info(f"{self.__class__.__name__} started.")
        while True:
            try:
                await queue.get()
            except asyncio.CancelledError:
                self.logger.warning(f"{self.__class__.__name__} cancelled.")
                return
