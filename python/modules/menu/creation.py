#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo del paquete contiene las funciones relacionadas al aspecto estético
y el funcionamiento de los scripts. Específicamente, contiene lo relacionado
a la impresión por pantalla del menú de opciones y el tratamiento de las
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
        4.2.2. Si se debe ejecutar una función, "action" puede tener uno de dos
               formatos:
               4.2.2.1. Para ejecutar funciones sin que se deban especificar
                        sus parámetros, "action" debe ser una lista de objetos
                        de función. Esto implica que la función no debe tener
                        parámetros obligatorios, de lo contrario, véase el
                        siguiente ítem.
               4.2.2.2. Para ejecutar funciones especificando sus parámetros,
                        "action" debe ser una lista de tuplas, donde cada tupla
                        debe contener un objeto de función y una lista con
                        todos los parámetros que se le quieran pasar a la
                        función.
        4.2.3. Si se deben ejecutar uno o varios comandos, "action" debe
               contener una lista, la cual estará compuesta a su vez por una o
               más listas de strings. Para correr comandos con pipes o permisos
               de superusuario, véase la sección "Modos especiales de
               ejecución".
        4.2.4. Si se desea salir de un menú de opciones para volver a otro menú
               anterior, "action" deberá contener el string 'exit_menu'.
        4.2.5. Si se desea salir del script, "action" deberá contener el string
               'exit_script'.
        4.2.6. Si se desea mostrar un título de apartado, "action" debe estar
               ausente o contener el valor None.
   4.3. "aesthetic_action": la acción estética a ejecutar antes de la acción
        principal. Puede contener los valores 'print_line' o 'clear_screen'.
   4.4. "prompt": el mensaje para solicitar una entrada del usuario.

### Obligatoriedad de los parámetros ###
A excepción de "dict_name", "title" y "options", que deben ser obligatorios,
todos los demás parámetros pueden ser opcionales en el diccionario de entrada.

Para cada elemento de la lista "options", el único parámetro que siempre es
obligatorio es "name", aunque el parámetro "aesthetic_action" también es
obligatorio en caso de que el parámetro "action" esté presente y se cumpla que
"action" es una lista. Por el contrario, si "action" tiene otro tipo, entonces
"aesthetic_action" NO debería estar presente ya que no tendría efecto.

La presencia de estos parámetros, así como la validez de sus definiciones, está
controlada por las siguientes funciones:
* _check_basic_dictionary_structure().
* _check_top_level_option_keys().
* _check_action()

Estas funciones están disponibles en el módulo "validation" de este paquete,
el cual contiene toda la lógica relacionada a la validación de elementos de un
diccionario.

### Modos especiales de ejecución de comandos ###
De acuerdo a lo estipulado en el inciso 4.2.3, a la hora de ejecutar uno o más
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
  ** Para los comandos que permiten recibir múltiples entradas separadas por
     espacios es posible incluir la etiqueta "#SPLIT-INPUT" junto a "#UINPUT",
     para que la entrada sea dividida y procesada correctamente por el
     intérprete de comandos.
* En caso de que dos comandos deban ejecutarse con pipes, el primer elemento de
  la lista contenida por la clave "action" debe ser el string "#PIPE", seguido
  de las listas con las definiciones de comandos.
  ** Asimismo, en caso de que alguno de los comandos deba ejecutarse con
     permisos de superusuario o se le deba anexar una entrada provista por el
     usuario, se deben incluir los strings "#ROOT" y "#UINPUT", de acuerdo a lo
     descripto para los casos anteriores.
