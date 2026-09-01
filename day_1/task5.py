def reversed (sentence):
    words = sentence.split()
    reversed_words = words[::-1]
    return reversed_words

sentence = "the cat sat"
result = reversed(sentence)
print(result)


# Write a function that counts how many times each word appears in a sentence (return a dict).
def wordcount(sentence):
    words = sentence.split()
    
    count={}
    
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
            
    return count

sentence = "the cat sat on the mat"
result = wordcount(sentence)
print(result)


# Given a list of numbers, use a comprehension to return only the even ones, each doubled.
number=[1,2,3,4,5,6,7,8,9,10]
evennumber=[]
evennumberdubbled=[]

for i in number:
    if i%2==0:
        i=i*2
        print("even number :",i)


# Given a list with duplicates, return the unique items, sorted.
numbers = [5, 2, 8, 2, 5, 1, 8, 3]

result = sorted(set(numbers))

print(result)


# Write one that checks if a word is a palindrome (reads the same backwards).

word = "RAR"

if word == word[::-1]:
    print(word,"is a Palindrome")
else:
    print(word,"is Not a palindrome")