#!/usr/bin/env python3

# Paquetes usados en este módulo:
# sys-apps/portage          - provee "emerge".
# app-admin/eselect         - provee "eselect" y sus módulos.
# app-portage/gentoolkit    - provee "equery".
# app-portage/portage-utils - provee "qlist".
# sys-apps/flatpak          - provee "flatpak".

PACKAGE_MANAGEMENT_MENU_DATA = {
    "title": "Apartado para manejar los paquetes y repositorios del sistema",
    "options": [
        {"name": "REPOSITORIOS"},
        {
            "name": "Añadir un repositorio externo.",
            "action": [
                ["eselect", "repository", "enable"],
                ["emerge", "--sync"],
            ],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del repositorio",
            "requires_root": True,
        },
        {
            "name": "Remover un repositorio externo.",
            "action": [["eselect", "repository", "remove"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del repositorio",
            "requires_root": True,
        },
        {"name": "PAQUETES"},
        {
            "name": "Instalar un paquete.",
            "action": [["emerge"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
            "requires_root": True,
        },
        {
            "name": "Añadir un paquete a @world.",
            "action": [["emerge", "-n"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
            "requires_root": True,
        },
        {
            "name": "Remover un paquete de @world.",
            "action": [["emerge", "-W"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
            "requires_root": True,
        },
        {
            "name": "Remover paquetes sin uso.",
            "action": [["emerge", "-c"]],
            "aesthetic_action": "clear_screen",
            "requires_root": True,
        },
        {
            "name": "Obtener una lista de paquetes que dependen de un paquete"
            "\n   determinado.",
            "action": [["equery", "d"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Buscar un paquete en la lista de paquetes instalados.",
            "action": [
                "pipe",
                ["qlist", "-IRv"],
                ["grep"],
            ],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
            "piped_cmd_input_position": "second",
        },
        {
            "name": "Buscar un paquete en los repositorios disponibles.",
            "action": [["equery", "l", "-Ipo"]],
            "aesthetic_action": "print_line",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Buscar el paquete que provee un comando o archivo"
            " específico.",
            "action": [["equery", "b"]],
            "aesthetic_action": "print_line",
            "prompt": "Comando/archivo",
        },
        {"name": "RECONSTRUCCIÓN DE PAQUETES POR ACTUALIZACIÓN"},
        {
            "name": "Reconstruir paquetes compilados con librerías viejas.",
            "action": [["emerge", "@preserved-rebuild"]],
            "aesthetic_action": "clear_screen",
            "requires_root": True,
        },
        {
            "name": "Reconstruir paquetes de Perl y remover los innecesarios.",
            "action": [["perl-cleaner", "--all"]],
            "aesthetic_action": "clear_screen",
            "requires_root": True,
        },
        {"name": "FLATPAK"},
        {
            "name": "Instalar una aplicación de Flatpak.",
            "action": [["flatpak", "install"]],
            "aesthetic_action": "clear_screen",
            "prompt": "Nombre del paquete",
        },
        {
            "name": "Remover una aplicación de Flatpak.",
            "action": [["flatpak", "remove"]],
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
