#!/usr/bin/env python3

# Paquetes usados en este modulo:
# app-admin/doas - provee "doas".

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

  -  Los errores de ejecución son captados a través del manejo de las
     excepciones "subprocess.CalledProcessError", "subprocess.TimeoutExpired",
     "FileNotFoundError" y "Exception" (para cualquier otro tipo de posible
     error imprevisto). En caso de ocurrir un error de ejecución se le
     informará al usuario y se mostrará un código y/o mensaje de error.

* Siempre que no se intente ejecutar comandos a través del intérprete de
  consola, run_command() permite deshabilitar el control de errores. Sin
  embargo, en el caso de run_command_as_root(), el control de errores
  siempre está habilitado.

### Particularidades de la función run_command_and_get_return_code() ###
* En esta función también se realiza una validación del comando pasado por
  parámetro, debiendo tratarse este de una lista de cadenas. Asimismo, también
  se controlan los mismos errores en tiempo de ejecución que se controlan en
  las funciones run_command() y run_command_as_root().

### Particularidades de la función pipe_commands() ###
* Al igual que con la función, run_command_and_get_return_code(), los
  argumentos "first_command" y "second_command" deben tratarse de listas
  de cadenas. En caso de que no tengan el formato correcto, sucederá lo
  mismo que sucede con las validaciones en run_command() y
  run_command_as_root(), a través de la función _check_command_argument_type().
