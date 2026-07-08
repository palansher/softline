from functools import wraps
from flask import session, flash, redirect, url_for
from models.user import UserModel


def login_required(f):
    """Редиректит неавторизованных пользователей на /login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_login" not in session:
            flash("Необходимо войти в систему", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Разрешает доступ только администраторам."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_login" not in session:
            flash("Необходимо войти в систему", "warning")
            return redirect(url_for("auth.login"))
        user = UserModel.find_by_login(session["user_login"])
        if not user or user["role_id"] != 1:
            flash("У вас нет прав администратора!", "danger")
            return redirect(url_for("shop.index"))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    """Возвращает текущего авторизованного пользователя или None."""
    if "user_login" not in session:
        return None
    return UserModel.find_by_login(session["user_login"])
