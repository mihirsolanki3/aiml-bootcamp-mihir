# Parent class
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, my name is {self.name}."


# Student inherits from Person
class Student(Person):
    def __init__(self, name, roll):
        super().__init__(name)
        self.roll = roll

    # Override greet() method
    def greet(self):
        return f"Hello, I am student {self.name}. My roll number is {self.roll}."


class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject


person = Person("Rahul")
student = Student("Mihir", 101)
teacher = Teacher("Aarav", "Python")


print(person.greet())
print(student.greet())
print(teacher.greet())

