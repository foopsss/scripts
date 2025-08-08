#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-fs/btrfs-progs - provee "btrfs".
# app-backup/snapper - provee "snapper".

from modules.console_ui import (
    bg_colour,
    clear_screen,
    draw_coloured_line,
    get_choice,
    press_enter,
)

from modules.subprocess_utils import (
    run_command,
    run_command_as_root,
)


def draw_snapshot_management_menu():
    draw_coloured_line(55, "=")
    print("Apartado para manejar las snapshots creadas con Snapper")
    print("y los subvolúmenes de BTRFS")
    draw_coloured_line(55, "=")
    print("")
    print("MANEJO DE SUBVOLÚMENES")
    draw_coloured_line(22)
    print("1. Obtener el listado de subvolúmenes presentes actualmente.")
    print("")
    print("MANEJO DE SNAPSHOTS")
    draw_coloured_line(19)
    print("2. Obtener el listado de snapshots existentes actualmente para")
    print("   los subvolúmenes del sistema.")
    print("3. Crear una snapshot del sistema.")
    print("4. Eliminar una snapshot del sistema.")
    print("")
    print("MISCELÁNEA")
    draw_coloured_line(10)
    print("5. Salir")
    print("")


def get_snapshots_list():
    draw_coloured_line(24, "=")
    print("Snapshots del volumen @/")
    draw_coloured_line(24, "=")
    run_command(["snapper", "-c", "root", "list"])
    print("")
    draw_coloured_line(28, "=")
    print("Snapshots del volumen @/home")
    draw_coloured_line(28, "=")
    run_command(["snapper", "-c", "home", "list"])


def create_system_snapshot(snapshot_description: str):
    # Limpieza de snapshots innecesarias.
    run_command(["snapper", "-c", "root", "cleanup", "number"])
    run_command(["snapper", "-c", "home", "cleanup", "number"])

    # Snapshot del volumen @.
    run_command(
        [
            "snapper",
            "-c",
            "root",
            "create",
            "-c",
            "number",
            "--description",
            f"{snapshot_description}",
        ],
    )

    # Snapshot del volumen @home.
    run_command(
        [
            "snapper",
            "-c",
            "home",
            "create",
            "-c",
            "number",
            "--description",
            f"{snapshot_description}",
        ],
    )


def get_input_and_create_snapshot():
    while True:
        snapshot_str = input("Introduzca una descripción para la snapshot: ")

        if snapshot_str == "":
            bg_colour("red", "¡Introduzca una descripción!")
            continue
        else:
            break

    create_system_snapshot(snapshot_str)


def delete_system_snapshot():
    get_snapshots_list()
    print("")

    while True:
        snapshot_number_str = input(
            "Introduzca el número de snapshot a borrar: "
        )

        if snapshot_number_str == "":
            bg_colour("red", "¡Introduzca una elección!")
            continue
        elif not snapshot_number_str.isdigit():
            bg_colour("red", "¡Solo se pueden introducir números!")
            continue
        else:
            break

    snapshot_number = int(snapshot_number_str)
    print("")

    run_command(["snapper", "-c", "root", "delete", f"{snapshot_number}"])
    run_command(["snapper", "-c", "home", "delete", f"{snapshot_number}"])


def snapshot_management_menu():
    while True:
        clear_screen()
        draw_snapshot_management_menu()
        choice = get_choice(1, 5)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        #
        # Si utilizo alguna opción que requiera limpiar
        # la pantalla, hago eso.
        if (choice == 1) or (choice > 2 and choice < 4):
            draw_coloured_line(59)
        else:
            clear_screen()

        match choice:
            case 1:
                run_command_as_root(["btrfs", "subvolume", "list", "/"])
            case 2:
                get_snapshots_list()
            case 3:
                get_input_and_create_snapshot()
            case 4:
                delete_system_snapshot()
            case 5:
                break

        if choice < 5:
            press_enter()
