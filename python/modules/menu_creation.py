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

1. "dict_name": debe contener el nombre que se le da a la variable que contiene
   la estructura de datos. Posteriormente se utiliza para poder otorgar
   mensajes de error informativos.
2. "title": debe contener el texto a mostrar en el encabezado.
3. "pre_menu_hook": debe contener una referencia a una función a ejecutar, que
   servirá para llevar a cabo tareas necesarias previo a la impresión por
   pantalla del encabezado de menú y las opciones.
4. "options": una lista que debe contener los títulos de los apartados y las
   opciones a ejecutar. Cada elemento de esta lista es un diccionario que
   puede tener los siguientes parámetros:
   4.1. "name": el texto a mostrar en el encabezado u opción del menú.
   4.2. "action": la acción a realizar. Su tipo de dato depende de la acción a
        realizar:
        4.2.1. Si se debe entrar a un menu, "action" debe contener una
               referencia al diccionario a pasarle como parámetro a la función
               run_menu(), sin que esta sea un string.
        4.2.2. Si se debe ejecutar una función, "action" debe contener una
               referencia a la función a ejecutar, sin que esta sea un string.
        4.2.3. Si se deben ejecutar uno o varios comandos, "action" debe
               contener una lista, la cual estará compuesta a su vez por una o
               más listas de strings. Para correr comandos con pipes o permisos
               de superusuario, véase la siguiente sección.
        4.2.4. Si se desea salir de un menú de opciones para volver a otro menú
               anterior, "action" deberá contener el string 'exit_menu'.
        4.2.5. Si se desea salir del script, "action" deberá contener el string
               'exit_script'.
        4.2.6. Si se desea mostrar un título de apartado, "action" debe estar
               ausente o contener el valor None.
   4.3. "aesthetic_action": la acción estética a ejecutar antes de la acción
        principal. Puede contener los valores 'print_line' o 'clear_screen'.
   4.4. "prompt": el mensaje para solicitar una entrada del usuario.

   A excepción de "dict_name", "title" y "name", que deben ser obligatorios,
   todos los demás parámetros pueden ser opcionales en el diccionario de
   entrada. Para cada elemento de la lista "options", el único parámetro
   obligatorio es "name".

### Modos especiales de ejecución ###
De acuerdo a lo estipulado en el inciso 3.2.3, a la hora de ejecutar uno o más
comandos, la clave "action" debe contener una lista que a su vez contenga otras
listas de strings en las cuales deben estar definidas los comandos a ejecutar.

Tanto la lista contenida por la clave "action" como las listas con definiciones
de comandos pueden incluir "etiquetas" (strings) que indiquen si estos comandos
deben ejecutarse de cierta forma:

* En caso de que un comando deba ejecutarse con permisos de superusuario, se le
  debe incluir el string "#ROOT" a la lista que lo define, antes de los strings
  pertenecientes al comando.
* En caso de que a un comando se le deba anexar una entrada introducida por el
  usuario, en caso de haberla, se le debe incluir el string "#UINPUT" a la
  lista que lo define, antes de los strings pertenecientes al comando.
* En caso de que dos comandos deban ejecutarse con pipes, el primer elemento de
  la lista contenida por la clave "action" debe ser el string "#PIPE", seguido
  de las listas con las definiciones de comandos.
  ** Asimismo, en caso de que alguno de los comandos deba ejecutarse con
     permisos de superusuario o se le deba anexar una entrada provista por el
     usuario, se deben incluir los strings "#ROOT" y "#UINPUT", de acuerdo a lo
     descripto para los casos anteriores.
