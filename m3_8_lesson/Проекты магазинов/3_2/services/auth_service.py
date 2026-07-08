from werkzeug.security import generate_password_hash, check_password_hash
from models.user import UserModel


class AuthService:
    """Бизнес-логика регистрации и аутентификации."""

    @staticmethod
    def validate_registration(login: str, password: str,
                               confirm: str) -> list[str]:
        errors = []
        if len(login) < 3:
            errors.append("Логин должен быть не менее 3 символов")
        if len(password) < 6:
            errors.append("Пароль должен быть не менее 6 символов")
        if password != confirm:
            errors.append("Пароли не совпадают")
        if UserModel.login_exists(login):
            errors.append("Пользователь с таким логином уже существует")
        return errors

    @staticmethod
    def register(login: str, password: str, phone: str = "") -> None:
        hashed = generate_password_hash(password)
        UserModel.create(login, hashed, phone)

    @staticmethod
    def authenticate(login: str, password: str):
        """Возвращает пользователя или None."""
        user = UserModel.find_by_login(login)
        if user and check_password_hash(user["pass"], password):
            return user
        return None
