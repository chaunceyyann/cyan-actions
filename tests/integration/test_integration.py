from math_utils import add, multiply, divide
from src.math_utils import subtract


def test_complex_calculation():
    # (3*4) + (10/2) = 12 + 5 = 17
    assert add(multiply(3, 4), divide(10, 2)) == 17


def test_chained_operations():
    # (2+3) * (20/4) = 5 * 5 = 25
    assert multiply(add(2, 3), divide(20, 4)) == 25


def test_integration_add_subtract():
    result = add(5, 3)
    assert result == 8
    result = subtract(result, 3)
    assert result == 5


def test_integration_multiply():
    result = multiply(2, 3)
    assert result == 6
