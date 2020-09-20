#!/usr/bin/python3

import os
os.environ['TERM'] = 'xterm-256color'
from random import randint
from asciimatics.screen import Screen

flag = open('./flag.txt', 'r').read().strip()

def rainbow(screen):
    while True:
        msg = 'Welcome to DUCTF!'
        n = randint(0, 250)
        if n == 7:
            msg = flag
        screen.print_at(msg,
                        randint(0, screen.width), randint(0, screen.height),
                        colour=randint(0, screen.colours - 1),
                        bg=randint(0, screen.colours - 1))
        screen.refresh()

Screen.wrapper(rainbow)
