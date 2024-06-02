import asyncio
from inspect import iscoroutinefunction, isawaitable

from icecream import ic


def example_decorator(func):
    if iscoroutinefunction(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
    else:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    @example_decorator
    def example_sync_func():
        print("Hello World!, from sync func")
        pass


    @example_decorator
    async def example_async_func():
        print("Hello World!, from async func")
        pass


    async def async_syn():
        print("Hello World!, from asyncio___________")
        pass


    e = example_decorator(async_syn)()
    print(isawaitable(e))
    asyncio.run(e)
