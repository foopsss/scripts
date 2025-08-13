#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
 	bash AppInstall.sh
}

menu_option_two() {
	Línea
	echo "En este apartado, usted podrá optar por «desinstalar» aplicaciones de su dispositivo. Tenga en cuenta"
	echo "que no es posible borrar completamente una aplicación del dispositivo, sino para el usuario actual, por"
	echo "lo que esta puede ser restaurada con un reseteo, o utilizando la siguiente opción de este apartado."
	echo
	echo "Para esto, se requiere el «ID» de la aplicación que quiera desinstalar. Para obtenerlo, puede descargar"
	echo "alguna aplicación de la Play Store o la Web, como «Package Name Viewer 2.0», o utilizar alguna de las"
	echo "opciones del sexto apartado del conjunto de opciones extra."
	Línea

	echo -n "ID de la aplicación: "
	read ID
	echo

	# Chequeo si la variable 'ID' contiene algún valor o no.
	if [ -z "$ID" ]
	then
		# Si la variable no recibe ningún valor, se informa al usuario y se aborta la operación.
		NV "$ID"
	else
		# Si la variable recibe un valor, realizo la operación.
		adb shell pm uninstall --user 0 $ID
	fi

	Repetir
}

menu_option_three() {
	Línea
	echo "En este apartado, usted podrá optar por «reinstalar» aquellas aplicaciones que haya removido de su"
	echo "dispositivo utilizando la opción anterior."
	echo
	echo "Se requiere el ID de la aplicación desinstalada."
	Línea

	echo -n "ID de la aplicación: "
	read ID
	echo

	if [ -z "$ID" ]
	then
		NV "$ID"
	else
		adb shell cmd package install-existing $ID
	fi

	Repetir
}

menu_option_four() {
	Línea
	echo "En este apartado, usted podrá optar por desactivar aplicaciones de su dispositivo. Tenga en cuenta que"
	echo "a diferencia de la supresión de aplicaciones mediante el sistema operativo, las que son desactivadas"
	echo "mediante este método solo pueden ser devueltas a la normalidad a través del mismo."
	echo
	echo "Se requiere el ID de la aplicación a desactivar."
	Línea

	echo -n "ID de la aplicación: "
	read ID
	echo

	if [ -z "$ID" ]
	then
		NV "$ID"
	else
		adb shell pm disable-user --user 0 $ID
	fi

	Repetir
}

menu_option_five() {
	Línea
	echo "En este apartado, usted podrá optar por reactivar aquellas aplicaciones que haya desactivado utilizando"
	echo "la opción anterior."
	echo
	echo "Se requiere el ID de la aplicación a reactivar."
	Línea

	echo -n "ID de la aplicación: "
	read ID
	echo

	if [ -z "$ID" ]
	then
		NV "$ID"
	else
		adb shell pm enable $ID
	fi

	Repetir
}

menu_option_six() {
	bash AppInfo.sh
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do
	clear
	Línea
	echo "En este apartado, usted podrá optar por realizar una serie de operaciones para administrar las"
	echo "aplicaciones del dispositivo."
	Línea
	echo "1. Instalar una aplicación."
	echo "2. Desinstalar una aplicación para el usuario actual.    (adb shell pm uninstall)"
	echo "3. Restaurar una aplicación desinstalada previamente.    (adb shell cmd package install-existing)"
	echo "4. Deshabilitar una aplicación.                          (adb shell pm disable-user)"
	echo "5. Habilitar una aplicación deshabilitada previamente.   (adb shell pm enable)"
	echo "6. Obtener información de las aplicaciones instaladas."
	echo "7. Volver al menú principal."
	echo

	read_selection

	case $selection in
		1) clear; menu_option_one;;
		2) clear; menu_option_two;;
		3) clear; menu_option_three;;
		4) clear; menu_option_four;;
		5) clear; menu_option_five;;
		6) clear; menu_option_six;;
		7) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done