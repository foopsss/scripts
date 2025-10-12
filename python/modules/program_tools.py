#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo contiene funciones relacionadas a la ejecución de scripts y
programas.
"""

import sys

from modules.console_ui import style_text


def execute_with_interrupt_handler(function: callable, *args, **kwargs) -> int:
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
            "bg",
            "red",
            "\nEjecución del programa interrupida manualmente. \n¡Saliendo!",
        )
        sys.exit(1)
