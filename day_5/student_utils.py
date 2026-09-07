"""Provide utilities for calculating and evaluating student marks."""


def calculate_average(marks: list[int]) -> float:
    """Return the average mark for a student.

    Args:
        marks: A list of integer marks. May be empty.

    Returns:
        The average mark as a float, or 0.0 if the list is empty.
    """
    if not marks:
        return 0.0

    return sum(marks) / len(marks)


def calculate_grade(average: float) -> str:
    """Return a letter grade based on the average mark.

    Args:
        average: The student's average mark.

    Returns:
        The corresponding letter grade:
        A for 90 and above, B for 80-89, C for 70-79,
        D for 60-69, and F below 60.
    """
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"

    return "F"


def has_passed(average: float, passing_mark: float = 40.0) -> bool:
    """Return whether a student has achieved the passing mark.

    Args:
        average: The student's average mark.
        passing_mark: The minimum average required to pass.

    Returns:
        True if the average is greater than or equal to the
        passing mark, otherwise False.
    """
    return average >= passing_mark


def student_result(marks: list[int]) -> str:
    """Return a student's grade and pass or fail result.

    Args:
        marks: A list of integer marks. May be empty.

    Returns:
        A formatted result containing the average, grade,
        and pass/fail status.
    """
    average = calculate_average(marks)
    grade = calculate_grade(average)
    result = "Pass" if has_passed(average) else "Fail"

    return f"Average: {average:.2f}, Grade: {grade}, Result: {result}"
