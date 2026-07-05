#!/usr/bin/env python3

import os
import shutil

from pathlib import Path

HOME = os.environ.get("HOME")
PORTAGE_FOLDER = "/etc/portage"
GENTOO_OVERLAY = "/var/db/repos/foopsss-gentoo-overlay"
CONFIG_FOLDER = f"{HOME}/.config"
GITHUB_FOLDER = f"{HOME}/Documentos/GitHub"

DATA_TO_COPY = [
    {
        "name": "DOTFILES",
        "elements": [
            f"{CONFIG_FOLDER}/powershell",
            f"{CONFIG_FOLDER}/helix",
            f"{CONFIG_FOLDER}/zellij",
            f"{HOME}/.bashrc",
            f"{HOME}/.bash_custom",
            f"{HOME}/.nanorc",
            f"{HOME}/.emacs.d/init.el",
        ],
        "backup_location": f"{GITHUB_FOLDER}/configs",
        "recreate_tree": True,
    },
    {
        "name": "GENTOO_CONFIGS",
        "elements": [
            f"{PORTAGE_FOLDER}/binrepos.conf",
            f"{PORTAGE_FOLDER}/env",
            f"{PORTAGE_FOLDER}/package.accept_keywords",
            f"{PORTAGE_FOLDER}/package.mask",
            f"{PORTAGE_FOLDER}/package.use",
            f"{PORTAGE_FOLDER}/make.conf",
            "/var/lib/portage/world",
        ],
        "backup_location": f"{GITHUB_FOLDER}/configs",
        "recreate_tree": True,
    },
    {
        "name": "EBUILD_REPO",
        "elements": [
            f"{GENTOO_OVERLAY}/app-misc",
            f"{GENTOO_OVERLAY}/net-misc",
            f"{GENTOO_OVERLAY}/metadata",
            f"{GENTOO_OVERLAY}/profiles",
        ],
        "backup_location": f"{GITHUB_FOLDER}/gentoo-overlay",
        "recreate_tree": False,
    },
]

for item in DATA_TO_COPY:
    item_name = item.get("name")
    element_list = item.get("elements")
    backup_location = Path(item.get("backup_location"))

    # "recreate_tree" es una llave de los diccionarios
    # que permite definir si se debe recrear dentro del
    # directorio objetivo toda la cadena de carpetas que
    # contienen los archivos/directorios a copiar.
    recreate_tree = item.get("recreate_tree", True)

    for element_str in element_list:
        element = Path(element_str)

        try:
            if not element.exists():
                raise FileNotFoundError(
                    f"¡El elemento '{element_str}' no existe!"
                )

            if element.is_dir() or element.is_file():
                if recreate_tree:
                    # Explicación de como se construye la ruta luego de
                    # backup_location:
                    # 1. "element.parent" obtiene el directorio que contiene a
                    #    "element".
                    # 2. "element.anchor" obtiene el directorio raíz de la ruta
                    #    indicada en "element".
                    # 3. "relative_to(element.anchor)" obtiene la ruta relativa
                    #    a la raíz obtenida, para remover la barra lateral de
                    #    la dirección almacenada en "element", de manera tal
                    #    que se la pueda concatenar con "backup_base".
                    dest_dir = backup_location / element.parent.relative_to(
                        element.anchor
                    )
                else:
                    dest_dir = backup_location

                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_path = dest_dir / element.name

                if dest_path.exists() and dest_path.is_dir():
                    # Las carpetas se borran antes de ser creadas nuevamente
                    # en el directorio de destino porque pathlib no ofrece
                    # nada a la hora de escribir esto que permita
                    # sobreescribir carpetas.
                    shutil.rmtree(dest_path)

                element.copy(dest_path)
            else:
                raise Exception(
                    f"¡El elemento '{element}' del diccionario {item_name} no"
                    " es ni una carpeta ni un archivo!"
                )
        except Exception as error:
            print(f"Diccionario procesado: {item_name}")
            print(f"Error producido procesando el elemento: {element}")
            print(f"Descripción del error: {error}\n")
