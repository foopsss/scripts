#!/bin/bash

# Defino la parte inicial de los comandos a utilizar.
BEGINNING="gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

KEY_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \
"['$KEY_PATH/custom0/', '$KEY_PATH/custom1/', '$KEY_PATH/custom2/']"

# Defino el primer atajo.
$BEGINNING/custom0/ name "Gestión del Sistema"
$BEGINNING/custom0/ command "gnome-terminal --command='python /home/lucas/Documentos/GitHub/scripts/python/genscript.py' --maximize"
$BEGINNING/custom0/ binding "<Control><Alt>Return"

# Defino el segundo atajo.
$BEGINNING/custom1/ name "Gestor de Archivos"
$BEGINNING/custom1/ command "nautilus"
$BEGINNING/custom1/ binding "<Control><Alt>f"

# Defino el tercer atajo.
$BEGINNING/custom2/ name "Terminal"
$BEGINNING/custom2/ command "gnome-terminal"
$BEGINNING/custom2/ binding "<Control><Alt>t"