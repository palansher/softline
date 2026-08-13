import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

# Запасной URL, если в .env ничего не указано
DEFAULT_CBR_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_currency_ratio(
    first_currency: str,
    second_currency: str,
    url: str | None = None,
) -> float:
    """Вычисляет отношение курса первой валюты к курсу второй валюты.

    Получает текущие данные ЦБ РФ по указанному URL и возвращает,
    во сколько раз стоимость одной единицы первой валюты отличается
    от стоимости одной единицы второй валюты (в рублевом эквиваленте).

    Args:
        first_currency (str): Трехбуквенный код первой валюты (например, 'USD').
        second_currency (str): Трехбуквенный код второй валюты (например, 'EUR').
        url (str | None, optional): URL веб-сервиса с JSON-данными.
            Если не передан, значение загружается из переменной окружения `CBR_API_URL`.
            Defaults to None.

    Returns:
        float: Коэффициент отношения первого курса ко второму (Rate1 / Rate2).
            Если значение > 1, первая валюта дороже второй.
            Если значение < 1, первая валюта дешевле второй.

    Raises:
        ValueError: Если URL не задан ни в параметрах, ни в .env.
        requests.RequestException: При ошибках сетевого запроса или статусах HTTP 4xx/5xx.
        KeyError: Если один из указанных кодов валют отсутствует в ответе API.
        ZeroDivisionError: Если курс второй валюты равен 0.
    """
    # Если URL не передан явно, пытаемся достать его из .env
    target_url = url or os.getenv("CBR_API_URL") or DEFAULT_CBR_URL

    if not target_url:
        raise ValueError("URL API не указан в параметрах и не найден в .env")

    # Выполняем GET-запрос с таймаутом в 10 секунд
    response = requests.get(target_url, timeout=10)
    response.raise_for_status()

    data: dict[str, Any] = response.json()
    valutes: dict[str, Any] = data.get("Valute", {})

    # Приводим коды валют к верхнему регистру для надежности
    code_1 = first_currency.upper()
    code_2 = second_currency.upper()

    # Проверяем наличие обеих валют в словаре
    for code in (code_1, code_2):
        if code not in valutes:
            raise KeyError(f"Валюта с кодом '{code}' не найдена в ответе сервиса.")

    # Вычисляем реальную стоимость 1 единицы валюты с учетом ее номинала (Nominal)
    val1_data = valutes[code_1]
    val2_data = valutes[code_2]

    unit_rate_1: float = val1_data["Value"] / val1_data["Nominal"]
    unit_rate_2: float = val2_data["Value"] / val2_data["Nominal"]

    if unit_rate_2 == 0:
        raise ZeroDivisionError(f"Курс валюты {code_2} равен нулю.")

    return unit_rate_1 / unit_rate_2


if __name__ == "__main__":
    # Пример использования функции
    currency_a = "USD"
    currency_b = "EUR"

    try:
        # URL берется автоматически из .env
        ratio = get_currency_ratio(first_currency=currency_a, second_currency=currency_b)

        print(f"Отношение курса {currency_a} к {currency_b}: {ratio:.4f}")

        if ratio < 1:
            diff = 1 / ratio
            print(f"1 {currency_b} дороже 1 {currency_a} в {diff:.2f} раз(а).")
        else:
            print(f"1 {currency_a} дороже 1 {currency_b} в {ratio:.2f} раз(а).")

    except requests.RequestException as e:
        print(f"Сетевая ошибка при запросе к сервису: {e}")
    except KeyError as e:
        print(f"Ошибка в кодах валют: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
