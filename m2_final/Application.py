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
                        если пользователь отменил ввод (нажал Enter).
        """
        while True:
            # Выбор одной строкой: подсказка + действие по умолчанию (Enter)
            password: str = input(
                "Введите пароль (или нажмите Enter для отмены): "
            ).strip()

            # Если строка пустая — возврат без изменения
            if not password:
                print("Операция отменена пользователем.\n")
                return None

            score: int = PasswordValidator.calculate_score(password)

            if score <= 2:
                print(
                    f"Пароль отклонен. Он является слабым (Баллов: {score}/5)."
                )
                print("Попробуйте еще раз.\n")
                continue

            elif score in (3, 4):
                print(
                    f"Пароль набрал {score}/5 баллов. Его можно улучшить."
                )
                choice: str = (
                    input("Хотите повторить попытку ввода? (да/д/yes/y/нет): ")
                    .strip()
                    .lower()
                )
                if choice in ("да", "д", "yes", "y"):
                    print("Окей, давайте улучшим.\n")
                    continue
                else:
                    return password
            else:
                print("Отлично! Это сильный пароль (5 из 5).")
                return password

    def handle_add_user(self) -> None:
        """Логика добавления нового пользователя."""
        while True:
            # для отмены нажать Enter на пустом логине
            login: str = input(
                "Введите логин (или нажмите Enter для отмены): "
            ).strip()

            if not login:
                print("Регистрация отменена.\n")
                return  # Возврат в главное меню

            if self.user_manager.user_exists(login):
                print("Этот идентификатор уже существует. Выберите другой.\n")
                continue
            break

        # Вызываем ввод пароля
        password: str | None = self._request_valid_password()

        # ловит None от нажатия Enter
        if password is None:
            return

        self.user_manager.add_user(login, password)
        print(f"Пользователь '{login}' успешно добавлен.\n")

    def handle_change_password(self) -> None:
        """Логика изменения существующего пароля."""
        login: str = input(
            "Введите логин для смены пароля (или нажмите Enter для отмены): "
        ).strip()

        if not login:
            print("Смена пароля отменена.\n")
            return

        if not self.user_manager.user_exists(login):
            print("Ошибка: такого пользователя не существует.\n")
            return

        print(f"Пользователь '{login}' найден.")

        # Вызываем ввод пароля
        new_password: str | None = self._request_valid_password()

        # возвращает в главное меню если словили None от нажатия Enter
        if new_password is None:
            return

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
