#!/bin/bash

# Defino la parte inicial de los comandos a utilizar.
BEGINNING="gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

KEY_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"

gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \
"['$KEY_PATH/custom0/', '$KEY_PATH/custom1/', '$KEY_PATH/custom2/', '$KEY_PATH/custom3/', '$KEY_PATH/custom4/', '$KEY_PATH/custom5/']"

# Defino el primer atajo.
$BEGINNING/custom0/ name "Actualizaciones de Software"
$BEGINNING/custom0/ command "/var/home/lucas/Documentos/GitHub/Scripts/Automatización/Actualizaciones.sh"
$BEGINNING/custom0/ binding "<Control><Alt>Return"

# Defino el segundo atajo.
$BEGINNING/custom1/ name "Configuración"
$BEGINNING/custom1/ command "gnome-control-center"
$BEGINNING/custom1/ binding "<Control><Alt>c"

# Defino el tercer atajo.
$BEGINNING/custom2/ name "Mozilla Firefox"
$BEGINNING/custom2/ command "flatpak run --socket=wayland --env=MOZ_ENABLE_WAYLAND=1 org.mozilla.firefox"
$BEGINNING/custom2/ binding "<Control><Super>f"

# Defino el cuarto atajo.
$BEGINNING/custom3/ name "Gestor de Archivos"
$BEGINNING/custom3/ command "nautilus"
$BEGINNING/custom3/ binding "<Control><Alt>f"

# Defino el quinto atajo.
$BEGINNING/custom4/ name "Software"
$BEGINNING/custom4/ command "gnome-software"
$BEGINNING/custom4/ binding "<Control><Alt>s"

# Defino el sexto atajo.
$BEGINNING/custom5/ name "Terminal"
$BEGINNING/custom5/ command "gnome-terminal"
$BEGINNING/custom5/ binding "<Control><Alt>t"
