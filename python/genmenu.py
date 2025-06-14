#!/usr/bin/env python3

# Paquetes usados en este script:
# app-portage/gentoolkit - provee "eclean".
# app-admin/eclean-kernel - provee "eclean-kernel".
# sys-boot/grub - provee "grub-install" y "grub-mkconfig".
# sys-apps/portage - provee "dispatch-conf".

# TODO: añadir CLI flags para abrir partes específicas del script por consola.
# TODO: añadir algún chequeo en get_choice para lidiar de manera limpia cuando
#       alguien presiona ENTER.
# TODO: añadir algún chequeo para cuando se sale forzosamente con CTRL + C.

import os
import shutil

from lib_misc import press_enter, run_with_pkexec
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
    print("6. Instalar GRUB.")
    print("7. Información sobre parámetros USE.")
    print("8. Tiempos de instalación de los paquetes.")
    print("9. Resolución de conflictos por diferencia de archivos.")
    print("10. Boletín de noticias de Gentoo.")
    print("11. SALIR.")
    print("")

def clean_thumbnails():
    thumbdir = os.environ.get('HOME') + "/.cache/thumbnails"

    if os.path.exists(thumbdir):
        try:
            shutil.rmtree(thumbdir)
            bg_colour("green", "La carpeta fue borrada exitosamente.")
        except OSError as error:
            bg_colour("red", f"La operación ha fallado. Error: {error}")
    else:
        bg_colour("blue", "¡La carpeta no existe! No se ha borrado nada.")

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
            case 8: print("HOLA8")
            case 9: run_with_pkexec(["dispatch-conf"])
            case 10: print("HOLA10")
            case 11: exit(0)

        # Si utilizo alguna de las opciones mencionadas
        # anteriormente, detengo el script hasta que el
        # usuario presione ENTER para poder leer cualquier
        # posible aviso emitido por los programas ejecutados.
        if (choice >= 3 and choice <= 6) or choice == 9:
            draw_line(59)

if __name__ == "__main__":
    main()
