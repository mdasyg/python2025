import pygame
import random
import math

random.seed()
x=random.random()
print("Random number:", x)
y=math.floor(x*100)+1
print("The number to guess is:", y)
counter=0
guess=0

while guess!=y:
    guess=input("Enter your guess (1-100): ")
    guess=int(guess)
    counter+=1
    if guess<y:
        print("Too low! Try again.")
    elif guess>y:
        print("Too high! Try again.")
    else:
        print(f"Congratulations! You've guessed the number {y} in {counter} attempts.")



