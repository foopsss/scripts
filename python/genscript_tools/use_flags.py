#!/usr/bin/env python3

# Paquetes usados en este módulo:
# app-portage/gentoolkit - provee "euse" y "equery".
# app-portage/eix        - provee "eix".

USE_FLAGS_MENU_DATA = {
    "dict_name": "USE_FLAGS_MENU_DATA",
    "title": "Apartado para obtener información sobre las USE flags",
    "options": [
        {
            "name": "Obtener información sobre una USE flag específica.",
            "action": [["#UINPUT", "euse", "-i"]],
            "prompt": "USE flag",
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Obtener una lista de USE flags disponibles para un\n"
            "   paquete específico.",
            "action": [["#UINPUT", "equery", "u"]],
            "prompt": "Nombre del paquete",
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Obtener una lista de paquetes que tienen una USE\n"
            "   flag específica.",
            "action": [["#UINPUT", "equery", "h"]],
            "prompt": "USE flag",
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Obtener una lista de paquetes compilados con una\n"
            "   USE flag específica.",
            "action": [["#UINPUT", "eix", "--installed-with-use"]],
            "prompt": "USE flag",
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "SALIR.",
            "action": "exit_menu",
        },
    ],
}
