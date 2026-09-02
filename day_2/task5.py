# TASK 05 - Generators and yield

# 1. Fibonacci using a list
def fib_list(n):
    result = []

    a, b = 0, 1

    for _ in range(n):
        result.append(a)
        a, b = b, a + b

    return result


# 2. Fibonacci using a generator
def fib_gen(n):
    a, b = 0, 1

    for _ in range(n):
        print("about to yield", a)
        yield a
        a, b = b, a + b


# First 10 Fibonacci numbers using list
list_result = fib_list(10)
print("List:", list_result)


# First 10 Fibonacci numbers using generator
gen_result = fib_gen(10)
print("Generator:", list(gen_result))


# 3. Check the types
print("Type of fib_list:", type(fib_list(10)))

print("Type of fib_gen:", type(fib_gen(10)))


# 4. Use the same generator object twice
numbers = fib_gen(5)

print("\nFirst loop:")
for number in numbers:
    print(number)

print("\nSecond loop:")
for number in numbers:
    print(number)

# The second loop prints nothing because a generator is an iterator.
# Once all values have been generated, the generator is exhausted.
# It cannot be restarted or reused.


# 5. The print before yield shows when the generator code runs
print("\nTesting when yield runs:")

numbers = fib_gen(3)

print("Generator created")

print(next(numbers))
print("After first next()")

print(next(numbers))
print("After second next()")