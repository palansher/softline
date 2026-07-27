"""Unit-тесты для функции get_sum из модуля funcs."""

import unittest

from m3_6_lab.unit_test.funcs import get_div, get_mult, get_sum


class TestGetSum(unittest.TestCase):
    """Тесты для функции сложения двух чисел."""

    def test_positive_numbers(self) -> None:
        """Проверка сложения положительных чисел."""
        self.assertEqual(get_sum(2, 3), 5)

    def test_negative_numbers(self) -> None:
        """Проверка сложения отрицательных чисел."""
        self.assertEqual(get_sum(-1, -1), -2)

    def test_mixed_numbers(self) -> None:
        """Проверка сложения положительных и отрицательных чисел."""
        self.assertEqual(get_sum(-1, 1), 0)

    def test_with_zero(self) -> None:
        """Проверка сложения с нулём."""
        self.assertEqual(get_sum(0, 5), 5)
        self.assertEqual(get_sum(5, 0), 5)

    def test_floats(self) -> None:
        """Проверка сложения дробных чисел."""
        self.assertAlmostEqual(get_sum(0.1, 0.2), 0.3)


"""Unit-тесты для функции get_div из модуля funcs."""


class TestGetDiv(unittest.TestCase):
    """Тесты для функции деления двух чисел."""

    def test_positive_numbers(self) -> None:
        """Проверка деления положительных чисел."""
        self.assertEqual(get_div(10, 2), 5)

    def test_negative_numbers(self) -> None:
        """Проверка деления отрицательных чисел."""
        self.assertEqual(get_div(-10, -2), 5)

    def test_mixed_signs(self) -> None:
        """Проверка деления чисел с разными знаками."""
        self.assertEqual(get_div(10, -2), -5)

    def test_float_result(self) -> None:
        """Проверка деления, дающего дробный результат."""
        self.assertAlmostEqual(get_div(7, 3), 2.333333, places=4)

    def test_division_by_zero(self) -> None:
        """Проверка, что деление на ноль выбрасывает ValueError."""
        with self.assertRaises(ValueError):
            get_div(10, 0)


class TestGetMult(unittest.TestCase):
    """Тесты для функции умножения двух чисел."""

    def test_positive_numbers(self) -> None:
        self.assertEqual(get_mult(2, 3), 6)

    def test_with_zero(self) -> None:
        self.assertEqual(get_mult(5, 0), 0)

"""
Этот блок позволяет запустить файл с тестами как обычный Python-скрипт из терминала:
python m3_6_lab/unit_test/test_funcs_my.py
Переменная __name__ внутри любого файла Python содержит имя модуля. Но если вы запускаете файл напрямую, Python присваивает ей значение "__main__".
Функция unittest.main() сама находит все классы-наследники TestCase в файле и запускает их тесты.
"""

if __name__ == "__main__": # pragma: no cover
    unittest.main()
    
"""
Спецкомментарий # pragma: no cover говорит анализатору покрытия: "Игнорируй эту секцию, не учитывай её в статистике".
"""
    
