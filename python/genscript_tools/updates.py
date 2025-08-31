#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-apps/portage   - provee "emerge", "emaint" y "glsa-check".
# sys-apps/flatpak   - provee "flatpak".
# sys-apps/fwupd     - provee "fwupdmgr".

from modules.console_ui import (
    bg_colour,
    draw_coloured_line,
)

from modules.subprocess_utils import (
    run_command,
    run_command_and_get_return_code,
    run_command_as_root,
)

from genscript_tools.snapshots import create_system_snapshot


def check_internet_connection():
    # Este chequeo de conexión es relativamente "barato"
    # en cuanto al tiempo que cuesta realizarlo, por lo
    # que me siento cómodo realizándolo cada vez que se
    # muestra el menú principal de actualizaciones.
    #
    # Yo al menos no observo una diferencia notable en
    # el tiempo que tarda el menú en mostrarse por
    # pantalla.
    ping_exit_code = run_command_and_get_return_code(
        ["ping", "-c", "1", "www.google.com"]
    )

    if ping_exit_code != 0:
        bg_colour("red", "¡No cuenta con conexión a Internet!")
        bg_colour("yellow", "No podrá utilizar algunas opciones del menú.")


def sincronize_repositories():
    draw_coloured_line(30)
    print("Sincronización de repositorios")
    draw_coloured_line(30)
    create_system_snapshot("Snapshot previa a una actualización del sistema")
    run_command_as_root(["emaint", "-a", "sync"])
    draw_coloured_line(36)
    print("Descarga de código fuente y paquetes")
    draw_coloured_line(36)
    run_command_as_root(["emerge", "-fuDN", "@world"])


def update_firmware():
    # Las dos últimas opciones se ejecutan con "check_return=False"
    # porque fwupdmgr devuelve códigos de salida distintos de cero
    # aún cuando no hubo errores de ejecución pero tampoco hay
    # actualizaciones disponibles.
    run_command(["fwupdmgr", "refresh", "--force"])
    run_command(["fwupdmgr", "get-updates"], check_return=False)
    run_command(["fwupdmgr", "update"], check_return=False)


CVE_CHECK_MENU_DATA = {
    "title": "Apartado para controlar posibles fallos de seguridad",
    "options": [
        {
            "name": "Controlar si el sistema está afectado por alguno de\n"
            "   los fallos publicados.",
            "action": [["glsa-check", "-t", "all"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Obtener los pasos requeridos para remediar un fallo.",
            "action": [["glsa-check", "-p"]],
            "prompt": "Ingrese la ID de un fallo reportado",
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "SALIR.",
            "action": "exit_menu",
        },
    ],
}


UPDATES_MENU_DATA = {
    "title": "Apartado para actualizar el software del sistema",
    "pre_menu_hook": check_internet_connection,
    "options": [
        {"name": "PAQUETES/REPOSITORIOS"},
        {
            "name": "Sincronizar repositorios.",
            "action": sincronize_repositories,
            "aesthetic_action": "clear_screen",
            "requires_root": True,
        },
        {
            "name": "Actualizar el sistema.",
            "action": [["emerge", "-uDN", "@world"]],
            "aesthetic_action": "clear_screen",
            "requires_root": True,
        },
        {
            "name": "Actualizar las aplicaciones de Flatpak.",
            "action": [
                ["flatpak", "uninstall", "--unused", "-y"],
                ["flatpak", "update", "-y"],
            ],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Actualizar el firmware del dispositivo.",
            "action": update_firmware,
            "aesthetic_action": "clear_screen",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "Pretender que se va a realizar una actualización.",
            "action": [["emerge", "-puDN", "@world"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Revisar si el sistema está expuesto a fallos de\n"
            "   ciberseguridad.",
            "action": CVE_CHECK_MENU_DATA,
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "SALIR.",
            "action": "exit_menu",
        },
    ],
}
