#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	Línea
	echo "Introduzca en el campo correspondiente la ubicación del archivo APK a instalar."
	echo
	echo "Ejemplo: «/home/Usuario/Documentos/Aplicación.apk»."
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
		# Si la variable recibe un valor, ejecuto el comando con normalidad.
		adb install $ubicacion
	fi

	Repetir
}

menu_option_two() {
	Línea
	echo "Introduzca en los campos correspondientes las ubicaciones de los archivos APK correspondientes a la"
	echo "aplicación a instalar. Se pueden instalar 3 partes al mismo tiempo."
	Línea
	
	echo -n "Ubicación del primer archivo: "
	read ubicacion
	echo -n "Ubicación del segundo archivo: "
	read ubicacion1
	echo -n "Ubicación del tercer archivo: "
	read ubicacion2
	echo
	
	adb install-multiple $ubicacion $ubicacion1 $ubicacion2

	Repetir
}

menu_option_three() {
	Línea
	echo "Introduzca en los campos correspondientes las ubicaciones de los archivos APK correspondientes a las"
	echo "aplicaciones a instalar. Se pueden instalar hasta 5 aplicaciones al mismo tiempo."
	Línea

	echo -n "Ubicación del primer archivo: "
	read ubicacion
	echo -n "Ubicación del segundo archivo: "
	read ubicacion1
	echo -n "Ubicación del tercer archivo: "
	read ubicacion2
	echo -n "Ubicación del cuarto archivo: "
	read ubicacion3
	echo -n "Ubicación del quinto archivo: "
	read ubicacion4
	echo

	adb install-multi-package $ubicacion $ubicacion1 $ubicacion2 $ubicacion3 $ubicacion4

	Repetir
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do   
	clear
	Línea
	echo "En este apartado, usted podrá optar por elegir entre distintas opciones para instalar aplicaciones en"
	echo "su dispositivo mediante archivos APK."
	Línea
	echo "1. Instalar una aplicación.                           (adb install)"
	echo "2. Instalar una aplicación por partes (split APKs).   (adb install-multiple)"
	echo "3. Instalar múltiples aplicaciones.                   (adb install-multi-package)"
	echo "4. Volver al menú de manejo de aplicaciones."
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