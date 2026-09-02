class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll
        self.marks = []

    def add_mark(self, score):
        self.marks.append(score)

    def average(self):
        if len(self.marks) == 0:
            return 0
        return sum(self.marks) / len(self.marks)

    # Used by print(student)
    def __str__(self):
        return f"{self.name} (Roll No: {self.roll})"

    # Used when the object is inside a list
    def __repr__(self):
        return f"Student(name='{self.name}', roll={self.roll})"


# Create students
s1 = Student("Mihir", 101)
s2 = Student("Rahul", 102)

# Add marks
s1.add_mark(85)
s1.add_mark(90)

s2.add_mark(78)
s2.add_mark(88)


# Using __str__
print("Individual students:")
print(s1)
print(s2)


# Using __repr__ inside a list
students = [s1, s2]

print("\nStudents inside a list:")
print(students)