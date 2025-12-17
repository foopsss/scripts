#!/usr/bin/env python3

from modules.program_tools import execute_with_interrupt_handler
from modules.subprocess_utils import run_command
from pathlib import Path


def format_with_black():
    walk_dir = Path.cwd()
    for file in walk_dir.rglob("*.py"):
        run_command(["black", f"{file}"])


if __name__ == "__main__":
    execute_with_interrupt_handler(format_with_black)
