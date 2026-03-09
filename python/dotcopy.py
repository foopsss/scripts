#!/usr/bin/env python3

# TODO: cuando Python 3.14 sea estabilizado en Gentoo,
#       reescribir el módulo utilizando pathlib.

import shutil
import os

BACKUP_LOCATION = os.environ.get("HOME") + "/Documentos/A"
DATA = ["/etc/hosts", "/etc/eclean"]

for item in DATA:
    if not os.path.exists(item):
        raise ValueError(f"¡La ruta {item} no existe!")

    if os.path.isdir(item):
        copy_path = BACKUP_LOCATION + item

        # shutil.copytree se va a quejar si la carpeta
        # a copiar ya existe, en vez de simplemente
        # sobreescribirla.
        if os.path.exists(copy_path):
            shutil.rmtree(copy_path)

        shutil.copytree(item, copy_path)
    elif os.path.isfile(item):
        item_path = os.path.dirname(item)
        copy_path = BACKUP_LOCATION + item_path

        # shutil.copy se va a quejar si la carpeta
        # contenedora no existe en primera instancia,
        # en vez de crearla.
        if not os.path.exists(copy_path):
            os.makedirs(copy_path, exist_ok=True)

        shutil.copy(item, copy_path)
    else:
        raise Exception(
            f"¡La ruta '{item}' no es ni una carpeta ni un archivo!"
        )
