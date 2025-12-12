#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo del paquete contiene las funciones relacionadas a la validación de
los contenidos de la estructura de datos utilizada para construir los menús con
los que se interactúa por pantalla.

Algunas de estas funciones luego son llamadas en el módulo "creation" para
realizar la validación de los contenidos antes y durante la ejecución de los
scripts con menús.
"""

import collections
import inspect
import warnings

from typing import Any, Callable, Literal

from modules.console_ui import (
    press_enter,
    style_text,
)

from modules.menu.types import EnvVarTuple, MenuDictionary, OptionDictionary


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


# --- Funciones privadas para realizar controles de tipo ---
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


def _is_action_a_command_list(action: list[Any]) -> bool:
    """
    _is_action_a_command_list() es una función
    utilizada para verificar si el parámetro
    'action' es provisto como una lista de
    comandos o no.

    Se realiza la verificación de esta manera
    debido a que no se cuenta con otra forma
    de realizar el control en tiempo de
    ejecución.
    """
    # Si "action" no es una lista, se
    # aborta inmediatamente.
    if not isinstance(action, list):
        return False

    # "action" es una lista, toca
    # revisar sus contenidos.
    for item in action:
        # Si "action" tiene uno o más elementos
        # que no son cadenas u otras listas, se
        # aborta inmediatamente.
        if not (isinstance(item, str) or isinstance(item, list)):
            return False

        # Si un elemento de "action" es una
        # lista, se deben revisar sus contenidos.
        if isinstance(item, list):
            for element in item:
                # Si el elemento no está compuesto
                # únicamente por cadenas, se aborta
                # inmediatamente.
                if not isinstance(element, str):
                    return False

    return True


def _check_env_vars_parameter_structure(
    env_vars: list[EnvVarTuple],
    option_number: int,
    dict_name: str,
) -> None:
    """
    _check_env_vars_parameter_structure() es
    una función utilizada para verificar que
    el parámetro 'env_vars' tenga el formato
    correcto, en caso de ser definido en una
    opción.
    """
    error_msg = (
        "El parámetro 'env_vars' fue definido con el formato incorrecto en el"
        f" elemento N.° {option_number} del parámetro 'options' del"
        f" diccionario {dict_name}."
        "\nEl parámetro debería tratarse de una lista de tuplas, donde cada"
        " tupla almacena un entero que represente el comando al cual se le"
        " debe modificar el entorno de ejecución, y un diccionario con las"
        " variables a añadir, donde tanto las llaves como los valores sean"
        " cadenas, en el formato {'variable': 'valor'}."
    )

    # Si "env_vars" no es una lista,
    # se aborta inmediatamente.
    if not isinstance(env_vars, list):
        raise TypeError(error_msg)

    # Si "env_vars" es una lista, se
    # deben revisar sus contenidos.
    for item in env_vars:
        # Si alguno de los elementos de
        # la lista no es una tupla, se
        # aborta inmediatamente.
        if not isinstance(item, tuple):
            raise TypeError(error_msg)

        # Si alguno de los elementos de
        # la lista no tiene la longitud
        # adecuada, se aborta inmediatamente.
        if len(item) > 2:
            raise ValueError(error_msg)

        # Si alguno de las tuplas de la
        # lista tiene componentes que no
        # tengan el formato adecuado, se
        # aborta inmediatamente.
        if not (isinstance(item[0], int) and isinstance(item[1], dict)):
            raise TypeError(error_msg)

        # Revisión del diccionaro incluido
        # en las tuplas de la lista, para
        # asegurarse de que sus contenidos
        # tengan el formato correcto.
        for key, value in item[1].items():
            if not (isinstance(key, str) and isinstance(value, str)):
                raise TypeError(error_msg)


def _check_hook_parameter_structure(
    hook: list[Callable],
    hook_name: str,
    dict_name: str,
) -> None:
    """
    _check_hook_parameter_structure() es una
    función utilizada para verificar que los
    parámetros "on_start", "on_draw" y
    "on_exit" tengan el formato correcto en
    caso de ser definidos en un diccionario
    de menú.

    Esta función no valida el parámetro
    "dict_name" porque se espera que ya llegue
    con el valor correcto.
    """
    if not isinstance(hook_name, str):
        raise TypeError("El parámetro 'hook_name' debe ser una cadena.")

    error_msg = (
        f"El parámetro '{hook_name}' fue definido con el formato incorrecto en"
        f" el diccionario {dict_name}."
        "\nDebería tratarse de una lista de objetos de función a ejecutar."
    )

    # Si "hook" no es una lista,
    # se aborta inmediatamente.
    if not isinstance(hook, list):
        raise TypeError(error_msg)

    # Si "hook" es una lista, se
    # deben revisar sus contenidos.
    for item in hook:
        # Si alguno de los elementos de
        # la lista no es un objeto de
        # función, se aborta inmediatamente.
        if not callable(item):
            raise TypeError(error_msg)


# --- Funciones privadas para realizar controles estructurales ---
def _check_dictionary_keys(
    dictionary: dict[Any, Any], dictionary_type: Literal["main", "option"]
) -> None:
    """
    _check_dictionary_keys() es una función utilizada
    para revisar las llaves de un diccionario, con la
    finalidad de verificar si estas están definidas
    correctamente o no.

    Correctamente implica en este caso que las llaves
    deben tratarse de strings que deben tener uno de
    los valores definidos en la lista
    ADMITTED_DICTIONARY_KEYS.
    """
    if not isinstance(dictionary, dict):
        raise TypeError(
            "El parámetro 'dictionary' debe tratarse de un diccionario."
        )

    if dictionary_type not in ["main", "option"]:
        raise TypeError(
            "El parámetro 'dictionary_type' únicamente admite los valores"
            " 'main' y 'option'."
        )

    ADMITTED_MAIN_DICTIONARY_KEYS = [
        "dict_name",
        "title",
        "on_start",
        "on_draw",
        "on_exit",
        "options",
    ]

    ADMITTED_OPTION_DICTIONARY_KEYS = [
        "name",
        "action",
        "aesthetic_action",
        "prompt",
        "env_vars",
    ]

    for key in dictionary.keys():
        if (
            key not in ADMITTED_MAIN_DICTIONARY_KEYS
            and key not in ADMITTED_OPTION_DICTIONARY_KEYS
        ):
            if dictionary_type == "main":
                valid_keys = ", ".join(ADMITTED_MAIN_DICTIONARY_KEYS)
            else:
                valid_keys = ", ".join(ADMITTED_OPTION_DICTIONARY_KEYS)

            raise ValueError(
                f"Por favor, revise el diccionario que tiene la llave '{key}'."
                "\nMotivo, la llave indicada (y posiblemente más) fue definida"
                " con un tipo de dato incorrecto, o con un nombre incorrecto."
                "\nLas llaves admitidas son las siguientes cadenas: "
                f" {valid_keys}."
            )


def _check_basic_dictionary_structure(menu_data: MenuDictionary) -> None:
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
    # Control de formato de las llaves del diccionario.
    _check_dictionary_keys(dictionary=menu_data, dictionary_type="main")

    dict_name = menu_data.get("dict_name", None)
    title = menu_data.get("title", None)
    options = menu_data.get("options", None)
    on_start = menu_data.get("on_start", None)
    on_draw = menu_data.get("on_draw", None)
    on_exit = menu_data.get("on_exit", None)

    # Control del parámetro "dict_name".
    _check_parameter(
        err_msg_context="dict_name", parameter=dict_name, expected_type=str
    )

    # Control del parámetro "title".
    _check_parameter(
        err_msg_context=f"'title' en el diccionario {dict_name}",
        parameter=title,
        expected_type=str,
    )

    # Control del parámetro "options".
    _check_parameter(
        err_msg_context=f"'options' en el diccionario {dict_name}",
        parameter=options,
        expected_type=list,
    )

    # Control del parámetro "on_start".
    if on_start is not None:
        _check_hook_parameter_structure(
            hook=on_start, hook_name="on_start", dict_name=dict_name
        )

    # Control del parámetro "on_draw".
    if on_draw is not None:
        _check_hook_parameter_structure(
            hook=on_draw, hook_name="on_draw", dict_name=dict_name
        )

    # Control del parámetro "on_exit".
    if on_exit is not None:
        _check_hook_parameter_structure(
            hook=on_exit, hook_name="on_exit", dict_name=dict_name
        )


def _check_top_level_option_keys(menu_data: MenuDictionary) -> None:
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
        # Control de formato de las llaves del diccionario de opción.
        _check_dictionary_keys(dictionary=option, dictionary_type="option")

        option_counter += 1
        name = option.get("name", None)
        action = option.get("action", None)
        aesthetic_action = option.get("aesthetic_action", None)
        prompt = option.get("prompt", None)
        env_vars = option.get("env_vars", None)

        # Evaluación de la llave 'name'.
        _check_parameter(
            err_msg_context=f"'name' en el elemento N.° {option_counter} del"
            f" parámetro 'options' del diccionario {dict_name}",
            parameter=name,
            expected_type=str,
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
            err_msg_context=f"'prompt' en el elemento N.° {option_counter} del"
            f" parámetro 'options' del diccionario {dict_name}",
            parameter=prompt,
            expected_type=str,
            is_optional=True,
        )

        # Evaluación de la llave 'env_vars'.
        if env_vars is not None:
            # Si la llave no tiene el formato correcto,
            # avisar al usuario.
            _check_env_vars_parameter_structure(
                env_vars=env_vars,
                option_number=option_counter,
                dict_name=dict_name,
            )

            # Si la llave no está definida cuando debería
            # estarlo, avisar al usuario.
            if action is None or not _is_action_a_command_list(action):
                raise ValueError(
                    "El parámetro 'action' no fue definido en el elemento N.°"
                    f" {option_counter} del parámetro 'options' del"
                    f" diccionario {dict_name}, o fue definido de manera tal"
                    "que no se trata de una lista de comandos a ejecutar."
                    "\nPor lo tanto, el parámetro 'env_vars' es inválido. Por"
                    " favor remuévalo."
                )


def _check_action_string(
    menu_option: OptionDictionary, dict_name: str
) -> None:
    """
    _check_action_string() es una de las funciones
    llamadas por _check_action() para verificar los
    contenidos del parámetro 'action' de una opción.
    Puntualmente, _check_action_string() se encarga
    de los controles cuando 'action' es una cadena.

    Nótese que esta función no incluye validación de
    parámetros porque se espera que ya lleguen con el
    tipo y valores correctos a la hora de llamar a
    esta función.
    """
    action = menu_option["action"]
    action_name = menu_option["name"]

    # Verificación del parámetro para asegurarse de
    # que únicamente contiene uno de los valores
    # permitidos.
    if action != "exit":
        raise ValueError(
            "Revise el parámetro 'action' en el elemento con el nombre"
            f" '{action_name}' del parámetro 'options' del diccionario"
            f" {dict_name}."
            "\nMotivo: el parámetro 'action' únicamente admite el valor"
            " 'exit' en caso de ser una cadena."
        )


def _check_action_command_list(
    menu_option: OptionDictionary, dict_name: str
) -> None:
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
    action = menu_option["action"]
    action_name = menu_option["name"]
    aesthetic_action = menu_option["aesthetic_action"]
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
        # Si un elemento por fuera de un comando es una
        # cadena, debe tratarse únicamente de la etiqueta
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
                # todos sus componentes sean cadenas, en caso
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
                colour_type="bg",
                colour="yellow",
                text="\nRevise el parámetro 'action' en el elemento con el"
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
    function: Callable[..., Any],
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
    menu_option: OptionDictionary, dict_name: str
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
    action_name = menu_option["name"]

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


def _check_action_tuple_call_list(
    menu_option: OptionDictionary, dict_name: str
) -> None:
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
    action_name = menu_option["name"]

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


def _check_action(menu_option: OptionDictionary, dict_name: str) -> None:
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
    action_name = menu_option["name"]

    if isinstance(action, str):
        _check_action_string(menu_option=menu_option, dict_name=dict_name)
    elif isinstance(action, list):
        if all(isinstance(item, (str, list)) for item in action):
            _check_action_command_list(
                menu_option=menu_option, dict_name=dict_name
            )
        elif all(callable(item) for item in action):
            _check_action_simple_function_list(
                menu_option=menu_option, dict_name=dict_name
            )
        elif all(isinstance(item, tuple) for item in action):
            _check_action_tuple_call_list(
                menu_option=menu_option, dict_name=dict_name
            )
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
