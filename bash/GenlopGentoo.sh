#!bin/bash

# Cargo los scripts secundarios requeridos.
. colored_text
. user_input
. misc

# Funciones locales.
package_emerge_time() {
	Línea
	ask_package
	Línea

	doas genlop -t $package
}

last_ten_emerge_time() {
	Línea
	doas genlop -l | tail -n 30
	Línea
}

estimated_compile_time() {
	Línea
	ask_package
	Línea

	emerge -p $package | doas genlop --pretend
}

# Menú de selección de opciones.
until [ $selection = "0" ];
do
	clear

	Línea
	echo "En este apartado se puede acceder a las distintas opciones para utilizar Genlop."
	echo "De esta forma, se puede obtener información sobre los tiempos de instalación de los paquetes."
	Línea
	echo "1. Obtener el tiempo de instalación de un paquete específico."
	echo "2. Obtener el tiempo de instalación de los últimos treinta paquetes."
	echo "3. Obtener el tiempo de instalación estimado de un paquete."
	echo "4. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; package_emerge_time; press_enter;;
		2) clear; last_ten_emerge_time; press_enter;;
		3) clear; estimated_compile_time; press_enter;;
		4) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
