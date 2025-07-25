#!/usr/bin/env python3

# TODO: investigar como funciona glsa-check para ponerlo acá.

from modules.console_ui import (
    bg_colour,
    clear_screen,
    draw_coloured_line,
    get_choice,
    press_enter,
)


def upd_menu():
    while True:
        clear_screen()
        draw_coloured_line(59, "=")
        print("Apartado para actualizar el software del sistema")
        draw_coloured_line(59, "=")
        print("")
        print("PAQUETES/REPOSITORIOS")
        draw_coloured_line(21)
        print("1. Sincronizar repositorios, actualizar aplicaciones de")
        print("   Flatpak y actualizar firmware del dispositivo.")
        print("2. Actualizar el sistema ignorando paquetes con altos")
        print("   tiempos de compilación.")
        print("3. Actualizar las aplicaciones de Flatpak.")
        print("4. Actualizar el firmware del dispositivo.")
        print("")
        print("MISCELÁNEA")
        draw_coloured_line(10)
        print("5. Pretender que se va a realizar una actualización.")
        print("6. SALIR.")
        print("")
        choice = get_choice(1, 6)

        match choice:
            # case 1:
            # case 2:
            # case 3:
            # case 4:
            # case 5:
            case 6:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
