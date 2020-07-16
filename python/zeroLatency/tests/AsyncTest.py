import asyncio
import time


async def nested():
    await asyncio.sleep(4)
    print("PATH")


if __name__ == '__main__':
    asyncio.gather(nested())
    for i in range(10):
        time.sleep(1)
        print("hello")
