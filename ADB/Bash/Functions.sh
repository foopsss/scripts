#!/bin/bash

GBT() {
	# GBT es el acrónimo para Green Bold Text.
	# Esta función imprime texto blanco, sobre un fondo verde y en negritas.
	echo -e "\e[1;42m$1\e[0m"
}
export -f GBT

RBT() {
	# RBT es el acrónimo para Red Bold Text.
	# Esta función imprime texto blanco, sobre un fondo rojo y en negritas.
	echo -e "\e[1;41m$1\e[0m"
}
export -f RBT

YBT() {
	# YBT es el acrónimo para Yellow Bold Text.
	# Esta función imprime texto blanco, sobre un fondo rojo y en negritas.
	echo -e "\e[1;43m$1\e[0m"
}
export -f YBT

BBT() {
	# BBT es el acrónimo para Blue Bold Text.
	# Esta función imprime texto blanco, sobre un fondo azul y en negritas.
	echo -e "\e[1;44m$1\e[0m"
}
export -f BBT

YT() {
	# YT es el acrónimo para Yellow Text.
	# Esta función solo imprime texto amarillo.
	echo -e "\e[1;33m$1\e[0m"
}
export -f YT

BT() {
	# BT es el acrónimo para Bold Text.
	# Esta función imprime texto en negritas.
	echo -e "\e[1m$1\e[0m"
}
export -f BT

UT() {
	# UT es el acrónimo para Underlined Text.
	# Esta función imprime texto subrayado.
	echo -e "\e[3m$1\e[0m"
}
export -f UT

resize_window() {
	# Esta función utiliza una secuencia para definir el tamaño de la ventana.
	printf '\e[8;32;104t'
}
export -f resize_window

read_selection() {
	# Esta función presenta el diálogo para introducir un valor.
	echo -n "Escriba el número correspondiente a la operación que desee realizar y presione ENTER: "
	read selection
	Línea
}
export -f read_selection

press_enter() {
	# Cuando se termina de ejecutar una acción, esta función muestra un mensaje para continuar.
	echo
	echo -n "Presione ENTER para continuar."
	read
	clear
}
export -f press_enter

incorrect_selection() {
	# En caso de que la selección realizada no sea la correcta, esta función muestra un mensaje de error.
	RBT "¡Selección incorrecta! Por favor, intente de nuevo."
}
export -f incorrect_selection

Línea() {
	# Esta función imprime una línea de guiones.
	YT "-------------------------------------------------------------------------------------------------------"
}
export -f Línea

adbcheck() {
	# Esta función chequea si las herramientas de plataforma se encuentran instaladas.
	# Si no se encuentran instaladas, le avisa al usuario y cierra el programa.

	# Ejecuto un comando de ADB y guardo el código de error.
	{
		adb devices
		coderr=$?
	} &> /dev/null

	# Actúo según el código de error.
	if [ "$coderr" -gt 0 ]
	then
		RBT "Las herramientas de plataforma NO se encuentran instaladas."
		echo
		echo "Para poder funcionar, este script requiere que las herramientas de plataforma"
		echo "se encuentren instaladas."
		echo
		echo "Las herramientas de plataforma se pueden descargar en el siguiente enlace:"
		BBT "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
		echo
		echo "Para mayor comodidad puede añadir las herramientas de plataforma a su"
		echo "variable de entorno:"
		BBT "https://www.xda-developers.com/adb-fastboot-any-directory-windows-linux/"
		echo
		echo "A continuación, este script se cerrará en 10 segundos o si presiona una tecla."
		echo "Intente usarlo de nuevo cuando tenga las herramientas de plataforma instaladas."
		read -n1 -t10
		clear
		exit
	fi
}
export -f adbcheck

NV() {
	# NV es el acrónimo para Null Value.
	# Esta función chequea por la posible nulidad de una variable dada, para avisar al usuario de ser necesario.
	if [ -n "$1" ]
	then
		GBT "Se ha introducido un valor."
	else
		BBT "NO se introdujo ningún valor."
	fi
}
export -f NV

OIE() {
	# OIE es el acrónimo para Open If Existing.
	# Esta función primero chequea si el comando solicitado se realizó con éxito.
	# De haberlo sido, chequea por la existencia de un archivo y ofrece abrirlo, de ser posible.
	# De no haber sucedido, elimina el archivo que se genera inevitablemente, al estar vacío.

	# Primero, ejecuto un comando cuyo resultado debo guardar, así como su código de error.
	{
		$1 > $2
		coderr=$?
	} &> /dev/null

	# Dependiendo del resultado del código de error, actúo.
	if [ "$coderr" -eq 0 ]
	then
		if [ -e "$2" ]
		then
			GBT "El archivo $2 se ha creado exitosamente en la ubicación actual."
			read -n1 -t1
			Línea
			echo -n "¿Le gustaría abrir el archivo recién generado? [S/N]: "
			read selection

			if [ ${selection} = "S" ]
			then
				xdg-open $2
			else
				clear
			fi
		else
			RBT "El archivo NO ha podido ser creado de forma exitosa."
		fi
	else
		RBT "No se encuentra un dispositivo conectado, por lo que se guardó una lista vacía."
		echo
		RBT "Borrando lista..."
		rm $2
	fi
}
export -f OIE

Repetir() {
	# Esta función ofrece un diálogo que pregunta al usuario si le gustaría volver a realizar una acción.
	# Si el usuario elige volver a realizar la acción, se ejecuta de nuevo la función correspondiente.
	# Para ello, se chequea la posición 1 del arreglo FUNCNAME.
	# En dicho arreglo se almacenan los nombres de las funciones en la pila de ejecución.
	Línea
	echo -n "¿Desea volver a realizar la acción? [S/N]: "
	read selection
	if [ ${selection} = "S" ]
	then
		clear
		${FUNCNAME[1]}
	else
		clear
	fi
}
export -f Repetir