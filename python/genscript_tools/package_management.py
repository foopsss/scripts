#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-apps/portage          - provee "emerge".
# app-admin/eselect         - provee "eselect" y sus módulos.
# app-portage/gentoolkit    - provee "equery".
# app-portage/portage-utils - provee "qlist".
# sys-apps/flatpak          - provee "flatpak".

from modules.console_ui import (
    clear_screen,
    draw_coloured_line,
    get_choice,
    get_validated_input,
    press_enter,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
    run_command_as_root,
)


def draw_package_management_menu():
    draw_coloured_line(61, "=")
    print("Apartado para manejar los paquetes y repositorios del sistema")
    draw_coloured_line(61, "=")
    print("")
    print("REPOSITORIOS")
    draw_coloured_line(12)
    print("1. Añadir un repositorio externo.")
    print("2. Remover un repositorio externo.")
    print("")
    print("PAQUETES")
    draw_coloured_line(8)
    print("3. Instalar un paquete.")
    print("4. Añadir un paquete a @world.")
    print("5. Remover un paquete de @world.")
    print("6. Remover paquetes sin uso.")
    print("7. Obtener una lista de paquetes que dependen de un paquete")
    print("   determinado.")
    print("8. Buscar un paquete en la lista de paquetes instalados.")
    print("9. Buscar un paquete en los repositorios disponibles.")
    print("10. Buscar el paquete que provee un comando o archivo específico.")
    print("")
    print("RECONSTRUCCIÓN DE PAQUETES POR ACTUALIZACIÓN")
    draw_coloured_line(44)
    print("11. Reconstruir paquetes compilados con librerías viejas.")
    print("12. Reconstruir paquetes de Perl y remover los innecesarios.")
    print("")
    print("FLATPAK")
    draw_coloured_line(7)
    print("13. Instalar una aplicación de Flatpak.")
    print("14. Remover una aplicación de Flatpak.")
    print("15. Remover dependencias sin uso.")
    print("")
    print("MISCELÁNEA")
    draw_coloured_line(10)
    print("16. SALIR.")
    print("")


def package_management_menu():
    while True:
        clear_screen()
        draw_package_management_menu()
        choice = get_choice(1, 16)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        #
        # Si utilizo alguna opción que requiera limpiar
        # la pantalla, hago eso.
        match choice:
            case 1 | 2 | 4 | 5 | 8 | 9 | 10:
                draw_coloured_line(61)
            case 16:
                break
            case _:
                clear_screen()

        # Muchas opciones requieren que el usuario introduzca
        # una entrada, así que voy a generalizar los diálogos
        # acá.
        match choice:
            case 1 | 2:
                user_input = get_validated_input("Nombre del repositorio: ")
                print("")
            case 3 | 4 | 5 | 7 | 8 | 9 | 13 | 14:
                user_input = get_validated_input("Nombre del paquete: ")
                print("")
            case 10:
                user_input = get_validated_input("Comando/archivo: ")
                print("")

        match choice:
            case 1:
                run_command_as_root(
                    ["eselect", "repository", "enable", f"{user_input}"]
                )
                run_command_as_root(["emerge", "--sync", f"{user_input}"])
            case 2:
                run_command_as_root(
                    ["eselect", "repository", "remove", f"{user_input}"]
                )
            case 3:
                run_command_as_root(["emerge", f"{user_input}"])
            case 4:
                run_command_as_root(["emerge", "-n", f"{user_input}"])
            case 5:
                run_command_as_root(["emerge", "-W", f"{user_input}"])
            case 6:
                run_command_as_root(["emerge", "-c"])
            case 7:
                run_command(["equery", "d", f"{user_input}"])
            case 8:
                package_search = pipe_commands(
                    ["qlist", "-IRv"], ["grep", f"{user_input}"]
                )
                print(f"{package_search}")
            case 9:
                run_command(["equery", "l", "-Ipo", f"{user_input}"])
            case 10:
                run_command(["equery", "b", f"{user_input}"])
            case 11:
                run_command_as_root(["emerge", "@preserved-rebuild"])
            case 12:
                run_command_as_root(["perl-cleaner", "--all"])
            case 13:
                run_command(["flatpak", "install", f"{user_input}"])
            case 14:
                run_command(["flatpak", "remove", f"{user_input}"])
            case 15:
                run_command(["flatpak", "uninstall", "--unused", "-y"])

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
