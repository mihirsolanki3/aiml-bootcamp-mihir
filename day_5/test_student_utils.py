from student_utils import (
    calculate_average,
    calculate_grade,
    has_passed,
    student_result,
)

# -------------------------
# calculate_average()
# -------------------------


def test_calculate_average_basic():
    assert calculate_average([70, 80, 90]) == 80.0


def test_calculate_average_empty():
    assert calculate_average([]) == 0.0


def test_calculate_average_single_mark():
    assert calculate_average([75]) == 75.0


# -------------------------
# calculate_grade()
# -------------------------


def test_calculate_grade_a():
    assert calculate_grade(95) == "A"


def test_calculate_grade_b():
    assert calculate_grade(85) == "B"


def test_calculate_grade_c():
    assert calculate_grade(75) == "C"


def test_calculate_grade_d():
    assert calculate_grade(65) == "D"


def test_calculate_grade_f():
    assert calculate_grade(50) == "F"


def test_calculate_grade_zero():
    assert calculate_grade(0) == "F"


# -------------------------
# has_passed()
# -------------------------


def test_has_passed():
    assert has_passed(60) is True


def test_has_passed_exact_boundary():
    assert has_passed(40) is True


def test_has_failed():
    assert has_passed(39) is False


# -------------------------
# student_result()
# -------------------------


def test_student_result_pass():
    assert student_result([80, 90, 100]) == ("Average: 90.00, Grade: A, Result: Pass")


def test_student_result_fail():
    assert student_result([20, 30, 30]) == ("Average: 26.67, Grade: F, Result: Fail")


def test_student_result_empty():
    assert student_result([]) == "Average: 0.00, Grade: F, Result: Fail"
