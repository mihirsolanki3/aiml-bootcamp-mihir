# Clear and readable version
print("\nClear and readable version\n")
for i in range(1, 101):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
        
# FizzBuzzBazz — Add 7 (if/elif version)
print("FizzBuzzBazz — Add 7 (if/elif version)")
for i in range(1, 101):
    if i % 105 == 0:
        print("FizzBuzzBazz")
    elif i % 15 == 0:
        print("FizzBuzz")
    elif i % 21 == 0:
        print("FizzBazz")
    elif i % 35 == 0:
        print("BuzzBazz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    elif i % 7 == 0:
        print("Bazz")
    else:
        print(i)        
        
        

# Compact comprehension version
print("Compact comprehension version")
result = [
    "FizzBuzzBazz" if i % 105 == 0
    else "FizzBuzz" if i % 15 == 0
    else "FizzBazz" if i % 21 == 0
    else "BuzzBazz" if i % 35 == 0
    else "Fizz" if i % 3 == 0
    else "Buzz" if i % 5 == 0
    else "Bazz" if i % 7 == 0
    else str(i)
    for i in range(1, 101)
]

print("\n".join(result))