#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo contiene una serie de funciones para ejecutar comandos externos en
un script de Python, las cuales se tratan básicamente de wrappers de los
métodos subprocess.run() y subprocess.Popen().

### Particularidades de las funciones run_command() y run_command_as_root() ###
* Tanto run_command() como run_command_as_root() comparten la peculiaridad de
  que el tipo de su argumento "command" depende del parámetro "use_shell":

  1. Si "use_shell=True":
     El argumento "command" DEBE ser una cadena (string).
     Esta cadena será pasada directamente al intérprete de consola del sistema
     para su ejecución, a través del método subprocess.run().

     Las únicas operaciones que deberían ejecutarse a través de un intérprete
     deberían ser aquellas que justamente se beneficien de sus capacidades y
     no se puedan realizar de manera convencional, con "use_shell=False".
     Ejemplo: "ls -l /tmp | grep .txt".

  2. Si "use_shell=False":
     El argumento "command" DEBE ser una lista de cadenas (list of strings).
     Los elementos de la lista se pasarán como argumentos individuales al
     método subprocess.run(), sin utilizar un intérprete de consola para
     ejecutar el comando introducido.
     Ejemplo: ["ls", "-l", "/var/log"].

  --- Manejo de errores por formato incorrecto ---

  -  Los tipos de los datos suministrados a las funciones son validados
     previo a intentar ejecutar los comandos. En caso de que estos no
     tengan el formato correcto, se producirá una excepción del tipo
     "TypeError", la cual abortará la ejecución del programa e indicará
     dónde se encuentra el error y porqué se produjo. Esta validación se
     realiza a través de una función llamada _check_command_argument_type().

  --- Manejo de errores en tiempo de ejecución ---

  -  Los errores de ejecución son captados a través del manejo de la excepción
     "subprocess.CalledProcessError". En caso de ocurrir un error de ejecución
     se le informará al usuario y se mostrará el código de error.

* Siempre que no se intente ejecutar comandos a través del intérprete de
  consola, run_command() permite deshabilitar el control de errores. Sin
  embargo, en el caso de run_command_as_root(), el control de errores
  siempre está habilitado.

### Particularidades de la función pipe_commands() ###
* Al igual que con las funciones run_command() y run_command_as_root(), los
  argumentos "first_command" y "second_command" deben tratarse de cadenas de
  strings. En caso de que no tengan el formato correcto, sucederá lo mismo
  que sucede con las validaciones en run_command() y run_command_as_root(),
  a través de la función _check_command_argument_type().
"""

import subprocess

from modules.console_ui import bg_colour


# --- Funciones privadas ---
def _check_command_argument_type(command, use_shell):
    # _check_command_argument_type() se encarga de validar
    # los tipos de los comandos que se quieren ejecutar en
    # las funciones que siguen, en función de si estos se
    # van a ejecutar a través de un intérprete de consola
    # o directamente a través de un método de la librería
    # subprocess.
    if use_shell:
        if not isinstance(command, str):
            raise TypeError("El comando debe suministrarse como un string.")
    else:
        if not isinstance(command, list):
            raise TypeError(
                "El comando debe suministrarse como una cadena de " "strings."
            )

        if not all(isinstance(item, str) for item in command):
            raise TypeError(
                "Todas los elementos de la cadena correspondiente "
                "al comando deben tratarse de strings."
            )


def _run_command_exception_message(exec_error):
    # Mensaje de error compartido para las funciones
    # run_command() y run_command_as_root() en caso de que
    # se esté manejando la excepción subprocess.CalledProcessError.
    bg_colour("red", "Error de ejecución del programa.")
    bg_colour("red", f"Código de salida: {exec_error.returncode}")


# --- Funciones públicas ---
def run_command(command, check_return=True, use_shell=False):
    # run_command es un wrapper de subprocess.run para
    # ejecutar programas externos. Permite deshabilitar
    # el control de errores de ser necesario, pero por
    # defecto se controla el código de salida que
    # devuelven los programas llamados.
    #
    # run_command también permite utilizar el intérprete
    # de consola del sistema para realizar operaciones,
    # pero esto solo se puede hacer con el control de
    # errores activado.
    if not check_return and use_shell:
        raise ValueError(
            "No se puede usar la función con check_return=False y "
            "con use_shell=True. No es seguro."
        )

    _check_command_argument_type(command, use_shell)

    try:
        subprocess.run(command, check=check_return, shell=use_shell)
    except subprocess.CalledProcessError as error:
        # Si el comando no se puede ejecutar por algún motivo, se manejará
        # este error.
        _run_command_exception_message(error)


def run_command_as_root(command, use_shell=False):
    # run_command_as_root() es un wrapper de subprocess.run
    # que sirve para ejecutar comandos externos con permisos
    # elevados, permitiendo realizar múltiples operaciones
    # de ser requerido a través de una llamada al intérprete
    # de consola.
    #
    # A diferencia de run_command(), no permite desactivar
    # el control de errores.
    _check_command_argument_type(command, use_shell)

    try:
        if use_shell:
            subprocess.run(f"doas {command}", check=True, shell=True)
        else:
            subprocess.run(["doas"] + command, check=True, shell=False)
    except subprocess.CalledProcessError as error:
        # Si el comando no se puede ejecutar por algún motivo, se manejará
        # este error.
        _run_command_exception_message(error)


def pipe_commands(first_command, second_command):
    # pipe_commands() es un wrapper de subprocess.Popen()
    # que sirve para simular el uso de pipelines, como las
    # que se utilizan en los intérpretes de consola. Solo
    # admite la llamada a dos programas.
    #
    # Recibe como entrada dos listas con los programas
    # a ejecutar.
    _check_command_argument_type(first_command, use_shell=False)
    _check_command_argument_type(second_command, use_shell=False)

    try:
        first_command_out = subprocess.Popen(
            first_command, stdout=subprocess.PIPE
        )
        second_command_out = subprocess.Popen(
            second_command,
            stdin=first_command_out.stdout,
            stdout=subprocess.PIPE,
            text=True,
        )
        first_command_out.stdout.close()
        return second_command_out.communicate()[0]
    except OSError as error:
        # Manejo de errores relacionados con el SO como "archivo
        # no encontrado", "permiso denegado", etc.
        bg_colour("red", "Error del SO durante la ejecución de un programa.")
        print(f"{error}")
        return None

