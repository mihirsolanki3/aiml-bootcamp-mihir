# day_5
# Software Engineering Habits & Week 1 Deliverable

# ---------------------------------------------------------

# Task_01


# def average(nums):
#     """Return the average of a list of numbers.

#     Return 0 for an empty list.
#     """
#     if not nums:
#         return 0

#     return sum(nums) / len(nums)


# def biggest(nums):
#     """Return the biggest number in the list.

#     Return None for an empty list.
#     """
#     if not nums:
#         return None

#     return max(nums)


# def is_prime(n):
#     """Return True if n is a prime number."""
#     if n < 2:
#         return False

#     for i in range(2, int(n**0.5) + 1):
#         if n % i == 0:
#             return False

#     return True


# ---------------------------------------------------------

# TAsk_02

# """Provide basic mathematical utility functions."""


# def average(nums: list[float]) -> float:
#     """Return the mean of a list of numbers.

#     Args:
#         nums: A list of numbers. May be empty.

#     Returns:
#         The mean as a float, or 0.0 if the list is empty.
#     """
#     if not nums:
#         return 0.0

#     return sum(nums) / len(nums)


# def biggest(nums: list[float]) -> float | None:
#     """Return the biggest number in a list.

#     Args:
#         nums: A list of numbers. May be empty.

#     Returns:
#         The biggest number, or None if the list is empty.
#     """
#     if not nums:
#         return None

#     return max(nums)


# def is_prime(n: int) -> bool:
#     """Return whether a number is prime.

#     Args:
#         n: An integer to check for primality.

#     Returns:
#         True if n is prime, otherwise False. Numbers less than 2
#         are not considered prime.
#     """
#     if n < 2:
#         return False

#     for i in range(2, int(n**0.5) + 1):
#         if n % i == 0:
#             return False

#     return True


# --------------------------------------------------------------

# Task_03 / TAsk_04


"""Provide basic mathematical utility functions."""


def average(nums: list[int]) -> float:
    if not nums:
        return 0.0
    return sum(nums) / len(nums)


def biggest(nums: list[int]) -> int | None:
    """Return the biggest number in a list.

    Args:
        nums: A list of integers. May be empty.

    Returns:
        The biggest integer, or None if the list is empty.
    """
    if not nums:
        return None

    return max(nums)


def is_prime(n: int) -> bool:
    """Return whether a number is prime.

    Args:
        n: An integer to check for primality.

    Returns:
        True if n is prime, otherwise False. Numbers less than 2
        are not considered prime.
    """
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


# ------------------------------------------------------------

# Task_04
