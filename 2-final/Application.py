from password_validator import PasswordValidator
from user_manager import UserManager

class Application:
    """Главный класс приложения, отвечающий за интерфейс и меню."""

    def __init__(self) -> None:
        """Инициализирует компоненты приложения."""
        self.user_manager = UserManager()

    def _request_valid_password(self) -> str | None:
        """Внутренний метод для интерактивного ввода и валидации пароля.

        Returns:
            str | None: Возвращает одобренный пароль или None,
                        если пользователь отказался дорабатывать пароль.
        """
        while True:
            password: str = input("Введите пароль: ")
            score: int = PasswordValidator.calculate_score(password)

            if score <= 2:
                print(f"Пароль отклонен. Он является слабым (Баллов: {score}/5).")
                print("Попробуйте еще раз.\n")
                continue

            elif score in (3, 4):
                print(f"Пароль набрал {score}/5 баллов. Его можно улучшить.")
                choice: str = (
                    input("Хотите повторить попытку ввода? (да/нет): ").strip().lower()
                )
                if choice in ("да", "yes", "д", "y"):
                    print("Окей, давайте улучшим.\n")
                    continue
                else:
                    # Пользователь отказался улучшать, пароль принимается
                    return password
            else:
                print("Отлично! Это сильный пароль (5 из 5).")
                return password

    def handle_add_user(self) -> None:
        """Логика добавления нового пользователя."""
        while True:
            login: str = input("Введите идентификатор пользователя (логин): ").strip()
            if not login:
                print("Логин не может быть пустым.\n")
                continue

            if self.user_manager.user_exists(login):
                print("Этот идентификатор уже существует. Выберите другой.\n")
                continue
            break

        password: str | None = self._request_valid_password()
        if password:
            self.user_manager.add_user(login, password)
            print(f"Пользователь '{login}' успешно добавлен.\n")

    def handle_change_password(self) -> None:
        """Логика изменения существующего пароля."""
        login: str = input("Введите логин пользователя для смены пароля: ").strip()

        if not self.user_manager.user_exists(login):
            print("Ошибка: такого пользователя не существует.\n")
            return

        print(f"Пользователь '{login}' найден. Введите новый пароль.")
        new_password: str | None = self._request_valid_password()

        if new_password:
            self.user_manager.update_password(login, new_password)
            print(f"Пароль для пользователя '{login}' успешно обновлен.\n")

    def handle_show_users(self) -> None:
        """Вывод списка логинов без паролей."""
        logins = self.user_manager.get_all_logins()

        if not logins:
            print("Список пользователей пуст.\n")
            return

        print("\n--- Список пользователей ---")
        for login in logins:
            print(f"- {login}")
        print("---------------------------\n")

    def run(self) -> None:
        """Запуск главного цикла приложения."""
        while True:
            print("Программа управления аккаунтами. Меню:")
            print("1) Добавить пользователя")
            print("2) Изменить пароль")
            print("3) Вывести пользователей")
            print("4) Выход")

            choice: str = input("Выберите пункт меню (1-4): ").strip()

            if choice == "1":
                self.handle_add_user()
            elif choice == "2":
                self.handle_change_password()
            elif choice == "3":
                self.handle_show_users()
            elif choice == "4":
                print("Программа завершена. До свидания!")
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите число от 1 до 4.\n")
