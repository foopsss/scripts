#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo contiene una serie de funciones relacionadas al aspecto estético
y el funcionamiento de los scripts. Específicamente, contiene lo relacionado
a la impresión por pantalla de un menú de opciones y el tratamiento de las
opciones definidas en el menú, cosas que estarán definidas en una estructura
de datos que deberá ser procesada por las funciones de este módulo.

### Estructura de datos a utilizar en la librería ###
La estructura de datos a procesar será un diccionario, el cual debe contener
el encabezado del menú, los títulos para agrupar opciones en apartados (si los
hubiere) y las opciones en sí mismas. La estructura que debe tener el
diccionario es la siguiente:

1. "title": debe contener el texto a mostrar en el encabezado.
2. "pre_menu_hook": debe contener una referencia a una función a ejecutar, que
   servirá para llevar a cabo tareas necesarias previo a la impresión por
   pantalla del encabezado de menú y las opciones.
3. "options": una lista que debe contener los títulos de los apartados y las
   opciones a ejecutar. Cada elemento de esta lista es un diccionario que
   puede tener los siguientes parámetros:
   3.1. "name": el texto a mostrar en el encabezado u opción del menú.
   3.2. "action": la acción a realizar. Su tipo de dato depende de la acción a
        realizar:
        3.2.1. Si se debe entrar a un menu, "action" debe contener una
               referencia al diccionario a pasarle como parámetro a la función
               run_menu(), sin que esta sea un string.
        3.2.2. Si se debe ejecutar una función, "action" debe contener una
               referencia a la función a ejecutar, sin que esta sea un string.
        3.2.3. Si se deben ejecutar uno o varios comandos, "action" debe
               contener una lista, la cual estará compuesta a su vez por una o
               más listas de strings. En caso de que se deban ejecutar dos
               comandos con pipes, el primer elemento de la lista deberá ser el
               string "pipe", luego del cual vendrán las dos listas de strings
               correspondientes a los comandos a ejecutar.
        3.2.4. Si se desea salir de un menú de opciones para volver a otro menú
               anterior, "action" deberá contener el string 'exit_menu'.
        3.2.5. Si se desea salir del script, "action" deberá contener el string
               'exit_script'.
        3.2.6. Si se desea mostrar un título de apartado, "action" debe estar
               ausente o contener el valor None.
   3.3. "aesthetic_action": la acción estética a ejecutar antes de la acción
        principal. Puede contener los valores 'print_line' o 'clear_screen'.
   3.4. "prompt": el mensaje para solicitar una entrada del usuario.
   3.5. "piped_cmd_input_position": indica a qué comando se le anexa la entrada
        provista por el usuario, si al primero o al segundo, en caso de que se
        deban ejecutar comandos con pipes. Puede contener los valores 'first' o
        'second'.
   3.6. "requires_root": describe si el comando debe ejecutarse con permisos
        de superusuario o no. Puede contener los valores True o False.

   A excepción de "title" y "name", que deben ser obligatorios, todos los demás
   parámetros pueden ser opcionales en el diccionario de entrada. Para cada
   elemento de la lista "options", el único parámetro obligatorio es "name".
