#!bin/bash

# Packages used here:
# app-eselect/eselect-repository - provides "eselect repository enable".
# app-portage/gentoolkit - provides "equery", "euse" and "eclean".
# app-admin/eclean-kernel - provides "eclean-kernel".
# app-portage/portage-utils - provides "qlist".
# app-portage/eix - provides "eix".
# app-portage/genlop - provides "genlop".
# sys-apps/flatpak - provides "flatpak".

# More information on:
# https://wiki.gentoo.org/wiki/Useful_Portage_tools
# https://wiki.gentoo.org/wiki/Gentoo_Cheat_Sheet
# https://wiki.gentoo.org/wiki/Eselect/Repository
# https://wiki.gentoo.org/wiki/Gentoolkit
	# https://wiki.gentoo.org/wiki/Equery
	# https://wiki.gentoo.org/wiki/Euse
	# https://wiki.gentoo.org/wiki/Eclean
# https://wiki.gentoo.org/wiki/Eix
# https://wiki.gentoo.org/wiki/Genlop
# https://wiki.gentoo.org/wiki/Flatpak

cd $HOME/Documentos/GitHub/scripts/bash

# Cargo los scripts secundarios requeridos.
. colored_text
. misc
. user_input

# Funciones locales.
updates() {
	bash UpdatesGentoo.sh
}

packages() {
	bash PackagesGentoo.sh
}

clean() {
	doas eclean-dist -d && doas eclean-pkg -d
}

genscript_clean_kernel() {
	Línea
	ask_version
	Línea

	cd /boot
	doas rm initramfs-$version-gentoo-dist.img kernel-$version-gentoo-dist
	doas rm -r /lib/modules/$version-gentoo-dist

	doas grub-mkconfig -o /boot/grub/grub.cfg
	doas dracut --force
}

clean-kernel() {
	Línea
	echo "¿Qué solución desea utilizar?"
	echo "-----------------------------"
	echo "1. Solución de GenScript"
	echo "2. eclean-kernel"
	Línea

	read_selection

	case $selection in
		1) clear; genscript_clean_kernel;;
		2) clear; doas eclean-kernel;;
		*) clear; incorrect_selection; press_enter;;
	esac
}

clean-thumbnail() {
	thumbdir=$HOME/.cache/thumbnails

	if [ -d $thumbdir ]
	then
		Línea
		rm -r $thumbdir

		if [ ! -d $thumbdir ]
		then
			GBT "¡Carpeta borrada exitosamente!"
		else
			RBT "Hubo un problema al borrar la carpeta de las miniaturas."
			RBT "Intente correr el programa de nuevo o remueva la carpeta manualmente."
		fi
	else
		Línea
		BBT "La carpeta no existe. No se borró ningún elemento."
	fi

	Línea
}

install-grub() {
	Línea
	doas grub-install --target=x86_64-efi --efi-directory=/boot --removable
	Línea
	doas grub-mkconfig -o /boot/grub/grub.cfg
	Línea
}

use() {
	bash EuseGentoo.sh
}

genlop() {
	bash GenlopGentoo.sh
}

diff-files() {
	doas dispatch-conf
}

news() {
	bash NewsGentoo.sh
}

# Defino el menú de selección de opciones.
until [ "$selection" = "0" ];
do
	clear

	Línea
	echo "¡Bienvenido a la herramienta de Gentoo de Lucas!"
	echo "Con esta herramienta se pueden llevar a cabo varias opciones de mantenimiento del sistema."
	Línea
	echo "Bienvenido $(whoami), hoy es $(date)."
	Línea
	echo
	echo "ACTUALIZACIONES"
	YT "---------------"
	echo "1. Consultar el menú de opciones de actualización."
	echo
	echo "PAQUETES Y REPOSITORIOS"
	YT "-----------------------"
	echo "2. Consultar el menú de manejo de paquetes y repositorios del sistema."
	echo
	echo "LIMPIEZA"
	YT "--------"
	echo "3. Limpieza de archivos residuales."
	echo "4. Limpieza de versiones antiguas del kernel."
	echo "5. Limpieza de miniaturas de Nautilus."
	echo
	echo "MISCELÁNEA"
	YT "----------"
	echo "6. Instalar GRUB."
	echo "7. Obtener información sobre parámetros USE."
	echo "8. Consultar los tiempos de instalación de los paquetes."
	echo "9. Resolución de conflictos por diferencia de archivos."
	echo "10. Lectura del boletín de noticias de Gentoo."
	echo "11. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; updates;;
		2) clear; packages;;
		3) clear; clean; press_enter;;
		4) clear; clean-kernel; press_enter;;
		5) clear; clean-thumbnail; press_enter;;
		6) clear; install-grub; press_enter;;
		7) clear; use;;
		8) clear; genlop;;
		9) clear; diff-files; press_enter;;
		10) clear; news;;
		11) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
