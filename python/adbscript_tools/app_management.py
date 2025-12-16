#!/usr/bin/env python3

# Paquetes usados en este módulo:
# dev-util/android-tools - provee "adb"
# x11-misc/xdg-user-dirs - provee "xdg-user-dir"

from modules.console_ui import get_validated_input, style_text
from modules.subprocess_utils import run_command


def _install_standalone_apps() -> None:
    """
    _install_standalone_files() es una función utilizada
    para instalar aplicaciones individuales que no están
    divididas en 'split APKs'. Permite instalar una o más
    aplicaciones en una misma ejecución, determinando
    automáticamente qué es lo que se debe realizar en
    función de la entrada provista por el usuario.
    """
    # El método ".split()" ya me devuelve una lista
    # luego de dividir la cadena, así que no debo
    # preocuparme por convertir la entrada obtenida
    # en una lista.
    apks_to_install = get_validated_input(
        "Ingrese las rutas de los archivos APK que desea instalar"
    ).split()

    if len(apks_to_install) > 1:
        install_command = ["adb", "install-multi-package"] + apks_to_install
    else:
        install_command = ["adb", "install"] + apks_to_install

    run_command(install_command)


def _save_app_info_report(adb_command: list[str], fileout_name: str) -> None:
    """
    _save_app_info_report() es una función creada
    para las opciones que permiten obtener información
    sobre las aplicaciones instaladas en el dispositivo,
    permitiendo correr comandos de ADB y guardar la
    salida producida por estos en un archivo en la
    carpeta de documentos del usuario.
    """
    if not isinstance(fileout_name, str):
        raise TypeError(
            "El parámetro 'fileout_name' debe tratarse de una cadena."
        )

    # Acá no se debe olvidar que, por defecto, una
    # invocación a run_commmand devuelve como resultado
    # un objeto de tipo subprocess.CompletedProcess en
    # caso de que se haya ejecutado correctamente la
    # operación y se quiera almacenar el resultado.
    #
    # Por lo tanto, para acceder a la salida emitida
    # por un comando ejecutado con run_command se debe
    # utilizar el método "stdout" para acceder a dicha
    # salida, así como posiblemente se deba utilizar
    # el método "strip()" para limpiar dicha salida y
    # remover los saltos de línea innecesarios.
    documents_folder = run_command(
        command=["xdg-user-dir", "DOCUMENTS"], capture_output=True
    ).stdout.strip()

    # A cualquier comando de listado de paquetes de ADB
    # se le debe añadir lo siguiente:
    # * "-f" para obtener la ruta al APK base de cada
    #   aplicación.
    # * "--show-versioncode" para obtener el número de
    #   versión de cada aplicación.
    parameters_to_append = ["-f", " --show-versioncode"]

    command_output = run_command(
        command=adb_command + parameters_to_append, capture_output=True
    )

    if command_output.returncode == 0:
        try:
            with open(f"{documents_folder}/{fileout_name}", "w") as file:
                # Ahora se requiere trabajar únicamente
                # con la salida estándar almacenada en
                # "command_output", para poder grabarla
                # en el achivo de salida.
                file.write(command_output.stdout)

            style_text(
                colour_type="bg",
                colour="green",
                text="Archivo guardado exitosamente en la siguiente ubicación:"
                f"\n{documents_folder}/{fileout_name}.",
            )
        except OSError as os_error:
            style_text(
                colour_type="bg",
                colour="red",
                text="Se ha producido un error del SO durante la creación del"
                f" archivo {fileout_name}."
                f"\nEl error encontrado es: {os_error}.",
            )


APP_MANAGEMENT_MENU_DATA = {
    "dict_name": "APP_MANAGEMENT_MENU_DATA",
    "title": "Apartado para administrar las aplicaciones del dispositivo",
    "options": [
        {"name": "INSTALACIÓN/DESINSTALACIÓN"},
        {
            "name": "Instalar una aplicación mediante un archivo APK.",
            "action": [_install_standalone_apps],
            "aesthetic_action": "clear_screen",
        },
        {
            "name": "Instalar una aplicación dividida en distintos archivos"
            " APK.",
            "action": [["#UINPUT", "#SPLIT-INPUT", "adb", "install-multiple"]],
            "aesthetic_action": "print_line",
            "prompt": "APKs de la aplicación a instalar",
        },
        {
            "name": "Desinstalar una aplicación globalmente.",
            "action": [["#UINPUT", "adb", "uninstall"]],
            "aesthetic_action": "print_line",
            "prompt": "ID de la aplicación",
        },
        {
            "name": "Desinstalar una aplicación para el usuario actual.",
            "action": [
                ["#UINPUT", "adb", "shell", "pm", "uninstall", "--user", "0"]
            ],
            "aesthetic_action": "print_line",
            "prompt": "ID de la aplicación",
        },
        {
            "name": "Restaurar una aplicación desinstalada previamente para"
            " un usuario.",
            "action": [
                [
                    "#UINPUT",
                    "adb",
                    "shell",
                    "cmd",
                    "package",
                    "install-existing",
                ]
            ],
            "aesthetic_action": "print_line",
            "prompt": "ID de la aplicación",
        },
        {"name": "HABILITACIÓN/DESHABILITACIÓN"},
        {
            "name": "Deshabilitar una aplicación.",
            "action": [
                [
                    "#UINPUT",
                    "adb",
                    "shell",
                    "pm",
                    "disable-user",
                    "--user",
                    "0",
                ]
            ],
            "aesthetic_action": "print_line",
            "prompt": "ID de la aplicación",
        },
        {
            "name": "Habilitar una aplicación deshabilitada previamente.",
            "action": [["#UINPUT", "adb", "shell", "pm", "enable"]],
            "aesthetic_action": "print_line",
            "prompt": "ID de la aplicación",
        },
        {"name": "LISTADOS DE APLICACIONES"},
        {
            "name": "Obtener un listado de aplicaciones del sistema.",
            "action": [
                (
                    _save_app_info_report,
                    [
                        adb_command := [
                            "adb",
                            "shell",
                            "pm",
                            "list",
                            "packages",
                            "-s",
                        ],
                        fileout_name := "AppsSistema.txt",
                    ],
                )
            ],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Obtener un listado de aplicaciones de terceros"
            " instaladas.",
            "action": [
                (
                    _save_app_info_report,
                    [
                        adb_command := [
                            "adb",
                            "shell",
                            "pm",
                            "list",
                            "packages",
                            "-3",
                        ],
                        fileout_name := "AppsTerceros.txt",
                    ],
                )
            ],
            "aesthetic_action": "print_line",
        },
        {
            "name": "Obtener un listado de aplicaciones desactivadas.",
            "action": [
                (
                    _save_app_info_report,
                    [
                        adb_command := [
                            "adb",
                            "shell",
                            "pm",
                            "list",
                            "packages",
                            "-d",
                        ],
                        fileout_name := "AppsDesactivadas.txt",
                    ],
                )
            ],
            "aesthetic_action": "print_line",
        },
        {"name": "MISCELÁNEA"},
        {
            "name": "SALIR.",
            "action": "exit",
        },
    ],
}
