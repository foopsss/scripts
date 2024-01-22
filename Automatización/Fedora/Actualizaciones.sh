#!/bin/bash

# Busco el archivo de funciones del sistema. 
if [ -f ~/.bash_functions ]; then
	. ~/.bash_functions
fi

comandos () {
	YT "--------------------------------------------------------------------------------"
	echo "                          Actualizador de programas                          "
	BT "                          -------------------------                          "
	YT "--------------------------------------------------------------------------------"

	GBT "Cancelando cualquier posible transacción en curso."
	rpm-ostree cancel
	echo

	GBT "Actualizando la imagen de la distribución."
	rpm-ostree update
	echo

	GBT "Actualizando el firmware del dispositivo."
	fwupdmgr refresh --force
	fwupdmgr get-updates
	fwupdmgr update
	echo

	GBT "Actualizando las aplicaciones de Flatpak."
	flatpak update -y
	echo

	GBT "Actualizando los paquetes de los contenedores."
	toolbox run -c lucas sudo dnf update -y
	toolbox run -c rpm sudo dnf update -y
	toolbox run -c shellbox sudo dnf update -y
	toolbox run -c rustbox sudo dnf update -y
	toolbox run -c cbox sudo dnf update -y
	read -n1

	clear

	# Cambio el tamaño de la terminal para poder visualizar correctamente el menú a continuación.
	printf '\e[8;8;89t'

	until [ "$selection" = "0" ];
	do   
		YT "----------------------------------------------------------------------------------------"
		echo "¿Qué le gustaría hacer?"
		YT "----------------------------------------------------------------------------------------"
		echo "1. Apagar el dispositivo."
		echo "2. Reiniciar el dispositivo."
		echo "3. SALIR."
		echo ""

		echo -n "Escriba el número correspondiente a la operación que desee realizar y presione ENTER: "
		read selection
		echo

		case $selection in
		    1) clear; systemctl poweroff;;
		    2) clear; systemctl reboot;;
		    3) clear; exit;;
		esac 
	done

	# Mantengo la terminal abierta luego de ejecutar los comandos necesarios.
	# $SHELL
}

# Hago que los comandos sean universalmente utilizables.
export -f comandos

# Comando para ejecutar la función luego de abrir una ventana de la terminal.
gnome-terminal -e "bash -c 'comandos'"
