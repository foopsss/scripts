#!/usr/bin/env python3

# Paquetes usados en este módulo:
# dev-util/android-tools - provee "adb" y "fastboot"

import shlex

from adbscript_tools.file_management import FILE_MANAGEMENT_MENU_DATA
from adbscript_tools.app_management import APP_MANAGEMENT_MENU_DATA
from modules.console_ui import get_validated_input
from modules.subprocess_utils import run_command


def _start_adb_server() -> None:
    """
    _start_adb_server() es una función utilizada
    para iniciar un servidor de ADB al iniciar la
    ejecución del script.
    """
    # A diferencia del comando "adb kill-server",
    # "adb start-server" sí imprime texto por
    # pantalla al iniciar el servidor, por lo que
    # se lo debe capturar para que no se lo vea
    # al iniciar el script.
    run_command(command=["adb", "start-server"], capture_output=True)


def _stop_adb_server() -> None:
    """
    _stop_adb_server() es una función utilizada
    para detener el servidor de ADB al finalizar
    la ejecución del script.
    """
    run_command(["adb", "kill-server"])


def _execute_custom_command() -> None:
    """
    _execute_custom_command() es una función
    que contiene la lógica para permitir que
    un usuario ejecute otros comandos de ADB
    que no estén incorporados en el script.

    Para ello, se toma un comando como cadena
    y se lo divide, convirtiéndolo en una lista,
    con la función split() de la librería
    'shlex'.
    """
    raw_command = get_validated_input("Introduzca el comando a ejecutar")
    split_command = shlex.split(raw_command)
    print("")

    run_command(split_command)


MAIN_MENU_DATA = {
    "dict_name": "MAIN_MENU_DATA",
    "title": "¡Bienvenido a la interfaz para usar ADB y Fastboot!",
    "on_start": [_start_adb_server],
    "on_exit": [_stop_adb_server],
    "options": [
        {"name": "COMANDOS DE ADB"},
        {
            "name": "Comprobar si el ordenador reconoce el dispositivo.",
            "action": [["adb", "devices"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Reiniciar el dispositivo.",
            "action": [["adb", "reboot"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Reiniciar el dispositivo en el modo recovery.",
            "action": [["adb", "reboot", "recovery"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Reiniciar el dispositivo en el modo fastboot.",
            "action": [["adb", "reboot", "fastboot"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Realizar operaciones con archivos.",
            "action": FILE_MANAGEMENT_MENU_DATA,
        },
        {
            "name": "Administrar las aplicaciones del dispositivo.",
            "action": APP_MANAGEMENT_MENU_DATA,
        },
        {"name": "COMANDOS DE FASTBOOT"},
        {
            "name": "Comprobar si el ordenador reconoce el dispositivo.",
            "action": [["fastboot", "devices"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Reiniciar el dispositivo.",
            "action": [["fastboot", "reboot"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Reiniciar el dispositivo en el modo recovery.",
            "action": [["fastboot", "reboot", "recovery"]],
            "aesthetic_action": "print_line",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "Ejecutar un comando propio.",
            "action": [_execute_custom_command],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "SALIR.",
            "action": "exit",
        },
    ],
}
