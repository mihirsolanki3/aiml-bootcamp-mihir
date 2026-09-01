# Write a calculate_stats(numbers) function that returns the min, max, mean, and count — as a dict.

"""Return the minimum, maximum, mean, and count of numbers."""
def calculate_stats(num):
    stats={"min" : min(num),
           "max": max(num),
           "mean": sum(num)/len(num),
           "count": len(num)
           }
    
    return stats
    
numbers = [1, 2, 3, 4, 5]   
print(calculate_stats(numbers))    


# Give it a sensible default or a clear error when handed an empty list (don't let it crash).
def calculate_stats(numbers):
    if not numbers:
        return {
            "min": None,
            "max": None,
            "mean": 0,
            "count": 0
        }

    return {
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
        "count": len(numbers)
    }


print(calculate_stats([10, 20, 30]))
print(calculate_stats([]))


#Write a safe_divide(a, b) that handles division by zero gracefully with try/except.
"""Divide two numbers and handle division by zero."""
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"


a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Result:", safe_divide(a, b))


# Add type hints to all your functions.
"""Return True if the given number is even."""
def is_even(number: int) -> bool:
    return number % 2 == 0

print(is_even(10))