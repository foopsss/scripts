#!/bin/bash

# Desinstalo algunos programas de Silverblue que no me interesan.
flatpak uninstall org.gnome.Weather -y
flatpak uninstall org.gnome.Maps -y
flatpak uninstall org.gnome.Extensions -y
flatpak uninstall org.gnome.Contacts -y
flatpak uninstall org.gnome.clocks -y
flatpak uninstall org.gnome.Characters -y
flatpak uninstall org.gnome.Connections -y
flatpak uninstall org.fedoraproject.MediaWriter -y

# Remuevo algunas aplicaciones de la imagen base.
rpm-ostree override remove firefox firefox-langpacks gnome-tour yelp

# Instalo Flathub.
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --if-not-exists flathub-beta https://flathub.org/beta-repo/flathub-beta.flatpakrepo

# Añado los repositorios externos a utilizar luego.
sudo wget -O /etc/yum.repos.d/copr-jstaf-onedriver.repo https://copr.fedorainfracloud.org/coprs/jstaf/onedriver/repo/fedora-rawhide/jstaf-onedriver-fedora-rawhide.repo
sudo wget -O /etc/yum.repos.d/negativo17-fedora-uld.repo https://negativo17.org/repos/fedora-uld.repo
sudo wget -O /etc/yum.repos.d/copr-SwayNotificationCenter.repo https://copr.fedorainfracloud.org/coprs/erikreider/SwayNotificationCenter/repo/fedora-rawhide/erikreider-SwayNotificationCenter-fedora-rawhide.repo
sudo wget -O /etc/yum.repos.d/copr-adw-gtk3.repo https://copr.fedorainfracloud.org/coprs/nickavem/adw-gtk3/repo/fedora-rawhide/nickavem-adw-gtk3-fedora-rawhide.repo
sudo wget -O /etc/yum.repos.d/copr-shell-color-scripts.repo https://copr.fedorainfracloud.org/coprs/foopsss/shell-color-scripts/repo/fedora-rawhide/foopsss-shell-color-scripts-fedora-rawhide.repo

# Añado las aplicaciones a instalar con rpm-ostree.
rpm-ostree install onedriver adw-gtk3 SwayNotificationCenter sway waybar light wofi grim slurp alacritty

# Instalo las aplicaciones de Flathub.

	# Internet.
	flatpak install flathub org.mozilla.firefox -y
	flatpak install flathub com.brave.Browser -y
	
		# Establezo Wayland como el modo determinado para utilizar Firefox.
		sudo flatpak override --socket=wayland --env=MOZ_ENABLE_WAYLAND=1 org.mozilla.firefox
	
		# Establezco Firefox como el navegador predeterminado.
		xdg-mime default org.mozilla.firefox.desktop x-scheme-handler/https x-scheme-handler/http
		xdg-settings set default-web-browser org.mozilla.firefox.desktop
	
	# Comunicación.
	flatpak install flathub org.mozilla.Thunderbird -y
	flatpak install flathub com.discordapp.Discord -y
	flatpak install flathub com.rtosta.zapzap -y
	
	# Multimedia.
	flatpak install flathub com.github.PintaProject.Pinta -y
	flatpak install flathub org.gimp.GIMP -y
	flatpak install flathub org.videolan.VLC -y
	
	# Oficina.
	flatpak install flathub org.libreoffice.LibreOffice -y
	flatpak install flathub org.onlyoffice.desktopeditors -y
	
	# Programación.
	flatpak install flathub io.github.shiftey.Desktop -y
	flatpak install flathub org.vim.Vim -y
	flatpak install flathub io.neovim.nvim -y
	flatpak install flathub com.vscodium.codium -y
	flatpak install flathub org.gnome.gitlab.somas.Apostrophe -y
	flatpak install flathub org.gnome.Builder -y
	
	# Juegos.
	flatpak install flathub com.valvesoftware.Steam -y
	
	# Extras.
	flatpak install flathub com.github.tchx84.Flatseal -y
	flatpak install flathub ca.desrt.dconf-editor -y
	flatpak install flathub com.mattjakeman.ExtensionManager -y
	flatpak install fedora org.gnome.FileRoller -y
	flatpak install flathub com.transmissionbt.Transmission -y
	
	# Códecs.
	flatpak install org.freedesktop.Platform.ffmpeg-full
	
	# Temas.
	flatpak install org.gtk.Gtk3theme.adw-gtk3 org.gtk.Gtk3theme.adw-gtk3-dark -y
	
