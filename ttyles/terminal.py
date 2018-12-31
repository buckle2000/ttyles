# TODO delete self._fin or do something with stdin

try:
    import termios
    import fcntl
    import tty
    HAS_TTY = True
except ImportError:
    _TTY_METHODS = ('setraw', 'cbreak', 'kbhit', 'height', 'width')
    _MSG_NOSUPPORT = (
        "One or more of the modules: 'termios', 'fcntl', and 'tty' "
        "are not found on your platform '{0}'. The following methods "
        "of Terminal are dummy/no-op unless a deriving class overrides "
        "them: {1}".format(sys.platform.lower(), ', '.join(_TTY_METHODS)))
    warnings.warn(_MSG_NOSUPPORT)
    HAS_TTY = False

import sys
from shutil import get_terminal_size
from types import MethodType
from typing import TextIO, List, Tuple
from contextlib import contextmanager

from . import Cursor
from . import constants as C

Coord = Tuple[int, int]


class Terminal:
    """This class represents a terminal that wraps an output stream."""

    @classmethod
    def from_std(cls) -> 'Terminal':
        return cls(fin=sys.stdin, fout=sys.stdout)

    def __init__(self, fin: TextIO, fout: TextIO):
        self._fin = fin
        self._fout = fout
        self._buffer = dict()
        self._line_buffered = True

    ##############
    # Properties #
    ##############

    size: Coord = property(doc="size of the terminal")

    @size.getter
    def size(self):
        """Query size of terminal"""
        if self._is_fout_tty():
            return get_terminal_size()
        else:
            raise NotImplementedError('Output stream is not a terminal.')

    @size.setter
    def size(self, value):
        """Resize terminal"""
        self.write(C.RESIZE.format(rows=value[1], cols=value[0]))

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
        self.write(Cursor.POS(x, y))

    def write(self, s: str, flush=True) -> None:
        """Print text, flush output by default."""
        self._fout.write(s)
        if flush:
            self.flush()

    def __setitem__(self, location, c: str):
        """Write character to buffer at certain location."""
        self.move(*location)
        self.write(c)

    def clear(self) -> None:
        """Clear screen, then scroll down."""
        self.write(C.CLEAR)

    def reset(self) -> None:
        """Reset terminal."""
        self.write(C.RESET)

    def flush(self):
        """Flush output."""
        return self._fout.flush()

    def _is_fout_tty(self):
        return HAS_TTY and self._fout in (sys.__stdout__, sys.__stderr__)

    ####################
    # Context managers #
    ####################

    @contextmanager
    def at(self, x: int, y: int):
        """Context manager for temporarily moving the cursor."""
        self.write(C.SAVE)
        self.move(x, y)
        try:
            yield
        finally:
            self.write(C.RESTORE)

    @contextmanager
    def buffer(self) -> List[str]:
        """
        Context manager for buffering output.
        
        Returns a list a strings, which is used internally as buffer.
        """
        _buffer = []

        def buffered_write(self, s: str):
            nonlocal _buffer
            _buffer.append(s)

        original_write = self.write
        self.write = MethodType(buffered_write, self)

        try:
            yield _buffer
        finally:

            original_write(''.join(_buffer))
            self.flush()
            self.write = original_write

    @contextmanager
    def fullscreen(self):
        """
        Context manager that switches to secondary screen, restoring on exit.

        Under the hood, this switches between the primary screen buffer and
        the secondary one. The primary one is saved on entry and restored on
        exit.  Likewise, the secondary contents are also stable and are
        faithfully restored on the next entry::

            with term.fullscreen():
                main()

        .. note:: There is only one primary and one secondary screen buffer.
           :meth:`fullscreen` calls cannot be nested, only one should be
           entered at a time.
        """
        self.write(C.ENTER_FULLSCREEN)
        try:
            yield
        finally:
            self.write(C.EXIT_FULLSCREEN)

    @contextmanager
    def cbreak(self):
        """
        Allow each keystroke to be read immediately after it is pressed.

        This is a context manager for :func:`tty.setcbreak`.

        This context manager activates 'rare' mode, the opposite of 'cooked'
        mode: On entry, :func:`tty.setcbreak` mode is activated disabling
        line-buffering of keyboard input and turning off automatic echo of
        input as output.

        .. note:: You must explicitly print any user input you would like
            displayed.  If you provide any kind of editing, you must handle
            backspace and other line-editing control functions in this mode
            as well!

        **Normally**, characters received from the keyboard cannot be read
        by Python until the *Return* key is pressed. Also known as *cooked* or
        *canonical input* mode, it allows the tty driver to provide
        line-editing before shuttling the input to your program and is the
        (implicit) default terminal mode set by most unix shells before
        executing programs.

        Technically, this context manager sets the :mod:`termios` attributes
        of the terminal attached to :obj:`sys.__stdin__`.

        .. note:: :func:`tty.setcbreak` sets ``VMIN = 1`` and ``VTIME = 0``,
            see http://www.unixwiz.net/techtips/termios-vmin-vtime.html
        """
        if self._is_fout_tty():
            # Save current terminal mode:
            save_mode = termios.tcgetattr(self._fout)
            save_line_buffered = self._line_buffered
            tty.setcbreak(self._fout, termios.TCSANOW)
            try:
                self._line_buffered = False
                yield
            finally:
                # Restore prior mode:
                termios.tcsetattr(self._fout, termios.TCSAFLUSH, save_mode)
                self._line_buffered = save_line_buffered
        else:
            yield