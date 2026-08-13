import pytest
from app.core.calculator import Calculator, DivisionByZeroError, InvalidExpressionError


@pytest.fixture
def calc() -> Calculator:
    """Фикстура создания экземпляра калькулятора перед каждым тестом."""
    return Calculator()


def test_basic_arithmetic(calc: Calculator) -> None:
    """Тестирование базвых методов класса."""
    assert calc.add(10, 5) == 15
    assert calc.subtract(10, 4) == 6
    assert calc.multiply(3, 4) == 12
    assert calc.divide(20, 4) == 5.0


def test_division_by_zero_method(calc: Calculator) -> None:
    """Тестирование выброса исключения при делении на 0."""
    with pytest.raises(DivisionByZeroError):
        calc.divide(10, 0)


def test_evaluate_expressions(calc: Calculator) -> None:
    """Тестирование безопасного вычисления сложных выражений."""
    assert calc.evaluate("2 + 2") == 4
    assert calc.evaluate("10 - 4 * 2") == 2
    assert calc.evaluate("10 + 20 / 4") == 15
    assert calc.evaluate("12.5 + 2.5") == 15


def test_evaluate_division_by_zero(calc: Calculator) -> None:
    """Тестирование деления на ноль внутри выражения."""
    with pytest.raises(DivisionByZeroError):
        calc.evaluate("15 / 0")


def test_evaluate_invalid_expression(calc: Calculator) -> None:
    """Тестирование некорректного синтаксиса."""
    with pytest.raises(InvalidExpressionError):
        calc.evaluate("2 ++ 3 *")
