#!/bin/bash

GRUBIN=/boot/grub/themes
PLYMOUTHIN=/usr/share/plymouth/themes
GITOUT=$HOME/Documentos/GitHub/natural-gentoo-remastered

echo "Sus directorios de entrada son: "
echo $GRUBIN
echo $PLYMOUTHIN
echo -n "Su directorio de salida es: "
echo $GITOUT

cp -r $GRUBIN/natural-gentoo-remastered/. $GITOUT/natural-gentoo-remastered-grub
cp -r $PLYMOUTHIN/natural-gentoo-remastered/. $GITOUT/natural-gentoo-remastered-plymouth