"""

# TODO: añadir controles de tipo, valores y estructura a la hora de ejecutar
#       los contenidos del diccionario.
#       * Considerar además si se debe tratar el tema de las etiquetas
#         repetidas en los chequeos de estructura. SÍ se debe mencionar en la
#         documentación que la librería filtra las etiquetas repetidas al
#         procesar los comandos a ejecutar.
# TODO: considerar el rearmar la lógica de ejecución de funciones para que se
#       pueda pasar una lista de listas de funciones y sus parámetros en la
#       llave "action".
# TODO: considerar el rediseñar la lógica de ejecución de la llave
#       "pre_menu_hook" para que no solo se pueda pasar una sola función, sino
#       una lista de funciones.

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

from typing import Literal


# --- Funciones privadas para controlar errores ---
def _check_parameter(
    param_name: str, param_type: Literal["str", "list"], param: str | list
) -> None:
    """
    _check_parameter() es una función que sirve para proveer
    controles de existencia, tipo y longitud para variables
    que sean cadenas o listas.

    La idea es que esta función se utilice luego en otras
    funciones que necesitan controlar varias variables de
    estos tipos, de manera que no se repita la escritura de
    la lógica de control.
    """
    # Controles de parámetros de la función.
    if not isinstance(param_name, str):
        raise TypeError(
            "El parámetro 'param_name' debe ser una cadena (string)."
        )

    if param_type not in ["str", "list"]:
        raise TypeError(
            "El parámetro 'param_type' debe contener las cadenas 'str' o"
            " 'list'."
        )

    if not (isinstance(param, str) or isinstance(param, list)):
        raise TypeError(
            "El parámetro 'param' debe ser una cadena (string) o una lista."
        )

    # Controles realizados por la función.
    if param is None:
        raise KeyError(f"Se debe proveer el parámetro '{param_name}'.")

    if param_type == "str" and not isinstance(param, str):
        raise TypeError(
            f"El parámetro '{param_name}' debe ser una cadena (string)."
        )
    elif param_type == "list" and not isinstance(param, list):
        raise TypeError(
            f"El parámetro '{param_name}' debe ser una lista (list)."
        )

    if (param_type == "str" or param_type == "list") and len(param) == 0:
        raise ValueError(
            f"El parámetro '{param_name}' debe tener una longitud mayor a"
            " cero."
        )


def _check_basic_dictionary_structure(menu_data: dict) -> None:
    """
    _check_basic_dictionary_structure() es una función
    que provee controles de estructura para detectar
    errores básicos en la definición de los primeros
    elementos del diccionario de entrada. Sin embargo,
    no realiza un control de las opciones definidas
    en el diccionario, aspecto que es delegado a las
    siguientes funciones de la sección.
    """
    if not isinstance(menu_data, dict):
        raise ValueError(
            "La estructura de datos a procesar debe ser un diccionario."
        )

    dict_name = menu_data.get("dict_name", None)
    title = menu_data.get("title", None)
    options_list = menu_data.get("options", None)

    _check_parameter("dict_name", "str", dict_name)
    _check_parameter("title", "str", title)
    _check_parameter("options_list", "list", options_list)


def _check_options_name(menu_data: dict) -> None:
    """
    _check_options_name() es una función que controla
    que cada elemento definido en la lista de opciones
    'options' contenga el parámetro 'name'.
    """
    if not isinstance(menu_data, dict):
        raise ValueError(
            "La estructura de datos a procesar debe ser un diccionario."
        )

    option_counter = 0
    for option in menu_data["options"]:
        option_counter += 1
        name = option.get("name", None)

        if name is None:
            raise KeyError(
                f"El elemento N.° {option_counter} del diccionario"
                f" {menu_data['dict_name']} no tiene el parámetro 'name'."
            )
        _check_parameter("name", "str", name)


# def _check_option_parameters(menu_option: dict) -> None:
#     """
#     """


# --- Funciones privadas para construir el menú y ejecutar acciones ---
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
    # Ejecución de la opción elegida.
    if callable(menu_option["action"]):
        menu_option["action"]()
    elif isinstance(menu_option["action"], list):
        # Trabajo con una copia del diccionario pasado
        # por parámetro para no alterar el original.
        commands_from_action = copy.deepcopy(menu_option["action"])

        # Si el comando a ejecutar requiere que el usuario
        # ingrese algo por pantalla, se lo pido acá.
        # Se utiliza el mensaje definido en el campo "prompt"
        # del diccionario almacenado en "menu_option".
        user_input = None
        if "prompt" in menu_option:
            user_input = get_validated_input(menu_option["prompt"])
            print("")

        if "#PIPE" in commands_from_action:
            piped_commands = []

            for command in commands_from_action:
                if not isinstance(command, str):
                    if "#ROOT" in command:
                        command.insert(0, "doas")
                    if "#UINPUT" in command:
                        command.append(user_input)
                    piped_commands.append([i for i in command if "#" not in i])

            result = pipe_commands(*piped_commands)
            print(f"{result}")
        else:
            for command in commands_from_action:
                command_without_tags = []
                requires_root = False

                if "#ROOT" in command:
                    requires_root = True
                if "#UINPUT" in command:
                    command.append(user_input)
                command_without_tags = [i for i in command if "#" not in i]

                if requires_root:
                    run_command_as_root(command_without_tags)
                else:
                    run_command(command_without_tags)


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
    _check_basic_dictionary_structure(menu_data)
    _check_options_name(menu_data)
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
