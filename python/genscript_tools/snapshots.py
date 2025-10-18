#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-fs/btrfs-progs - provee "btrfs".
# app-backup/snapper - provee "snapper".

from modules.console_ui import (
    draw_coloured_line,
    get_validated_input,
)

from modules.subprocess_utils import run_command


def get_snapshots_list() -> None:
    """
    get_snapshots_list() es una función utilizada
    para obtener un listado de snapshots de cada
    subvolumen de BTRFS del sistema.
    """
    title1_str = "Snapshots del volumen @/"
    draw_coloured_line(len(title1_str), "=")
    print(title1_str)
    draw_coloured_line(len(title1_str), "=")
    run_command(["snapper", "-c", "root", "list"])
    print()

    title2_str = "Snapshots del volumen @/home"
    draw_coloured_line(len(title2_str), "=")
    print(title2_str)
    draw_coloured_line(len(title2_str), "=")
    run_command(["snapper", "-c", "home", "list"])


def create_system_snapshot(snapshot_description: str) -> None:
    """
    create_system_snapshot() es una función
    utilizada para limpiar snapshots innecesarias
    y luego crear una snapshot del sistema.

    Debe recibir como parámetro una cadena que
    contenga una descripción de la snapshot
    que se va a crear.
    """
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


def create_system_snapshot_with_prompt() -> None:
    """
    create_system_snapshot_with_prompt() es una
    función que sirve para crear una snapshot
    del sistema tras pedirle al usuario que
    introduzca una descripción para dicha
    snapshot.
    """
    snapshot_str = get_validated_input(
        "Introduzca una descripción para la snapshot"
    )
    create_system_snapshot(snapshot_str)


def delete_system_snapshot() -> None:
    """
    delete_system_snapshot() es una función
    utilizada para borrar snapshots del sistema.
    Le muestra al usuario un listado de snapshots
    disponibles y le pide que especifique cuál
    desea borrar.
    """
    get_snapshots_list()
    print("")

    snapshot_number = get_validated_input(
        "Introduzca el número de snapshot a borrar",
    )

    run_command(["snapper", "-c", "root", "delete", f"{snapshot_number}"])
    run_command(["snapper", "-c", "home", "delete", f"{snapshot_number}"])


SNAPSHOT_MANAGEMENT_MENU_DATA = {
    "dict_name": "SNAPSHOT_MANAGEMENT_MENU_DATA",
    "title": "Apartado para manejar snapshots de Snapper y subvolúmenes de"
    " BTRFS",
    "options": [
        {"name": "MANEJO DE SUBVOLÚMENES"},
        {
            "name": "Obtener el listado de subvolúmenes presentes"
            " actualmente.",
            "action": [["#ROOT", "btrfs", "subvolume", "list", "/"]],
            "aesthetic_action": "print_line",
        },
        {"name": "MANEJO DE SNAPSHOTS"},
        {
            "name": "Obtener el listado de snapshots existentes actualmente\n"
            "   para los subvolúmenes del sistema.",
            "action": [get_snapshots_list],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Crear una snapshot del sistema.",
            "action": [create_system_snapshot_with_prompt],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Eliminar una snapshot del sistema.",
            "action": [delete_system_snapshot],
            "aesthetic_action": "clear_screen",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "SALIR.",
            "action": "exit_menu",
        },
    ],
}
