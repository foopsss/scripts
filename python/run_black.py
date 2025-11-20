#!/usr/bin/env python3

import os

from modules.program_tools import execute_with_interrupt_handler
from modules.subprocess_utils import run_command


def format_with_black():
    walk_dir = os.getcwd()
    for root, subdirs, files in os.walk(walk_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                run_command(["black", f"{root}/{file}"])


if __name__ == "__main__":
    execute_with_interrupt_handler(format_with_black)
