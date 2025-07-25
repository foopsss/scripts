#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# app-portage/genlop - provee "genlop".
# sys-apps/portage - provee "dispatch-conf".
# app-admin/eselect - provee "eselect" y sus módulos.

import os
import shutil
import sys

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
    run_command_as_root,
)
from modules.console_ui import (
    bg_colour,
    clear_screen,
    draw_coloured_line,
    get_choice,
    press_enter,
)

from genmenu_tools.updates import upd_menu


def draw_menu():
    draw_coloured_line(59, "=")
    print("¡Bienvenido a la herramienta de administración del sistema!")
    draw_coloured_line(59, "=")
    print("")
    print("ACTUALIZACIONES")
    draw_coloured_line(15)
    print("1. Menú de opciones de actualización.")
    print("")
    print("PAQUETES Y REPOSITORIOS")
    draw_coloured_line(23)
    print("2. Menú de manejo de paquetes y repositorios del sistema.")
    print("")
    print("LIMPIEZA")
    draw_coloured_line(8)
    print("3. Limpieza de archivos residuales.")
    print("4. Limpieza de versiones antiguas del kernel.")
    print("5. Limpieza de miniaturas de Nautilus.")
    print("")
    print("MISCELÁNEA")
    draw_coloured_line(10)
    print("6. Obtención de información sobre parámetros USE.")
    print("7. Obtención del tiempo de instalación de un paquete.")
    print("8. Resolución de conflictos por diferencia de archivos.")
    print("9. Lectura del boletín de noticias de Gentoo.")
    print("10. SALIR.")
    print("")


def clean_thumbnails():
    thumbdir = os.environ.get("HOME") + "/.cache/thumbnails"

    if os.path.exists(thumbdir):
        try:
            shutil.rmtree(thumbdir)
            bg_colour("green", "La carpeta fue borrada exitosamente.")
        except OSError as error:
            bg_colour("red", "La operación ha fallado.")
            print(f"{error}")
    else:
        bg_colour("blue", "¡La carpeta no existe! No se ha borrado nada.")


def read_news():
    # Obtención del número de noticias disponibles para
    # leer. Acá se simula el pipeline de una consola con
    # pipe_commands y se obtiene el número total de entradas
    # entradas de noticias disponibles para leer revisando
    # los contenidos de la carpeta "/var/lib/gentoo/news".
    read_news = pipe_commands(
        ["cat", "/var/lib/gentoo/news/news-gentoo.read"], ["wc", "-l"]
    )
    unread_news = pipe_commands(
        ["cat", "/var/lib/gentoo/news/news-gentoo.unread"], ["wc", "-l"]
    )

    # Si por algún motivo falla alguno de los dos pipes,
    # entonces no se puede proceder. Eso se considera acá.
    if (read_news is not None) and (unread_news is not None):
        news_count = int(read_news) + int(unread_news)

        # Presentación del menú de noticias disponibles
        # para leer. Debido a que "eselect news list"
        # devuelve 1 como código de salida aún si se lo
        # ejecutó exitosamente, debo desactivar el control
        # de errores para este programa.
        clear_screen()
        run_command(
            ["eselect", "news", "list"], check_return=False, use_shell=False
        )
        print("")

        # Lectura del boletín de noticias deseado.
        # Se utiliza el intérprete de consola del sistema
        # para poder pasar la entrada de noticias por less.
        entry = get_choice(1, news_count)
        run_command(
            f"eselect news read {entry} | less",
            check_return=True,
            use_shell=True,
        )


def get_install_times():
    while True:
        clear_screen()
        draw_coloured_line(59, "=")
        print("Apartado para ver tiempos de instalación de paquetes")
        draw_coloured_line(59, "=")
        print("1. Obtener el tiempo de instalación pasado de un paquete.")
        print("2. Obtener el tiempo de instalación estimado de un paquete.")
        print("3. SALIR.")
        print("")
        choice = get_choice(1, 3)

        if choice < 3:
            pkg = input("Ingrese el nombre de un paquete: ")
            print("")

        match choice:
            case 1:
                run_command(["genlop", "-t", f"{pkg}"])
            case 2:
                # Para esta opción, la idea es no utilizar un pipe
                # con un intérprete de consola, por lo que solo puedo
                # recibir la salida de la operación cuando se termina
                # de ejecutar. Proceso dicha salida para obtener el
                # string que me interesa de ella.
                genlop_output = pipe_commands(
                    ["emerge", "-p", f"{pkg}"], ["genlop", "-p"]
                )
                index = genlop_output.find("Estimated")

                # Para especificar la cota superior de la longitud del
                # trozo de la salida a mostrar por pantalla, utilizo
                # "len(genlop_out) - 1" porque la salida original incluye
                # un salto de línea al final que no me interesa mostrar.
                extracted_string = genlop_output[
                    index : len(genlop_output) - 1
                ]
                print(f"{extracted_string}")
            case 3:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()


def main():
    while True:
        clear_screen()
        draw_menu()
        choice = get_choice(1, 10)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        if (choice >= 3 and choice <= 5) or (choice == 8):
            draw_coloured_line(59)

        match choice:
            case 1:
                upd_menu()
            case 2:
                print("HOLA2")
            case 3:
                run_command_as_root(
                    "eclean-dist -d && eclean-pkg -d", use_shell=True
                )
            case 4:
                run_command_as_root(["eclean-kernel", "-A", "-d", "-n 2"])
            case 5:
                clean_thumbnails()
            case 6:
                print("HOLA6")
            case 7:
                get_install_times()
            case 8:
                run_command_as_root(["dispatch-conf"])
            case 9:
                read_news()
            case 10:
                sys.exit(0)

        # Detengo el script hasta que el usuario presione
        # ENTER para poder leer la información emitida por
        # pantalla al utilizar ciertas opciones.
        if (choice >= 3 and choice <= 5) or (choice == 8):
            press_enter()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        bg_colour("red", "\nEjecución del programa interrupida. ¡Saliendo!")
        sys.exit(1)
