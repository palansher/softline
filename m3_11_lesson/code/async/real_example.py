import asyncio
import aiohttp

async def show_info(session,host):
    url = 'https://' + str(host)
    try:
        async with session.get(url,timeout=3) as response:
            size = response.headers.get('Content-Length')
            if not size:
                size = len(await response.read())
            if response.status == 200:
                return "Host " + str(host) + " онлайн! Размер содержимого " + str(size)
            return "Host " + str(host) + "офлайн! Статус:" + str(response.status)
    except Exception as e:
        return e.__doc__

async def main():
   hosts = [
       "mail.ru",
       "yandex.ru",
       "vk.com",
       "8.8.8.8",
       "unexist_domain.com"
   ]
   async with aiohttp.ClientSession() as session:
       tasks = [asyncio.create_task(show_info(session,host)) for host in hosts]
       results = await asyncio.gather(*tasks)
       for result in results:
           print(result)

asyncio.run(main())