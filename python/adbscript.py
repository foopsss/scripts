#!/usr/bin/env python3

import shutil
import sys

from modules.console_ui import style_text
from modules.program_tools import execute_with_interrupt_handler
from modules.menu.creation import run_menu
from adbscript_tools.main_menu import MAIN_MENU_DATA

if __name__ == "__main__":
    # Si ADB no está disponible en el sistema,
    # se debe advertir al usuario.
    if not (shutil.which("adb") and shutil.which("fastboot")):
        style_text(
            colour_type="bg",
            colour="red",
            text="No se ha podido detectar una instalación de ADB y/o Fastboot"
            " en el sistema. \nInstale ADB y Fastboot en el sistema antes de"
            " ejecutar este script.",
        )
        sys.exit(1)

    # Si ADB está disponible en el sistema,
    # se puede ejecutar el script.
    execute_with_interrupt_handler(run_menu, MAIN_MENU_DATA)
