#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert.

Entry for the make.fun bounty
``u-swift-raven-16-the-long-roast-lawmakers-and-the-f3a3bdf7``.

The program writes one satirical sentence to ``entry.txt``. The bounty
gate accepts UTF-8 text of 1 to 320 characters that is not only white
space, so the sentence is checked against that contract before it is
written. Pure Python standard library; no third-party imports.

Output directory, first writable one wins:

1. ``$MAKEFUN_OUTPUT_DIR`` (the grader sets this),
2. ``/output``,
3. the directory holding this script,
4. ``/tmp``.

Each candidate is tried in order and an ``OSError`` on one candidate
moves on to the next instead of failing the run.
"""

import os
import sys

ENTRY_TEXT = (
    "They voted to ban the app, license the model, and audit the "
    "algorithm \u2014 then renamed the bill from .docx to .pdf and "
    "called the conversion complete."
)

MAX_CHARS = 320


def candidate_dirs():
    """Yield output directories in the order they should be tried."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        yield env_dir
    yield "/output"
    yield os.path.dirname(os.path.abspath(__file__))
    yield "/tmp"


def write_entry() -> str:
    """Write ENTRY_TEXT to the first writable candidate; return its path."""
    if not ENTRY_TEXT.strip() or len(ENTRY_TEXT) > MAX_CHARS:
        raise ValueError("entry text violates the 1..320 character gate")
    failures = []
    for directory in candidate_dirs():
        path = os.path.join(directory, "entry.txt")
        try:
            os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(ENTRY_TEXT)
            return path
        except OSError as exc:  # read-only or missing dir: try the next one
            failures.append(f"{path}: {exc}")
    raise OSError("no writable output directory: " + "; ".join(failures))


def main() -> int:
    path = write_entry()
    print(f"wrote {len(ENTRY_TEXT)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