"""

# TODO: investigar una manera de usar marcadores "root" para etiquetar los
#       comandos que deben ejecutarse con permisos de superusuario, en vez de
#       usar la llave "requires_root".
#       * Se pueden añadir los tags al principio de cada elemento de la lista
#         "actions", de manera que no choquen con el tag "pipe" que debe ir
#         como primer elemento de la lista "actions" si hay que usar la función
#         pipe_commands.
# TODO: investigar una manera de usar marcadores "prompt" para etiquetar los
#       comandos a los que se les debe añadir la entrada provista por el
#       usuario.

# Chequear luego:
# https://stackoverflow.com/questions/847936/how-can-i-find-the-number-of-arguments-of-a-python-function#41188411

import copy
import sys

from modules.console_ui import (
    clear_screen,
    draw_coloured_line,
    get_choice,
    get_validated_input,
    press_enter,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
    run_command_as_root,
)


# --- Funciones privadas ---
def _draw_menu(menu_data: dict) -> None:
    """
    _draw_menu() es una función utilizada para imprimir
    dinámicamente un menú de opciones a partir de un
    diccionario de entrada, el cual debe contener las
    opciones a ejecutar, así como el título del menú
    y cualquier posible encabezado de sección a mostrar
    para dividir las opciones disponibles en apartados.
    """
    # Ejecución de cualquier posible cosa requerida
    # previo a la impresión del encabezado y el menú
    # de opciones.
    title_length = len(menu_data["title"])
    pre_menu_hook = menu_data.get("pre_menu_hook", None)
    if pre_menu_hook is not None and callable(pre_menu_hook):
        draw_coloured_line(title_length, "=")
        pre_menu_hook()

    # Impresión del encabezado de la sección.
    draw_coloured_line(title_length, "=")
    print(menu_data["title"])
    draw_coloured_line(title_length, "=")

    # Impresión del listado de opciones.
    option_number = 1
    for item in menu_data["options"]:
        if "action" not in item:
            print(f"\n{item["name"]}")
            draw_coloured_line(len(item["name"]))
        else:
            print(f"{option_number}. {item["name"]}")
            option_number += 1

    # Esta línea en blanco se deja para que el
    # listado de opciones no colisione con el pedido
    # de elección al usuario, provisto por get_choice().
    print("")


def _get_command_options(menu_data: dict) -> list:
    """
    _get_command_options() es una función utilizada
    para procesar un diccionario de entrada que contiene
    definiciones de comandos a ejecutar, así como la
    definición del título principal de un menú y los
    encabezados de sección que agrupan las distintas
    opciones disponibles (si hubiera).

    Se encarga de otorgar como salida una lista aparte
    que contenga únicamente los posibles comandos a
    ejecutar, de manera que después se pueda recorrer
    esta nueva lista para encontrar y ejecutar la
    opción elegida por el usuario.
    """
    # Inicialización de una lista vacía que contenga
    # los posibles comandos a ejecutar.
    command_options = []

    # Recorrido de la lista "options" definida dentro
    # del diccionario de entrada.
    for item in menu_data["options"]:
        if "action" in item:
            # Si un ítem de la lista "opciones" contenida
            # dentro del diccionario de entrada tiene una
            # llave "action" definida, entonces lo añado
            # a la lista de salida.
            command_options.append(item)

    return command_options


def _handle_action(menu_option: dict) -> None:
    """
    _handle_action() es una función utilizada para
    ejecutar un comando provisto en un diccionario
    de entrada, englobando toda la lógica necesaria
    en un solo lugar, para no mezclarla con el resto
    de la lógica de ejecución presente en run_menu().

    Se encarga de procesar los parámetros provistos
    en el diccionario y de recibir una entrada de
    parte del usuario en caso de ser necesario, previo
    a la ejecución del comando provisto.
    """
    # Si el comando a ejecutar requiere que el usuario
    # ingrese algo por pantalla, se lo pido acá.
    # Se utiliza el mensaje definido en el campo "prompt"
    # del diccionario almacenado en "menu_option".
    user_input = None
    if "prompt" in menu_option:
        user_input = get_validated_input(menu_option["prompt"])
        print("")

    # Ejecución de la opción elegida.
    if callable(menu_option["action"]):
        # Se debe ejecutar una función.
        menu_option["action"]()
    elif isinstance(menu_option["action"], list):
        # Trabajo con una copia del diccionario pasado por
        # parámetro para no alterar el original.
        commands_to_run = copy.deepcopy(menu_option["action"])
        run_as_root = menu_option.get("requires_root", False)

        if commands_to_run[0] == "pipe":
            # Se deben ejecutar comandos con pipes.
            piped_commands = commands_to_run[1:]
            if user_input:
                input_position = menu_option["piped_cmd_input_position"]
                if input_position == "first":
                    piped_commands[0].append(user_input)
                elif input_position == "second":
                    piped_commands[1].append(user_input)

            result = pipe_commands(*piped_commands)
            print(f"{result}")
        else:
            # Se deben ejecutar uno o varios comandos de
            # forma sucesiva.
            for command in commands_to_run:
                if user_input:
                    command.append(user_input)

                if run_as_root:
                    run_command_as_root(command)
                else:
                    run_command(command)


# --- Funciones públicas ---
def run_menu(menu_data: dict) -> None:
    """
    run_menu() es una función utilizada para mostrar
    un menú de opciones al usuario, recibir su elección
    y ejecutar la opción elegida por este.

    Todo esto se realiza a partir de una definición
    de menú contenida en un diccionario, el cual es
    pasado como parámetro a la función y debe tener
    un formato específico, descripto en la documentación
    de la librería "menu_creation".
    """
    while True:
        clear_screen()
        _draw_menu(menu_data)

        # Obtengo la elección del usuario.
        options = _get_command_options(menu_data)
        option_number = get_choice(1, len(options))

        # Obtengo el elemento de la lista "options" del
        # diccionario de entrada que corresponde a la
        # operación que se quiere realizar, el cual es
        # un diccionario también.
        #
        # Los números de índice de la listas empiezan a
        # contarse desde el 0, mientras que yo en los
        # menús acostumbro a empezar desde el 1, por lo
        # que se debe subsanar esa diferencia.
        #
        # También controlo que la opción elegida por el
        # usuario no tenga combinaciones incorrectas de
        # parámetros en su definición.
        option = options[option_number - 1]
        # _check_option_parameters(option)

        # Luego de obtener el elemento, obtengo el valor
        # de la clave "action".
        action = option["action"]

        # En primera instancia, controlo si el usuario
        # desea salir o dirigirse a otro menú.
        if isinstance(action, dict):
            run_menu(action)
            continue
        elif isinstance(action, str) and action == "exit_menu":
            break
        elif isinstance(action, str) and action == "exit_script":
            sys.exit(0)

        # Por motivos estéticos, si utilizo alguna de las
        # opciones que se ejecutan justo debajo del menú,
        # imprimo un separador.
        #
        # Si utilizo alguna opción que requiera limpiar
        # la pantalla, hago eso.
        if "aesthetic_action" in option:
            if option["aesthetic_action"] == "clear_screen":
                clear_screen()
            elif option["aesthetic_action"] == "print_line":
                draw_coloured_line(len(menu_data["title"]))

        # Si la elección del usuario no es salir del script,
        # ir o salir de un menú, ejecuto la acción elegida.
        _handle_action(option)

        # Luego de ejecutar la acción elegida, pauso el script.
        if action != "exit_menu":
            press_enter()
