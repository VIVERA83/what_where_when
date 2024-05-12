import logging
import re
from typing import Literal, Any, Union

from store.game.cache_manager import CacheAccessor
from store.game.db_manager import DataBaseManager

EVENT = Literal["text", "callback_data"]


class BaseGameAccessor:
    def __init__(
            self,
            database: DataBaseManager,
            cache: CacheAccessor,
            logger=logging.getLogger(__name__),
    ):
        self.db = database
        self.cache = cache
        self.logger = logger
        self.__text_event_handlers: dict[str, Any] = {}
        self.__callback_data_handlers: dict[str | re.Pattern, Any] = {}

    async def event_handler(self, event: EVENT, text_event: str, **kwargs) -> None:
        """Обработчик событий."""
        self.logger.info(f"event_handler: {event=}, {kwargs=}")
        if event == "callback_data":
            return await getattr(self, text_event)(**kwargs)
        if event == "text":
            return self.get_text_event_handler(text_event)(**kwargs)
        ValueError("Event must : 'text' or 'callback_data'")

    def get_text_event_handler(self, text):
        if handler := self.__text_event_handlers.get(text):
            return handler
        raise KeyError(f"Callback data event handler not fount: {text}")

    def add_text_event_handler(self, handler: Any, text: Union[str, re.Pattern]):
        self.__text_event_handlers[text] = handler
