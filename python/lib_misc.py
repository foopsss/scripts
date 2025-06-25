#!/usr/bin/env python3

import subprocess

from lib_io import bg_colour

def run_program(command, check_return=True, use_shell=False):
    # run_program es un wrapper de subprocess.run para
    # ejecutar programas externos. Permite deshabilitar
    # el control de errores de ser necesario, pero por
    # defecto se controla el código de salida que
    # devuelven los programas llamados.
    #
    # run_program también permite utilizar el intérprete
    # de consola del sistema para realizar operaciones,
    # pero esto solo se puede hacer con el control de
    # errores activado.
    if check_return:
        try:
            if use_shell:
                subprocess.run(command, check=True, shell=True)
            else:
                subprocess.run(command, check=True)
        except subprocess.CalledProcessError as error:
            bg_colour("red", "Error de ejecución del programa.")
            bg_colour("red", f"Código de salida: {error.returncode}")
    else:
        if use_shell:
            raise ValueError("No se puede usar check=False con shell=True.")
        else:
            subprocess.run(command, check = False)

def run_with_pkexec(command, mult_op=False):
    # run_with_pkexec es un wrapper de subprocess.run
    # que sirve para ejecutar programas externos con
    # permisos elevados, permitiendo realizar múltiples
    # operaciones al mismo tiempo de ser requerido a
    # través de una llamada al intérprete de Bash,
    # pasándole todos los comandos en cadena.
    if mult_op:
        pkexec_var = ["pkexec", "bash", "-c"]
    else:
        pkexec_var = ["pkexec"]

    try:
        subprocess.run(pkexec_var + command, check=True)
    except subprocess.CalledProcessError as error:
        bg_colour("red", "Error de ejecución del programa.")
        bg_colour("red", f"Código de salida: {error.returncode}")

def pipe_programs(proc1, proc2):
    # pipe_programs es un wrapper de subprocess.Popen
    # que sirve para simular el uso de pipelines como
    # las que se utilizan en los intérpretes de consola.
    # Solo admite la llamada a dos programas.
    #
    # Recibe como entrada dos listas con los programas
    # a ejecutar.
    try:
        proc1_out = subprocess.Popen(proc1, stdout=subprocess.PIPE)
        proc2_out = subprocess.Popen(proc2, stdin=proc1_out.stdout,
                                     stdout=subprocess.PIPE, text=True)
        proc1_out.stdout.close()
        return proc2_out.communicate()[0]
    except OSError as error:
        # Manejo de errores relacionados con el SO como "archivo
        # no encontrado", "permiso denegado", etc.
        bg_colour("red", "Error del SO durante la ejecución de un programa.")
        print(f"{error}")
        return None

def press_enter():
    print("")
    print("Presione ENTER para continuar.", end='')
    input()
