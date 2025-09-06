#!/usr/bin/env python3

import os

from modules.subprocess_utils import run_command

walk_dir = os.getcwd()
for root, subdirs, files in os.walk(walk_dir):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            run_command(["black", f"{root}/{file}"])
