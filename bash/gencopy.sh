#!/bin/bash

DIRIN=/etc/portage
PORTAGEOUT=$HOME/Documentos/GitHub/gentoo-configs/etc/portage
DIRENV=$HOME/Documentos/GitHub/gentoo-configs/etc
DIRVAR=$HOME/Documentos/GitHub/gentoo-configs/var/lib/portage

folders=("binrepos.conf" "env" "package.accept_keywords" "package.mask" "package.use" "savedconfig")
files=("make.conf" "world")

create_folders() {
	if [ ! -e $PORTAGEOUT  ]
	then
		mkdir -p $PORTAGEOUT
	fi
	
	if [ ! -e $DIRVAR  ]
	then
		mkdir -p $DIRVAR
	fi
}

echo -n "Su directorio de entrada es: "
echo $DIRIN
echo "Sus directorios de salida son: "
echo $PORTAGEOUT
echo $DIRENV
echo $DIRVAR

create_folders

for folder in ${folders[@]}
do
	cp -r $DIRIN/$folder/. $PORTAGEOUT/$folder
done

for file in ${files[@]}
do
	case $file in
		world) cp /var/lib/portage/world $DIRVAR/world;;
		*) cp $DIRIN/$file $PORTAGEOUT/$file;;
	esac
done
