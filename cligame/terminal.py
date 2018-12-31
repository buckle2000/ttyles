# TODO cached API (like vdom diff)
#      tty.cached[x, y] = str((x + y + i) % 10)

# TODO delete self._fin or do something with stdin

import blessings
from typing import TextIO


class Terminal:
    @classmethod
    def from_std(cls):
        import sys
        return cls(fin=sys.stdin, fout=sys.stdout)
    
    def __init__(self, fin: TextIO, fout: TextIO):
        self._fin = fin
        self._fout = fout
        self._bless = blessings.Terminal(stream=fout, force_styling=True)
        self._buffer = dict()

    def print(self, s: str):        
        self._fout.write(s)

    @property
    def size(self) -> (int, int) or (None, None):
        h, w = self._bless._height_and_width()
        return w, h

    @size.setter
    def size(self, value: (int, int)):
        """Set size of terminal with escape string"""
        self.print("\x1b[8;{rows};{cols}t".format(
            rows=value[1], cols=value[0]))

    cursor: (int, int) = property()

    @cursor.setter
    def cursor(self, value: (int, int)):
        """Set location of cursor"""
        self.print(self._bless.move(value[1], value[0]))

    def at(self, *args):
        """Move cursor to location, do something, then move cursor back"""
        return self._bless.location(*args)

    def __setitem__(self, location, c: str):
        """Write character to buffer at certain location"""
        self._buffer[location] = c

    def flush(self):
        self.print(self._bless.save)
        for location, c in self._buffer.items():
            self.cursor = location
            self.print(c)
        self.print(self._bless.restore)
        self._buffer.clear()

    def clear(self):
        """Clear screen, scroll down"""
        self.print(self._bless.clear)

    def reset(self):
        """Reset terminal"""
        self.print('\x1bc')

    def __getattr__(self, name):
        """Proxy to helpers in blessings"""
        return getattr(self._bless, name)
