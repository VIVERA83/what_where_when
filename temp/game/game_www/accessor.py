import logging


class GameAccessor:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    async def connect(self): ...

    async def event_handler(self, event): ...
