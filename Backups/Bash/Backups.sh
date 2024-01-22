#!/bin/bash

bashlibs=$HOME/Documentos/GitHub/scripts/Libraries/Bash

if [ -d $bashlibs ]; then
	. $bashlibs/colored_text
	. $bashlibs/misc
fi

Línea
echo "DOTCOPY"
YT "-------"
bash Dotcopy.sh
Línea
echo "EBCOPY"
YT "------"
bash Ebcopy.sh
Línea
echo "GENCOPY"
YT "-------"
bash Gencopy.sh
Línea
echo "NATGENCOPY"
YT "----------"
bash Natgencopy.sh
Línea
