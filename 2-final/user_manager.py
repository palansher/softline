import json
import os
from typing import Dict
from pathlib import Path


class UserManager:
    """Класс для управления пользователями и их данными в JSON-файле."""

    def __init__(self, file_name: str = "users.json") -> None:
        """Инициализирует менеджер пользователей.

        Args:
            file_name (str): Имя файла JSON для хранения данных.
        """
        ## Чтобы сохранять josn файл в папку, где лажит main.py. Вместо сохранения в текущую папку.
        # Получаем абсолютный путь к папке, где находится текущий файл скрипта
        current_dir: Path = Path(__file__).resolve().parent

        # Объединяем путь к папке с именем файла
        self.file_path: Path = current_dir / file_name

        # Загружаем данные в память при старте
        self._users: dict[str, str] = self._load_data()

    def _load_data(self) -> Dict[str, str]:
        """Загружает данные из JSON файла.

        Returns:
            Dict[str, str]: Словарь {логин: пароль}.
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    def _save_data(self) -> None:
        """Сохраняет текущее состояние словаря пользователей в файл JSON."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self._users, f, ensure_ascii=False, indent=4)

    def user_exists(self, login: str) -> bool:
        """Проверяет, существует ли пользователь с таким логином.

        Args:
            login (str): Проверяемый логин.

        Returns:
            bool: True, если пользователь найден, иначе False.
        """
        return login in self._users

    def add_user(self, login: str, password: str) -> None:
        """Добавляет нового пользователя и сохраняет изменения.

        Args:
            login (str): Уникальный логин.
            password (str): Валидный пароль.
        """
        self._users[login] = password
        self._save_data()

    def update_password(self, login: str, new_password: str) -> bool:
        """Изменяет пароль существующего пользователя.

        Args:
            login (str): Логин пользователя.
            new_password (str): Новый пароль.

        Returns:
            bool: True, если пароль изменен, False, если пользователя нет.
        """
        if not self.user_exists(login):
            return False

        self._users[login] = new_password
        self._save_data()
        return True

    def get_all_logins(self) -> list[str]:
        """Возвращает список всех зарегистрированных логинов.

        Returns:
            list[str]: Список строк с именами пользователей.
        """
        return list(self._users.keys())
