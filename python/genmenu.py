#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit  - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# app-portage/genlop      - provee "genlop".
# sys-apps/portage        - provee "emerge" y "dispatch-conf".
# app-admin/eselect       - provee "eselect" y sus módulos.

import os
import shutil
import sys

from modules.console_ui import (
    bg_colour,
    clear_screen,
    draw_coloured_line,
    get_choice,
    press_enter,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
    run_command_as_root,
)

from genmenu_tools.updates import updates_menu
from genmenu_tools.snapshots import snapshot_management_menu


def draw_menu():
    draw_coloured_line(59, "=")
    print("¡Bienvenido a la herramienta de administración del sistema!")
    draw_coloured_line(59, "=")
    print("")
    print("APARTADOS ADICIONALES")
    draw_coloured_line(21)
    print("1. Menú de opciones de actualización.")
    print("2. Menú de manejo de paquetes y repositorios del sistema.")
    print("3. Menú de manejo de snapshots.")
    print("")
    print("OPCIONES DE LIMPIEZA")
    draw_coloured_line(20)
    print("4. Limpiar archivos residuales.")
    print("5. Limpiar versiones antiguas del kernel.")
    print("6. Limpiar miniaturas de Nautilus.")
    print("")
    print("MISCELÁNEA")
    draw_coloured_line(10)
    print("7. Resolver conflictos por diferencia de archivos.")
    print("8. Leer el boletín de noticias de Gentoo.")
    print("9. SALIR.")
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


def main():
    while True:
        clear_screen()
        draw_menu()
        choice = get_choice(1, 9)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        #
        # Si utilizo alguna opción que requiera limpiar
        # la pantalla, hago eso.
        if choice >= 4 and choice <= 7:
            draw_coloured_line(59)
        elif choice == 8:
            clear_screen()

        match choice:
            case 1:
                updates_menu()
            case 2:
                print("HOLA2")
            case 3:
                snapshot_management_menu()
            case 4:
                # doas recuerda al último usuario autenticado
                # por 5 minutos, tiempo más que suficiente para
                # ejecutar estas dos opciones, por lo que no es
                # necesario llamarlas juntas a través de un
                # intérprete de consola para mantener los permisos
                # de superusuario.
                run_command_as_root(["eclean-dist", "-d"])
                run_command_as_root(["eclean-pkg", "-d"])
            case 5:
                run_command_as_root(["eclean-kernel", "-A", "-d", "-n 2"])
            case 6:
                clean_thumbnails()
            case 7:
                run_command_as_root(["dispatch-conf"])
            case 8:
                read_news()
            case 9:
                sys.exit(0)

        # Detengo el script hasta que el usuario presione
        # ENTER para poder leer la información emitida por
        # pantalla al utilizar ciertas opciones.
        if choice >= 4 and choice <= 7:
            press_enter()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        bg_colour("red", "\nEjecución del programa interrupida. ¡Saliendo!")
        sys.exit(1)
