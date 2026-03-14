#!/bin/bash

config=$HOME/.config

# $HOME dotfiles.
wget https://raw.githubusercontent.com/foopsss/configs/main/home/lucas/.bashrc -O $HOME/.bashrc
wget https://raw.githubusercontent.com/foopsss/configs/main/home/lucas/.bash_custom -O $HOME/.bash_custom
wget https://raw.githubusercontent.com/foopsss/configs/main/home/lucas/.nanorc -O $HOME/.nanorc

# PowerShell.
mkdir $config/powershell
wget https://raw.githubusercontent.com/foopsss/configs/main/home/lucas/.config/powershell/profile.ps1 -O $config/powershell/profile.ps1
