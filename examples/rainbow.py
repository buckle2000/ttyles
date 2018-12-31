from colorama import Style

def step(tty, i):
    for y in range(size[1]):
        for x in range(size[0]):
            digit = (x + y + i) % 8
            tty[x, y] = f"\x1b[{30+digit}m{digit:X}" # foreground color + digit

    l_cycle = -i % l_text

    tty.write(Style.RESET_ALL)
    tty[l_x, l_y - 1] = ' ' * (l_text + 2)
    tty[l_x, l_y] = ' ' + TEXTTEXT[l_cycle:l_cycle + l_text] + ' '
    tty[l_x, l_y + 1] = ' ' * (l_text + 2)


if __name__ == "__main__":
    from time import sleep
    from itertools import cycle
    from ttyles import Terminal

    # config
    size = (40, 20)
    TEXT = '  Hello World!  '

    # calculate numbers
    TEXTTEXT = TEXT + TEXT
    l_text = len(TEXT)
    l_x = (size[0] - l_text) // 2 - 1
    l_y = size[1] // 2

    # setup tty
    tty = Terminal.from_std()
    tty.size = size

    # infinite loop in full-screen mode
    # disable input
    with tty.fullscreen(), tty.cbreak():
        try:
            for i in cycle(range(16 * l_text)):
                with tty.buffer():
                    step(tty, i)
                sleep(0.1)
        except KeyboardInterrupt:
            pass
