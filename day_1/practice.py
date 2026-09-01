# Write a function that finds all the prime numbers up to N, and time how long it takes for N = 10000.


import time 

def find_primes(n:int)-> list[int]:
    primes=[]
     
    for num in range (2,n+1):
        is_prime=True
        
        for i in range(2,num):
            if num%i==0:
                is_prime=False
                break
        
        if is_prime:
            primes.append(num)
            
    return primes 

n=10000
start_time=time.time()
primes=find_primes(n)
end_time=time.time()
print("number of primes",len(primes)) 
print("first 10 primes :",primes[:10])
print("time taken :", end_time-start_time,"seconds")

# Explore the standard library: use collections.Counter to do word-counting in one line, and compare to your Task 5 version.

from collections import Counter 

text = "apple banana apple orange banana apple"

word_count=Counter(text.split())

print(word_count)


#Write a simple number-guessing game: the computer picks a number, you guess, it says higher/lower.
import random


def number_guessing_game() -> None:
    """Play a game where the user guesses a randomly selected number."""

    secret_number = random.randint(1, 100)

    print("Guess the number between 1 and 100!")

    while True:
        guess = int(input("Enter your guess: "))

        if guess < secret_number:
            print("Higher!")
        elif guess > secret_number:
            print("Lower!")
        else:
            print("Correct! You guessed the number.")
            break


number_guessing_game()