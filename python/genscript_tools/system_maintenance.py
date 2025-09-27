#!/usr/bin/env python3

# Paquetes usados en este módulo:
# app-admin/eselect - provee "eselect" y sus módulos.

import os
import shutil
import threading

from modules.console_ui import (
    get_choice,
    style_text,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
)


def clean_thumbnails():
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


def read_news():
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
