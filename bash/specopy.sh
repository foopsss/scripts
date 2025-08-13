#!/bin/bash

DIRSPEC=~/rpmbuild/SPECS
DIRSRC=~/rpmbuild/SOURCES
DIROUT=$HOME/Documentos/GitHub/specfiles

for file in $DIRSPEC/*.spec ; do
	filext=${file##*/}
	filewoext=${filext%.*}
	
	if [ ! -e "$DIROUT/$filewoext" ]
	then
		mkdir "$DIROUT/$filewoext"
	fi
	cp -r "$DIRSPEC"/$filext "$DIROUT/$filewoext"
done

# This will work for patch files as long as there's only a single patch file per spec file.
# It works because I name every patch file as my spec files.
for file in $DIRSRC/*.patch ; do
	filext=${file##*/}
	filewoext=${filext%.*}
	
	if [ ! -e "$DIROUT/$filewoext" ]
	then
		mkdir "$DIROUT/$filewoext"
	fi
	cp -r "$DIRSRC"/$filext "$DIROUT/$filewoext"
done
