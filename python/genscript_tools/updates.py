#!/usr/bin/env python3

# Paquetes usados en este módulo:
# net-misc/iputils   - provee "ping".
# sys-apps/portage   - provee "emerge", "emaint" y "glsa-check".
# sys-apps/flatpak   - provee "flatpak".
# sys-apps/fwupd     - provee "fwupdmgr".

from modules.console_ui import style_text, draw_coloured_line
from modules.subprocess_utils import run_command, run_command_as_root
from genscript_tools.snapshots import create_system_snapshot


def check_internet_connection() -> None:
    """
    check_internet_connection() es un chequeo de conexión
    que consiste en realizar un ping a Google y se ejecuta
    al pasarle el objeto de esta función a un diccionario
    a través del parámetro "pre_menu_hook".

    En función del código de salida que devuelva esta
    operación, se decide si mostrar un mensaje de éxito
    o un mensaje de error.

    Debido a que es relativamente "barato" en cuanto al
    tiempo que cuesta realizarlo se lo hace de esta
    manera.
    """
    ping = run_command(
        command=["ping", "-c", "1", "www.google.com"],
        # No se desea controlar si se produce un error porque
        # se muestra un mensaje de error en la cabecera del
        # apartado si se obtiene un código de salida distinto
        # de 0.
        check_return=False,
        capture_output=True,
    )

    if ping is None or ping.returncode != 0:
        style_text(
            colour_type="bg",
            colour="red",
            text="¡No cuenta con conexión a Internet!",
        )
        style_text(
            colour_type="bg",
            colour="yellow",
            text="No podrá utilizar algunas opciones del menú.",
        )
    else:
        style_text(
            colour_type="bg",
            colour="green",
            text="¡Cuenta con conexión a Internet!",
        )
        style_text(
            colour_type="bg",
            colour="yellow",
            text="Podrá utilizar todas las opciones del menú.",
        )


def sincronize_repositories() -> None:
    """
    sincronize_repositories() es una función utilizada
    para crear una snapshot del sistema, sincronizar
    los repositorios y descargar automáticamente el
    código fuente o binario precompilado de los
    paquetes que se deban actualizar.
    """
    title1_str = "Sincronización de repositorios"
    title1_str_length = len(title1_str)
    draw_coloured_line(title1_str_length, "=")
    print(title1_str)
    draw_coloured_line(title1_str_length, "=")
    create_system_snapshot("Snapshot previa a una actualización del sistema")
    run_command_as_root(["emaint", "-a", "sync"])
    print("")

    title2_str = "Descarga de código fuente y paquetes"
    title2_str_length = len(title2_str)
    draw_coloured_line(title2_str_length, "=")
    print(title2_str)
    draw_coloured_line(title2_str_length, "=")
    run_command_as_root(["emerge", "-fuDN", "--ask=n", "@world"])


def update_flatpak_apps() -> None:
    """
    update_flatpak_apps() es una función utilizada
    para remover runtimes innecesarios y actualizar
    paquetes de Flatpak.
    """
    title1_str = "Remoción de paquetes innecesarios"
    title1_str_length = len(title1_str)
    draw_coloured_line(title1_str_length, "=")
    print(title1_str)
    draw_coloured_line(title1_str_length, "=")
    run_command(["flatpak", "uninstall", "--unused", "-y"])
    print("")

    title2_str = "Actualización de paquetes"
    title2_str_length = len(title2_str)
    draw_coloured_line(title2_str_length, "=")
    print(title2_str)
    draw_coloured_line(title2_str_length, "=")
    run_command(["flatpak", "update", "-y"])


CVE_CHECK_MENU_DATA = {
    "dict_name": "CVE_CHECK_MENU_DATA",
    "title": "Apartado para controlar posibles fallos de seguridad",
    "options": [
        {
            "name": "Controlar si el sistema está afectado por alguno de"
            " los fallos publicados.",
            "action": [["glsa-check", "-t", "all"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Obtener los pasos requeridos para remediar un fallo.",
            "action": [["#UINPUT", "#SPLIT-INPUT", "glsa-check", "-p"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Ingrese la ID de un fallo reportado",
        },
        {
            "name": "SALIR.",
            "action": "exit",
        },
    ],
}


UPDATES_MENU_DATA = {
    "dict_name": "UPDATES_MENU_DATA",
    "title": "Apartado para actualizar el software del sistema",
    "on_draw": [check_internet_connection],
    "options": [
        {"name": "PAQUETES/REPOSITORIOS"},
        {
            "name": "Sincronizar repositorios.",
            "action": [sincronize_repositories],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Actualizar el sistema.",
            "action": [["#ROOT", "emerge", "-uDN", "@world"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Actualizar las aplicaciones de Flatpak.",
            "action": [update_flatpak_apps],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Actualizar el firmware del dispositivo.",
            "action": [
                # Las dos últimas opciones se ejecutan con "check_return=False"
                # porque fwupdmgr devuelve códigos de salida distintos de cero
                # aún cuando no hubo errores de ejecución pero tampoco hay
                # actualizaciones disponibles.
                (run_command, [["fwupdmgr", "refresh", "--force"]]),
                (
                    run_command,
                    [
                        ["fwupdmgr", "get-updates"],
                        check_return := False,
                        use_shell := False,
                    ],
                ),
                (
                    run_command,
                    [
                        ["fwupdmgr", "update"],
                        check_return := False,
                        use_shell := False,
                    ],
                ),
            ],
            "aesthetic_action": "clear_screen",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "Pretender que se va a realizar una actualización.",
            "action": [["emerge", "-puDN", "@world"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Revisar si el sistema está expuesto a fallos de"
            " ciberseguridad.",
            "action": CVE_CHECK_MENU_DATA,
        },
        {
            "name": "SALIR.",
            "action": "exit",
        },
    ],
}
