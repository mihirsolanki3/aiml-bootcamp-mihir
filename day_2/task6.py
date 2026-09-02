# TASK 06 - Read a big file without loading it

# Step 1: Create a file with 500,000 lines
with open("big.txt", "w") as f:
    for i in range(1, 500001):
        f.write(f"This is line {i} and it contains Python\n")


# Step 2: Read the file line by line
line_count = 0
python_count = 0

with open("big.txt", "r") as f:
    for line in f:
        line_count += 1

        if "Python" in line:
            python_count += 1


print("Total lines:", line_count)
print("Lines containing Python:", python_count)