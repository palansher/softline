import asyncio

async def wait_call():
    print('Созвон через 5 минут')
    await asyncio.sleep(5)
    print('Созвон начался')

async def dinner():
    print('Обед')

async def main():
    await asyncio.gather(wait_call(),dinner())

asyncio.run(main())