#!/usr/bin/env python3

"""
========================
DOCUMENTACIÓN DEL MÓDULO
========================
Este módulo del paquete define tipos personalizados para representar de forma
adecuada la información que se recibe como parámetro en muchas funciones de los
módulos "creation.py" y "validation.py".

Puntualmente, se definen tipos para representar a los diccionarios utilizados
en dichos módulos, así como para representar a los tipos de datos que contienen
dichos diccionarios.
"""

from typing import (
    Any,
    Callable,
    Union,
    TypedDict,
    NotRequired,
    Required,
    Never,
)


# --- Tipos de dato de las diferentes clases de acciones ejecutables ---
SequentialCommandList = list[list[str]]

PipedCommandList = list[str | list[str]]

FunctionList = list[Callable[..., Any]]

CustomParametersFunctionList = list[
    tuple[
        # El segundo elemento de la tupla
        # es una lista que puede contener
        # prácticamente cualquier cosa, ya
        # que se utiliza para definir los
        # parámetros de la función que se
        # llama.
        Callable[..., Any],
        list[Any],
    ]
]

PossibleActionParameterTypes = Union[
    # Esta unión representa que el valor
    # del parámetro "action" podría tener
    # una lista en cualquiera de los
    # formatos indicados a continuación.
    SequentialCommandList,
    PipedCommandList,
    FunctionList,
    CustomParametersFunctionList,
]

# --- Tipo de dato de las tuplas que contienen variables de entorno ---
EnvVarTuple = tuple[int, dict[str, str]]


# --- Tipos de dato de los diccionarios utilizados en la librería ---
class OptionDictionary(TypedDict, total=False):
    name: Required[str]
    # Marcado como no requerido porque no
    # siempre tiene que estar, pero sí
    # debe estar definido siempre que se
    # quiera ejecutar algo.
    action: NotRequired[PossibleActionParameterTypes]
    # Marcado como no requerido porque no
    # siempre tiene que estar, pero sí
    # debe estar definido si el parámetro
    # "action" es una lista con cualquier
    # tipo de contenido.
    aesthetic_action: NotRequired[str]
    # Marcado como no requerido porque no
    # siempre tiene que estar, pero sí
    # debe estar definido si un comando en
    # el parámetro "action" incluye la
    # etiqueta '#UINPUT'.
    prompt: NotRequired[str]
    env_vars: NotRequired[list[EnvVarTuple]]


class MenuDictionary(TypedDict, total=False):
    dict_name: Required[str]
    title: Required[str]
    pre_menu_hook: NotRequired[Callable[..., Any]]
    options: Required[list[OptionDictionary]]
