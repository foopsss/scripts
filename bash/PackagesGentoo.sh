#!bin/bash

# Cargo los scripts secundarios requeridos.
. modules/colored_text
. modules/misc
. modules/user_input

# Funciones locales.
add_overlay() {
	Línea
	ask_repository
	Línea

	doas eselect repository enable $repository
}

remove_overlay() {
	Línea
	ask_repository
	Línea

	doas eselect repository remove $repository
}

install_package() {
	Línea
	ask_package
	Línea

	doas emerge -avq $package
}

add_world() {
	Línea
	ask_package
	Línea

	doas emerge --noreplace $package
}

remove_world() {
	Línea
	ask_package
	Línea

	doas emerge --deselect $package
}

clean_dependencies() {
	doas emerge --ask --depclean
}

list_dependencies() {
	Línea
	ask_package
	Línea

	equery depends $package
}

list_package() {
	Línea
	ask_package
	Línea

	qlist -IRv | grep "$package"
}

search_package() {
	Línea
	ask_package
	Línea

	equery list -Ipo $package
}

which_package_command() {
	Línea
	ask_command
	Línea

	equery b $command
}

which_package_file() {
	Línea
	ask_file
	Línea

	equery belongs $file
}

emacs_rebuild() {
	Línea
	BBT "Recompilando paquetes de Emacs..."
	Línea

	emacs-updater
}

go_rebuild() {
	Línea
	BBT "Recompilando paquetes de Go..."
	Línea

	doas emerge -avq @golang-rebuild
}

perl_rebuild() {
	Línea
	BBT "Limpiando y recompilando paquetes de Perl..."
	Línea
	
	doas perl-cleaner --all
}

preserved_rebuild() {
	Línea
	BBT "Recompilando paquetes compilados con librerías viejas..."
	Línea
	
	doas emerge @preserved-rebuild
}

install_flatpak() {
	Línea
	ask_package
	Línea

	flatpak install $package
}

remove_flatpak() {
	Línea
	ask_package
	Línea

	flatpak remove $package
}

remove_flatpak_runtimes() {
	flatpak uninstall --unused -y
}

# Defino el menú de selección de opciones.
until [ "$selection" = "0" ];
do
	clear

	Línea
	echo "En este apartado se puede acceder a las distintas opciones para manejar los paquetes y repositorios del"
	echo "sistema."
	Línea
	echo
	echo "REPOSITORIOS"
	YT "------------"
	echo "1. Añadir un repositorio externo."
	echo "2. Remover un repositorio externo."
	echo
	echo "PAQUETES"
	YT "--------"
	echo "3. Instalar un paquete."
	echo "4. Añadir un paquete a @world."
	echo "5. Remover un paquete de @world."
	echo "6. Remover paquetes sin uso."
	echo "7. Listar paquetes que dependen de un paquete determinado."
	echo "8. Buscar un paquete en la lista de paquetes instalados."
	echo "9. Buscar un paquete en los repositorios disponibles."
	echo "10. Buscar el paquete que provee un comando específico."
	echo "11. Buscar el paquete que provee un archivo específico."
	echo
	echo "RECONSTRUCCIÓN DE PAQUETES POR ACTUALIZACIÓN"
	YT "--------------------------------------------"
	echo "12. Reconstruir paquetes de Emacs."
	echo "13. Reconstruir paquetes de Go."
	echo "14. Reconstruir paquetes de Perl y remover los innecesarios."
	echo "15. Reconstruir paquetes compilados con librerías viejas."
	echo
	echo "FLATPAK"
	YT "-------"
	echo "16. Instalar aplicaciones de Flatpak."
	echo "17. Remover aplicaciones de Flatpak."
	echo "18. Remover dependencias sin uso."
	echo
	echo "MISCELÁNEA"
	YT "----------"
	echo "19. SALIR"
	echo

	read_selection

	case $selection in
		1) clear; add_overlay; press_enter;;
		2) clear; remove_overlay; press_enter;;
		3) clear; shutdown_system install_package; press_enter;;
		4) clear; add_world; press_enter;;
		5) clear; remove_world; press_enter;;
		6) clear; clean_dependencies; press_enter;;
		7) clear; list_dependencies; press_enter;;
		8) clear; list_package; press_enter;;
		9) clear; search_package; press_enter;;
		10) clear; which_package_command; press_enter;;
		11) clear; which_package_file; press_enter;;
		12) clear; shutdown_system emacs_rebuild;;
		13) clear; shutdown_system go_rebuild;;
		14) clear; shutdown_system perl_rebuild;;
		15) clear; shutdown_system preserved_rebuild;;
		16) clear; install_flatpak; press_enter;;
		17) clear; remove_flatpak; press_enter;;
		18) clear; remove_flatpak_runtimes; press_enter;;
		19) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
