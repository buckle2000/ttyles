def step(tty, i):
    tty.reset()
    for y in range(size[1]):
        for x in range(size[0]):
            digit = (x + y + i) % 16
            tty[x, y] = f"{tty.color(digit)}{digit:X}"

    l_cycle = -i % l_text

    tty.print(tty.normal)
    tty[l_x, l_y - 1] = ' ' * (l_text + 2)
    tty[l_x, l_y] = ' ' + TEXTTEXT[l_cycle:l_cycle + l_text] + ' '
    tty[l_x, l_y + 1] = ' ' * (l_text + 2)


if __name__ == "__main__":
    from time import sleep
    from itertools import cycle
    import os, sys
    sys.path.append(os.getcwd())
    from cligame import Terminal

    # config
    size = (40, 20)
    TEXT = ' Hello World!   '

    # calculate numbers
    TEXTTEXT = TEXT + TEXT
    l_text = len(TEXT)
    l_x = (size[0] - l_text) // 2 - 1
    l_y = size[1] // 2

    # setup tty
    tty = Terminal.from_std()
    tty.size = size

    # infinite loop
    for i in cycle(range(16 * l_text)):
        with tty.buffered():
            step(tty, i)
        sleep(0.1)
