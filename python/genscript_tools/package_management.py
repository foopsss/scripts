#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-apps/portage          - provee "emerge".
# app-admin/eselect         - provee "eselect" y sus módulos.
# app-portage/gentoolkit    - provee "equery".
# app-portage/portage-utils - provee "qlist".
# app-portage/genlop        - provee "genlop".
# sys-apps/flatpak          - provee "flatpak".

PACKAGE_MANAGEMENT_MENU_DATA = {
    "title": "Apartado para manejar los paquetes y repositorios del sistema",
    "options": [
        {"name": "REPOSITORIOS"},
        {
            "name": "Añadir un repositorio externo.",
            "action": [
                ["#ROOT", "#UINPUT", "eselect", "repository", "enable"],
                ["#ROOT", "#UINPUT", "emerge", "--sync"],
            ],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del repositorio",
        },
        {
            "name": "Remover un repositorio externo.",
            "action": [
                ["#ROOT", "#UINPUT", "eselect", "repository", "remove"],
            ],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del repositorio",
        },
        {"name": "PAQUETES"},
        {
            "name": "Instalar un paquete.",
            "action": [["#ROOT", "#UINPUT", "emerge"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Añadir un paquete a @world.",
            "action": [["#ROOT", "#UINPUT", "emerge", "-n"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Remover un paquete de @world.",
            "action": [["#ROOT", "#UINPUT", "emerge", "-W"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Remover paquetes sin uso.",
            "action": [["#ROOT", "emerge", "-c"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Obtener una lista de paquetes que dependen de un paquete"
            "\n   determinado.",
            "action": [["#UINPUT", "equery", "d"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Buscar un paquete en la lista de paquetes instalados.",
            "action": [
                "#PIPE",
                ["qlist", "-IRv"],
                ["#UINPUT", "grep"],
            ],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Buscar un paquete en los repositorios disponibles.",
            "action": [["#UINPUT", "equery", "l", "-Ipo"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Buscar el paquete que provee un comando o archivo"
            " específico.",
            "action": [["#UINPUT", "equery", "b"]],
            "aesthetic_action": "print_line",
            "prompt": "Comando/archivo",
        },
        {
            "name": "Obtener el tiempo de instalación de un paquete.",
            "action": [["#UINPUT", "genlop", "-t"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {"name": "RECONSTRUCCIÓN DE PAQUETES POR ACTUALIZACIÓN"},
        {
            "name": "Reconstruir paquetes compilados con librerías viejas.",
            "action": [["#ROOT", "emerge", "@preserved-rebuild"]],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Reconstruir paquetes de Perl y remover los innecesarios.",
            "action": [["#ROOT", "perl-cleaner", "--all"]],
            "aesthetic_action": "clear_screen",
        },
        {"name": "FLATPAK"},
        {
            "name": "Instalar una aplicación de Flatpak.",
            "action": [["#UINPUT", "flatpak", "install"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Remover una aplicación de Flatpak.",
            "action": [["#UINPUT", "flatpak", "remove"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Remover dependencias sin uso.",
            "action": [["flatpak", "uninstall", "--unused", "-y"]],
            "aesthetic_action": "clear_screen",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "SALIR.",
            "action": "exit_menu",
        },
    ],
}
