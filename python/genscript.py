#!/usr/bin/env python3

from modules.menu_creation import run_menu
from modules.program_tools import execute_with_interrupt_handler
from genscript_tools.main_menu import MAIN_MENU_DATA

if __name__ == "__main__":
    execute_with_interrupt_handler(run_menu, MAIN_MENU_DATA)
