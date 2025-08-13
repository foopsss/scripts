#!/bin/bash

DIRIN=$HOME/.config
DIROUT=$HOME/Documentos/GitHub/dotfiles
HOMEOUT=home

configs=("alacritty" "sway" "waybar" "wofi" "swaync" "hypr" "powershell")
homeconfigs=(".bashrc" ".bash_custom" ".nanorc")

ConfigCheck() {
    if [ -e $DIRIN/$1 ]
    then
        if [ ! -e $DIROUT/$1 ]
        then
            mkdir -p $DIROUT/$1
        fi
        cp -r $DIRIN/$1/. $DIROUT/$1
    fi
}

HomeCheck() {
    if [ ! -e $DIROUT/$HOMEOUT ]
    then
        mkdir -p $DIROUT/$HOMEOUT
    fi
    cp $HOME/$1 $DIROUT/$HOMEOUT/$1
}

echo -n "Su directorio de entrada es: "
echo $DIRIN
echo -n "Su directorio de salida es: "
echo $DIROUT

for config in ${configs[@]}
do
    ConfigCheck $config
done

for homeconfig in ${homeconfigs[@]}
do
    HomeCheck $homeconfig
done
