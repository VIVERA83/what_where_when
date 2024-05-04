import asyncio
import logging

from rabbit.accessor import RabbitAccessor


class Application:
    def __init__(self, rabbit: RabbitAccessor, logger=logging.getLogger(name=__name__)):
        self.logger = logger
        self.rabbit = rabbit
        self.__queue = asyncio.Queue()

    async def start(self):
        pass

    async def stop(self):
        pass

    @property
    def queue(self) -> asyncio.Queue:
        return self.__queue
