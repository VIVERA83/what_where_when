import asyncio

import logging

from typing import MutableMapping

from aio_pika.abc import AbstractIncomingMessage

from game_www.accessor import GameAccessor
from store.database import RabbitAccessor

from .utils import create_future


class BaseApp:
    def __init__(
        self,
        rabbit: RabbitAccessor,
        game: GameAccessor,
        logger=logging.getLogger(__name__),
    ):
        self.rabbit = rabbit
        self.game = game
        self.logger = logger
        self.callback_queue = None

        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.users: MutableMapping[str, str] = {}
        self.queue_name = "game"

    async def _connect(self):
        await self.rabbit.consume(self._message_handler, name=self.queue_name)

    async def start(self):
        await self._connect()
        await self.__worker()

    async def stop(self):
        self.logger.info(f"{self.__class__.__name__} stopped.")

    async def _message_handler(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            self.logger.warning(f"Bad message {message!r}")
            return
        # username = self.users.pop(message.correlation_id)
        print(message.body.decode("utf-8"))
        result = await self._wait_future(message.correlation_id, message.body)
        # TODO: сделать обработку некорректных данных в ответе
        # msg = create_message(json.loads(result.decode("utf-8")))

        # сюда мы пишем очередь в которую отправляем результат
        # await self.bot.send_message(username, message)
        # users = [message.reply_to]
        # for
        await self.rabbit.reply_to(message, result)
        await self.rabbit.send_message("hello", result)
        await message.ack(True)
        self.logger.debug(f"Got response: {message}")

    async def _wait_future(self, correlation_id: str, body: bytes) -> bytes:
        """Awaits for a future to be set with a result and returns the result.

        Parameters:
            correlation_id (str): The unique identifier for the future.
            body (bytes): The body of the future.
        Returns:
            bytes: The result of the future.
        """
        result = b"{'status': 'error'}"
        future = create_future()
        self.futures[correlation_id] = future
        try:
            future: asyncio.Future = self.futures.pop(correlation_id)
            future.set_result(body)
            result = await future
        except KeyError:
            self.logger.warning(f"Future {correlation_id!r} not found")
        return result

    async def __worker(self):
        """Worker function that listens for tasks in a queue."""

        queue = asyncio.Queue(1)
        self.logger.info(f"{self.__class__.__name__} started.")
        while True:
            try:
                await queue.get()
            except asyncio.CancelledError:
                self.logger.warning("Application cancelled")
                return
