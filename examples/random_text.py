from time import sleep
from ttyles import Terminal
from random import choice, randrange

charset = '1234567890)(*&^%$#@!;:",./?><{}[]|'

# create terminal with stdout
tty = Terminal.from_std()

# set size of terminal
width, height = 80, 1
tty.size = (width, height)

# clear screen
tty.clear()

# print a bunch of random characters
row = [choice(charset) for _ in range(width)]
tty[0, 0] = ''.join(row)

for i in range(100):
    # print random character at random position
    tty[randrange(width), 0] = choice(charset)
    sleep(0.01)

tty.print('\n')
