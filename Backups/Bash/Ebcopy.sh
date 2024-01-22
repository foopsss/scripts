#!bin/bash

DIRIN=/var/db/repos/foopsss-gentoo-overlay
DIROUT=$HOME/Documentos/GitHub/gentoo-overlay

echo -n "Su directorio de entrada es: "
echo $DIRIN
echo -n "Su directorio de salida es: "
echo $DIROUT

cp -a $DIRIN/. $DIROUT/
