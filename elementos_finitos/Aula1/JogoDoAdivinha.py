from random import randint
secret = randint(1, 10)
print('Welcome')
guess = 0
while True:
    guess = int(input('Guess: '))
    if guess == secret:
        print('You win!')
        break
    else:
        if guess > secret:
            print('Too high!')
        else:
            print('Too low!')
print('Game over!')
