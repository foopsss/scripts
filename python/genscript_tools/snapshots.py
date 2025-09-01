#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-fs/btrfs-progs - provee "btrfs".
# app-backup/snapper - provee "snapper".

from modules.console_ui import (
    clear_screen,
    draw_coloured_line,
    get_choice,
    get_validated_input,
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
    print("2. Obtener el listado de snapshots existentes actualmente")
    print("   para los subvolúmenes del sistema.")
    print("3. Crear una snapshot del sistema.")
    print("4. Eliminar una snapshot del sistema.")
    print("")
    print("MISCELÁNEA")
    draw_coloured_line(10)
    print("5. Salir")
    print("")


def get_snapshots_list():
    title1_str = "Snapshots del volumen @/"
    draw_coloured_line(len(title1_str), "=")
    print(title1_str)
    draw_coloured_line(len(title1_str), "=")
    run_command(["snapper", "-c", "root", "list"])

    title2_str = "Snapshots del volumen @/home"
    draw_coloured_line(len(title2_str), "=")
    print(title2_str)
    draw_coloured_line(len(title2_str), "=")
    run_command(["snapper", "-c", "home", "list"])


def create_system_snapshot(snapshot_description: str):
    if not isinstance(snapshot_description, str):
        raise ValueError("La descripción de la snapshot debe ser un string.")

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


def delete_system_snapshot():
    get_snapshots_list()
    print("")

    snapshot_number = get_validated_input(
        "Introduzca el número de snapshot a borrar",
    )

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
        if choice == 1 or choice == 3:
            draw_coloured_line(59)
        else:
            clear_screen()

        match choice:
            case 1:
                run_command_as_root(["btrfs", "subvolume", "list", "/"])
            case 2:
                get_snapshots_list()
            case 3:
                snapshot_str = get_validated_input(
                    "Introduzca una descripción para la snapshot"
                )
                create_system_snapshot(snapshot_str)
            case 4:
                delete_system_snapshot()
            case 5:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
