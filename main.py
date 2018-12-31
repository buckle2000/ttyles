from itertools import count
from cligame import Terminal

tty = Terminal.from_std()
size = (40, 20)
tty.size = size

for i in range(700):
    for y in range(size[1] -1):
        for x in range(size[0]- 1):
            digit = (x + y + i) % 16
            tty[x, y] =  f"{tty.color(digit)}{digit:X}"
    tty.reset()
    tty.flush()
