import asyncio

import platform

async def async_ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE, #перенаправляем стандартный вывод
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return f"{host} доступен!"
        return f"{host} не доступен!"
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

    tasks = [async_ping(host) for host in hosts] #подготовили задачи для запуска

    results = await asyncio.gather(*tasks) #запустили задачи одновременно
    for result in results:
        print(result)

asyncio.run(main())