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
* _check_action(), que depende de:
  * _check_action_string().
  * _check_action_command_list().
  * _check_action_simple_function_list().
  * _check_action_tuple_call_list().

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

import collections
import copy
import inspect
import sys
import warnings

from modules.console_ui import (
    clear_screen,
    draw_coloured_line,
    get_choice,
    get_validated_input,
    press_enter,
    style_text,
)

from modules.subprocess_utils import (
    pipe_commands,
    run_command,
    run_command_as_root,
)


# --- Modificación del comportamiento de warnings.warn ---
def _overwrite_warn_err_msg(message, *args, **kwargs) -> None:
    """
    _overwrite_warn_err_msg() es una función sin contenido
    que se utiliza para sobreescribir la información mostrada
    en las advertencias realizadas con la función warnings.warn.

    La idea es que solo se vea el mensaje personalizado pasado
    por parámetro, porque el resto de la información que se
    muestra no es muy útil.
    """
    print(f"{message}")


warnings.showwarning = _overwrite_warn_err_msg


# --- Funciones privadas para controlar errores ---
def _check_parameter(
    err_msg_context: str,
    parameter: any,
    expected_type: type,
    is_optional: bool = False,
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
    if not isinstance(err_msg_context, str):
        raise TypeError("El parámetro 'err_msg_context' debe ser una cadena.")
    if not isinstance(expected_type, type):
        raise TypeError(
            "El parámetro 'expected_type' debe ser un objeto de"
            " tipo (type)."
        )

    # Control de existencia de parámetros.
    if not is_optional and parameter is None:
        raise KeyError(f"Se debe proveer el parámetro {err_msg_context}.")

    # Control de tipo de parámetros.
    if parameter is not None:
        if not isinstance(parameter, expected_type):
            raise TypeError(
                f"El parámetro {err_msg_context} debe ser del tipo"
                f" {expected_type.__name__}."
            )

        # Control de longitud de parámetros.
        if isinstance(parameter, (str, list)) and len(parameter) == 0:
            raise ValueError(
                f"El parámetro {err_msg_context} debe tener una longitud mayor"
                " a cero."
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

    Nótese que esta función no valida el parámetro
    recibido porque se espera que ya llegue con el
    tipo correcto a la hora de llamar a esta función.
    """
    dict_name = menu_data.get("dict_name", None)
    title = menu_data.get("title", None)
    options = menu_data.get("options", None)
    pre_menu_hook = menu_data.get("pre_menu_hook", None)

    # Control del parámetro "dict_name".
    _check_parameter("dict_name", dict_name, str)

    # Control del parámetro "title".
    _check_parameter(f"'title' en el diccionario {dict_name}", title, str)

    # Control del parámetro "options".
    _check_parameter(
        f"'options' en el diccionario {dict_name}",
        options,
        list,
    )

    # Control del parámetro "pre_menu_hook".
    if pre_menu_hook is not None and not callable(pre_menu_hook):
        raise TypeError(
            "Revise el parámetro 'pre_menu_hook' en el diccionario"
            f" {dict_name}."
            "\nMotivo: 'pre_menu_hook' únicamente puede tratarse de"
            " un objeto de función."
        )


def _check_top_level_option_keys(menu_data: dict) -> None:
    """
    _check_top_level_option_keys() es una función que
    controla que cada elemento definido en la lista de
    opciones 'options' contenga el parámetro 'name', y
    que los parámetros opcionales como 'prompt' o
    'aesthetic_action' estén bien definidos en caso de
    estar presentes.

    Nótese que esta función no incluye validación de
    parámetros porque se espera que ya lleguen con el
    tipo y valores correctos a la hora de llamar a
    esta función.

    Asimismo, el control de los datos definidos en el
    parámetro 'action' es delegado a la función
    _check_action().
    """
    dict_name = menu_data.get("dict_name", None)
    option_counter = 0

    # Iteración sobre los elementos del parámetro
    # "options".
    for option in menu_data["options"]:
        option_counter += 1
        name = option.get("name", None)
        action = option.get("action", None)
        aesthetic_action = option.get("aesthetic_action", None)
        prompt = option.get("prompt", None)

        # Evaluación de la llave 'name'.
        _check_parameter(
            f"'name' en el elemento N.° {option_counter} del parámetro"
            f" 'options' del diccionario {dict_name}",
            name,
            str,
        )

        # Evaluación de la llave 'aesthetic_action'.
        if aesthetic_action is not None:
            # Si la llave es definida cuando no hay acciones o
            # cuando la acción no precisa de una acción estética
            # que la acompañe, avisar al usuario.
            if action is None or isinstance(action, (dict, str)):
                raise ValueError(
                    "El parámetro 'action' no fue definido en el elemento N.°"
                    f" {option_counter} del parámetro 'options' del"
                    f" diccionario {dict_name}, o fue definido como un objeto"
                    " de diccionario o una cadena."
                    "\nPor lo tanto, el parámetro 'aesthetic_action' es"
                    " inválido. Por favor remuévalo."
                )

            # Si la llave no tiene un valor válido, avisar al usuario.
            if aesthetic_action not in ["clear_screen", "print_line"]:
                raise ValueError(
                    "Revise el parámetro 'aesthetic_action' en el elemento N.°"
                    f" {option_counter} del parámetro 'options' del"
                    f" diccionario {dict_name}."
                    "\nMotivo: únicamente se admiten los valores"
                    " 'clear_screen' y 'print_line'."
                )
        else:
            # Si la llave no está definida cuando debería
            # estarlo, avisar al usuario.
            if action is not None and isinstance(action, list):
                raise KeyError(
                    f"Revise el elemento N.° {option_counter} del parámetro"
                    f" 'options' del diccionario {dict_name}."
                    " El parámetro 'aesthetic_action' debe estar definido."
                )

        # Evaluación de la llave 'prompt'.
        _check_parameter(
            f"'prompt' en el elemento N.° {option_counter} del parámetro"
            f" 'options' del diccionario {dict_name}",
            prompt,
            str,
            is_optional=True,
        )


def _check_action_string(menu_option: dict, dict_name: str) -> None:
    """
    _check_action_string() es una de las funciones
    llamadas por _check_action() para verificar los
    contenidos del parámetro 'action' de una opción.
    Puntualmente, _check_action_string() se encarga
    de los controles cuando 'action' es un string.

    Nótese que esta función no incluye validación de
    parámetros porque se espera que ya lleguen con el
    tipo y valores correctos a la hora de llamar a
    esta función.
    """
    EXIT_STRINGS = ["exit_script", "exit_menu"]
    action = menu_option.get("action", None)
    action_name = menu_option.get("name", None)

    # Verificación del parámetro para asegurarse de
    # que únicamente contiene uno de los valores
    # permitidos.
    if action not in EXIT_STRINGS:
        raise ValueError(
            "Revise el parámetro 'action' en el elemento con el nombre"
            f" '{action_name}' del parámetro 'options' del diccionario"
            f" {dict_name}."
            "\nMotivo: el parámetro 'action' únicamente admite los valores"
            " 'exit_script' y 'exit_menu' en caso de ser una cadena."
        )


def _check_action_command_list(menu_option: dict, dict_name: str) -> None:
    """
    _check_action_list() es una de las funciones
    llamadas por _check_action() para verificar los
    contenidos del parámetro 'action' de una opción.
    Puntualmente, _check_action_list() se encarga
    de los controles cuando 'action' es una lista
    compuesta por cadenas y otras listas, es decir,
    cuando contiene comandos a ejecutar.

    Nótese que esta función no incluye validación de
    parámetros porque se espera que ya lleguen con el
    tipo y valores correctos a la hora de llamar a
    esta función.
    """
    COMMAND_TAGS = ["#ROOT", "#UINPUT", "#SPLIT-INPUT"]
    ACTION_TAGS = ["#PIPE"]
    action = menu_option.get("action", None)
    action_name = menu_option.get("name", None)
    aesthetic_action = menu_option.get("aesthetic_action", None)
    prompt = menu_option.get("prompt", None)

    # Esta variable se usa para controlar si ningún
    # comando define la etiqueta "#UINPUT" en su
    # estructura, aún cuando debería estar presente
    # en algún comando.
    uinput_tag_undefined_globally = True

    # Estas variables se usan para controlar la
    # presencia de la etiqueta #SPLIT-INPUT, la
    # cual debería estar presente únicamente si
    # está presente la etiqueta #UINPUT.
    split_input_tag_defined_somewhere = False

    # Lista que se usa para almacenar los comandos
    # que tienen etiquetas repetidas, así como las
    # etiquetas repetidas.
    # Dicha lista se usará al final de los controles
    # para informarle al usuario qué comandos están
    # mal definidos, en caso de haber.
    commands_with_repeated_tags = []

    # Revisión de cada elemento de la lista 'action'.
    for item in action:
        # Si un elemento por fuera de un comando es un
        # string, debe tratarse únicamente de la etiqueta
        # "#PIPE".
        if isinstance(item, str) and item not in ACTION_TAGS:
            raise ValueError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: la única etiqueta permitida en el parámetro"
                " 'action' por fuera de las listas con los comandos es la"
                " etiqueta '#PIPE'."
            )

        # Si un elemento es una lista, se deben revisar
        # sus contenidos.
        if isinstance(item, list):
            # Contador de usos de etiquetas.
            # La idea es utilizar el contador para verificar
            # si algún comando incluye etiquetas repetidas.
            tag_counts = collections.Counter()

            # Revisión de los comandos para verificar
            # si alguno tiene la etiqueta "#UINPUT"
            # aún cuando el parámetro "prompt" no está
            # definido, por lo que no se le puede pedir
            # al usuario que provea una entrada.
            if "#UINPUT" in item:
                uinput_tag_undefined_globally = False
                if prompt is None:
                    raise KeyError(
                        "Revise el parámetro 'action' en el elemento con el"
                        f" nombre '{action_name}' del parámetro 'options' del"
                        f" diccionario {dict_name}."
                        " Motivo: uno de los comandos definidos en el"
                        " parámetro 'action' tiene la etiqueta '#UINPUT', pero"
                        " no está definido en el elemento el parámetro"
                        " 'prompt' para pedirle una entrada al usuario."
                    )

            # Revisión de los comandos para verificar
            # si alguno tiene la etiqueta "#SPLIT-INPUT".
            # Esto será importante luego para saber si
            # algún comando tiene dicha etiqueta, pero
            # no tiene definida también la etiqueta
            # "#UINPUT."
            if "#SPLIT-INPUT" in item:
                split_input_tag_defined_somewhere = True

            for string in item:
                # Revisión de los elementos para verificar que
                # todos sus componentes sean strings, en caso
                # de que sean listas.
                if not isinstance(string, str):
                    raise TypeError(
                        "Revise el parámetro 'action' en el elemento con el"
                        f" nombre '{action_name}' del parámetro 'options' del"
                        f" diccionario {dict_name}."
                        "\nMotivo: las listas con los comandos únicamente"
                        " pueden estar compuestas por cadenas."
                    )

                # Revisión de las etiquetas de los comandos
                # para verificar que solo se introduzcan
                # etiquetas válidas.
                if "#" in string and string not in COMMAND_TAGS:
                    raise ValueError(
                        "Revise el parámetro 'action' en el elemento con el"
                        f" nombre '{action_name}' del parámetro 'options' del"
                        f" diccionario {dict_name}."
                        "\nMotivo: las únicas etiquetas que se pueden"
                        f" definir para un comando son: {COMMAND_TAGS}."
                    )

                # Control de la cantidad de usos en un comando
                # de cada etiqueta definida en COMMAND_TAGS.
                if string in COMMAND_TAGS:
                    tag_counts[string] += 1

            # Si el comando tiene etiquetas repetidas, se lo
            # debe almacenar en la lista definida anteriormente
            # para almacenar aquellos que estén mal definidos.
            if any(count > 1 for count in tag_counts.values()):
                commands_with_repeated_tags.append(item)

    # Si ningún comando incluye la etiqueta "#UINPUT",
    # aunque la opción SÍ define el parámetro 'prompt',
    # se le debe advertir al usuario.
    if prompt is not None and uinput_tag_undefined_globally:
        raise ValueError(
            "Revise el parámetro 'action' en el elemento con el nombre"
            f" '{action_name}' del parámetro 'options' del diccionario"
            f" {dict_name}."
            "\nMotivo: ningún comando incluye la etiqueta '#UINPUT' para"
            " indicar que se le debe anexar la entrada provista por el"
            " usuario, aunque el parámetro 'prompt' está definido en el"
            " elemento."
        )

    # Si ningún comando incluye la etiqueta "#UINPUT"
    # aún cuando alguno sí incluye la etiqueta
    # "#SPLIT-INPUT", se le debe avisar al usuario.
    if split_input_tag_defined_somewhere and uinput_tag_undefined_globally:
        raise ValueError(
            "Revise el parámetro 'action' en el elemento con el nombre"
            f" '{action_name}' del parámetro 'options' del diccionario"
            f" {dict_name}."
            "\nMotivo: ningún comando incluye la etiqueta '#UINPUT' para"
            " indicar que se le debe anexar la entrada provista por el"
            " usuario, aunque uno o más de uno de ellos definen la etiqueta"
            " #SPLIT-INPUT para indicar que la entrada debe ser dividida"
            " en partes."
        )

    # Si algún comando incluye etiquetas repetidas se
    # le debe advertir al usuario.
    if len(commands_with_repeated_tags) > 0:
        warnings.warn(
            style_text(
                "bg",
                "yellow",
                "\nRevise el parámetro 'action' en el elemento con el"
                f" nombre '{action_name}' del parámetro 'options' del"
                f" diccionario {dict_name}."
                "\nMotivo: una o más etiquetas están repetidas en uno o"
                " varios comandos, a pesar de que solo se las debería"
                " incluir una vez. Las etiquetas repetidas serán"
                " ignoradas."
                "\nA continuación, verá una lista de los comandos que"
                " tienen etiquetas repetidas:"
                f"\n{commands_with_repeated_tags}",
                print_line=False,
            ),
            UserWarning,
        )

        # Si no se pausa la ejecución del programa cuadndo
        # la acción estética es limpiar la pantalla, la
        # advertencia no se ve.
        if aesthetic_action == "clear_screen":
            press_enter()


def _count_required_and_optional_function_args(
    function: callable,
) -> tuple[int, int]:
    """
    _count_required_and_optional_function_args() es
    una función utilizada para contar la cantidad de
    parámetros obligatorios y opcionales que tiene una
    función, a través de la inspección de su definición.
    """
    func_sig = inspect.signature(function)
    required_args = 0
    optional_args = 0

    for name, param in func_sig.parameters.items():
        if param.default is inspect.Parameter.empty:
            required_args += 1
        else:
            optional_args += 1

    return (required_args, optional_args)


def _check_action_simple_function_list(
    menu_option: dict, dict_name: str
) -> None:
    """
    _check_action_simple_function_list() es una de las funciones
    llamadas por _check_action() para verificar los contenidos
    del parámetro 'action' de una opción. Puntualmente,
    _check_action_simple_function_list() se encarga de los
    controles cuando 'action' es una lista compuesta por
    objetos de función, es decir, cuando contiene funciones
    a ejecutar, pero sin los parámetros que hay que pasarles
    al llamarlas, porque estas funciones no tienen parámetros.

    Para controlar las llamadas de funciones cuando se necesita
    especificar parámetros, se utilizan las verificaciones
    definidas en la función _check_action_tuple_call_list().

    Nótese que esta función no incluye validación de parámetros
    porque se espera que ya lleguen con el tipo y valores correctos
    a la hora de llamar a esta función.
    """
    action_name = menu_option.get("name", None)

    for function in menu_option["action"]:
        required_args, _ = _count_required_and_optional_function_args(function)

        # Si la cantidad de parámetros obligatorios es
        # mayor a cero, la función debería proveerse en
        # una tupla junto con la lista de parámetros a
        # pasarle. Por lo tanto, avisar al usuario.
        if required_args > 0:
            raise ValueError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: para ejecutar funciones sin parámetros, únicamente"
                " se pueden incluir en la lista funciones que no tengan"
                " parámetros que se deban especificar obligatoriamente."
            )


def _check_action_tuple_call_list(menu_option: dict, dict_name: str) -> None:
    """
    _check_action_tuple_call_list() es una de las funciones
    llamadas por _check_action() para verificar los contenidos
    del parámetro 'action' de una opción. Puntualmente,
    _check_action_tuple_call_list() se encarga de los
    controles cuando 'action' es una lista compuesta por
    tuplas, es decir, cuando contiene funciones a ejecutar,
    así como los parámetros que hay que pasarles al llamarlas.

    Para controlar las llamadas de funciones cuando se
    ejecutan sin especificar parámetros, se utilizan las
    verificaciones definidas en la función
    _check_action_simple_function_list().

    Nótese que esta función no incluye validación de
    parámetros porque se espera que ya lleguen con el
    tipo y valores correctos a la hora de llamar a esta
    función.
    """
    action_name = menu_option.get("name", None)

    # Revisión de cada elemento de la lista 'action'.
    for function_tuple in menu_option["action"]:
        tuple_len = len(function_tuple)

        # Si una tupla no tiene exactamente un objeto
        # de función y una lista con parámetros a
        # pasarle a la función, avisar al usuario.
        if tuple_len != 2:
            raise ValueError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: para ejecutar funciones con parámetros específicos,"
                " el parámetro 'action' debe tratarse de una lista de tuplas"
                " que tengan exactamente dos elementos cada una."
            )

        if not (
            callable(function_tuple[0]) and isinstance(function_tuple[1], list)
        ):
            raise TypeError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: para ejecutar funciones con parámetros específicos,"
                " el primer elemento del parámetro 'action' debe ser un objeto"
                " de función y el segundo elemento una lista con los"
                " parámetros a pasarle a la función."
            )

        # Evaluación de la cantidad de parámetros provistos
        # para la función. Pueden darse dos escenarios:
        # 1. La cantidad de parámetros provistos es insuficiente,
        #    debido a que no se proveen valores para uno o más
        #    parámetros obligatorios.
        # 2. La cantidad de parámetros provistos es exagerada,
        #    debido a que se proveen más valores de los que
        #    admite la función.
        req_param_amount, opt_param_amount = (
            _count_required_and_optional_function_args(function_tuple[0])
        )

        if len(function_tuple[1]) < req_param_amount:
            raise ValueError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: la definición de parámetros en una de las tuplas"
                " no contiene valores para uno o más parámetros requeridos"
                " por la función."
            )
        elif len(function_tuple[1]) > req_param_amount + opt_param_amount:
            raise ValueError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: la definición de parámetros en una de las tuplas"
                " contiene más parámetros que los que la función referenciada"
                " en la tupla acepta."
            )


def _check_action(menu_option: dict, dict_name: str) -> None:
    """
    _check_action() es una función que actúa como un
    wrapper para una familia de funciones derivadas,
    las cuales se encargan de validar el formato del
    parámetro "action" de un elemento en función de
    su tipo. Esta función se encarga de determinar
    el tipo del parámetro "action" y llamar a la
    función que corresponda según el tipo.

    Nótese que esta función no incluye validación de
    parámetros porque se espera que ya lleguen con el
    tipo y valores correctos a la hora de llamar a
    esta función.
    """
    action = menu_option["action"]
    action_name = menu_option.get("name", None)

    if isinstance(action, str):
        _check_action_string(menu_option, dict_name)
    elif isinstance(action, list):
        if all(isinstance(item, (str, list)) for item in action):
            _check_action_command_list(menu_option, dict_name)
        elif all(callable(item) for item in action):
            _check_action_simple_function_list(menu_option, dict_name)
        elif all(isinstance(item, tuple) for item in action):
            _check_action_tuple_call_list(menu_option, dict_name)
        else:
            raise TypeError(
                "Revise el parámetro 'action' en el elemento con el nombre"
                f" '{action_name}' del parámetro 'options' del diccionario"
                f" {dict_name}."
                "\nMotivo: si el parámetro 'action' es una lista, sus"
                " contenidos únicamente pueden ser: "
                "\n1. Listas de cadenas, combinadas con cadenas si es"
                " necesario."
                "\n2. Objetos de función."
                "\n3. Tuplas."
            )
    elif isinstance(action, dict):
        # Los diccionarios son controlados por las
        # funciones _check_basic_dictionary_structure()
        # y _check_top_level_option_keys() llamadas al
        # principio de la función run_menu(). No
        # corresponde hacer nada acá.
        pass
    else:
        raise TypeError(
            "Revise el parámetro 'action' en el elemento con el nombre"
            f" '{action_name}' del parámetro 'options' del diccionario"
            f" {dict_name}."
            "\nMotivo: el parámetro 'action' únicamente puede ser:"
            "\n1. Una cadena."
            "\n2. Una lista, cuyos contenidos únicamente pueden ser: objetos"
            " de función, tuplas o una combinación de cadenas y otras listas."
            "\n3. Un diccionario."
        )


# --- Funciones privadas para ejecutar acciones ---
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

    # Impresión del menú de opciones.
    draw_coloured_line(title_length, "=")
    print(menu_data["title"])
    draw_coloured_line(title_length, "=")

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
            print(f"{option_number}. {item["name"]}")
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
                    command.insert(0, "doas")
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

    Esta función depende de otra, llamada
    _handle_command_list(), la cual se encarga del
    procesamiento del parámetro "action" cuando este
    se trata de una lista de comandos a ejecutar,
    con el fin de no tener una sola función con
    mucha complejidad ciclomática, debido a la gran
    cantidad de ciclos condicionales que se utilizan
    en el tratamiento del parámetro "action".
    """
    action = menu_option.get("action", None)

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
