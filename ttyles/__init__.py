"""Easy to use terminal manipulation library with a Pythonic interface."""

import colorama
from colorama import Fore, Back, Cursor, Style
from .terminal import Terminal

__all__ = ['Terminal', 'Fore', 'Back', 'Cursor', 'Style']

colorama.init()
