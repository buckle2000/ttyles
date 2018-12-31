# TODO delete self._fin or do something with stdin

import sys, blessed
from types import MethodType
from typing import TextIO, List, Tuple
from contextlib import contextmanager

Coord = Tuple[int, int]


class Terminal:
    """This class represents a terminal that wraps an output stream."""

    @classmethod
    def from_std(cls) -> 'Terminal':
        return cls(fin=sys.stdin, fout=sys.stdout)

    def __init__(self, fin: TextIO, fout: TextIO):
        self._fin = fin
        self._fout = fout
        self._bless = blessed.Terminal(stream=fout, force_styling=True)
        self._buffer = dict()

    ##############
    # Properties #
    ##############

    size: Coord = property(doc="size of the terminal")

    @size.getter
    def size(self):
        """Get current size of the terminal."""
        h, w = self._bless._height_and_width()
        return w, h

    @size.setter
    def size(self, value):
        """Resize terminal"""
        self.print("\x1b[8;{rows};{cols}t".format(
            rows=value[1], cols=value[0]))

    cursor: Coord = property(doc="cursor position")

    @cursor.setter
    def cursor(self, value):
        """Move cursor."""
        self.move(*value)

    ###########
    # Methods #
    ###########
    def move(self, x: int, y: int) -> None:
        """Move cursor."""
        self.print(self._bless.move(y, x))

    def print(self, s: str, flush=True) -> None:
        """Print text, flush output by default."""
        self._fout.write(s)
        if flush:
            self.flush()

    def __setitem__(self, location, c: str):
        """Write character to buffer at certain location."""
        self.move(*location)
        self.print(c)

    def clear(self) -> None:
        """Clear screen, then scroll down."""
        self.print(self._bless.clear)

    def reset(self) -> None:
        """Reset terminal."""
        self.print('\x1bc')
        
    def flush(self):
        """Flush output."""
        return self._fout.flush()

    def __getattr__(self, name):
        """Proxy function to __getattr__ of 'blessed.Terminal'."""
        param_s = getattr(self._bless, name)
        if len(param_s) == 0:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return param_s

    ####################
    # Context managers #
    ####################

    def at(self, *args):
        """Context manager for temporarily moving the cursor."""
        return self._bless.location(*args)

    @contextmanager
    def buffer(self) -> List[str]:
        """
        Context manager for buffering output.
        
        Returns a list a strings, which is used internally as buffer.
        """
        _buffer = []

        def buffered_print(self, s: str):
            nonlocal _buffer
            _buffer.append(s)

        original_print = self.print
        self.print = MethodType(buffered_print, self)

        self.print(self._bless.save)
        try:
            yield _buffer
        finally:
            self.print(self._bless.restore)

            original_print(''.join(_buffer))
            self.flush()
            self.print = original_print
