#!bin/bash

# Cargo los scripts secundarios requeridos.
bashlibs=$HOME/Documentos/GitHub/scripts/Libraries/Bash

if [ -d $bashlibs ]; then
	. $bashlibs/colored_text
	. $bashlibs/user_input
	. $bashlibs/misc
fi

# Funciones locales.
repo-sync() {
	# Clean the distfiles directory.
	Línea
	doas eclean-dist -d && doas eclean-pkg -d

	# Sync all the repositories.
	# I'll use emaint sync since it's the recommend method.
	# This process is hooked to Portage to update cache after every sync.
	Línea
	doas emaint -a sync

	# Download the source files for all the packages to be upgraded.
	Línea
	doas emerge -vqfuDN --ask=n --with-bdeps=y @world
}

update() {
	Línea
	doas emerge --ask --verbose --quiet --update --deep --newuse --keep-going --read-news=y --exclude=net-libs/webkit-gtk @world

	Línea
	doas eclean-dist -d && doas eclean-pkg -d
}

update-build-deps() {
	Línea
	doas emerge --ask --verbose --quiet --update --deep --newuse --keep-going --with-bdeps=y --read-news=y --exclude=net-libs/webkit-gtk @world

	Línea
	doas eclean-dist -d && doas eclean-pkg -d
}

buildpackage() {
	Línea
	echo "¿Qué paquete le gustaría actualizar?"
	echo "1. webkit-gtk"
	echo "2. gcc"
	Línea

	read_selection
	Línea

	case $selection in
		1) doas emerge --ask --verbose --quiet --getbinpkg --buildpkg net-libs/webkit-gtk; doas eclean-dist -d && doas eclean-pkg -d;;
		2) doas emerge --ask --verbose --quiet --buildpkg sys-devel/gcc; doas eclean-dist -d && doas eclean-pkg -d;;
		*) clear; incorrect_selection; press_enter;;
	esac
}

flatpak-update() {
	# Remove unnecessary Flatpak runtimes.
	Línea
	flatpak uninstall --unused -y

	# Update Flatpak apps.
	Línea
	flatpak update -y
}

firmware-update() {
	Línea
	fwupdmgr refresh --force
	fwupdmgr get-updates
	fwupdmgr update
}

pretend-update() {
	emerge --verbose --pretend --update --deep --newuse --read-news=y @world
}

# Menú de selección de opciones.
until [ $selection = "0" ];
do
	clear

	Línea
	echo "En este apartado se pueden acceder a las distintas opciones para actualizar el sistema."
	Línea
	echo
	echo "REPOSITORIOS"
	YT "------------"
	echo "1. Sincronizar los repositorios."
	echo
	echo "PAQUETES/SISTEMA"
	YT "----------------"
	echo "2. Actualizar el sistema."
	echo "3. Actualizar el sistema considerando las dependencias de compilación (--with-bdeps)."
	echo "4. Actualizar paquetes grandes."
	echo "5. Actualizar aplicaciones de Flatpak."
	echo "6. Actualizar el firmware del dispositivo."
	echo
	echo "MISCELÁNEA"
	YT "----------"
	echo "7. Pretender que se va a realizar una actualización."
	echo "8. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; repo-sync; press_enter;;
		2) clear; shutdown_system update;;
		3) clear; shutdown_system update-build-deps;;
		4) clear; shutdown_system buildpackage;;
		5) clear; shutdown_system flatpak-update;;
		6) clear; shutdown_system firmware-update;;
		7) clear; pretend-update; press_enter;;
		8) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
