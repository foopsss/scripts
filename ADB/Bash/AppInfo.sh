#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	Línea
	echo "Introduzca en el campo correspondiente la ID de la aplicación cuya ruta quiere averiguar."
	Línea

	echo -n "ID de la aplicación: "
	read ID
	
	# Chequeo si la variable 'ID' contiene algún valor o no.
	if [ -z "$ID" ]
	then
		# Si la variable no recibe ningún valor, se informa al usuario y se aborta la operación.
		NV "$ID"
	else
		# Si la variable recibe un valor, muestro por pantalla la ruta de la aplicación solicitada.
		echo
		IDPATH=$(adb shell pm path $ID)
		echo "La ruta de la aplicación indicada es: "
		YBT "${IDPATH}"
	fi

	Repetir
}

menu_option_two() {
	Apps=Apps.txt

	Línea
	echo "A continuación, obtendrá una lista de las aplicaciones instaladas en su dispositivo tanto por el"
	echo "fabricante como por usted mismo. Los directorios escaneados son system/app, /priv-app/ y data/app."
	echo
	echo "Una vez que presione cualquier tecla, se imprimirá la lista y se la guardará en un archivo de texto en"
	echo "la carpeta actual, ya que será extensa."
	Línea

	read -n1
	OIE "adb shell pm list packages -f" "$Apps"

	Repetir
}

menu_option_three() {
	AppsDes=AppsDes.txt

	Línea
	echo "A continuación, obtendrá una lista de las aplicaciones de su dispositivo que se encuentran suprimidas."
	echo
	echo "Una vez que presione cualquier tecla, se imprimirá la lista y se la guardará en un archivo de texto en"
	echo "la carpeta actual, ya que será extensa."
	Línea

	read -n1
	OIE "adb shell pm list packages -d -f" "$AppsDes"

	Repetir
}

menu_option_four() {
	AppsClave=AppsClave.txt

	Línea
	echo "Introduzca en el campo correspondiente alguna palabra que quiera utilizar para poder identificar el ID"
	echo "de alguna aplicación, junto con su ruta."
	echo
	echo "Una vez que introduzca la palabra, se imprimirá la lista y se la guardará en la carpeta actual. De"
	echo "estar vacío el archivo, es porque no se encontró nada y deberá probar con otra clave."
	Línea

	echo -n "Palabra clave: "
	read clave
	echo 
	
	if [ -z "$clave" ]
	then
		NV "$clave"
	else
		OIE "adb shell pm list packages -f $clave" "$AppsClave"
	fi

	Repetir
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do
	clear
	Línea
	echo "En este apartado, usted podrá optar por obtener cierta información de las aplicaciones instaladas en su"
	echo "dispositivo."
	Línea
	echo "1. Obtener la ruta de una aplicación.                               (adb shell pm path)"
	echo "2. Obtener un listado de aplicaciones y sus rutas.                  (adb shell pm list packages -f)"
	echo "3. Obtener un listado de aplicaciones desactivadas y sus rutas.     (adb shell pm list packages -d -f)"
	echo "4. Obtener un listado de aplicaciones buscando por palabra clave.   (adb shell pm list packages -f)"
	echo "5. Volver al menú de manejo de aplicaciones."
	echo

	read_selection

	case $selection in
		1) clear; menu_option_one;;
		2) clear; menu_option_two;;
		3) clear; menu_option_three;;
		4) clear; menu_option_four;;
		5) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done