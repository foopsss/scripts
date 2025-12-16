#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-fs/btrfs-progs - provee "btrfs".
# app-backup/snapper - provee "snapper".

import functools
import json
import sys

from modules.console_ui import (
    draw_coloured_line,
    get_validated_input,
    style_text,
)

from modules.subprocess_utils import run_command


@functools.cache
def _get_snapper_config_list() -> list[tuple[str, str]]:
    """
    _get_snapper_config_list() es una función
    utilizada para determinar cuáles son los
    subvolúmenes de BTRFS configurados para
    que se les realice snapshots con Snapper.

    Esta función devuelve una lista de tuplas,
    cada una de las cuales contiene una
    configuración de Snapper y el subvolumen
    a la que está asociada.
    """
    # Acá no se debe olvidar que, por defecto, una
    # invocación a run_commmand devuelve como resultado
    # un objeto de tipo subprocess.CompletedProcess en
    # caso de que se haya ejecutado correctamente la
    # operación y se quiera almacenar el resultado.
    #
    # Por lo tanto, para acceder a la salida emitida
    # por un comando ejecutado con run_command se debe
    # utilizar el método "stdout" para acceder a dicha
    # salida.
    snapper_raw_output = run_command(
        command=["snapper", "--machine-readable", "json", "list-configs"],
        capture_output=True,
    ).stdout

    try:
        # Si el comando funcionó correctamente,
        # se puede tratar de obtener la lista de
        # configuraciones existentes a partir de
        # la salida provista por Snapper.
        snapper_json_output = json.loads(snapper_raw_output)
        config_list = []

        for element in snapper_json_output["configs"]:
            config_subvolume_tuple = (
                element.get("config", None),
                element.get("subvolume", None),
            )
            config_list.append(config_subvolume_tuple)

        return config_list
    except json.JSONDecodeError as json_error:
        # Si no se puede procesar el JSON obtenido
        # correctamente, es mejor salir de inmediato.
        style_text(
            colour_type="bg",
            colour="red",
            text="No se pudo obtener la lista de configuraciones de Snapper."
            f" Hubo un error al procesar la variable '{json_error.doc}'."
            "\nEl procesamiento empezó a fallar en la posición"
            f" {json_error.pos}, línea {json_error.lineno} y columna"
            f" {json_error.colno}.",
        )
        sys.exit(1)


def get_snapshots_list() -> None:
    """
    get_snapshots_list() es una función utilizada
    para obtener un listado de snapshots de cada
    subvolumen de BTRFS del sistema que tiene
    una configuración de Snapper asociada.
    """
    config_list = _get_snapper_config_list()

    # Se precisa conocer cuál es el último
    # elemento de la lista por motivos
    # estéticos.
    last_config_in_list = config_list[-1][0]

    for config, subvolume in config_list:
        title_str = f"Snapshots del subvolumen '{subvolume}'"
        title_str_length = len(title_str)
        draw_coloured_line(length=title_str_length, symbol="=")
        print(title_str)
        draw_coloured_line(length=title_str_length, symbol="=")
        run_command(["snapper", "-c", f"{config}", "list"])

        # Si todavía no se está trabajando con
        # el último elemento de la lista de
        # configuraciones, corresponde imprimir
        # un separador para separar cada listado.
        if not (config == last_config_in_list):
            print("")


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

    config_list = _get_snapper_config_list()
    for config, _ in config_list:
        # Limpieza de snapshots innecesarias.
        run_command(["snapper", "-c", f"{config}", "cleanup", "number"])

        # Creación de snapshot.
        run_command(
            [
                "snapper",
                "-c",
                f"{config}",
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
    config_list = _get_snapper_config_list()
    get_snapshots_list()
    print("")

    snapshot_number = get_validated_input(
        "Introduzca el número de snapshot a borrar",
    )

    for config, _ in config_list:
        run_command(
            ["snapper", "-c", f"{config}", "delete", f"{snapshot_number}"]
        )


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
            "name": "Obtener el listado de snapshots existentes actualmente"
            " para los subvolúmenes del sistema.",
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
            "action": "exit",
        },
    ],
}
