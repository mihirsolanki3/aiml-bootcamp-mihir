# TASK 03
# Combinations with itertools

from itertools import combinations, permutations, product


# ---------------------------------------------------------
# 1. Generate every possible pair of students
# ---------------------------------------------------------

students = ["Mihir", "ravi", "aarav", "dev", "jeet"]

pairs = list(combinations(students, 2))

print("All possible pairs:")
for pair in pairs:
    print(pair)

print("\nNumber of pairs:", len(pairs))


# ---------------------------------------------------------
# 2. Generate every possible ordered pair
# ---------------------------------------------------------

ordered_pairs = list(permutations(students, 2))

print("\nAll possible ordered pairs:")
for pair in ordered_pairs:
    print(pair)

print("\nNumber of ordered pairs:", len(ordered_pairs))


# ---------------------------------------------------------
# 3. Product of shirt colours and sizes
# ---------------------------------------------------------

colours = ["red", "blue", "green"]
sizes = ["S", "M"]

shirt_combinations = list(product(colours, sizes))

print("\nShirt combinations:")
for shirt in shirt_combinations:
    print(shirt)

print("\nNumber of shirt combinations:", len(shirt_combinations))


# ---------------------------------------------------------
# 4. Every possible subset of dataset features
# ---------------------------------------------------------

features = ["age", "income", "height", "weight"]

all_subsets = []

for r in range(len(features) + 1):
    subsets = combinations(features, r)

    for subset in subsets:
        all_subsets.append(subset)

print("\nAll possible feature subsets:")

for subset in all_subsets:
    print(subset)

print("\nTotal number of feature subsets:", len(all_subsets))

