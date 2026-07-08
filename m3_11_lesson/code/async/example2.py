import asyncio

async def task1():
    await asyncio.sleep(3)
    print('Задача 1 завершена')


async def task2():
    await asyncio.sleep(2)
    print('Задача 2 завершена')

async def main():
    await asyncio.gather(task2(),task1())

asyncio.run(main())