"""

import copy
import sys
import textwrap

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

from modules.menu.validation import (
    _check_basic_dictionary_structure,
    _check_top_level_option_keys,
    _check_action,
)

from modules.program_tools import get_privilege_elevation_command


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
    # Ejecución del parámetro "pre_menu_hook", en
    # caso de que esté definido.
    title_length = len(menu_data["title"])
    pre_menu_hook = menu_data.get("pre_menu_hook", None)
    if pre_menu_hook is not None:
        draw_coloured_line(title_length, "=")
        pre_menu_hook()

    # Impresión del título del menú.
    draw_coloured_line(title_length, "=")
    print(menu_data["title"])
    draw_coloured_line(title_length, "=")

    # Impresión del menú de opciones.
    option_number = 1

    for item in menu_data["options"]:
        if "action" not in item:
            # El elemento a imprimir es un encabezado
            # de sección.
            print(f"\n{item["name"]}")
            draw_coloured_line(len(item["name"]))
        else:
            # El elemento a imprimir es una opción
            # del menú.
            prefix_len = len(f"{option_number}. ")
            prefix_str = " " * prefix_len

            # Como detalle estético, se busca que la
            # longitud de las descripciones de las
            # opciones no sobrepasen la longitud del
            # título. Para ello, se dividen las líneas
            # y se las guarda en una lista, respecto
            # de la cual se debe iterar.
            wrapped_lines = textwrap.wrap(
                text=item["name"],
                width=title_length,
                initial_indent=f"{option_number}. ",
                subsequent_indent=prefix_str,
            )

            for line in wrapped_lines:
                print(line)

            option_number += 1

    # Esta línea en blanco se deja para que el
    # listado de opciones no colisione con el
    # pedido de elección al usuario, realizado
    # por get_choice().
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
            # Si un ítem de la lista "options" contenida
            # dentro del diccionario de entrada tiene un
            # parámetro "action" definido, entonces se lo
            # añade a la lista de salida.
            command_options.append(item)

    return command_options


def _handle_command_list(menu_option: dict) -> None:
    """
    _handle_command_list() es una subfunción de
    _handle_action() que se encarga de procesar el
    parámetro "action" en una opción del diccionario
    de entrada cuando este es provisto como una lista
    de comandos a ejecutar.

    Se encarga de procesar los parámetros provistos
    en la opción y de recibir una entrada de parte
    del usuario en caso de ser necesario, previo
    a la ejecución del comando provisto.
    """
    # Se realiza una copia "profunda" del parámetro
    # "action" para no alterar la versión definida
    # en el diccionario. Esto podría pasar, por
    # ejemplo, cuando a un comando se le debe anexar
    # una entrada provista por el usuario.
    action_deepcopy = copy.deepcopy(menu_option["action"])
    user_input = None

    if "prompt" in menu_option:
        user_input = get_validated_input(menu_option["prompt"])
        print("")

    # Se analiza si los comandos deben ejecutarse a
    # través de un pipe o no.
    if "#PIPE" in action_deepcopy:
        # Lista para almacenar los comandos
        # a ejecutar.
        piped_commands = []

        # Se inspecciona cada comando para anexarle
        # cualquier cosa que pueda llegar a ser
        # necesaria, según las etiquetas que tenga.
        # Luego se limpia el comando para remover
        # las etiquetas, de manera que se lo pueda
        # ejecutar sin problemas.
        for command in action_deepcopy:
            if not isinstance(command, str):
                if "#ROOT" in command:
                    root_cmd = get_privilege_elevation_command()
                    command.insert(0, f"{root_cmd}")
                if "#UINPUT" in command:
                    if "#SPLIT-INPUT" in command:
                        user_input = user_input.split()
                        command = command + user_input
                    else:
                        command.append(user_input)
                piped_commands.append([i for i in command if "#" not in i])

        # Ejecución de los comandos y resguardo de
        # la salida producida por este.
        result = pipe_commands(*piped_commands)
        print(f"{result}")
    else:
        for command in action_deepcopy:
            # Lista para almacenar cada comando
            # a ejecutar.
            command_without_tags = []
            requires_root = False

            # Se inspecciona el comando para determinar
            # si se lo debe ejecutar con permisos de
            # superusuario o se le debe anexar alguna
            # entrada provista por el usuario.
            # Luego se lo limpia para remover cualquier
            # etiqueta que pueda tener, de manera que
            # se lo pueda ejecutar sin problemas.
            if "#ROOT" in command:
                requires_root = True
            if "#UINPUT" in command:
                if "#SPLIT-INPUT" in command:
                    user_input = user_input.split()
                    command = command + user_input
                else:
                    command.append(user_input)

            command_without_tags = [i for i in command if "#" not in i]

            # Ejecución del comando.
            if requires_root:
                run_command_as_root(command_without_tags)
            else:
                run_command(command_without_tags)


def _handle_action(menu_option: dict) -> None:
    """
    _handle_action() es una función utilizada para
    ejecutar comandos o funciones provistas en un
    diccionario de entrada. La idea es encapsular
    casi toda la lógica de ejecución de interpretación
    y ejecución del parámetro "action" en esta función
    (y en sus funciones asociadas), de modo que la
    menor cantidad de lógica de procesamiento
    posible esté definida en run_menu().

    Esta función depende de otra función, llamada
    _handle_command_list(), la cual se encarga del
    procesamiento del parámetro "action" cuando este
    se trata de una lista de comandos a ejecutar,
    con el fin de no tener una sola función con
    mucha complejidad ciclomática, debido a la gran
    cantidad de ciclos condicionales que se utilizan
    en el tratamiento del parámetro "action".
    """
    action = menu_option.get("action")

    if all(isinstance(item, (str, list)) for item in action):
        # Tratamiento de listas de comandos.
        _handle_command_list(menu_option)
    elif all(callable(item) for item in action):
        # Tratamiento de listas de funciones.
        for function in action:
            function()
    elif all(isinstance(item, tuple) for item in action):
        # Tratamiento de listas de tuplas con
        # objetos de función y listas de
        # parámetros.
        for func_tuple in action:
            function = func_tuple[0]
            function_params = func_tuple[1]
            function(*function_params)


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
    if not isinstance(menu_data, dict):
        raise ValueError(
            "La estructura de datos a procesar debe ser un diccionario."
        )

    # Control de estructura del diccionario
    # de entrada.
    _check_basic_dictionary_structure(menu_data)
    _check_top_level_option_keys(menu_data)

    # Ciclo principal para imprimir el menú,
    # recibir una elección y ejecutarla.
    while True:
        # Impresión por pantalla del menú.
        clear_screen()
        _draw_menu(menu_data)

        # Determinación de la opción elegida
        # por el usuario.
        options = _get_command_options(menu_data)
        option_number = get_choice(1, len(options))
        option = options[option_number - 1]

        # Control de formato de la acción elegida
        # por el usuario.
        _check_action(option, menu_data["dict_name"])

        # En primera instancia, se controla si el
        # usuario desea salir o dirigirse a otro
        # menú de un script.
        # En caso de que no se desee hacer ninguna
        # de estas cosas, se prosigue con las
        # opciones de ejecución definidas abajo.
        action = option["action"]
        if isinstance(action, dict):
            run_menu(action)
            continue
        elif isinstance(action, str) and action == "exit_menu":
            break
        elif isinstance(action, str) and action == "exit_script":
            sys.exit(0)

        # Ejecución de la acción estética definida
        # en la opción elegida por el usuario, así
        # como de la acción principal.
        if option["aesthetic_action"] == "clear_screen":
            clear_screen()
        elif option["aesthetic_action"] == "print_line":
            draw_coloured_line(len(menu_data["title"]))
        _handle_action(option)

        # Se pausa la ejecución del script tras
        # ejecutar una opción para ver la salida
        # que produce por pantalla.
        press_enter()
