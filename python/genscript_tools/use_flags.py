#!/usr/bin/env python3

# Paquetes usados en este módulo:
# app-portage/gentoolkit - provee "euse" y "equery".
# app-portage/eix        - provee "eix".

from modules.console_ui import (
    clear_screen,
    draw_coloured_line,
    get_choice,
    get_validated_input,
    press_enter,
)

from modules.subprocess_utils import (
    run_command,
)


def draw_use_flags_management_menu():
    draw_coloured_line(53, "=")
    print("Apartado para obtener información sobre las USE flags")
    draw_coloured_line(53, "=")
    print("1. Obtener información sobre una USE flag específica.")
    print("2. Obtener una lista de USE flags disponibles para un")
    print("   paquete específico.")
    print("3. Obtener una lista de paquetes que tienen una USE")
    print("   flag específica.")
    print("4. Obtener una lista de paquetes compilados con una")
    print("   USE flag específica.")
    print("5. SALIR.")
    print("")


def use_flags_management_menu():
    while True:
        clear_screen()
        draw_use_flags_management_menu()
        choice = get_choice(1, 5)

        # Limpio la pantalla irrespectivamente de la opción
        # elegida.
        clear_screen()

        if (choice == 1) or (choice >= 3 and choice < 5):
            user_input = get_validated_input("USE flag")
        elif choice == 2:
            user_input = get_validated_input("Nombre del paquete")

        # Pequeño separador entre el diálogo de arriba y la
        # salida de la opción a ejecutar.
        print("")

        match choice:
            case 1:
                run_command(["euse", "-i", f"{user_input}"])
            case 2:
                run_command(["equery", "u", f"{user_input}"])
            case 3:
                run_command(["equery", "h", f"{user_input}"])
            case 4:
                run_command(["eix", "--installed-with-use", f"{user_input}"])
            case 5:
                break

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
