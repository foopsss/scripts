#!/usr/bin/env python3

# Paquetes usados en este módulo:
# dev-util/android-tools - provee "adb"

from modules.console_ui import get_validated_input
from modules.subprocess_utils import run_command


def _copy_files_to_device() -> None:
    """
    _copy_files_to_device() es una función
    utilizada para copiar archivos desde una
    computadora hacia un dispositivo Android.
    """
    computer_location = get_validated_input(
        "Ubicación en la computadora desde la cual copiar un archivo"
    )
    device_location = get_validated_input(
        "Ubicación en el dispositivo a la cual copiar un archivo"
    )
    print("")
    run_command(["adb", "push", f"{computer_location}", f"{device_location}"])


def _copy_files_from_device() -> None:
    """
    _copy_files_from_device() es una función
    utilizada para copiar archivos desde un
    dispositivo Android hacia una computadora.
    """
    device_location = get_validated_input(
        "Ubicación en el dispositivo desde la cual copiar un archivo"
    )
    computer_location = get_validated_input(
        "Ubicación en la computadora a la cual copiar un archivo"
    )
    print("")
    run_command(["adb", "pull", f"{device_location}", f"{computer_location}"])


FILE_MANAGEMENT_MENU_DATA = {
    "dict_name": "FILE_MANAGEMENT_MENU_DATA",
    "title": "Apartado para transferir archivos desde y hacia el dispositivo",
    "options": [
        {"name": "COPIA DE ARCHIVOS"},
        {
            "name": "Copiar un archivo hacia el dispositivo.",
            "action": [_copy_files_to_device],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Copiar un archivo desde el dispositivo.",
            "action": [_copy_files_from_device],
            "aesthetic_action": "print_line",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "SALIR.",
            "action": "exit",
        },
    ],
}