# Descargo los archivos de configuración necesarios.

	# Alacritty.
	mkdir $HOME/.config/alacritty
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Alacritty/alacritty.yml -O $HOME/.config/alacritty/alacritty.yml
	
	# Bash.
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Bash/.bashrc -O $HOME/.bashrc
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Bash/.bash_aliases -O $HOME/.bash_aliases
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Bash/.bash_functions -O $HOME/.bash_functions
	
	# Mako.
	# mkdir $HOME/.config/mako
	# wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Mako/config -O $HOME/.config/mako/config
	
	# SwayNotificationCenter.
	mkdir $HOME/.config/swaync
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Swaync/config.json -O $HOME/.config/swaync/config.json
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Swaync/style.css -O $HOME/.config/swaync/style.css
	
	# Sway.
	mkdir $HOME/.config/sway
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Sway/config -O $HOME/.config/sway/config
	
	# Waybar.
	mkdir $HOME/.config/waybar
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Waybar/config -O $HOME/.config/waybar/config
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Waybar/modules -O $HOME/.config/waybar/modules
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Waybar/style.css -O $HOME/.config/waybar/style.css
	
	# Wofi.
	mkdir $HOME/.config/wofi
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Wofi/colors -O $HOME/.config/wofi/colors
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Wofi/config -O $HOME/.config/wofi/config
	wget https://raw.githubusercontent.com/foopsss/Dotfiles/main/Wofi/style.css -O $HOME/.config/wofi/style.css

# Descargo las herramientas de plataforma de Android.
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip -O $HOME/Documentos/platform-tools-latest-linux.zip
unzip -d $HOME/Documentos $HOME/Documentos/platform-tools-latest-linux.zip
rm $HOME/Documentos/platform-tools-latest-linux.zip

	# Exporto la ubicación de las herramientas de plataforma de Android.
	# echo '' >> $HOME/.bashrc
	# echo '# Global platform-tools' >> $HOME/.bashrc
	# echo 'export PATH=${PATH}:$HOME/Documentos/platform-tools' >> $HOME/.bashrc

# Descargo los drivers de HP para la impresora.
wget https://ftp.hp.com/pub/softlib/software13/printers/CLP150/uld-hp_V1.00.39.12_00.15.tar.gz -O $HOME/Descargas/DriversHP.tar.gz
tar -x -f $HOME/Descargas/DriversHP.tar.gz

# Descargo GeoGebra.
# wget download.geogebra.org/package/linux-port6 -O $HOME/Descargas/GeoGebra.zip
# unzip -d $HOME/Descargas $HOME/Descargas/GeoGebra.zip
# mv $HOME/Descargas/GeoGebra-linux-x64 $HOME/Descargas/GeoGebra
# chmod +x $HOME/Descargas/GeoGebra/GeoGebra

# Descargo una versión nueva de las fuentes FontAwesome.
fontver=6.2.1
wget https://use.fontawesome.com/releases/v$fontver/fontawesome-free-$fontver-desktop.zip -O $HOME/Descargas/fontawesome-free-$fontver-desktop.zip
unzip -d $HOME/Descargas $HOME/Descargas/fontawesome-free-$fontver-desktop.zip
mkdir -p $HOME/.local/share/fonts/fontawesome
mv $HOME/Descargas/fontawesome-free-$fontver-desktop/otfs/* $HOME/.local/share/fonts/fontawesome
rm -r $HOME/Descargas/fontawesome-free-$fontver-desktop

# Establezco los atajos de teclado a utilizar luego.
/bin/bash Atajos.sh

# Creo el contenedor para utilizar de ser requerido.
/bin/bash Contenedores.sh
    
# Pregunto al usuario que le gustaría hacer luego de que se instalen las actualizaciones.

	# Limpio la terminal y cambio su tamaño para poder visualizar correctamente el menú a continuación.
	clear && printf '\e[8;8;89t'

	# Imprimo por pantalla el menú.
	until [ "$selection" = "0" ];
	do   
		# Imprimo el menú con las opciones.
		echo "----------------------------------------------------------------------------------------"
		echo "¿Qué le gustaría hacer?"
		echo "----------------------------------------------------------------------------------------"
		echo "1. Apagar el dispositivo."
		echo "2. Reiniciar el dispositivo."
		echo "3. SALIR."
		echo ""
		
		# Creo una entrada para recibir un valor elegido por el usuario.
		echo -n "Escriba el número correspondiente a la operación que desee realizar y presione ENTER: "
		read selection
		echo
		
		# Determino la opción a ejecutar según el número elegido por el usuario.
		case $selection in
		    1) clear; systemctl poweroff;;
		    2) clear; systemctl reboot;;
		    3) clear; exit;;
		esac 
	done
