#!/usr/bin/env python3

import subprocess

from lib_io import bg_colour

def run_with_pkexec(command, mult_op=False):
    # "mult_op" significa "multiples operaciones"
    # y se usa para indicar si se van a realizar
    # múltiples operaciones con pkexec o no, en
    # cuyo caso es necesario pasarle todos los
    # comandos en una cadena al intérprete de
    # Bash y ejecutar eso con pkexec.
    if mult_op:
        pkexec_var = ["pkexec", "bash", "-c"]
    else:
        pkexec_var = ["pkexec"]

    try:
        result = subprocess.run(pkexec_var + command, check = True)
    except subprocess.CalledProcessError as error:
        bg_colour("red", "La operación ha fallado.")
        bg_colour("red", f"Código de error: {error.returncode}")

def press_enter():
    print("")
    print("Presione ENTER para continuar.", end='')
    input()
