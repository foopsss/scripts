#!/usr/bin/env python3

import subprocess

def clear_screen():
    subprocess.run(["clear"])

def draw_line(length, symbol="-"):
    for i in range(length - 1):
        print(symbol, end='')
    print(symbol)

def bg_colour(colour, text):
    # Reglas de uso de los colores:
    # El rojo se usa para mensajes de error.
    # El verde para mensajes de éxito o confirmación.
    # El azul para mostrar otros mensajes por pantalla.
    match colour:
        case "red": colour = 41
        case "green": colour = 42
        case "blue": colour = 44

    print(f"\033[1;37;{colour}m{text}\033[0m")

def get_choice(low_lim, upp_lim):
    # low_lim hace referencia a la cota inferior del rango
    # de opciones disponibles para elegir en un menú. De la
    # misma forma, upp_lim hace referencia a la cota superior
    # de dicho rango.
    while True:
        choice_str = input("Ingrese su elección: ")
        choice = int(choice_str)

        if choice < low_lim or choice > upp_lim:
            # Si el usuario introduce un valor por fuera del rango
            # aceptado, hay que imprimir un mensaje de error y luego
            # solicitarle una elección correcta.
            bg_colour("red", "¡Introduzca un número válido!")
            continue
        else:
            # De lo contrario, se puede seguir con el programa.
            return(choice)
