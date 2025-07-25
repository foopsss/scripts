#!/usr/bin/env python3

import subprocess

# Diccionarios a utilizar en las funciones encargadas de colorear contenidos.
BACKGROUND_COLOURS = {
    # Reglas de uso de los colores:
    # * El rojo se usa para mensajes de error.
    # * El verde para mensajes de éxito o confirmación.
    # * El azul para mostrar otros mensajes por pantalla.
    # * Los demás colores no tienen un propósito establecido
    #   actualmente.
    "red": 41,
    "green": 42,
    "blue": 44,
    "yellow": 43,
    "magenta": 45,
    "cyan": 46,
}


FOREGROUND_COLOURS = {
    "red": 31,
    "green": 32,
    "blue": 34,
    "yellow": 33,
    "magenta": 35,
    "cyan": 36,
}


# --- Funciones privadas ---
def _background_and_foreground_colour_exception():
    raise ValueError(
        "El parámetro colour solo admite los valores 'red', 'green', "
        "'blue', 'yellow', 'magenta' y 'cyan'."
    )


# --- Funciones públicas ---


## --- Funciones para recibir entradas del usuario ---
def get_choice(low_lim: int, upp_lim: int) -> None:
    """
    get_choice() es una función encargada de recibir la
    elección de un usuario en forma de un valor numérico
    dentro de un rango establecido mediante los parámetros
    low_lim (para el límite inferior) y upp_lim (para el
    límite superior).

    Si el valor recibido se encuentra por fuera del rango
    establecido, si no se realiza una elección (se presiona
    la tecla ENTER sin introducir contenido) o si se introduce
    una letra, la función mostrará un mensaje de error y le
    pedirá al usuario nuevamente que introduzca su elección.
    """
    while True:
        choice_str = input("Ingrese su elección: ")

        # Si el usuario no introduce nada y presiona ENTER,
        # o si introduce caracteres que no sean números, hay
        # que imprimir un mensaje de error y solicitar una
        # elección correcta.
        if choice_str == "":
            bg_colour("red", "¡Introduzca una elección!")
            continue
        elif not choice_str.isdigit():
            bg_colour("red", "¡Solo se pueden introducir números!")
            continue
        else:
            choice = int(choice_str)
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


## --- Funciones de visualización y formato ---
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
    if length <= 0:
        raise ValueError("La longitud de la línea debe ser mayor a cero.")
    if not isinstance(symbol, str) or len(symbol) != 1:
        raise ValueError(
            "El símbolo debe tratarse de un string compuesto por un solo "
            "carácter."
        )

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
    disponibles en el diccionario BACKGROUND_COLOURS,
    disponible en la cabecera de esta librería, y el texto
    a imprimir por pantalla.

    En caso de que el usuario introduzca un color que no
    está definido en el diccionario, se producirá una
    excepción y se mostrará un mensaje de error por
    pantalla.
    """
    try:
        background_code = BACKGROUND_COLOURS[colour]
        print(f"\033[1;37;{background_code}m{text}\033[0m")
    except KeyError:
        _background_and_foreground_colour_exception()


def fg_colour(colour: str, text: str, print_line: bool = True) -> None | str:
    """
    fg_colour() es una función utilizada para imprimir
    texto coloreado y en negritas.

    Permite especificar el color a utilizar con una cadena
    (string), la cual debe tratarse de una de los colores
    disponibles en el diccionario FOREGROUND_COLOURS,
    disponible en la cabecera de esta librería, y el texto
    a imprimir por pantalla o devolver como resultado.

    En caso de que el usuario introduzca un color que no
    está definido en el diccionario, se producirá una
    excepción y se mostrará un mensaje de error por
    pantalla.
    """
    try:
        foreground_code = FOREGROUND_COLOURS[colour]
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
    """
    line_str = draw_line(length, symbol, print_line=False)
    fg_colour(colour, line_str, print_line=True)
