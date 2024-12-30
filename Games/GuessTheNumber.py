import random

number = random.randint(1,100)
print("Guess the number between 1 and 100")

while True:
    guess = int(input("Your guess: "))
    if guess == number:
        print("Congrats! U guessed it!")
        break
    elif guess < number:
        print("too low! hint: the number is greater than ",guess)
    else:
        print("too high! hint: the number is less than ",guess)
