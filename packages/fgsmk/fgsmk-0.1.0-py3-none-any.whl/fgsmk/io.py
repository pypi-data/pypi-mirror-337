from pathlib import Path

from fgpyo.io import assert_path_is_readable

__LINES_PER_LOGFILE: int = 50
"""The default number of lines to return from the log files for each failed job."""


def _last_lines(path: Path, max_lines: int | None = __LINES_PER_LOGFILE) -> list[str]:
    """
    Returns the last N lines from a file as a list.

    Args:
        path: the path to the file (must exist)
        max_lines: the number of line to return, None will return all lines
    Return:
        the last n lines of the file as a list, or the whole file < n lines.

    Raises:
        ValueError: If the number of lines requested is <= 0.
    """
    assert_path_is_readable(path=path)

    if max_lines is not None and max_lines <= 0:
        raise ValueError(f"Number of lines requested must be > 0. Saw {max_lines}.")

    lines: list[str] = path.read_text().splitlines()
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[-max_lines : len(lines)]
    return lines
