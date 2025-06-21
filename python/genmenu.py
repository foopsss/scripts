#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# sys-boot/grub - provee "grub-install" y "grub-mkconfig".
# app-portage/genlop - provee "genlop".
# sys-apps/portage - provee "dispatch-conf".
# app-admin/eselect - provee "eselect" y sus módulos.

# TODO: añadir algún chequeo para cuando se sale forzosamente con CTRL + C.

import os
import shutil

from lib_misc import pipe_programs, press_enter, run_program, run_with_pkexec
from lib_io import bg_colour, clear_screen, draw_line, get_choice

def draw_menu():
    draw_line(59, "=")
    print("¡Bienvenido a la herramienta de administración del sistema!")
    draw_line(59, "=")
    print("ACTUALIZACIONES")
    draw_line(15)
    print("1. Menú de opciones de actualización.")
    print("")
    print("PAQUETES Y REPOSITORIOS")
    draw_line(23)
    print("2. Menú de manejo de paquetes y repositorios del sistema.")
    print("")
    print("LIMPIEZA")
    draw_line(8)
    print("3. Limpieza de archivos residuales.")
    print("4. Limpieza de versiones antiguas del kernel.")
    print("5. Limpieza de miniaturas de Nautilus.")
    print("")
    print("MISCELÁNEA")
    draw_line(10)
    print("6. Instalación de GRUB.")
    print("7. Obtención de información sobre parámetros USE.")
    print("8. Obtención del tiempo de instalación de un paquete.")
    print("9. Resolución de conflictos por diferencia de archivos.")
    print("10. Lectura del boletín de noticias de Gentoo.")
    print("11. SALIR.")
    print("")

def clean_thumbnails():
    thumbdir = os.environ.get('HOME') + "/.cache/thumbnails"

    if os.path.exists(thumbdir):
        try:
            shutil.rmtree(thumbdir)
            bg_colour("green", "La carpeta fue borrada exitosamente.")
        except OSError as error:
            bg_colour("red", f"La operación ha fallado.")
            print(f"{error}")
    else:
        bg_colour("blue", "¡La carpeta no existe! No se ha borrado nada.")

def read_news():
    # Obtención del número de noticias disponibles para
    # leer. Acá se simula el pipeline de una consola con
    # pipe_programs y se obtiene el número total de entradas
    # entradas de noticias disponibles para leer revisando
    # los contenidos de la carpeta "/var/lib/gentoo/news".
    read_news = pipe_programs(
                    ["cat", "/var/lib/gentoo/news/news-gentoo.read"],
                    ["wc", "-l"]
                )
    unread_news = pipe_programs(
                    ["cat", "/var/lib/gentoo/news/news-gentoo.unread"],
                    ["wc", "-l"]
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
        run_program(["eselect", "news", "list"], False, False)
        print("")

        # Lectura del boletín de noticias deseado.
        # Se utiliza el intérprete de consola del sistema
        # para poder pasar la entrada de noticias por less.
        entry = get_choice(1, news_count)
        run_program([f"eselect news read {entry} | less"], True, True)

def get_install_times():
    while True:
        clear_screen()
        draw_line(59, "=")
        print("Apartado para ver tiempos de instalación de paquetes")
        draw_line(59, "=")
        print("1. Obtener el tiempo de instalación pasado de un paquete.")
        print("2. Obtener el tiempo de instalación estimado de un paquete.")
        print("3. SALIR.")
        print("")
        choice = get_choice(1, 3)

        if (choice < 3):
            pkg = input("Ingrese el nombre de un paquete: ")
            print("")

        match choice:
            case 1: run_program(["genlop", "-t", f"{pkg}"])
            case 2: print(pipe_programs(["emerge", "-p", f"{pkg}"],
                                        ["genlop", "-p"]))
            case 3: break

        press_enter()

def main():
    while True:
        clear_screen()
        draw_menu()
        choice = get_choice(1, 11)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        if (choice >= 3 and choice <= 6) or choice == 9:
            draw_line(59)

        match choice:
            case 1: print("HOLA")
            case 2: print("HOLA2")
            case 3: run_with_pkexec(["eclean-dist -d && eclean-pkg -d"], True)
            case 4: run_with_pkexec(["eclean-kernel", "-A", "-d", "-n 2"])
            case 5: clean_thumbnails()
            case 6: run_with_pkexec(["grub-install --target=x86_64-efi \
                                    --efi-directory=/boot --removable && \
                                    grub-mkconfig -o /boot/grub/grub.cfg"],
                                    True)
            case 7: print("HOLA7")
            case 8: get_install_times()
            case 9: run_with_pkexec(["dispatch-conf"])
            case 10: read_news()
            case 11: exit(0)

        # Detengo el script hasta que el usuario presione
        # ENTER para poder leer la información emitida por
        # pantalla al utilizar ciertas opciones.
        if (choice >= 3 and choice <= 6) or (choice >= 9 and choice <= 10):
            press_enter()

if __name__ == "__main__":
    main()
