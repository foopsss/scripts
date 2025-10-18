#!/usr/bin/env python3

# TODO: generalizar el tratamiento de excepciones en las funciones para correr
#       comandos.
# TODO: ver si se puede hacer que la lógica de las funciones
#       get_snapshots_list(), create_system_snapshot() y
#       delete_system_snapshot() sea independiente de los volúmenes, de manera
#       que se pueda realizar las snapshots independiente del esquema de
#       subvolúmenes, iterando sobre una lista de subvolúmenes o algo así.
# TODO: discutir con Gemini la idea de dividir líneas largas de alguna manera
#       inteligente, a la hora de mostrar opciones por pantalla.
# TODO: considerar otra manera de separar el input: usando una etiqueta en los
#       comandos.
#       ** Esto añadiría la restricción de que se debe chequear que esta
#          etiqueta y la de UINPUT estén sí o sí al mismo tiempo.
#       ** Para sortear la funcionalidad se puede usar un booleano cuando se
#          detecte la etiqueta, de manera que una vez finalizado el
#          procesamiento de un comando se divide el input y luego se lo aniade
#          a un comando.
# TODO: ver como pasarle variables de entorno a los comandos sin que fallen.
#       Uno de los comandos a modificar es "eix --installed-with-use" con la
#       variable de entorno "EIX_LIMIT=0".
#       ** Para esto se le deben pasar las variables de entorno modificadas al
#          parámetro "env" de subprocess.run(), por lo que probablemente
#          corresponda aniadir una llave extra al parámetro "action", junto con
#          los chequeos que correspondan, como verificar

from modules.menu_creation import run_menu
from modules.program_tools import execute_with_interrupt_handler
from genscript_tools.main_menu import MAIN_MENU_DATA

if __name__ == "__main__":
    execute_with_interrupt_handler(run_menu, MAIN_MENU_DATA)
