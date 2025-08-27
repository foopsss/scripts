#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit  - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# sys-apps/portage        - provee "dispatch-conf".
# sys-apps/coreutils      - provee "cat" y "wc".
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

from genscript_tools.updates import updates_menu
from genscript_tools.package_management import package_management_menu
from genscript_tools.snapshots import snapshot_management_menu
from genscript_tools.use_flags import use_flags_management_menu


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
    print("4. Menú de obtención de información sobre USE flags.")
    print("")
    print("OPCIONES DE LIMPIEZA")
    draw_coloured_line(20)
    print("5. Limpiar archivos residuales.")
    print("6. Limpiar versiones antiguas del kernel.")
    print("7. Limpiar miniaturas de Nautilus.")
    print("")
    print("MISCELÁNEA")
    draw_coloured_line(10)
    print("8. Resolver conflictos por diferencia de archivos.")
    print("9. Leer el boletín de noticias de Gentoo.")
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
    news_folder = "/var/lib/gentoo/news"
    news_count = 0

    for file in os.listdir(news_folder):
        if file.endswith(".read") or file.endswith(".unread"):
            file_line_count = pipe_commands(
                ["cat", f"/var/lib/gentoo/news/{file}"], ["wc", "-l"]
            )
            news_count += int(file_line_count)

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
        choice = get_choice(1, 10)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        #
        # Si utilizo alguna opción que requiera limpiar
        # la pantalla, hago eso.
        if choice >= 5 and choice <= 8:
            draw_coloured_line(59)
        elif choice == 9:
            clear_screen()

        match choice:
            case 1:
                updates_menu()
            case 2:
                package_management_menu()
            case 3:
                snapshot_management_menu()
            case 4:
                use_flags_management_menu()
            case 5:
                # doas recuerda al último usuario autenticado
                # por 5 minutos, tiempo más que suficiente para
                # ejecutar estas dos opciones, por lo que no es
                # necesario llamarlas juntas a través de un
                # intérprete de consola para mantener los permisos
                # de superusuario.
                run_command_as_root(["eclean-dist", "-d"])
                run_command_as_root(["eclean-pkg", "-d"])
            case 6:
                run_command_as_root(["eclean-kernel", "-A", "-d", "-n 2"])
            case 7:
                clean_thumbnails()
            case 8:
                run_command_as_root(["dispatch-conf"])
            case 9:
                read_news()
            case 10:
                sys.exit(0)

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú o se entra a otro apartado del script u otros
        # módulos.
        if choice >= 5 and choice <= 8:
            press_enter()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        bg_colour("red", "\nEjecución del programa interrupida. ¡Saliendo!")
        sys.exit(1)
