#!/usr/bin/env python3

# Paquetes usados en este módulo:
# app-portage/gentoolkit  - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# sys-apps/portage        - provee "dispatch-conf".
# sys-apps/coreutils      - provee "cat" y "wc".
# app-admin/eselect       - provee "eselect" y sus módulos.

import os
import shutil
import sys
import threading

from modules.console_ui import (
    get_choice,
    style_text,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
)

from genscript_tools.package_management import PACKAGE_MANAGEMENT_MENU_DATA
from genscript_tools.snapshots import SNAPSHOT_MANAGEMENT_MENU_DATA
from genscript_tools.updates import UPDATES_MENU_DATA
from genscript_tools.use_flags import USE_FLAGS_MENU_DATA


def clean_thumbnails() -> None:
    """
    clean_thumbnails() es una función que sirve para borrar
    las miniaturas del sistema, localizadas en la carpeta
    "~/.cache/thumbnails".
    """
    thumbdir = os.environ.get("HOME") + "/.cache/thumbnails"

    if os.path.exists(thumbdir):
        try:
            shutil.rmtree(thumbdir)
            style_text("bg", "green", "La carpeta fue borrada exitosamente.")
        except OSError as error:
            style_text("bg", "red", "La operación ha fallado.")
            print(f"{error}")
    else:
        style_text(
            "bg", "blue", "¡La carpeta no existe! No se ha borrado nada."
        )


def _get_news_count(result_container: list) -> None:
    """
    _get_news_count() es una función utilizada para obtener
    la cantidad de noticias que aparecerán en pantalla al
    utilizar el comando "eselect news list".

    _get_news_count() es llamada por read_news() y se ejecuta
    de manera concurrente a la vez que se muestra el listado
    de noticias, utilizando hilos o threads para tal fin.

    Esta función se ejecuta en el hilo secundario, o hilo
    concurrente, por lo que luego el resultado de la ejecución
    debe ser devuelto al hilo principal a través del parámetro
    "result_container" que toma como entrada.
    """
    try:
        # Obtención del número de noticias disponibles para
        # leer. Acá se simula el pipeline de una consola con
        # pipe_commands y se obtiene el número total de entradas
        # entradas de noticias disponibles para leer revisando
        # los contenidos de la carpeta "/var/lib/gentoo/news".
        news_folder = "/var/lib/gentoo/news"
        news_count = 0

        for file in os.listdir(news_folder):
            if file.endswith((".read", ".unread")):
                file_line_count = pipe_commands(
                    ["cat", f"/var/lib/gentoo/news/{file}"], ["wc", "-l"]
                )
                news_count += int(file_line_count)

        # Guardo el resultado del recuento en la lista de
        # entrada, para que el hilo principal pueda acceder
        # al número.
        result_container.append(news_count)
    except OSError as os_error:
        # Si no se puede obtener el número de noticias
        # correctamente, es mejor salir de inmediato.
        style_text(
            "bg",
            "red",
            "Se produjo un error del sistema al procesar la carpeta"
            f" '{news_folder}' y no se pudo obtener la cantidad de"
            " entradas de noticias de Gentoo disponibles para leer."
            f"\nEl error encontrado es: {os_error}.",
        )
        sys.exit(1)


def read_news() -> None:
    """
    read_news() es una función que se utiliza para
    mostrarle al usuario el listado de entradas de
    noticias disponibles para leer y pedirle que
    seleccione una noticia con el fin de leerla.
    """
    # Inicio el recuento de noticias disponibles en
    # un hilo secundario o concurrente, de manera que
    # esta tarea se realice "al mismo tiempo" que
    # la impresión por pantalla del listado de noticias
    # para leer.
    #
    # Las comillas se deben a que esto no es paralelismo,
    # pero simplemente concurrencia, por lo que solo
    # estoy simulando que las tareas se ejecutan al
    # mismo tiempo.
    result_container = []
    count_thread = threading.Thread(
        target=_get_news_count,
        args=[result_container],
    )
    count_thread.start()

    # Presentación del menú de noticias disponibles
    # para leer. Debido a que "eselect news list"
    # devuelve 1 como código de salida aún si se lo
    # ejecutó exitosamente, debo desactivar el control
    # de errores para este programa.
    run_command(
        ["eselect", "news", "list"], check_return=False, use_shell=False
    )
    print("")

    # Espero que el hilo secundario/concurrente termine
    # con el recuento de noticias y luego obtengo el
    # valor.
    count_thread.join()
    news_count = result_container[0]

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
            "action": [["#ROOT", "eclean-kernel", "-A", "-d", "-n 3"]],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Limpiar miniaturas de Nautilus.",
            "action": [clean_thumbnails],
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
            "action": [read_news],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "SALIR.",
            "action": "exit_script",
        },
    ],
}
