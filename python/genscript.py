#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit  - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# sys-apps/portage        - provee "dispatch-conf".
# sys-apps/coreutils      - provee "cat" y "wc".
# app-admin/eselect       - provee "eselect" y sus módulos.

import sys

from modules.console_ui import (
    style_text,
)

from modules.menu_creation import run_menu
from genscript_tools.system_maintenance import clean_thumbnails, read_news
from genscript_tools.package_management import PACKAGE_MANAGEMENT_MENU_DATA
from genscript_tools.snapshots import SNAPSHOT_MANAGEMENT_MENU_DATA
from genscript_tools.updates import UPDATES_MENU_DATA
from genscript_tools.use_flags import USE_FLAGS_MENU_DATA


MAIN_MENU_DATA = {
    "dict_name": "MAIN_MENU_DATA",
    "title": "¡Bienvenido a la herramienta de administración del sistema!",
    "options": [
        {"name": "APARTADOS ADICIONALES"},
        {
            "name": "Menú de opciones de actualización.",
            "action": UPDATES_MENU_DATA,
        },
        {
            "name": "Menú de manejo de paquetes y repositorios del sistema.",
            "action": PACKAGE_MANAGEMENT_MENU_DATA,
        },
        {
            "name": "Menú de manejo de snapshots.",
            "action": SNAPSHOT_MANAGEMENT_MENU_DATA,
        },
        {
            "name": "Menú de obtención de información sobre USE flags.",
            "action": USE_FLAGS_MENU_DATA,
        },
        {"name": "OPCIONES DE LIMPIEZA"},
        {
            "name": "Limpiar archivos residuales.",
            "action": [
                ["#ROOT", "eclean-dist", "-d"],
                ["#ROOT", "eclean-pkg", "-d"],
            ],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Limpiar versiones antiguas del kernel.",
            "action": [["#ROOT", "eclean-kernel", "-A", "-d", "-n 2"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Limpiar miniaturas de Nautilus.",
            "action": clean_thumbnails,
            "aesthetic_action": "print_line",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "Resolver conflictos por diferencia de archivos.",
            "action": [["#ROOT", "dispatch-conf"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Leer el boletín de noticias de Gentoo.",
            "action": read_news,
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "SALIR.",
            "action": "exit_script",
        },
    ],
}


if __name__ == "__main__":
    try:
        run_menu(MAIN_MENU_DATA)
    except (KeyboardInterrupt, EOFError):
        style_text(
            "bg", "red", "\nEjecución del programa interrupida. ¡Saliendo!"
        )
        sys.exit(1)
