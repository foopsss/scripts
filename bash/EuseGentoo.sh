#!bin/bash

# Cargo los scripts secundarios requeridos.
. modules/colored_text
. modules/user_input
. modules/misc

# Funciones locales.
about_use() {
	Línea
	ask_use
	Línea

	euse -i $use
}

package_use_flags() {
	Línea
	ask_package
	Línea

	equery uses $package
}

packages_have_use() {
	Línea
	ask_use
	Línea

	equery hasuse $use
}

packages_built_with_use() {
	Línea
	ask_use
	Línea

	eix --installed-with-use $use
}

# Menú de selección de opciones.
until [ $selection = "0" ];
do
	clear

	YT "-------------------------------------------------------------------------------------------------------------"
	echo "En este apartado se puede acceder a las distintas opciones para obtener información sobre los parámetros USE."
	YT "-------------------------------------------------------------------------------------------------------------"
	echo "1. Obtener información sobre un parámetro USE específico."
	echo "2. Obtener una lista de parámetros USE disponibles para un paquete específico."
	echo "3. Obtener una lista de paquetes que tienen un parámetro USE específico."
	echo "4. Obtener una lista de paquetes compilados con un parámetro USE específico."
	echo "5. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; about_use; press_enter;;
		2) clear; package_use_flags; press_enter;;
		3) clear; packages_have_use; press_enter;;
		4) clear; packages_built_with_use; press_enter;;
		5) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
