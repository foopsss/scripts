#!/bin/bash

config=$HOME/.config

# $HOME dotfiles.
wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/home/.bashrc -O $HOME/.bashrc
wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/home/.bash_custom -O $HOME/.bash_custom
wget https://raw.githubusercontent.com/foopsss/dotfiles/gentoo/home/.nanorc -O $HOME/.nanorc

# PowerShell.
mkdir $config/powershell
wget https://raw.githubusercontent.com/foopsss/dotfiles/refs/heads/gentoo/powershell/profile.ps1 -O $config/powershell/profile.ps1