from src.math_utils import add, multiply, divide

def test_complex_calculation():
    # (3*4) + (10/2) = 12 + 5 = 17
    assert add(multiply(3, 4), divide(10, 2)) == 17

def test_chained_operations():
    # (2+3) * (20/4) = 5 * 5 = 25
    assert multiply(add(2, 3), divide(20, 4)) == 25 