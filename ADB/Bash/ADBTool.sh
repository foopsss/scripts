#!/bin/bash
# NOTA: las funciones utilizadas aquí están explicadas en Functions.sh.

# Importo las funciones a utilizar de otro archivo.
source Functions.sh

# Defino las propiedades de la ventana.
resize_window

# Defino las opciones a utilizar.
menu_option_one() {
	clear
	Línea
	adb devices
	Repetir
}

menu_option_two() {
	clear
	Línea
	GBT "¡Reiniciando!"
	adb reboot
	Repetir
}

menu_option_three() {
	clear
	Línea
	GBT "¡Reiniciando!"
	adb reboot recovery
	Repetir
}

menu_option_four() {
	clear
	Línea
	GBT "¡Reiniciando!"
	adb reboot bootloader
	Repetir
}

menu_option_five() {
	bash Files.sh
}

menu_option_six() {
	clear
	Línea
	fastboot devices
	Repetir
}

menu_option_seven() {
	clear
	Línea
	fastboot reboot
	Repetir
}

menu_option_eight() {
	clear
	Línea
	fastboot reboot recovery
	Repetir
}

menu_option_nine() {
	bash Format.sh
}

menu_option_ten() {
	bash Fastboot.sh
}

menu_option_eleven() {
	bash Extra.sh
}

menu_option_twelve() {
	adb kill-server
	clear
	exit
}

# Defino el menú de selección de opciones.
until [ $selection = "0" ];
do
	clear
	adbcheck

	Línea
	echo "Bienvenido a mi herramienta para usar ADB y Fastboot."
	echo "Espero que encuentres esta herramienta de utilidad y te haga el uso de ADB más fácil."
	echo
	BBT "No te olvides que para poder usar estos comandos es necesario tener la 'Depuración USB' encendida."
	BBT "Asimismo, algunos también pueden requerir que la opción 'Desbloqueo OEM' esté activada."
	Línea
	echo "Bienvenido $(whoami), hoy es $(date)."
	Línea
	echo "ADB"
	YT "---"
	echo "1. Comprobar si el ordenador reconoce el dispositivo.    (adb devices)"
	echo "2. Reiniciar el dispositivo.                             (adb reboot)"
	echo "3. Reiniciar el dispositivo en modo Recovery.            (adb reboot recovery)"
	echo "4. Reiniciar el dispositivo en modo Fastboot/Descarga.   (adb reboot bootloader)"
	echo "5. Realizar operaciones con archivos."
	echo
	echo "FASTBOOT"
	YT "--------"
	echo "6. Comprobar si el ordenador reconoce el dispositivo.    (fastboot devices)"
	echo "7. Reiniciar el dispositivo.                             (fastboot reboot)"
	echo "8. Reiniciar el dispositivo en modo Recovery.            (fastboot reboot recovery)"
	echo "9. Formatear particiones del dispositivo.                (fastboot format)"
	echo "10. Realizar operaciones adicionales con Fastboot."
	echo
	echo "MISCELÁNEA"
	YT "----------"
	echo "11. Elegir más opciones."
	echo "12. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; menu_option_one;;
		2) clear; menu_option_two;;
		3) clear; menu_option_three;;
		4) clear; menu_option_four;;
		5) clear; menu_option_five;;
		6) clear; menu_option_six;;
		7) clear; menu_option_seven;;
		8) clear; menu_option_eight;;
		9) clear; menu_option_nine;;
		10) clear; menu_option_ten;;
		11) clear; menu_option_eleven;;
		12) menu_option_twelve;;
		*) clear; incorrect_selection; press_enter;;
	esac
done