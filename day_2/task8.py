def class_average(students, passing=40):
    total = 0
    passed = 0

    for s in students:
        breakpoint()

        # Bug 1: total was overwritten with = instead of accumulated.
        # pdb showed total becoming 88, 92, 79, then 40.
        total += s["marks"]

        # Bug 2: > rejected Dev because 40 > 40 is False.
        # pdb showed Dev's marks=40 and passing=40.
        # >= means exactly 40 is also a passing score.
        if s["marks"] >= passing:
            passed += 1

    average = total / len(students)

    # Bug 3: the original wrong total caused the average to be wrong.
    # After pdb revealed total was being overwritten, accumulating it
    # gives 299, so the average is 299 / 4 = 74.75.
    pass_rate = passed / len(students) * 100

    return average, pass_rate


data = [
    {"name": "asha",  "marks": 88},
    {"name": "ravi",  "marks": 92},
    {"name": "meera", "marks": 79},
    {"name": "dev",   "marks": 40},
]

avg, rate = class_average(data)

print(f"average: {avg}")
print(f"pass rate: {rate}%")