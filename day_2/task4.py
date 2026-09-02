# TASK 04 - Take a for loop apart

numbers = [1, 2, 3]

it = iter(numbers)

print(next(it))
print(next(it))
print(next(it))

try:
    print(next(it))
except StopIteration:
    print("StopIteration error occurred")

print("\nUsing for loop:")
for x in [1, 2, 3]:
    print(x)

# Reproduce the for loop using iter(), next(), try/except and break
print("\nUsing iterator and while loop:")

it = iter([1, 2, 3])

while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break