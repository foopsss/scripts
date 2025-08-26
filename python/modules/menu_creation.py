#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo contiene una serie de funciones relacionadas al aspecto estético
y el funcionamiento de los scripts. Específicamente, contiene lo relacionado
a la impresión por pantalla de un menú de opciones y el tratamiento de las
opciones definidas en un menú, cosas que estarán todas definidas en una
estructura de datos que deberá ser procesada por las funciones de este módulo.

### Estructura de datos a utilizar en la librería ###
La estructura de datos a procesar será un diccionario, el cual debe contener
la cabecera del menú, los encabezados para agrupar opciones en apartados (si
los hubiere) y las opciones en sí mismas. La estructura que debe tener el
diccionario es la siguiente.

1. "title": parámetro que contiene el texto a mostrar en la cabecera.
2. "options": una lista que debe contener el texto a mostrar en los encabezados
   y las opciones a ejecutar. Cada elemento de esta lista se tratará de un
   diccionario, el cual podrá tener los siguientes parámetros:
   2.1. "type": describe el tipo de elemento que contiene el diccionario y
        puede contener los valores 'header', 'menu', 'cmd', 'multiple_cmd',
        'piped_cmd', 'function', 'exit_script' y 'exit_menu'.
   2.2. "name": contiene el texto a mostrar en el encabezado u opción del
        menú.
   2.3. "action": contiene la acción a realizar. Su tipo de dato depende de la
        acción a realizar definida en el parámetro "type":
        2.3.1. Si "type" tiene el valor 'header', debería estar vacío o tener
               el valor 'None'.
        2.3.2. Si "type" tiene el valor 'menu', debe contener una referencia al
               diccionario a pasarle como parámetro a la función run_menu(),
               sin que esta sea un string.
        2.3.3. Si "type" tiene los valores 'cmd', 'multiple_cmd' o 'piped_cmd',
               debe tratarse de una lista.
        2.3.4. Si "type" tiene el valor 'function', debe contener un llamado
               a la función a ejecutar, sin que este sea un string.
        2.3.5. Si "type" tiene los valores 'exit_script' o 'exit_menu', debería
               estar vacío o tener el valor 'None'.
   2.4. "aesthetic_action": describe que acción estética debe ejecutarse antes
        de ejecutar la acción definida en "action". Puede contener los valores
        'print_line' o 'clear_screen'.
   2.5. "prompt": contiene el mensaje a mostrarle por pantalla al usuario en
        caso de que se le deba pedir que provea una entrada.
   2.6. "prompt_input": contiene el tipo de dato que debe tener la entrada
        provista por el usuario.
   2.7. "piped_cmd_input_position": si el valor del parámetro "type" es
        'piped_cmd', indica a qué comando se le anexa la entrada provista por
        el usuario, si al primero o al segundo. Puede contener los valores
        'first' o 'second'.
   2.8. "requires_root": describe si el comando debe ejecutarse con permisos
        de superusuario o no. Puede contener los valores 'True' o 'False'.

   A excepción de "type" y "name", que deben ser obligatorios. Todos los demás
   parámetros pueden ser opcionales.
"""

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
    # Impresión del encabezado de la sección.
    # Este debe ser el primer elemento de la lista que
    # define su estructura, de nombre "title".
    draw_coloured_line(len(menu_data["title"]), "=")
    print(menu_data["title"])
    draw_coloured_line(len(menu_data["title"]), "=")

    # Impresión del listado de opciones.
    option_number = 1
    for item in menu_data["options"]:
        if item["type"] == "header":
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
        if item["type"] != "header":
            # Si un ítem de la lista "opciones" contenida
            # dentro del diccionario de entrada NO es del
            # tipo encabezado, se lo añade a la lista de
            # salida.
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
    if "prompt" in menu_option:
        if "prompt_input" == "str":
            user_input = get_validated_input(menu_option["prompt"])
        elif "prompt_input" == "int":
            user_input = get_validated_input(
                msg=menu_option["prompt"],
                return_type="int",
            )

    # En aquellos casos donde trabajo con comandos, hago
    # copias de sus valores, de manera que no las pueda
    # alterar irreversiblemente en caso de procesar una
    # entrada provista por el usuario, anexando dicha
    # entrada a la definición en el diccionario de los
    # comandos.
    match menu_option["type"]:
        case "cmd":
            command = menu_option["action"].copy()
            if "prompt" in menu_option:
                command.append(user_input)

            if menu_option["requires_root"] is True:
                run_command_as_root(command)
            elif menu_option["requires_root"] is False:
                run_command(command)
        case "multiple_cmd":
            for cmd in menu_option["action"]:
                command = cmd.copy()
                if "prompt" in menu_option:
                    command.append(user_input)

                if menu_option["requires_root"] is True:
                    run_command_as_root(command)
                elif menu_option["requires_root"] is False:
                    run_command(command)
        case "piped_cmd":
            piped_commands_list = []

            for cmd in menu_option["action"]:
                cmd_copy = cmd.copy()
                piped_commands_list.append(cmd_copy)

            if "prompt" in menu_option:
                if menu_option["piped_cmd_input_position"] == "first":
                    piped_commands_list[0].append(user_input)
                elif menu_option["piped_cmd_input_position"] == "second":
                    piped_commands_list[1].append(user_input)

            # Le paso todas las operaciones contenidas en la
            # lista "piped_commands_list" como argumentos a
            # piped_commands y ejecuto.
            result = pipe_commands(*piped_commands_list)
            print(f"{result}")
        case "function":
            menu_option["action"]()


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

        # Obtengo el elemento de la lista "options" del diccionario
        # de entrada que corresponde a la operación que se quiere
        # realizar, el cual es un diccionario también.
        #
        # Los números de índice de la listas empiezan a contarse
        # desde el 0, mientras que yo en los menús acostumbro a
        # empezar desde el 1, por lo que se debe subsanar esa
        # diferencia.
        #
        # También controlo que la opción elegida por el usuario
        # no tenga combinaciones incorrectas de parámetros en
        # su definición.
        option = options[option_number - 1]

        # En primera instancia, controlo si el usuario desea
        # salir o dirigirse a otro menú.
        if option["type"] == "exit_script":
            sys.exit(0)
        elif option["type"] == "exit_menu":
            break
        elif option["type"] == "menu":
            run_menu(option["action"])

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

        # Ejecuto la acción elegida por el usuario.
        _handle_action(option)

        # Esta llamada a press_enter() pausa la ejecución en
        # cualquier caso, a excepción de cuando se elige salir
        # del menú.
        press_enter()
