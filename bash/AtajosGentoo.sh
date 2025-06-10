#!/bin/bash

# Defino la parte inicial de los comandos a utilizar.
BEGINNING="gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

KEY_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \
"['$KEY_PATH/custom0/', '$KEY_PATH/custom1/', '$KEY_PATH/custom2/', '$KEY_PATH/custom3/', '$KEY_PATH/custom4/']"

# Defino el primer atajo.
$BEGINNING/custom0/ name "Gestión del Sistema"
$BEGINNING/custom0/ command "gnome-terminal --command="bash /home/lucas/Documentos/GitHub/scripts/Automatización/Gentoo/GenScript/GenScript.sh" --maximize"
$BEGINNING/custom0/ binding "<Control><Alt>Return"

# Defino el segundo atajo.
$BEGINNING/custom1/ name "Configuración"
$BEGINNING/custom1/ command "gnome-control-center"
$BEGINNING/custom1/ binding "<Control><Alt>c"

# Defino el tercer atajo.
$BEGINNING/custom2/ name "Mozilla Firefox"
$BEGINNING/custom2/ command "firefox-bin"
$BEGINNING/custom2/ binding "<Control><Super>f"

# Defino el cuarto atajo.
$BEGINNING/custom3/ name "Gestor de Archivos"
$BEGINNING/custom3/ command "nautilus"
$BEGINNING/custom3/ binding "<Control><Alt>f"

# Defino el quinto atajo.
$BEGINNING/custom4/ name "Terminal"
$BEGINNING/custom4/ command "gnome-terminal"
$BEGINNING/custom4/ binding "<Control><Alt>t"
