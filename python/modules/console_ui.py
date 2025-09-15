#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo contiene una serie de funciones relacionadas al aspecto estético
de los scripts y el control de entradas recibidas por parte del usuario.
"""

import subprocess

from typing import Literal

# Diccionarios a utilizar en las funciones encargadas de colorear contenidos.
_BACKGROUND_COLOURS = {
    # Reglas de uso de los colores:
    # * El rojo se usa para mensajes de error.
    # * El amarillo se usa para mostrar advertencias.
    # * El verde para mensajes de éxito o confirmación.
    # * El azul para mostrar otros mensajes por pantalla.
    # * Los demás colores no tienen un propósito establecido
    #   actualmente.
    "red": 41,
    "yellow": 43,
    "green": 42,
    "blue": 44,
    "magenta": 45,
    "cyan": 46,
}


_FOREGROUND_COLOURS = {
    "red": 31,
    "yellow": 33,
    "green": 32,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
}


# --- Funciones privadas ---
def _background_and_foreground_colour_exception():
    """
    Mensaje de error para las funciones bg_colour() y
    fg_colour(), en caso de que se esté manejando la
    excepción KeyError.
    """
    raise ValueError(
        "El parámetro 'colour' solo admite los valores 'red', 'green',"
        " 'blue', 'yellow', 'magenta' y 'cyan'."
    )


# --- Funciones públicas para recibir entradas del usuario ---
def get_validated_input(
    msg: str, return_type: Literal["str", "int"] = "str"
) -> str | int:
    """
    get_validated_input() es un wrapper de la función input() que
    sirve para controlar la entrada recibida por parte del usuario.
    La idea es evitar que se permita introducir respuestas vacías o
    que no concuerden con el tipo de dato especificado.

    La función admite dos tipos de datos: cadenas ("str") y números
    enteros ("int").
    """
    # Validación de parámetros de la función.
    if not isinstance(msg, str):
        raise TypeError("El parámetro 'msg' debe ser una cadena.")

    if return_type not in ["str", "int"]:
        raise TypeError(
            "El parámetro 'return_type' debe ser una cadena o un número"
            " entero."
        )

    # Validaciones realizadas por la función.
    while True:
        input_str = input(f"{msg}: ")

        # Si el usuario no introduce nada y presiona ENTER,
        # o si introduce caracteres que no sean números cuando
        # se necesita recibir un número, hay que imprimir un
        # mensaje de error y solicitar una elección correcta.
        if input_str == "":
            bg_colour("red", "¡Introduzca un valor!")
            continue
        elif return_type == "int" and not input_str.isdigit():
            bg_colour("red", "¡Solo se pueden introducir números!")
            continue
        else:
            break

    if return_type == "str":
        return input_str
    else:
        return int(input_str)


def get_choice(low_lim: int, upp_lim: int) -> None:
    """
    get_choice() es una función encargada de recibir la
    elección de un usuario en forma de un valor numérico
    dentro de un rango establecido mediante los parámetros
    low_lim (para el límite inferior) y upp_lim (para el
    límite superior).

    Esta función se apoya en los chequeos realizados
    previamente al llamar a la función get_validated_input()
    y luego verifica si el usuario realiza una elección que
    se encuentra por fuera del rango permitido.

    Asimismo, si los límites especificados al llamar a la
    la función son menores a uno, se producirá una excepción
    y se mostrará un mensaje de error por pantalla.
    """
    if not isinstance(low_lim, int) or not isinstance(upp_lim, int):
        raise TypeError(
            "Los parámetros 'low_lim' y 'upp_lim' deben tratarse de números"
            " enteros."
        )

    if low_lim <= 0 or upp_lim <= 0:
        raise ValueError(
            "Los parámetros 'low_lim' y 'upp_lim' no pueden ser menores a uno."
        )

    if upp_lim < low_lim:
        raise ValueError(
            "El parámetro 'upp_lim' no puede ser menor que 'low_lim'."
        )

    while True:
        choice = get_validated_input(
            msg="Ingrese su elección",
            return_type="int",
        )

        if choice < low_lim or choice > upp_lim:
            # Si el usuario introduce un valor por fuera del
            # rango aceptado, hay que imprimir un mensaje de
            # error y luego solicitarle una elección correcta.
            bg_colour("red", "¡Introduzca un número válido!")
            continue
        else:
            # De lo contrario, se puede seguir con el programa.
            return choice


def press_enter() -> None:
    """
    press_enter() es una función que permite pausar
    la ejecución de un programa y mostrar un mensaje
    por pantalla para indicarle al usuario como
    continuar.
    """
    print("")
    print("Presione ENTER para continuar.", end="")
    input()


# --- Funciones públicas de visualización y formato ---
def clear_screen() -> None:
    """
    clear_screen() es un wrapper de subprocess.run()
    utilizado para llamar al comando 'clear' y poder
    limpiar la pantalla.
    """
    subprocess.run(["clear"])


def draw_line(
    length: int, symbol: str = "-", print_line: bool = True
) -> None | str:
    """
    draw_line() permite dibujar una línea de símbolos
    de una longitud pasada por parámetro, permitiendo
    especificar además el símbolo a dibujar, aunque
    por defecto se imprimen guiones.

    En función de lo especificado en el parámetro
    'print_line', la función puede imprimir la línea
    por pantalla o devolvera para que la utilice otra
    función.

    Asimismo, si la longitud especificada no es mayor
    a cero, si el símbolo suministrado no es un string
    o si su longitud es distinta de uno, se producirá
    una excepción y se mostrará un mensaje de error
    por pantalla.
    """
    if not isinstance(length, int):
        raise TypeError(
            "El parámetro 'length' debe tratarse de un número entero."
        )

    if length <= 0:
        raise ValueError("El parámetro 'length' debe ser mayor a cero.")

    if not isinstance(symbol, str):
        raise TypeError("El parámetro 'symbol' debe tratarse de una cadena.")

    if len(symbol) != 1:
        raise ValueError(
            "El parámetro 'length' debe tener exactamente un elemento."
        )

    if not isinstance(print_line, bool):
        raise TypeError("El parámetro 'print_line' debe ser un valor lógico.")

    # Composición de la cadena a mostrar/devolver utilizando
    # multiplicación de cadenas.
    line = symbol * length

    if print_line:
        print(line)
        return None
    else:
        return line


def bg_colour(colour: str, text: str) -> None:
    """
    bg_colour() es una función utilizada para imprimir
    texto blanco y en negritas sobre un fondo coloreado.

    Permite especificar el color a utilizar con una cadena
    (string), la cual debe tratarse de una de los colores
    disponibles en el diccionario _BACKGROUND_COLOURS,
    disponible en la cabecera de esta librería, y el texto
    a imprimir por pantalla.

    En caso de que el usuario introduzca un color que no
    está definido en el diccionario, se producirá una
    excepción y se mostrará un mensaje de error por
    pantalla.
    """
    if not isinstance(colour, str) or not isinstance(text, str):
        raise TypeError(
            "Los parámetros 'colour' y 'text' deben tratarse de cadenas."
        )

    try:
        background_code = _BACKGROUND_COLOURS[colour]
        print(f"\033[1;37;{background_code}m{text}\033[0m")
    except KeyError:
        _background_and_foreground_colour_exception()


def fg_colour(colour: str, text: str, print_line: bool = True) -> None | str:
    """
    fg_colour() es una función utilizada para imprimir
    texto coloreado y en negritas.

    Permite especificar el color a utilizar con una cadena
    (string), la cual debe tratarse de una de los colores
    disponibles en el diccionario _FOREGROUND_COLOURS,
    disponible en la cabecera de esta librería, y el texto
    a imprimir por pantalla o devolver como resultado.

    En caso de que el usuario introduzca un color que no
    está definido en el diccionario, se producirá una
    excepción y se mostrará un mensaje de error por
    pantalla.
    """
    if not isinstance(colour, str) or not isinstance(text, str):
        raise TypeError(
            "Los parámetros 'colour' y 'text' deben tratarse de cadenas."
        )

    if not isinstance(print_line, bool):
        raise TypeError("El parámetro 'print_line' debe ser un valor lógico.")

    try:
        foreground_code = _FOREGROUND_COLOURS[colour]
        line = f"\033[1;{foreground_code}m{text}\033[0m"

        if print_line:
            print(line)
            return None
        else:
            return line
    except KeyError:
        _background_and_foreground_colour_exception()


def draw_coloured_line(
    length: int, symbol: str = "-", colour: str = "yellow"
) -> None:
    """
    draw_coloured_line() es una combinación de draw_line()
    y fg_colour() que permite dibujar una línea de símbolos
    de una longitud pasada por parámetro, permitiendo
    especificar además el símbolo a dibujar y el color a
    utilizar. Por defecto, se imprime una línea de guiones
    amarilla.

    Aquí aplican las restricciones de las funciones
    mencionadas anteriormente con respecto a la longitud de
    la línea, el símbolo pasado por parámetro y el color
    pasado por parámetro.

    Asimismo, también aplican los controles de tipo
    realizados con respecto a los parámetros de dichas
    funciones.
    """
    line_str = draw_line(length, symbol, print_line=False)
    fg_colour(colour, line_str, print_line=True)
