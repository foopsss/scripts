#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	Línea
	fastboot format system
	Repetir
}

menu_option_two() {
	Línea
	fastboot format userdata
	Repetir
}

menu_option_three() {
	Línea
	fastboot format cache
	Repetir
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do
	clear
	Línea
	echo "En este apartado, usted podrá optar por formatear ciertas particiones de su dispositivo utilizando el"
	echo "modo Fastboot."
	Línea
	echo "1. Formatear la partición /system.   (fastboot format system)"
	echo "2. Formatear la partición /data.     (fastboot format userdata)"
	echo "3. Formatear la partición /cache.    (fastboot format cache)"
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