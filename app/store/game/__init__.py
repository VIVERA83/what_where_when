import logging
from typing import Literal

from store.manager.cache_manager import CacheAccessor
from store.manager.db_manager import DataBaseManager

EVENTS = Literal["create_game", "start"]


class BaseGameAccessor:
    def __init__(self, database: DataBaseManager, cache: CacheAccessor, logger=logging.getLogger(__name__)):
        self.db = database
        self.cache = cache
        self.logger = logger

    async def event_handler(self, event: EVENTS, **kwargs) -> None:
        """Обработчик событий."""
        return await getattr(self, event)(**kwargs)
