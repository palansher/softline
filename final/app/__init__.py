from typing import Any

from flask import Flask, Response, jsonify, render_template, request

from app.core.calculator import Calculator, CalculatorError


def create_app() -> Flask:
    """Фабрика для создания и настройки веб-приложения Flask."""
    app = Flask(__name__)
    calc_service = Calculator()

    @app.route("/")
    def index() -> str:
        """Отображает главную страницу с калькулятором."""
        return render_template("index.html")

    @app.route("/api/calculate", methods=["POST"])
    def calculate() -> tuple[Response, int] | Response:
        """API эндпоинт для вычисления математических выражений."""
        data: dict[str, Any] | None = request.get_json()

        if not data or "expression" not in data:
            return jsonify({"status": "error", "message": "Отсутствует поле 'expression'"}), 400

        expression: str = str(data["expression"])

        try:
            result = calc_service.evaluate(expression)
            return jsonify({"status": "success", "result": result})
        except CalculatorError as err:
            """
            Перехватит и DivisionByZeroError, и InvalidExpressionError!
            Это гарантирует, что мы отловим только наши бизнес-ошибки вычислений и отдадим их пользователю в понятном виде,
            но при этом случайно не скроем критические системные сбои Python.
            """
            return jsonify({"status": "error", "message": str(err)}), 400

    return app
