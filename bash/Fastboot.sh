#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	Línea
	echo "En esta sección, usted podrá instalar una imagen a una partición específica de su dispositivo. Para"
	echo "ello, primero especifique la ubicación de la ROM cuyas imágenes quiere instalar. Luego, especifique"
	echo "la partición y la imagen a instalar."
	echo
	echo "Una lista de particiones se puede ver aquí: "
	BBT "https://source.android.com/docs/core/architecture/bootloader/partitions"
	echo
	echo "Ejemplo: 'fastboot flash boot boot.img' o 'fastboot flash boot /home/usuario/Documentos/boot.img'"
	Línea

	echo -n "Introduzca la ubicación donde se encuentran los archivos de su ROM: "
	read ubicacion
	echo

	if [ -z "$ubicacion" ]
	then
		RBT "NO se indicó una ubicación."
		Repetir
	else
		if [ "$ubicacion" != "$PWD" ]
		then
			cd $ubicacion
			echo "La ubicación indicada es: "
			YBT "${ubicacion}"
		else
			BBT "La ubicación que especificó es la ubicación actual."
			echo "Procediendo al siguiente paso..."
		fi

		menu_option_one_part2
	fi
}

	menu_option_one_part2() {
		Línea

		echo -n "Introduzca la partición en la que quiere instalar la imagen: "
		read fbootcom
		echo -n "Introduzca la imagen a instalar: "
		read fbootcom1
		echo

		# Chequeo que ambas variables utilizadas contengan un valor.
		if [ -n "$fbootcom" ] && [ -n "$fbootcom1" ]
		then
			# Si ambas variables reciben un valor ejecuto la acción.
			fastboot flash $fbootcom $fbootcom1
		else
			# Si ambas o alguna de las variables no reciben un valor informo al usuario y aborto la acción.
			RBT "Una o ambas opciones NO fueron especificadas."
			Repetir
		fi
	}

menu_option_two() {
	Línea
	echo "En esta sección, usted podrá iniciar o 'bootear' su dispositivo con una imagen determinada utilizando"
	echo "el modo Fastboot. Por ejemplo, puede iniciar temporalmente su dispositivo en un modo Recovery"
	echo "personalizado utilizando este apartado."
	echo
	echo "Para ello, debe introducir la ubicación y el nombre de la imagen que quiere iniciar en su dispositivo."
	echo "Ejemplo: 'fastboot boot twrp.img' o 'fastboot boot /home/usuario/Documentos/twrp.img'."
	Línea

	echo -n "Introduzca la ubicación de la imagen a iniciar: "
	read fbootcom
	echo

	if [ -z "$fbootcom" ]
	then
		NV "$fbootcom"
	else
		fastboot boot $fbootcom
	fi

	Repetir
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do
	clear
	Línea
	echo "En este apartado, usted podrá optar por realizar una serie de operaciones adicionales"
	echo "con el modo Fastboot."
	Línea
	echo "1. Instalar una imagen en una partición.              (fastboot flash)"
	echo "2. Iniciar el dispositivo con una imagen determinada. (fastboot boot)"
	echo "3. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; menu_option_one;;
		2) clear; menu_option_two;;
		3) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done