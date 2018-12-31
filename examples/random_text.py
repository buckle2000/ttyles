from time import sleep
from ttyles import Terminal
from random import choice

tty = Terminal.from_std() # create terminal with stdout

width, height = 80, 1
tty.size = (width, height) # set size of terminal

charset = '1234567890)(*&^%$#@!;:",./?><{}[]|'

for i in range(100):
    tty.reset() # reset (RIS) terminal
    row = [choice(charset) for _ in range(width)]
    tty[0, 0] = ''.join(row) # print text at (0, 0)
    sleep(0.1)
