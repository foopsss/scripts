#!/usr/bin/env python3

import subprocess

# --- Funciones para recibir entradas del usuario ---
def get_choice(low_lim, upp_lim):
    # low_lim hace referencia a la cota inferior del rango
    # de opciones disponibles para elegir en un menú. De la
    # misma forma, upp_lim hace referencia a la cota superior
    # de dicho rango.
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
                return(choice)

def press_enter():
    print("")
    print("Presione ENTER para continuar.", end='')
    input()

# --- Funciones de visualización y formato ---
def clear_screen():
    subprocess.run(["clear"])

def draw_line(length, symbol="-"):
    # length permite indicar la longitud deseada para
    # las líneas, mientras que symbol permite indicar
    # el símbolo a utilizar, aunque por defecto se
    # imprimen líneas con el carácter "-".
    for i in range(length - 1):
        print(symbol, end='')
    print(symbol)

def bg_colour(colour, text):
    # Reglas de uso de los colores:
    # El rojo se usa para mensajes de error.
    # El verde para mensajes de éxito o confirmación.
    # El azul para mostrar otros mensajes por pantalla.
    #
    # Si no especifica ningún color válido no
    # se colorea el fondo del texto y solo se
    # lo imprime en negritas.
    match colour:
        case "red": background = 41
        case "green": background = 42
        case "blue": background = 44
        case _: background = 49

    print(f"\033[1;37;{background}m{text}\033[0m")
