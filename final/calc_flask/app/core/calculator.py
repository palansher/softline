import ast
import operator
from collections.abc import Callable

"""
присваивание, создающее псевдоним типа (Type Alias)
Чтобы не писать в аннотациях функций каждый раз конструкцию:

def add(self, a: int | float, b: int | float) -> int | float:
Мы один раз определяем Number = int | float и пишем лаконично:

def add(self, a: Number, b: Number) -> Number:
"""
Number = int | float

class CalculatorError(Exception):
    """Базовое исключение для ошибок калькулятора."""

    pass


class DivisionByZeroError(CalculatorError):
    """Исключение при попытке деления на ноль."""

    pass


class InvalidExpressionError(CalculatorError):
    """Исключение при некорректном математическом выражении."""

    pass


class Calculator:
    """Сервис вычислений калькулятора.

    Реализует основные математические операции и безопасное вычисление
    строковых математических выражений.
    """

    # Маппинг допустимых бинарных операций AST в функции
    _OPERATORS: dict[type[ast.operator], Callable[[Number, Number], Number]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def add(self, a: Number, b: Number) -> Number:
        """Сложение двух чисел."""
        return a + b

    def subtract(self, a: Number, b: Number) -> Number:
        """Вычитание двух чисел."""
        return a - b

    def multiply(self, a: Number, b: Number) -> Number:
        """Умножение двух чисел."""
        return a * b

    def divide(self, a: Number, b: Number) -> Number:
        """Деление двух чисел.

        Raises:
            DivisionByZeroError: Если делитель равен 0.
        """
        if b == 0:
            raise DivisionByZeroError("Деление на 0!.")
        return a / b

    def evaluate(self, expression: str) -> Number:
        """Безопасно вычисляет математическое выражение из строки.

        Args:
            expression: Строка с выражением, например "12.5 + 4 * 2"

        Returns:
            Числовой результат вычисления (int или float).

        Raises:
            InvalidExpressionError: При синтаксической ошибке или недопустимых символах.
            DivisionByZeroError: При делении на ноль.
        """
        clean_expr = expression.strip().replace("×", "*").replace("÷", "/")

        if not clean_expr:
            raise InvalidExpressionError("Пустое выражение!.")

        try:
            node = ast.parse(clean_expr, mode="eval").body
            result = self._eval_node(node)

            # Приведение к int, если число целое (10.0 -> 10)
            if isinstance(result, float) and result.is_integer():
                return int(result)

            return round(result, 8)
        except SyntaxError as err:
            raise InvalidExpressionError("Некорректное математическое выражение.") from err
        except CalculatorError:
            raise
        except Exception as err:
            raise InvalidExpressionError(f"Ошибка вычисления: {err}") from err

    def _eval_node(self, node: ast.AST) -> Number:
        """Рекурсивный разбор абстрактного синтаксического дерева (AST)."""
        match node:
            case ast.Constant(value=int(v) | float(v)):
                return v
            case ast.UnaryOp(op=ast.UAdd(), operand=sub_node):
                return +self._eval_node(sub_node)
            case ast.UnaryOp(op=ast.USub(), operand=sub_node):
                return -self._eval_node(sub_node)
            case ast.BinOp(left=left_node, op=op, right=right_node):
                op_type = type(op)
                if op_type not in self._OPERATORS:
                    raise InvalidExpressionError(f"Неподдерживаемый оператор: {op_type.__name__}")

                left_val = self._eval_node(left_node)
                right_val = self._eval_node(right_node)

                if op_type is ast.Div and right_val == 0:
                    raise DivisionByZeroError("Деление на 0!")

                return self._OPERATORS[op_type](left_val, right_val)
            case _:
                raise InvalidExpressionError("Выражение содержит недопустимые элементы.")
