import asyncio


async def second():
    while True:
        await asyncio.sleep(1)
        print("Second")


async def long():
    await asyncio.sleep(3)
    print("Long")


async def main():
    await asyncio.gather(second(), long())

if __name__ == "__main__":
    asyncio.run(main())