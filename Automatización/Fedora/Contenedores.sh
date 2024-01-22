#!/bin/bash

# Lucas.
toolbox create lucas
sudo dnf copr enable nickavem/adw-gtk3 -y
toolbox run -c lucas sudo dnf update -y
toolbox run -c lucas sudo dnf install adw-gtk3 gnome-tweaks ImageMagick htop -y

# RPM.
toolbox create rpm
toolbox run -c rpm sudo dnf update -y
toolbox run -c rpm sudo dnf install rpmdevtools rpmlint make -y
toolbox run -c rpm rpmdev-setuptree

# Shellbox.
toolbox create shellbox
toolbox run -c shellbox sudo dnf update -y
toolbox run -c shellbox sudo dnf install ShellCheck shfmt -y

# Rustbox.
toolbox create rustbox
toolbox run -c rustbox sudo dnf update -y
toolbox run -c rustbox sudo dnf install rust cargo rustfmt -y

# Cbox.
toolbox create cbox
toolbox run -c cbox sudo dnf update -y
toolbox run -c cbox sudo dnf install gcc mingw32-gcc mingw64-gcc -y
