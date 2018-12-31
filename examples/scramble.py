import re
from time import sleep
from ttyles import Terminal
from random import choice, randrange

REGEX_NUMBER = re.compile(r'\d+')
CHARSET = '1234567890)(*&^%$#@!;:",./?><{}[]|                '

seen = set()

# create terminal with stdout
tty = Terminal.from_std()

# set size of terminal
width, height = tty.width or 80, 1
tty.size = (width, height)

# row of characters
row = [choice(CHARSET) for _ in range(width)]

try:
    tty.move(0, 1)
    while True:
        # set random position in row to random character
        index = randrange(width)
        c = choice(CHARSET)
        row[index] = c

        # print a bunch of random characters at 0, 0
        text = ''.join(row)
        with tty.buffer():
            with tty.at(0, 0):
                tty.print(text)
            for match in REGEX_NUMBER.finditer(text):
                number = match[0]
                if number not in seen:
                    tty.print(number + ' ')
                    seen.add(number)
        sleep(0.001)
except:
    tty.clear()
    raise
