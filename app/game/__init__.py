import json
import logging
import re
from typing import Literal, Any, Union, Callable, Awaitable

from game.dc import UserState, GameSettings
from game.model import User
from store.game.cache_manager import CacheAccessor
from store.game.db_manager import DataBaseManager

EVENT = Literal["text", "callback_data"]


def check_cache(
        func: Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]]
):
    async def wrapper(self: "BaseGameAccessor", tg_user_id: str, *args, **kwargs):
        if user_state_raw := await self.cache.get(tg_user_id):
            user_state = str_to_user_state(user_state_raw)
            new_user_state = await func(self, user_state, *args, **kwargs)
        else:
            user_raw = await self.db.get_user_by_id(tg_user_id) or await self.db.add_user(tg_user_id=tg_user_id)
            user = User(**user_raw)
            new_user_state = UserState(
                id=user.id.hex,
                tg_user_id=user.tg_user_id,
                position="start",
                settings=GameSettings(),
            )
        await self.cache.set(new_user_state.tg_user_id, new_user_state.to_string(), 3600)
        return new_user_state

    return wrapper


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
        self.__text_event_handlers: dict[
            str, Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]]
        ] = {}
        self.__callback_data_handlers: dict[
            str | re.Pattern,
            Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]],
        ] = {}
        self.__commands_regex_handler: dict[
            re.Pattern, Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]]
        ] = {}
        self.init()

    def init(self):
        ...

    async def event_handler(self, event: EVENT, text_event: str, **kwargs) -> bytes:
        """Обработчик событий."""
        self.logger.info(f"event_handler: {event=}, {kwargs=}")
        if event == "callback_data":
            return (await getattr(self, text_event)(**kwargs)).to_bytes()
        if event == "text":
            print(text_event, kwargs)
            return (await self.get_text_event_handler(text_event)(**kwargs)).to_bytes()
        ValueError("Event must : 'text' or 'callback_data'")

    def get_text_event_handler(
            self, text
    ) -> Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]]:
        if handler := self.__text_event_handlers.get(text):
            return handler
        for pattern, _handler in self.__commands_regex_handler.items():
            if pattern.fullmatch(text):
                return _handler
        self.logger.error(f"Callback data event handler not fount: {text}")

    def add_text_event_handler(
            self,
            handler: Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]],
            text: Union[str, re.Pattern],
    ):
        self.__text_event_handlers[text] = handler

    def add_regex_text_event_handler(
            self,
            handler: Callable[["BaseGameAccessor", UserState, Any], Awaitable["UserState"]],
            pattern: re.Pattern,
    ):
        self.__commands_regex_handler[pattern] = handler


def str_to_user_state(data: str) -> UserState:
    user_state = UserState(**json.loads(data))
    if isinstance(user_state.settings, dict):
        user_state.settings = GameSettings(**user_state.settings)
    return user_state
