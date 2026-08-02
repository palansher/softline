# Routes package initialization

# Вынес зависимости сюда ради упрощения app.py

from .main import main_bp
from .auth import auth_bp
from .catalog import catalog_bp
from .cart import cart_bp
from .admin import admin_bp

# определяем специальный список __all__, в котором перечисляем  строки с именами объектов, доступных для экспорта из этого пакета.
# Это типа явный стандарт в Python-разработке.

__all__ = [
    "main_bp",
    "auth_bp",
    "catalog_bp",
    "cart_bp",
    "admin_bp",
]
