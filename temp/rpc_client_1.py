import asyncio
import json
import uuid
from typing import MutableMapping

from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)
from icecream import ic


class FibonacciRpcClient:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue

    def __init__(self) -> None:
        self.futures: MutableMapping[str, asyncio.Future] = {}

    async def connect(self) -> "FibonacciRpcClient":
        self.connection = await connect("amqp://guest:guest@localhost/")
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response, no_ack=True)

        return self

    async def on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            print(f"Bad message {message!r}")
            return
        # if message.body:
        #     ic(message.message_id, json.loads(message.body))

        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, **kwargs) -> int:
        correlation_id = str(uuid.uuid4())
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                json.dumps(kwargs).encode(),
                content_type="text/plain",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            # routing_key="rpc_queue",
            routing_key="game",
        )
        result = await future
        return ic(json.loads(result))


async def main():
    fibonacci_rpc = await FibonacciRpcClient().connect()

    data = {
        "event": "create_user",
        "user_name": "sergievskiy_an",
        "email": "1@example.com",
    }
    data = {
        "event": "create_user",
        "user_name": "mihailov_rs1",
        "email": "2@example.com",
    }
    ############################################################
    data = {
        "event": "create_game",
        "users": ["sergievskiy_an", "mihailov_rs1"],
        "timeout": 60,
        "questions_count": 5,
    }
    #############################################################################
    data = {
        "event": "start",
        "tg_user_id": "tg_user_1",
    }
    # data2 = {"login": "maryushkin_av", "password": "SSSS8888ssss", "course_type": "z"}
    # data2 = {"login": "mikhaylov_rs1", "password": "AAAAaaaa2349", "course_type": "z"}
    # data = {}
    ic(data)
    result = await fibonacci_rpc.call(**data)
    result = await fibonacci_rpc.call(**{"event": "main_menu", **result})
    # await task


if __name__ == "__main__":
    asyncio.run(main())
