#!/usr/bin/env python3
from os import urandom
from random import randint

print('Welcome! As you may know, guessing is one of the most important skills in CTFs and in life in general. This game is designed to train your guessing skills so that you\'ll be able to solve any CTF challenge after enough practice. Good luck!\n')

class LCG:
    M = 937954372991277727569919570466170502903005281412586514689603
    a = randint(2, M-1)
    c = randint(2, M-1)
    print(f'M = {M}')
    print(f'a = {a}')
    trunc = 20

    def __init__(self, x0):
        self.x = x0

    def next(self):
        self.x = (self.a * self.x + self.c) % self.M
        return ((self.x % 2**self.trunc) << self.trunc) + (self.x >> (self.M.bit_length() - self.trunc))

NUM_GUESSES = 5 # higher chances of winning!!
rng = LCG(int(urandom(25).hex(), 16))
wins = 0

for r in range(1, 24):
    try:
        num = rng.next()
        print('Round ' + str(r) + '. What\'s the lucky number? ')
        guesses = [int(guess) for guess in input().split(' ')[:NUM_GUESSES]]
        if any(guess == num for guess in guesses):
            print('Nice guess! The number was', num)
            wins += 1
        else:
            print('Unlucky! The number was', num)
    except ValueError:
        print('Please enter your three numbers separated by spaces next time! e.g. 123 1337 999')
        exit()

if wins > 10:
    print('YOU WIN! Your guessing skills are superb. Here\'s the flag:', open('flag.txt', 'r').read().strip())
else:
    print('Better luck next time :(')
