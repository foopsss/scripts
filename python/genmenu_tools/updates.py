#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-apps/portage - provee "emerge" y "emaint".
# sys-apps/flatpak - provee "flatpak".
# sys-apps/fwupd   - provee "fwupdmgr".

from modules.console_ui import (
    clear_screen,
    draw_coloured_line,
    get_choice,
    press_enter,
)

from modules.subprocess_utils import (
    run_command,
    run_command_as_root,
)


def sincronize_repositories():
    draw_coloured_line(30)
    print("Sincronización de repositorios")
    draw_coloured_line(30)
    run_command_as_root(["emaint", "-a", "sync"])
    draw_coloured_line(36)
    print("Descarga de código fuente y paquetes")
    draw_coloured_line(36)
    run_command(["emerge", "-fuDN", "@world"])


def update_flatpak_apps():
    draw_coloured_line(27)
    print("Remoción de runtimes viejos")
    draw_coloured_line(27)
    run_command(["flatpak", "uninstall", "--unused", "-y"])
    draw_coloured_line(25)
    print("Actualización de Flatpaks")
    draw_coloured_line(25)
    run_command(["flatpak", "update", "-y"])


def update_firmware():
    # Las dos últimas opciones se ejecutan con "check_return=False"
    # porque fwupdmgr devuelve códigos de salida distintos de cero
    # aún cuando no hubo errores de ejecución pero tampoco hay
    # actualizaciones disponibles.
    run_command(["fwupdmgr", "refresh", "--force"])
    run_command(["fwupdmgr", "get-updates"], check_return=False)
    run_command(["fwupdmgr", "update"], check_return=False)


def updates_menu():
    while True:
        clear_screen()
        draw_coloured_line(48, "=")
        print("Apartado para actualizar el software del sistema")
        draw_coloured_line(48, "=")
        print("")
        print("PAQUETES/REPOSITORIOS")
        draw_coloured_line(21)
        print("1. Sincronizar repositorios.")
        print("2. Actualizar el sistema.")
        print("3. Actualizar las aplicaciones de Flatpak.")
        print("4. Actualizar el firmware del dispositivo.")
        print("")
        print("MISCELÁNEA")
        draw_coloured_line(10)
        print("5. Pretender que se va a realizar una actualización.")
        print("6. SALIR.")
        print("")
        choice = get_choice(1, 6)

        # Antes de ejecutar las opciones, conviene limpiar
        # la pantalla. De lo contrario, se genera un caos
        # visual tremendo.
        clear_screen()

        match choice:
            case 1:
                sincronize_repositories()
            case 2:
                run_command_as_root(["emerge", "-uDN", "@world"])
            case 3:
                update_flatpak_apps()
            case 4:
                update_firmware()
            case 5:
                run_command(["emerge", "-puDN", "@world"])
            case 6:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
