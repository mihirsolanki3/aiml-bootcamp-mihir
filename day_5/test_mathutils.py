from mathutils import average, biggest, is_prime

# -------------------------
# Tests for average()
# -------------------------


def test_average_basic():
    assert average([2, 4, 6]) == 4.0


def test_average_empty():
    assert average([]) == 0


def test_average_single_element():
    assert average([]) == 0.0


# -------------------------
# Tests for biggest()
# -------------------------


def test_biggest_basic():
    assert biggest([3, 9, 5, 2]) == 9


def test_biggest_empty():
    assert biggest([]) is None


def test_biggest_negative_numbers():
    assert biggest([-10, -5, -20]) == -5


# -------------------------
# Tests for is_prime()
# -------------------------


def test_is_prime_two():
    assert is_prime(2) is True


def test_is_prime_four():
    assert is_prime(4) is False


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_negative():
    assert is_prime(-7) is False


def test_is_prime_zero():
    assert is_prime(0) is False


def test_is_prime_large_prime():
    assert is_prime(17) is True
