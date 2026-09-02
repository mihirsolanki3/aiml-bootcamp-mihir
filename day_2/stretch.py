# 1. Add __eq__ to Student so two students with the same roll number compare equal. Then try putting them in aset — what breaks, and why? (Search: __hash__)

class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented

        return self.roll_no == other.roll_no


student1 = Student("Mihir", 101)
student2 = Student("Rahul", 101)

print(student1 == student2)


# Fix it with __hash__
class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented

        return self.roll_no == other.roll_no

    def __hash__(self):
        return hash(self.roll_no)


student1 = Student("Mihir", 101)
student2 = Student("Rahul", 101)

print(student1 == student2)

students = {student1, student2}

print(len(students))


# 2.Write a generator that reads your 500k-line file and yields only lines matching a condition. Chain it with another generator.

def read_matching_lines(filename, condition):
    """Read file and yield only lines matching the condition."""
    with open(filename, "r") as file:
        for line in file:
            if condition in line:
                yield line.strip()


def make_uppercase(lines):
    """Take lines from the first generator and yield them in uppercase."""
    for line in lines:
        yield line.upper()


# First generator
matching_lines = read_matching_lines("bigfile.txt", "Python")

# Chain it with the second generator
uppercase_lines = make_uppercase(matching_lines)

# Read the final results
for line in uppercase_lines:
    print(line)
    
# 3. Build a Classroom class that holds many Students. Give it __len__ so len(classroom) works, and make it iterable so for s in classroom works.

class Student:
    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no

    def __str__(self):
        return f"{self.roll_no} - {self.name}"


class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def __len__(self):
        return len(self.students)

    def __iter__(self):
        return iter(self.students)


# Create students
student1 = Student("Mihir", 101)
student2 = Student("Rahul", 102)
student3 = Student("Amit", 103)

# Create classroom
classroom = Classroom()

# Add students
classroom.add_student(student1)
classroom.add_student(student2)
classroom.add_student(student3)

# __len__ allows len(classroom)
print("Number of students:", len(classroom))

# __iter__ allows for s in classroom
print("Students:")

for s in classroom:
    print(s)
    
    
# 4. Read about @property. Convert average() into a property and decide whether you prefer it.

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    @property
    def average(self):
        return sum(self.marks) / len(self.marks)


student = Student("Mihir", [80, 90, 70])

print(student.average)

# 5. Find out what a generator expression is — (x*x for x in nums) versus [x*x for x in nums]. When would you use each?

# 1. List comprehension
nums = [1, 2, 3, 4, 5]

squares = [x * x for x in nums]

print(squares)

# 2. Generator expression
nums = [1, 2, 3, 4, 5]

squares = (x * x for x in nums)

print(squares)