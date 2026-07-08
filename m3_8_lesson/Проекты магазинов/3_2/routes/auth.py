from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, flash)
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login_val = request.form["login"].strip()
        password  = request.form["password"].strip()
        confirm   = request.form["password_confirm"].strip()
        phone     = request.form.get("phone", "").strip()

        errors = AuthService.validate_registration(login_val, password, confirm)
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("register.html", login=login_val, phone=phone)

        AuthService.register(login_val, password, phone)
        flash("Регистрация успешна! Войдите в систему.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_val = request.form["login"].strip()
        password  = request.form["password"].strip()

        user = AuthService.authenticate(login_val, password)
        if not user:
            flash("Неверный логин или пароль", "danger")
            return render_template("login.html", login=login_val)

        session["user_login"] = user["login"]
        session["user_id"]    = user["id"]
        session["role_id"]    = user["role_id"]
        flash(f"Добро пожаловать, {user['login']}!", "success")

        return redirect(
            url_for("admin.dashboard") if user["role_id"] == 1
            else url_for("shop.index")
        )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("shop.index"))
