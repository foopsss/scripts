#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo contiene una serie de funciones relacionadas a la ejecución de
scripts y programas.
"""

import functools
import shutil
import subprocess
import sys

from pathlib import Path
from typing import Callable, NoReturn

from modules.console_ui import style_text


def execute_with_interrupt_handler(
    function: Callable, *args, **kwargs
) -> NoReturn:
    """
    execute_with_interrupt_handler() es una función
    encargada de ejecutar funciones y salir de manera
    limpia en caso de que el usuario interrumpa
    manualmente la ejecución con un atajo de teclado.
    """
    if not callable(function):
        raise TypeError(
            "El argumento 'function' debe ser un objeto de función."
        )

    try:
        # Ejecución exitosa de la función,
        # devolviendo el número 0 como código
        # de salida.
        function(*args, **kwargs)
        sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        # Ejecución de la función interrumpida.
        # Se devuelve el número 1 como código
        # de salida.
        style_text(
            colour_type="bg",
            colour="red",
            text="\nEjecución del programa interrupida manualmente."
            "\n¡Saliendo!",
        )
        sys.exit(1)


@functools.cache
def get_privilege_elevation_command() -> str:
    """
    get_privilege_escalation_command() es una función
    que sirve para verificar si el sistema en el que
    corre un script cuenta con alguno de los programas
    de elevación de privilegios especificados en la
    variable PRIVILEGE_ELEVATION_COMMANDS.

    Se la utiliza de manera que se pueda determinar
    dinámicamente cuál es el comando utilizado en el
    sistema para ejecutar programas con permisos de
    superusuario.
    """
    PRIVILEGE_ELEVATION_COMMANDS = ["doas", "sudo", "run0"]

    for cmd in PRIVILEGE_ELEVATION_COMMANDS:
        if shutil.which(cmd):
            return cmd

    # Si ninguno de los programas buscados se
    # encuentra en el sistema, se trata de usar
    # "pkexec" como salida de emergencia, al
    # estar ampliamente disponible en Linux por
    # ser provisto por Polkit.
    pk_str = "pkexec"

    if shutil.which(pk_str):
        return pk_str
    else:
        raise RuntimeError(
            "No se ha podido encontrar ningún programa de elevación de"
            " privilegios en el sistema, por lo que no se puede ejecutar"
            " comandos como superusuario."
        )


def check_if_tools_installed(tools: list[str]) -> None:
    """
    check_if_tools_installed() es una función que
    sirve para revisar si los programas indicados
    en una lista de entrada se encuentran instalados
    en el sistema.
    """
    for tool in tools:
        if not shutil.which(tool):
            raise RuntimeError(
                f"{tool} no está instalado en el sistema, o no se encuentra"
                " añadido a la variable de entorno PATH."
            )


def get_repo_root() -> Path:
    """
    get_repo_root()  es una función utilizada para
    devolver la raíz de un repositorio de git.
    """
    try:
        root_str = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(root_str.stdout.strip())
    except subprocess.CalledProcessError:
        print("¡No se pudo obtener la raíz del repositorio!")
        sys.exit(1)
