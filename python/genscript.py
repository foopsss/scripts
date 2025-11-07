#!/usr/bin/env python3

# TODO: discutir con Gemini la idea de dividir líneas largas de alguna manera
#       inteligente, a la hora de mostrar opciones por pantalla.
# TODO: ver como pasarle variables de entorno a los comandos sin que fallen.
#       Uno de los comandos a modificar es "eix --installed-with-use" con la
#       variable de entorno "EIX_LIMIT=0".
#       ** Para esto se le deben pasar las variables de entorno modificadas al
#          parámetro "env" de subprocess.run(), por lo que probablemente
#          corresponda aniadir una llave extra al diccionario, junto con los
#          chequeos que correspondan.
#       ** La llave podría tomar como parámetro una lista de tuplas, donde el
#          primer elemento es el número de comando al que se le debe anexar la
#          variable de entorno, mientras que el segundo elemento es un string
#          con la variable de entorno en sí.
# TODO: ver una manera de arreglar el uso hardcodeado de doas.
# TODO: mejores type hints para menu_creation.py. Usar lo de TypedDict y crear
#       un subpaquete para todas las cosas que tienen que ver con la creación
#       de menús.

from modules.menu_creation import run_menu
from modules.program_tools import execute_with_interrupt_handler
from genscript_tools.main_menu import MAIN_MENU_DATA

if __name__ == "__main__":
    execute_with_interrupt_handler(run_menu, MAIN_MENU_DATA)
