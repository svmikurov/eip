"""Функции для вывода управляющих последовательностей."""

import shutil
import sys


def save_cursor_position() -> None:
    """Save cursor position."""
    sys.stdout.write('\0337')


def restore_cursor_position() -> None:
    """Restore cursor position."""
    sys.stdout.write('\0338')


def move_to_top_of_screen() -> None:
    """Move to top of screen."""
    sys.stdout.write('\033[H')


def delete_line() -> None:
    """Delete line."""
    sys.stdout.write('\033[2K')


def clear_line() -> None:
    """Clear line."""
    sys.stdout.write('\033[2K\033[0G')


def move_back_one_char() -> None:
    """Move to bottom of screen."""
    sys.stdout.write('\033[1D')


def move_to_bottom_of_screen() -> int:
    """Move to bottom of screen."""
    _, total_rows = shutil.get_terminal_size()
    input_row = total_rows - 1
    sys.stdout.write(f'\033[{input_row}E')
    return total_rows
