# Part A — the ten problems
# TASK 01
# mihirSolanki

# functional_ten.py

from functools import reduce


# ============================================================
# TASK 01
# Given a list of numbers, return the squares of only the odd ones.
# ============================================================

nums = [1, 2, 3, 4, 5, 6]

# Loop version
out = []
for n in nums:
    if n % 2 == 1:
        out.append(n * n)

print("1. Loop:", out)

# Functional version
out = [n * n for n in nums if n % 2 == 1]

print("1. Functional:", out)

# I prefer the functional version because it is shorter and easier to read.


# ============================================================
# TASK 02
# Given a list of names, return them uppercased and stripped
# of whitespace.
# ============================================================

names = [" Mihir ", " Rahul", " Priya ", "Amit "]

# Loop version
out = []
for name in names:
    out.append(name.strip().upper())

print("2. Loop:", out)

# Functional version
out = list(map(lambda name: name.strip().upper(), names))

print("2. Functional:", out)

# I prefer the functional version because map clearly shows that we transform every name.


# ============================================================
# TASK 03
# Given two lists of equal length, return a list of their
# pairwise products.
# ============================================================

list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]

# Loop version
out = []
for i in range(len(list1)):
    out.append(list1[i] * list2[i])

print("3. Loop:", out)

# Functional version
out = list(map(lambda pair: pair[0] * pair[1], zip(list1, list2)))

print("3. Functional:", out)

# I prefer the functional version because zip and map express pairwise processing clearly.


# ============================================================
# TASK 04
# Given a list of words, return only those longer than 4 characters.
# ============================================================

words = ["apple", "cat", "banana", "dog", "python", "AI"]

# Loop version
out = []
for word in words:
    if len(word) > 4:
        out.append(word)

print("4. Loop:", out)

# Functional version
out = list(filter(lambda word: len(word) > 4, words))

print("4. Functional:", out)

# I prefer the functional version because filter directly represents selecting matching words.


# ============================================================
# TASK 05
# Given a list of numbers, find the product of all of them.
# Use reduce.
# ============================================================

nums = [1, 2, 3, 4, 5]

# Loop version
product = 1
for n in nums:
    product *= n

print("5. Loop:", product)

# Functional version
product = reduce(lambda a, b: a * b, nums)

print("5. Functional:", product)

# I prefer the functional version because reduce directly represents combining all values into one result.


# ============================================================
# TASK 06
# Given a list of dicts with a "price" key, return the total price.
# ============================================================

items = [
    {"name": "Pen", "price": 10},
    {"name": "Book", "price": 50},
    {"name": "Bag", "price": 500}
]

# Loop version
total = 0
for item in items:
    total += item["price"]

print("6. Loop:", total)

# Functional version
total = sum(map(lambda item: item["price"], items))

print("6. Functional:", total)

# I prefer the functional version because sum and map make the calculation concise.


# ============================================================
# TASK 07
# Given a nested list [[1,2],[3,4],[5]], flatten it to
# [1,2,3,4,5].
# ============================================================

nested = [[1, 2], [3, 4], [5]]

# Loop version
out = []
for sublist in nested:
    for item in sublist:
        out.append(item)

print("7. Loop:", out)

# Functional version
out = list(map(lambda item: item, [item for sublist in nested for item in sublist]))

print("7. Functional:", out)

# I prefer the loop version because flattening nested lists is clearer with explicit loops.


# ============================================================
# TASK 08
# Given a list of strings, return a dict mapping each string
# to its length.
# ============================================================

strings = ["apple", "cat", "python", "AI"]

# Loop version
out = {}
for string in strings:
    out[string] = len(string)

print("8. Loop:", out)

# Functional version
out = dict(map(lambda string: (string, len(string)), strings))

print("8. Functional:", out)

# I prefer the functional version because map directly creates key-value pairs.


# ============================================================
# TASK 09
# Given a list of mixed values, drop everything falsy.
# ============================================================

values = [0, 1, "", "hello", None, [], [1, 2], False, True]

# Loop version
out = []
for value in values:
    if value:
        out.append(value)

print("9. Loop:", out)

# Functional version
out = list(filter(None, values))

print("9. Functional:", out)

# I prefer the functional version because filter(None, values) is very concise and readable.


# ============================================================
# TASK 10
# Given a list of numbers, return the running total.
# [1,2,3] becomes [1,3,6].
# ============================================================

nums = [1, 2, 3]

# Loop version
out = []
total = 0

for n in nums:
    total += n
    out.append(total)

print("10. Loop:", out)

# Functional version
def running_total(nums):
    total = 0

    def add_to_total(n):
        nonlocal total
        total += n
        return total

    return list(map(add_to_total, nums))


out = running_total(nums)

print("10. Functional:", out)

# I prefer the loop version because maintaining a running state is clearer with a loop.