# Day_2 
# Task_1
# Create student.py.
# Write a Student class with __init__ taking a name and a roll number, and storing an empty marks list.
# Add add_mark(score) that appends to the list.
# Add average() that returns the mean — and does not crash on a student with no marks.
# Add highest() and lowest().
# Create three students, give them marks, print each one's average.

class student:
    def __init__(self,name,rollno):
        self.name=name
        self.rollno=rollno
        self.marks=[]
        
    def add_mark(self,score):
        self.marks.append(score)   
        
    def avg(self):
        if len(self.marks)==0:
            return 0
        else:
            return sum(self.marks)/len(self.marks)
        
    def hightest(self):
        if len(self.marks)==0:
            return 0
        else:
            return max(self.marks)  

    def lowest(self):
            if len(self.marks)==0:
                return 0
            else:
                return min(self.marks)  
            
 
student1 = student("Mihir", 101)
student2 = student("Rahul", 102)
student3 = student("Amit", 103)

for mark in [80, 90, 85]:
    student1.add_mark(mark)

for mark in [70, 75, 80]:
    student2.add_mark(mark)

for mark in [90, 95, 88]:
    student3.add_mark(mark)

# Print details
for student in [student1, student2, student3]:
    print(student.name)
    print("Average:", student.avg())
    print("Highest:", student.hightest())
    print("Lowest:", student.lowest())
    print()
 