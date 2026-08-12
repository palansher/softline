import asyncio


async def demo():
    print("Привет")

    # Приостанавливаем поток выполнения программы на одну секунду.
    await asyncio.sleep(1)
    print("Как дела?")


asyncio.run(demo())
