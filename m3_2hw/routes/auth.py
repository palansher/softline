from typing import Any
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from connect_db import connection

# Создаем Blueprint для авторизации и регистрации
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Any:
    """
    Handles user registration.
    Saves user email (in lowercase), password (hashed), full_name, phone, address.
    Assigns role_id = 0 (user) and creates a cart in the same transaction.
    """
    if session.get("user_email"):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email: str = request.form.get("email", "").strip().lower()
        password: str = request.form.get("password", "").strip()
        full_name: str = request.form.get("full_name", "").strip()
        phone: str = request.form.get("phone", "").strip()
        address: str = request.form.get("address", "").strip()

        if not email or not password or not full_name or not phone or not address:
            flash("Пожалуйста, заполните все поля формы.", "danger")
            return render_template("register.html")

        # Проверяем, существует ли уже пользователь с таким email
        sql_check = "SELECT id FROM users WHERE email = %s;"
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_check, (email,))
            user_exists = cursor.fetchone()

        if user_exists:
            flash("Пользователь с таким email уже зарегистрирован.", "danger")
            return render_template("register.html")

        password_hash: str = generate_password_hash(password)

        try:
            # Отключаем autocommit, чтобы выполнить обе вставки в одной транзакции
            connection.autocommit = False
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Вставляем пользователя
                sql_insert_user = """
                    INSERT INTO users (email, password_hash, full_name, phone, address, role_id)
                    VALUES (%s, %s, %s, %s, %s, 0)
                    RETURNING id;
                """
                cursor.execute(sql_insert_user, (email, password_hash, full_name, phone, address))
                user_id: int = cursor.fetchone()["id"]  # type: ignore

                # Создаем пустую корзину для этого пользователя
                sql_insert_cart = """
                    INSERT INTO carts (user_id)
                    VALUES (%s);
                """
                cursor.execute(sql_insert_cart, (user_id,))

            connection.commit()
            flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
            return redirect(url_for("auth.login"))
        except Exception:
            connection.rollback()
            flash("Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.", "danger")
            return render_template("register.html")
        finally:
            connection.autocommit = True

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Any:
    """
    Handles user authentication.
    Validates user credentials against password hash.
    Saves user_id, user_email (in lowercase), and role_id in session upon successful login.
    """
    if session.get("user_email"):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email: str = request.form.get("email", "").strip().lower()
        password: str = request.form.get("password", "").strip()

        if not email or not password:
            flash("Пожалуйста, заполните все поля.", "danger")
            return render_template("login.html")

        sql_user = "SELECT id, email, password_hash, role_id FROM users WHERE email = %s;"
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql_user, (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):  # type: ignore
            session["user_id"] = user["id"]  # type: ignore
            session["user_email"] = user["email"]  # type: ignore
            session["role_id"] = user["role_id"]  # type: ignore
            flash("Вы успешно вошли в систему!", "success")
            return redirect(url_for("catalog.catalog"))
        else:
            flash("Неверный email или пароль.", "danger")
            return render_template("login.html")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout() -> Any:
    """
    Logs out the user by clearing the session data.
    """
    session.clear()
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("main.index"))  # type: ignore
