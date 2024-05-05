import logging
from typing import Optional

import redis.asyncio as redis
from core.settings import RedisSettings
from redis.client import Redis


class RedisAccessor:

    def __init__(self, logger=logging.getLogger(__name__)):
        self.settings = RedisSettings()
        self.logger = logger
        self.connector: Optional[Redis] = None

    async def connect(self):
        self.connector = await redis.from_url(
            self.settings.dsn(True), decode_responses=True
        )
        self.logger.info(f"{self.__class__.__name__} connected")

    async def disconnect(self):
        await self.connector.close()
        self.logger.info(f"{self.__class__.__name__} disconnected")
