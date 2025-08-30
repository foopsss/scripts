#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-apps/portage   - provee "emerge", "emaint" y "glsa-check".
# sys-apps/flatpak   - provee "flatpak".
# sys-apps/fwupd     - provee "fwupdmgr".

from modules.console_ui import (
    bg_colour,
    clear_screen,
    draw_coloured_line,
    get_choice,
    get_validated_input,
    press_enter,
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
        draw_coloured_line(48, "=")
        bg_colour("red", "¡No cuenta con conexión a Internet!")
        bg_colour("yellow", "No podrá utilizar algunas opciones del menú.")


def draw_updates_menu():
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
    print("6. Revisar si el sistema está expuesto a fallos de")
    print("   ciberseguridad.")
    print("7. SALIR.")
    print("")


def sincronize_repositories():
    draw_coloured_line(30)
    print("Sincronización de repositorios")
    draw_coloured_line(30)
    create_system_snapshot("Snapshot previa a una actualización del sistema")
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


def cve_check_menu():
    while True:
        clear_screen()
        draw_coloured_line(56, "=")
        print("Apartado para verificar si el sistema está expuesto a un")
        print("un fallo de seguridad")
        draw_coloured_line(56, "=")
        print("1. Controlar si el sistema está afectado por alguno de")
        print("   los fallos publicados.")
        print("2. Obtener los pasos requeridos para remediar un fallo.")
        print("3. SALIR.")
        print("")
        choice = get_choice(1, 3)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        if choice < 3:
            draw_coloured_line(59)

        match choice:
            case 1:
                run_command(["glsa-check", "-t", "all"])
            case 2:
                cve_id = get_validated_input(
                    msg="Ingrese la ID de un fallo reportado: ",
                )
                print("")
                run_command(["glsa-check", "-p", f"{cve_id}"])
            case 3:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()


def updates_menu():
    while True:
        clear_screen()
        check_internet_connection()
        draw_updates_menu()
        choice = get_choice(1, 7)

        # Antes de ejecutar las opciones, conviene limpiar
        # la pantalla. De lo contrario, se genera un caos
        # visual tremendo.
        if choice < 7:
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
                cve_check_menu()
            case 7:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú o se entra a otro apartado del módulo.
        if choice < 6:
            press_enter()
