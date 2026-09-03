# Part C — put it together
# TASK 05
# collections bake-off

from collections import defaultdict, namedtuple, deque, Counter


# =========================================================
# 1. defaultdict
# Group employees by department
# =========================================================

employees = [
    ("IT", "Mihir"),
    ("HR", "Aarav"),
    ("IT", "Ravi"),
    ("Finance", "Jeet"),
    ("HR", "Suresh"),
    ("Finance", "Dev"),
]

departments = defaultdict(list)

for department, employee in employees:
    departments[department].append(employee)

print("Employees by department:")

for department, employees_list in departments.items():
    print(department, ":", employees_list)

# No KeyError checks are needed.
# If a department does not exist, defaultdict automatically
# creates an empty list for it.


# =========================================================
# 2. namedtuple
# Give names to tuple fields
# =========================================================

Person = namedtuple("Person", ["name", "age", "city"])

people = [
    Person("Asha", 21, "Ahmedabad"),
    Person("Ravi", 22, "Mumbai"),
    Person("Meera", 20, "Delhi"),
]

print("\nPeople:")

for p in people:
    print(p)


# Accessing data using indexes:
print("\nUsing index:")
print(people[0][2])


# Accessing data using the field name:
print("\nUsing named field:")
print(people[0].city)


# p.city is easier to understand than p[2].
# p.city clearly tells us that we are accessing the city.
# p[2] only tells us that we are accessing the third item.

# =========================================================
# 3. deque
# Last 5 searches history
# =========================================================

history = deque(maxlen=5)

searches = [
    "python",
    "django",
    "pandas",
    "numpy",
    "machine learning",
    "data analysis",
]

for search in searches:
    history.append(search)
    print("\nAfter searching:", search)
    print("History:", list(history))


# maxlen=5 automatically keeps only the last 5 items.
# When the 6th search is added, the oldest search
# automatically drops off.

# =========================================================
# 4. Counter
# Find common and unique words in two texts
# =========================================================

text1 = "python is easy and python is powerful"
text2 = "python is powerful and python is popular"

# Convert text into words
words1 = text1.lower().split()
words2 = text2.lower().split()

# Count words in each text
c1 = Counter(words1)
c2 = Counter(words2)

print("\nText 1 word counts:")
print(c1)

print("\nText 2 word counts:")
print(c2)

# Words common to both texts

common_words = c1 & c2

print("\nWords common to both:")
print(common_words)

# Words appearing in text1 but not text2

only_text1 = c1 - c2

print("\nWords only in text 1:")
print(only_text1)

# Words appearing in text2 but not text1

only_text2 = c2 - c1

print("\nWords only in text 2:")
print(only_text2)

# Counter | operator

all_words = c1 | c2

print("\nMaximum count of each word:")
print(all_words)