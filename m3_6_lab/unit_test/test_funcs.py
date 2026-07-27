from unittest import TestCase

# from funcs import get_div, get_mult, get_sum
from m3_6_lab.unit_test.funcs import get_div, get_mult, get_sum


class Test(TestCase):
    def test_get_sum(self):
        self.assertEqual(get_sum(2, 3), 5)
        self.assertEqual(get_sum(-2, -3), -5)
        self.assertEqual(get_sum(0, 0), 0)
        
            

    def test_get_mult(self):
        self.assertEqual(get_mult(2, 2), 4)
        self.assertEqual(get_mult(-2, -2), 4)
        self.assertEqual(get_mult(-2, 0), 0)

    def test_get_div(self):
        self.assertEqual(get_div(2, 2), 1)
