#!bin/bash

# Cargo los scripts secundarios requeridos.
. modules/colored_text
. modules/misc
. modules/user_input

# Funciones locales.
news_list() {
	eselect news list
}

news_read() {
	Línea
	ask_news
	Línea

	doas eselect news read $news | less
}

# Menú de selección de opciones.
until [ $selection = "0" ];
do
	clear

	Línea
	echo "En este apartado se puede acceder a las distintas opciones para leer las noticias de Gentoo."
	Línea
	echo "1. Imprimir el listado de noticias."
	echo "2. Leer una noticia específica."
	echo "3. SALIR."
	echo

	read_selection

	case $selection in
		1) clear; news_list; press_enter;;
		2) clear; news_read; press_enter;;
		3) clear; exit;;
		*) clear; incorrect_selection; press_enter;;
	esac
done
