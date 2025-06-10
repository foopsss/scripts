#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	Línea
	echo "Para copiar un archivo hacia el dispositivo, por favor, indique su ubicación incluyendo el nombre de"
	echo "este, y la ubicación en el dispositivo a la cual le gustaría copiarlo."
	echo
	echo "Ejemplo: 'adb push /home/usuario/Documentos/Texto.txt/ /sdcard/Textos/'."
	Línea
	
	echo -n "Ubicación del archivo: "
	read ubicacion
	echo -n "Ubicación a la cual copiar: "
	read ubicacion1
	echo

	# Chequeo que ambas variables utilizadas contengan un valor.
	if [ -n "$ubicacion" ] && [ -n "$ubicacion1" ]
	then
		# Si ambas variables reciben un valor ejecuto la acción.
		adb push $ubicacion $ubicacion1
	else
		# Si ambas o alguna de las variables no reciben un valor informo al usuario y aborto la acción.
		RBT "Una o ambas ubicaciones NO fueron especificadas."
	fi
	
	Repetir
}

menu_option_two() {
	Línea
	echo "Para copiar un archivo desde el dispositivo, por favor, indique su ubicación incluyendo el nombre de"
	echo "este, y la ubicación en el ordenador a la cual le gustaría copiarlo."
	echo
	echo "Ejemplo: 'adb pull /sdcard/Textos/Texto.txt/ /home/usuario/Documentos/'."
	Línea
	
	echo -n "Ubicación del archivo: "
	read ubicacion
	echo -n "Ubicación a la cual copiar: "
	read ubicacion1
	echo

	if [ -n "$ubicacion" ] && [ -n "$ubicacion1" ]
	then
		adb pull $ubicacion $ubicacion1
	else
		RBT "Una o ambas ubicaciones NO fueron especificadas."
	fi
	
	Repetir
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do   
	clear
	Línea
	echo "En este apartado, usted podrá optar por copiar archivos desde o hacia su dispositivo móvil."
	Línea
	echo "1. Copiar archivos hacia el dispositivo.                      (adb push)"
	echo "2. Copiar archivos desde el dispositivo hacia el ordenador.   (adb pull)"
	echo "3. Volver al menú principal."
	echo

	read_selection

	case $selection in
		1) clear; menu_option_one;;
		2) clear; menu_option_two;;
		3) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done