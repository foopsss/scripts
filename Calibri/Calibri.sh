# Declaro el intérprete a utilizar.
#!/bin/bash

# Defino una variable para almacenar una ruta.
ruta=~/.local/share/fonts/calibri/

# Defino las funciones a utilizar.
GBT() {
# GBT es el acrónimo para Green Bold Text.
# Esta función imprime texto blanco, sobre un fondo verde y en negritas.
    echo -e "\e[1;42m$1\e[0m"
}
export -f GBT

RBT() {
# RBT es el acrónimo para Red Bold Text.
# Esta función imprime texto blanco, sobre un fondo rojo y en negritas.
    echo -e "\e[1;41m$1\e[0m"
}
export -f RBT

# Aquí comienza la operación.
echo "Instalando fuentes..."

# Creo la carpeta y copio los contenidos.
mkdir -p $ruta
{
    find "$(pwd)"/ ! -name Calibri.sh -exec cp -t $ruta {} +
} 2>/dev/null

# Me aseguro de que el proceso haya finalizado exitosamente.
cd $ruta
count=$(ls | wc -l)

if [ ${count} -eq 6 ]
then
 GBT "¡Hecho! Fuentes instaladas en '$ruta'."
else
 RBT "¡Error! Las fuentes no se instalaron correctamente. Por favor intente de nuevo."
fi

# Refresco la cache de las fuentes.
fc-cache -v > /dev/null