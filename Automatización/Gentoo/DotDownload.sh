#!/bin/bash

config=$HOME/.config

# Bash dotfiles.
wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/bash/.bashrc -O $HOME/.bashrc
wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/bash/.bash_aliases -O $HOME/.bash_aliases
wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/bash/.bash_functions -O $HOME/.bash_functions

# .config dotfiles.

	# Alacritty.
	mkdir $config/alacritty
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/alacritty/alacritty.yml -O $config/alacritty/alacritty.yml

	# GTK.
	mkdir $config/gtk-3.0
	mkdir $config/gtk-4.0
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/gtk-3.0/gtk.css -O $config/gtk-3.0/gtk.css
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/gtk-4.0/gtk.css -O $config/gtk-4.0/gtk.css

	# Hyprland.
	mkdir $config/hypr
	mkdir $config/hypr/hyprscripts
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/hypr/hyprland.conf -O $config/hypr/hyprland.conf
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/hypr/hypr-autostart.conf -O $config/hypr/hypr-autostart.conf
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/hypr/hypr-colors.conf -O $config/hypr/hypr-colors.conf
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/hypr/hypr-keybindings.conf -O $config/hypr/hypr-keybindings.conf
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/hypr/hyprscripts/powermenu -O $config/hypr/hyprscripts/powermenu

	# Sway.
	mkdir $config/sway
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/sway/config -O $config/sway/config

	# SwayNC.
	mkdir $config/swaync
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/swaync/config.json -O $config/swaync/config.json
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/swaync/style.css -O $config/swaync/style.css

	# Waybar.
	mkdir $config/waybar
	mkdir $config/waybar/hyprland
	mkdir $config/waybar/sway
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/waybar/modules -O $config/waybar/modules
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/waybar/hyprland/config -O $config/waybar/hyprland/config
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/waybar/sway/config -O $config/waybar/sway/config
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/waybar/style.css -O $config/waybar/style.css

	# Wofi.
	mkdir $config/wofi
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/wofi/colors -O $config/wofi/colors
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/wofi/config -O $config/wofi/config
	wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/wofi/style.css -O $config/wofi/style.css
