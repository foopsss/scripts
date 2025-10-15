#!/usr/bin/env python3

# TODO: discutir con Gemini la idea de dividir líneas largas de alguna manera
#       inteligente, a la hora de mostrar opciones por pantalla.
# TODO: añadir en updates.py un parámetro para descargar los distfiles
#       automáticamente al actualizar los repositorios.
# TODO: ver si se puede hacer que la lógica de las funciones
#       get_snapshots_list(), create_system_snapshot() y
#       delete_system_snapshot() sea independiente de los volúmenes, de manera
#       que se pueda realizar las snapshots independiente del esquema de
#       subvolúmenes, iterando sobre una lista de subvolúmenes o algo así.
# TODO: a la hora de instalar paquetes no se puede pasarle más de un paquete
#       a Portage cuando se usa la opción correspondiente. Tratar de
#       arreglarlo.

from modules.menu_creation import run_menu
from modules.program_tools import execute_with_interrupt_handler
from genscript_tools.main_menu import MAIN_MENU_DATA

if __name__ == "__main__":
    execute_with_interrupt_handler(run_menu, MAIN_MENU_DATA)
