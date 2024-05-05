import asyncio
import json
from typing import Any, Awaitable, Callable

from aio_pika.abc import AbstractIncomingMessage

from store.database.rabbit.accessor import RabbitAccessor
from store.game.accessor import MainGameAccessor

from core.logger import setup_logging
from store.manager.cache_manager import CacheAccessor
from store.manager.db_manager import DataBaseManager


def callback(rabbit: RabbitAccessor) -> Callable:
    def decorator(func: Callable[[Any], Awaitable[Any]]):
        async def wrapper(message: AbstractIncomingMessage):
            rabbit.logger.debug(f"Got request: {message.body}")
            result = b'{"status": "error"}'
            try:
                # a = getattr(func, name)
                # result = await a(func, **json.loads(message.body)) or b'{"status": "Empty response"}'

                result = (
                        await func(**json.loads(message.body))
                        or b'{"status": "Empty response"}'
                )
            except Exception as ex:
                rabbit.logger.error(ex)
            await rabbit.reply_to(message, result)
            await rabbit.send_message("hello", result)
            await message.ack(True)
            rabbit.logger.debug("Got response")
            return

        return wrapper

    return decorator


async def run_app():
    logger = setup_logging()
    rabbit = RabbitAccessor(logger=logger)
    db = DataBaseManager(logger=logger)
    cache = CacheAccessor(logger=logger)
    game = MainGameAccessor(db, cache, logger=logger)
    try:
        await asyncio.gather(rabbit.connect(), cache.connect())
        await rabbit.consume(callback(rabbit)(game.event_handler), name="game")
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Application stopped")
    finally:
        await asyncio.gather(rabbit.disconnect(), db.disconnect(), cache.disconnect())

