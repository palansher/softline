import asyncio

async def demo():
    print('Привет')
    await asyncio.sleep(1)
    print('Как дела?')

asyncio.run(demo())