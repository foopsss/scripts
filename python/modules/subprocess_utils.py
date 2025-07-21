#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
* Tanto run_command como run_command_as_root comparten la peculiaridad de
  que el tipo de su argumento "command" depende del parámetro "use_shell":

  1.  Si "use_shell=True":
      El argumento "command" DEBE ser una **cadena (string)**.
      Esta cadena será pasada directamente al intérprete de consola del sistema.
      Ejemplo: "ls -l /tmp | grep .txt".

      En aquellos casos donde no se necesite utilizar pipelines o anidar
      comandos, la función SÍ podrá ejecutar comandos en formato de lista
      correctamente, pero se recomienda utilizar un string completo en todos
      los casos para mantener la coherencia y aprovechar toda la funcionalidad
      de un intérprete de consola.
      Ejemplo: ["ls", "-l"]

  2.  Si "use_shell=False":
      El argumento "command" DEBE ser una **lista de cadenas (list of strings)**.
      Los elementos de la lista se pasarán como argumentos individuales al programa,
      sin interpretación de shell.
      Ejemplo: ["ls", "-l", "/var/log"]

  --- Manejo de errores por formato incorrecto (TypeError y otros) ---

  -   Si NO se respeta el tipo de formato principal esperado (es decir, se pasa
      una cadena cuando "use_shell=False"), se producirá una excepción del tipo
      `TypeError`, la cual abortará la ejecución del programa e indicará dónde
      se encuentra el error.

  -   Si se pasa un formato válido pero que el intérprete de consola no puede
      procesar correctamente (como una lista compleja cuando "use_shell=True"
      o un string con sintaxis inválida), o si el comando es válido pero falla
      durante su ejecución (ej. el comando no existe, tiene permisos incorrectos
      o devuelve un código de salida distinto de cero), se capturará una excepción
      del tipo `subprocess.CalledProcessError`. En ese caso, se mostrará un
      mensaje de error y el código de salida del programa. Asimismo, en casos
      raros de comandos que no terminan, el script podría quedarse "colgado".
"""

import subprocess

from modules.console_ui import bg_colour

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
        raise ValueError("No se puede usar la función con check_return=False y "
                         "con use_shell=True. No es seguro.")

    try:
        subprocess.run(command, check=check_return, shell=use_shell)
    except subprocess.CalledProcessError as error:
        # Si el comando no se puede ejecutar por algún motivo, se manejará
        # este error.
        bg_colour("red", "Error de ejecución del programa.")
        bg_colour("red", f"Código de salida: {error.returncode}")
    except TypeError:
        # Si el comando a ejecutar tiene una sintaxis incorrecta, interrumpir la
        # ejecución del programa.
        bg_colour("red", "Tipo de comando incorrecto.")
        bg_colour("red", "Cuando 'use_shell=True', 'command' debe ser una "
                         "cadena (string).")
        bg_colour("red", "Cuando 'use_shell=False', 'command' debe ser una lista "
                         "de cadenas (list of strings).")
        raise

def run_command_as_root(command, use_shell=False):
    # run_command_as_root es un wrapper de subprocess.run
    # que sirve para ejecutar comandos externos con
    # permisos elevados, permitiendo realizar múltiples
    # operaciones con un solo llamado de ser requerido a
    # través de una llamada al intérprete de consola,
    # pasándole todos los comandos en cadena.
    try:
        if use_shell:
            subprocess.run(f"doas {command}", check=True, shell=True)
        else:
            subprocess.run(["doas"] + command, check=True, shell=False)
    except subprocess.CalledProcessError as error:
        # Si el comando no se puede ejecutar por algún motivo, se manejará
        # este error.
        bg_colour("red", "Error de ejecución del programa.")
        bg_colour("red", f"Código de salida: {error.returncode}")
    except TypeError:
        # Si el comando a ejecutar está mal formateado, interrumpir la
        # ejecución del programa.
        bg_colour("red", "Tipo de comando incorrecto.")
        bg_colour("red", "Cuando 'use_shell=True', 'command' debe ser una "
                         "cadena (string).")
        bg_colour("red", "Cuando 'use_shell=False', 'command' debe ser una lista "
                         "de cadenas (list of strings).")
        raise

def pipe_commands(proc1, proc2):
    # pipe_commands es un wrapper de subprocess.Popen
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
