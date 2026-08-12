import asyncio  # Импортируем модуль для асинхронного программирования (Event Loop, параллельные задачи)
import platform  # Модуль для получения информации об операционной системе (Windows, Linux, macOS)


# [ОПРЕДЕЛЕНИЕ КОРОУТИНЫ]
# async def указывает, что это асинхронная функция, возвращающая объект-корутину.
async def async_ping(host):
    # [ТЕРНАРНЫЙ ОПЕРАТОР (Обычный Python)]
    # Выбираем ключ количества пакетов в зависимости от ОС:
    # В Windows флаг '-n' (number), в Linux/macOS флаг '-c' (count).
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # [СПИСОК КОМАНДЫ (Обычный Python)]
    # Формируем список аргументов для вызова системной консольной утилиты: ping <param> 1 <host>
    command = ["ping", param, "1", host]

    try:
        # [НЕБЛОКИРУЮЩИЙ ЗАПУСК СИСТЕМНОГО ПРОЦЕССА]
        # create_subprocess_exec запускает внешнюю программу (ping) в отдельном процессе ОС.
        # *command — распаковывает список ["ping", param, "1", host] в 4 отдельных аргумента.
        # PIPE означает, что вывод программы не печатается в консоль, а перехватывается Python.
        # await означает, что Event Loop отдает контроль другим задачам, пока ОС создает процесс.
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,  # Перенаправляем стандартный вывод (результат ping)
            stderr=asyncio.subprocess.PIPE,  # Перенаправляем поток ошибок
        )

        # [АСИНХРОННОЕ ОЖИДАНИЕ ЗАВЕРШЕНИЯ ПРОЦЕССА]
        # communicate() ждет, пока утилита ping закончит работу и вернет вывод.
        # await позволяет выполнять другие пинги на заднем фоне, пока мы ждем ответа от этого host.
        stdout, stderr = await process.communicate()

        # [ПРОВЕРКА КОДА ВОЗВРАТА СИСТЕМЫ]
        # В операционных системах код 0 означает 'Успешно' (узел ответил на ping).
        if process.returncode == 0:
            return f"{host} доступен!"
        return f"{host} не доступен!"

    except Exception as e:
        # [ОБРАБОТКА ОШИБОК (Обычный Python)]
        # Если системный процесс вообще не смог запуститься (например, команда ping не найдена),
        # e.__doc__ возвращает краткое описание (docstring) класса возникшего исключения.
        return e.__doc__


# [ГЛАВНАЯ КОРОУТИНА]
async def main():
    # Список доменов и IP-адресов для проверки (включая заведомо несуществующий)
    hosts = ["mail.ru", "yandex.ru", "vk.com", "8.8.8.8", "unexist_domain.com"]

    # [LIST COMPREHENSION / ГЕНЕРАТОР СПИСКА (Обычный Python)]
    # Вызываем async_ping(host) для каждого хоста.
    # ВАЖНО: Это НЕ запускает пинги! Это создает список из 5 объектов-корутин [coro1, coro2, ...]
    tasks = [async_ping(host) for host in hosts]

    # [Параллельный запуск через gather]
    # *tasks распаковывает список из 5 корутин в отдельные аргументы для gather().
    # asyncio.gather зажимает все 5 пингов одновременно в Event Loop.
    # await ждет, пока завершатся ВСЕ 5 пингов, и возвращает список их результативных строк.
    results = await asyncio.gather(*tasks)

    # [ЦИКЛ FOR (Обычный Python)]
    # Проходим по полученному списку результатов и печатаем их
    for result in results:
        print(result)


# [ТОЧКА ВХОДА]
# Создает новый Event Loop, запускает в нем main() и закрывает цикл по завершении.
asyncio.run(main())
