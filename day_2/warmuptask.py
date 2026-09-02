class Calculator:

    def average(self, numbers):
        return sum(numbers) / len(numbers)


# Create an object
calc = Calculator()

# Example 1
numbers = [10, 20, 30, 40, 50]

result = calc.average(numbers)

print("Numbers:", numbers)
print("Average:", result)