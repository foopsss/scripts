#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit  - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# sys-apps/portage        - provee "dispatch-conf".
# sys-apps/coreutils      - provee "cat" y "wc".
# app-admin/eselect       - provee "eselect" y sus módulos.

import os
import shutil
import sys

from modules.console_ui import (
    bg_colour,
    get_choice,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
)

from modules.menu_creation import run_menu
from genscript_tools.package_management import PACKAGE_MANAGEMENT_MENU_DATA
from genscript_tools.snapshots import SNAPSHOT_MANAGEMENT_MENU_DATA
from genscript_tools.updates import UPDATES_MENU_DATA
from genscript_tools.use_flags import USE_FLAGS_MENU_DATA

# TODO: volver a añadir una opción para obtener el tiempo de instalación de un
#       paquete.

def clean_thumbnails():
    thumbdir = os.environ.get("HOME") + "/.cache/thumbnails"

    if os.path.exists(thumbdir):
        try:
            shutil.rmtree(thumbdir)
            bg_colour("green", "La carpeta fue borrada exitosamente.")
        except OSError as error:
            bg_colour("red", "La operación ha fallado.")
            print(f"{error}")
    else:
        bg_colour("blue", "¡La carpeta no existe! No se ha borrado nada.")


def read_news():
    # Obtención del número de noticias disponibles para
    # leer. Acá se simula el pipeline de una consola con
    # pipe_commands y se obtiene el número total de entradas
    # entradas de noticias disponibles para leer revisando
    # los contenidos de la carpeta "/var/lib/gentoo/news".
    news_folder = "/var/lib/gentoo/news"
    news_count = 0

    for file in os.listdir(news_folder):
        if file.endswith(".read") or file.endswith(".unread"):
            file_line_count = pipe_commands(
                ["cat", f"/var/lib/gentoo/news/{file}"], ["wc", "-l"]
            )
            news_count += int(file_line_count)

    # Presentación del menú de noticias disponibles
    # para leer. Debido a que "eselect news list"
    # devuelve 1 como código de salida aún si se lo
    # ejecutó exitosamente, debo desactivar el control
    # de errores para este programa.
    run_command(
        ["eselect", "news", "list"], check_return=False, use_shell=False
    )
    print("")

    # Lectura del boletín de noticias deseado.
    # Se utiliza el intérprete de consola del sistema
    # para poder pasar la entrada de noticias por less.
    entry = get_choice(1, news_count)
    run_command(
        f"eselect news read {entry} | less",
        check_return=True,
        use_shell=True,
    )


MAIN_MENU_DATA = {
    "title": "¡Bienvenido a la herramienta de administración del sistema!",
    "options": [
        {"name": "APARTADOS ADICIONALES"},
        {
            "name": "Menú de opciones de actualización.",
            "action": UPDATES_MENU_DATA,
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Menú de manejo de paquetes y repositorios del sistema.",
            "action": PACKAGE_MANAGEMENT_MENU_DATA,
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Menú de manejo de snapshots.",
            "action": SNAPSHOT_MANAGEMENT_MENU_DATA,
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Menú de obtención de información sobre USE flags.",
            "action": USE_FLAGS_MENU_DATA,
            "aesthetic_action": "clear_screen",
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
        bg_colour("red", "\nEjecución del programa interrupida. ¡Saliendo!")
        sys.exit(1)
