import asyncio
import time


async def task1(name,delay):
    print(f"{name} началась в {time.strftime("%H:%M:%S",time.localtime())}")
    await asyncio.sleep(delay)
    print(f"{name} завершилась в {time.strftime("%H:%M:%S", time.localtime())}")
    return f'Результат {name}'

async def task2(name,delay):
    print(f"{name} началась в {time.strftime("%H:%M:%S",time.localtime())}")
    await asyncio.sleep(delay)
    print(f"{name} завершилась в {time.strftime("%H:%M:%S", time.localtime())}")
    return f'Результат {name}'

async def main():
    print(f'Начало программы в {time.strftime("%H:%M:%S",time.localtime())}')

    task_1=asyncio.create_task(task1(name='Задача №1',delay=3))
    task_2=asyncio.create_task(task1(name='Задача №2',delay=2))
    result1 = await task_1
    print("Получен результат:",result1)
    result2 = await task_2
    print("Получен результат:", result2)

asyncio.run(main())