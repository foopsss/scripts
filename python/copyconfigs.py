#!/usr/bin/env python3

# TODO: cuando Python 3.14 sea estabilizado en Gentoo,
#       reescribir el módulo utilizando pathlib.

import shutil
import os

HOME = os.environ.get("HOME")
PORTAGE_FOLDER = "/etc/portage"
GENTOO_OVERLAY = "/var/db/repos/foopsss-gentoo-overlay"
GITHUB_FOLDER = f"{HOME}/Documentos/GitHub"

DATA_TO_COPY = [
    {
        "name": "DOTFILES",
        "elements": [
            f"{HOME}/.config/powershell",
            f"{HOME}/.bashrc",
            f"{HOME}/.bash_custom",
            f"{HOME}/.nanorc",
            f"{HOME}/.emacs.d/init.el"
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
    backup_location = item.get("backup_location")
    # "recreate_tree" es una llave de los diccionarios
    # que permite definir si se debe recrear dentro del
    # directorio objetivo toda la cadena de carpetas que
    # contienen los archivos/directorios a copiar.
    recreate_tree = item.get("recreate_tree", True)

    for element in element_list:
        try:
            if os.path.isdir(element):
                if recreate_tree:
                    copy_path = os.path.join(
                        backup_location, element.lstrip("/")
                    )
                else:
                    copy_path = os.path.join(
                        backup_location, os.path.basename(element)
                    )
                shutil.copytree(src=element, dst=copy_path, dirs_exist_ok=True)
            elif os.path.isfile(element):
                if recreate_tree:
                    element_path = os.path.dirname(element)
                    copy_path = os.path.join(
                        backup_location, element_path.lstrip("/")
                    )
                    os.makedirs(copy_path, exist_ok=True)
                else:
                    copy_path = os.path.join(
                        backup_location, os.path.basename(element)
                    )
                shutil.copy2(src=element, dst=copy_path)
            else:
                raise Exception(
                    f"¡El elemento '{element}' del diccionario {item_name} no"
                    " es ni una carpeta ni un archivo!"
                )
        except Exception as error:
            print(f"Diccionario procesado: {item_name}")
            print(f"\nError producido procesando el elemento: {element}")
            print(f"\nDescripción del error: {error}")
            print("")
