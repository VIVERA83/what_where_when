import asyncio
import json
from typing import Any, Awaitable, Callable

from aio_pika.abc import AbstractIncomingMessage
from icecream import ic

from core.logger import setup_logging

from store.database.rabbit.accessor import RabbitAccessor
from game.accessor import MainGameAccessor
from store.game.cache_manager import CacheAccessor
from store.game.db_manager import DataBaseManager


def callback(rabbit: RabbitAccessor) -> Callable:
    def decorator(func: Callable[[Any], Awaitable[Any]]):
        async def wrapper(message: AbstractIncomingMessage):
            try:
                print(message.reply_to)
                result = (
                    await func(**json.loads(message.body))
                    or b'{"status": "Empty response"}'
                )
            except Exception as ex:
                result = json.dumps({"status": "Error", "message": str(ex)}).encode(
                    "utf-8"
                )
                rabbit.logger.error(ex)
            ic(result)
            await rabbit.reply_to(message, result)
            await message.ack(True)
            rabbit.logger.debug(f"Got response: {result}")
            return

        return wrapper

    return decorator


async def run_app():
    logger = setup_logging()
    rabbit = RabbitAccessor(logger=logger)
    db = DataBaseManager(logger=logger)
    cache = CacheAccessor(logger=logger)
    game = MainGameAccessor(db, cache, rabbit,logger=logger)
    try:
        await asyncio.gather(rabbit.connect(), cache.connect())
        await rabbit.consume(callback(rabbit)(game.event_handler), name="game")
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Application stopped")
    finally:
        await asyncio.gather(rabbit.disconnect(), db.disconnect(), cache.disconnect())