"""

import functools
import subprocess

from typing import Any, Callable

from modules.console_ui import style_text


# --- Funciones privadas ---
def _check_command_argument_type(command: list | str, use_shell: bool) -> None:
    """
    _check_command_argument_type() se encarga de validar
    los tipos de los comandos que se quieren ejecutar en
    las funciones que siguen, en función de si estos se
    van a ejecutar a través de un intérprete de consola
    o directamente a través de un método de la librería
    subprocess.
    """
    if not isinstance(use_shell, bool):
        raise TypeError("El parámetro 'use_shell' debe ser un valor lógico.")

    if use_shell:
        if not isinstance(command, str):
            raise TypeError(
                "El parámetro 'command' debe suministrarse como una cadena."
            )
    else:
        if not isinstance(command, list):
            raise TypeError(
                "El parámetro 'command' debe suministrarse como una lista."
            )

        if not all(isinstance(item, str) for item in command):
            raise TypeError(
                "Todos los elementos de la lista 'command' deben tratarse de"
                " cadenas."
            )


def _run_commands_exception_handler(
    func: Callable[..., Any],
) -> Callable[..., Any]:
    """
    _run_commands_exception_handler() es un decorador
    encargado de generalizar el control de excepciones
    en el módulo, permitiendo definir múltiples wrappers
    de subprocess.run() sin tener que repetir la lógica
    para controlar errores.
    """

    # Se llama a la función "functools.wraps" con el
    # propósito de preservar el nombre y el docstring
    # de las funciones a las cuales se les anexa este
    # decorador.
    @functools.wraps(func)
    def inner_exception_handling(*args: Any, **kwargs: Any) -> Any | None:
        try:
            return func(*args, **kwargs)
        except subprocess.CalledProcessError as exec_error:
            # Si el comando no logra ejecutarse correctamente por algún
            # motivo, se manejará este error.
            style_text(
                "bg",
                "red",
                f"Error de ejecución del comando {exec_error.cmd}.",
            )
            style_text(
                "bg", "red", f"Código de salida: {exec_error.returncode}."
            )
            return None
        except subprocess.TimeoutExpired as timeout_error:
            # Si el comando no logra ejecutarse aún después de esperar
            # una determinada cantidad de tiempo, se manejará este error.
            style_text(
                "bg",
                "red",
                f"Se esperaron {timeout_error.timeout} segundos para ejecutar"
                f" el comando {timeout_error.cmd}, pero no se recibió"
                " respuesta.",
            )
            return None
        except FileNotFoundError as filenotfound_error:
            # Si el comando no existe, ya sea porque corresponde a un
            # programa que no está instalado, invocado incorrectamente,
            # o cualquier otra razón, se manejará este error.
            style_text(
                "bg",
                "red",
                f"No existe el comando '{filenotfound_error.filename}'.",
            )
            return None
        except OSError as os_error:
            # Manejo de errores relacionados con el SO como "archivo
            # no encontrado", "permiso denegado", etc.
            style_text(
                "bg",
                "red",
                "Se ha producido un error del SO durante la ejecución de un"
                " programa."
                f"\nEl error encontrado es: {os_error}.",
            )
            return None
        except Exception as unknown_error:
            # Cualquier otro error que no se haya podido manejar
            # anteriormente se tratará acá.
            style_text(
                "bg",
                "red",
                "Se produjo un error inesperado al ejecutar el comando."
                f"\nError encontrado: {unknown_error}.",
            )
            return None

    return inner_exception_handling


# --- Funciones públicas ---
@_run_commands_exception_handler
def run_command(
    command: list | str,
    check_return: bool = True,
    use_shell: bool = False,
    return_output: bool = False,
) -> None | subprocess.CompletedProcess:
    """
    run_command() es un wrapper de subprocess.run para
    ejecutar programas externos. Permite deshabilitar
    el control de errores de ser necesario, pero por
    defecto se controla el código de salida que
    devuelven los programas llamados.

    run_command() también permite utilizar el intérprete
    de consola del sistema para realizar operaciones,
    pero esto solo se puede hacer con el control de
    errores activado.
    """
    if (
        not isinstance(check_return, bool)
        or not isinstance(use_shell, bool)
        or not isinstance(return_output, bool)
    ):
        raise TypeError(
            "Los parámetros 'check_return', 'use_shell' y 'return_output'"
            " deben ser valores lógicos."
        )

    if not check_return and use_shell:
        raise ValueError(
            "No se puede usar la función con check_return=False y"
            " con use_shell=True. No es seguro."
        )

    _check_command_argument_type(command, use_shell)
    result = subprocess.run(
        command,
        check=check_return,
        shell=use_shell,
        capture_output=return_output,
        text=return_output,
    )

    if return_output:
        return result


@_run_commands_exception_handler
def run_command_as_root(
    command: list | str,
    use_shell: bool = False,
    return_output: bool = False,
) -> None | subprocess.CompletedProcess:
    """
    run_command_as_root() es un wrapper de subprocess.run
    que sirve para ejecutar comandos externos con permisos
    elevados, permitiendo realizar múltiples operaciones
    de ser requerido a través de una llamada al intérprete
    de consola.

    A diferencia de run_command(), no permite desactivar
    el control de errores.
    """
    if not isinstance(use_shell, bool) or not isinstance(return_output, bool):
        raise TypeError(
            "Los parámetros 'use_shell' y 'return_output' deben ser valores"
            " lógicos."
        )

    _check_command_argument_type(command, use_shell)

    if use_shell:
        command_to_run = f"doas {command}"
    else:
        command_to_run = ["doas"] + command

    result = subprocess.run(
        command_to_run,
        check=True,
        shell=use_shell,
        capture_output=return_output,
        text=return_output,
    )

    if return_output:
        return result


@_run_commands_exception_handler
def run_command_and_get_return_code(command: list) -> int | None:
    """
    run_command_and_get_return_code() es un wrapper de subprocess.run()
    que sirve para ejecutar comandos externos y almacenar el código de
    salida de estos.

    A diferencia de las otras funciones, el control de errores está
    desactivado para que no se produzca una excepción del tipo
    subprocess.CalledProcessError, devolviendo directamente el código
    de salida de la función. Tampoco se muestra por pantalla la salida
    estándar o el error estándar del comando externo ejecutado.
    """
    _check_command_argument_type(command, use_shell=False)
    result = subprocess.run(command, check=False, capture_output=True)
    return result.returncode


@_run_commands_exception_handler
def pipe_commands(first_command: list, second_command: list) -> str | None:
    """
    pipe_commands() es un wrapper de subprocess.Popen()
    que sirve para simular el uso de pipelines, como las
    que se utilizan en los intérpretes de consola. Solo
    admite la llamada a dos programas.

    Recibe como entrada dos listas con los programas
    a ejecutar.
    """
    _check_command_argument_type(first_command, use_shell=False)
    _check_command_argument_type(second_command, use_shell=False)

    with subprocess.Popen(
        first_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as first_process:
        with subprocess.Popen(
            second_command,
            stdin=first_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as second_process:
            # Cierro la salida del primer comando para evitar
            # deadlocks (puntos muertos o bloqueos).
            first_process.stdout.close()

            # Guardo la salida estándar del segundo proceso y
            # descarto el error estándar, ya que no me interesa.
            stdout_second, _ = second_process.communicate()

        # Descarto tanto la salida estándar como el error
        # estándar del primer proceso, ya que no me interesa
        # ninguna de las dos cosas.
        _, _ = first_process.communicate()

    # Si alguno de los comandos ejecutados falla, causar
    # una excepción. Esta excepción luego será atrapada
    # como una excepción genérica en el decorador
    # "_run_commands_exception_handler".
    if first_process.returncode != 0:
        raise RuntimeError(
            f"El primer comando, '{' '.join(first_command)}', falló con"
            f" el código de salida {first_process.returncode}."
        )

    if second_process.returncode != 0:
        raise RuntimeError(
            f"El segundo comando, '{' '.join(second_command)}', falló"
            f" con el código de salida {second_process.returncode}."
        )

    # Antes de devolver la salida del segundo comando,
    # conviene limpiarla para remover cosas como espacios
    # en blanco innecesarios.
    return stdout_second.strip()
