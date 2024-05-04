import asyncio
from core.logger import setup_logging
from game import Application
from rabbit.accessor import RabbitAccessor


async def run_app():
    logger = setup_logging()
    rabbit = RabbitAccessor(logger=logger)
    app = Application(rabbit, logger)
    try:
        await rabbit.connect()
        await app.start()
    except asyncio.CancelledError:
        logger.info("Application stopped")
    finally:
        await rabbit.disconnect()
        await app.stop()
