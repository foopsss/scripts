#!/usr/bin/env python

from lib_io import bg_colour, clear_screen, draw_line, get_choice
from lib_misc import press_enter

def upd_menu():
    while True:
        clear_screen()
        draw_line(59, "=")
        print("Apartado para actualizar el software del sistema")
        draw_line(59, "=")
        print("")
        print("PAQUETES/REPOSITORIOS")
        draw_line(21)
        print("1. Sincronizar repositorios, actualizar aplicaciones de")
        print("   Flatpak y actualizar firmware del dispositivo.")
        print("2. Actualizar el sistema ignorando paquetes con altos")
        print("   tiempos de compilación.")
        print("3. Actualizar el sistema utilizando paquetes precompilados")
        print("   de los repositorios de Gentoo.")
        print("4. Actualizar las aplicaciones de Flatpak.")
        print("5. Actualizar el firmware del dispositivo.")
        print("")
        print("MISCELÁNEA")
        draw_line(10)
        print("6. Pretender que se va a realizar una actualización.")
        print("7. SALIR.")
        print("")
        choice = get_choice(1, 7)

        match choice:
            # case 1:
            # case 2:
            # case 3:
            # case 4:
            # case 5:
            # case 6:
            case 7: break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
