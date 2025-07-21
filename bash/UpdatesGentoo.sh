#!bin/bash

# Cargo los scripts secundarios requeridos.
. modules/colored_text
. modules/misc
. modules/user_input

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

update-exclude() {
	exclude_pkg="llvm-core/llvm net-libs/webkit-gtk"
	
	Línea
	doas emerge --verbose --update --deep --newuse --exclude="$exclude_pkg" @world

	Línea
	doas eclean-dist -d && doas eclean-pkg -d
}

update-binpkg() {
	Línea
	doas emerge --verbose --update --deep --changed-use --getbinpkg @world

	Línea
	doas eclean-dist -d && doas eclean-pkg -d
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
	echo "2. Actualizar el sistema (ignorar paquetes grandes)."
	echo "3. Actualizar paquetes pesados (binarios de Gentoo)."
	echo "4. Actualizar aplicaciones de Flatpak."
	echo "5. Actualizar el firmware del dispositivo."
	echo
	echo "MISCELÁNEA"
	YT "----------"
	echo "6. Pretender que se va a realizar una actualización."
	echo "7. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; repo-sync; press_enter;;
		2) clear; shutdown_system update-exclude;;
		3) clear; shutdown_system update-binpkg;;
		4) clear; shutdown_system flatpak-update;;
		5) clear; shutdown_system firmware-update;;
		6) clear; pretend-update; press_enter;;
		7) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
