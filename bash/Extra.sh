#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	bash AppMan.sh
}

menu_option_two() {
	Línea
	echo "En este apartado, usted podrá optar por instalar un archivo .zip mediante el modo Recovery. Para ello,"
	echo "por favor, indique su ubicación, incluyendo el nombre de este."
	echo
	echo "Ejemplo: '/home/Usuario/Documentos/Ejemplo.zip/'."
	Línea

	echo -n "Ubicación del archivo: "
	read ubicacion
	echo

	# Chequeo si la variable 'ubicacion' contiene algún valor o no.
	if [ -z "$ubicacion" ]
	then
		# Si la variable no recibe ningún valor, se informa al usuario y se aborta la operación.
		NV "$ubicacion"
	else
		# Si la variable recibe un valor, realizo la operación.
		adb sideload $ubicacion
	fi

	Repetir
}

menu_option_three() {
	Línea
	echo "En este apartado, usted podrá optar por ejecutar cualquier otro tipo de comando no incluido en esta"
	echo "herramienta."
	echo
	echo "Para ello, por favor, indique el comando a ejecutar en el campo correspondiente."
	Línea

	echo -n "Comando a ejecutar: "
	read comando
	echo

	# Chequeo si la variable 'ubicacion' contiene algún valor o no.
	if [ -z "$comando" ]
	then
		# Si la variable no recibe ningún valor, se informa al usuario y se aborta la operación.
		NV "$comando"
	else
		# Si la variable recibe un valor, realizo la operación.
		$comando
	fi

	Repetir
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do
	clear
	Línea
	echo "En este apartado, usted podrá optar por elegir entre una serie de comandos adicionales para ejecutar."
	Línea
	echo "1. Administrar las aplicaciones instaladas."
	echo "2. Instalar un archivo .zip utilizando el recovery.   (adb sideload)"
	echo "3. Ejecutar un comando propio."
	echo "4. Volver al menú principal."
	echo

	read_selection

	case $selection in
		1) clear; menu_option_one;;
		2) clear; menu_option_two;;
		3) clear; menu_option_three;;
		4) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done