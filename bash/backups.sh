#!/bin/bash

# Cargo los scripts secundarios requeridos.
. colored_text
. misc

Línea
echo "DOTCOPY"
YT "-------"
bash dotcopy.sh
Línea
echo "EBCOPY"
YT "------"
bash ebcopy.sh
Línea
echo "GENCOPY"
YT "-------"
bash gencopy.sh
# Línea
# echo "NATGENCOPY"
# YT "----------"
# bash natgencopy.sh
# Línea
