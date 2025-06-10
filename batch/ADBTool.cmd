REM Turn off echo-ing

@ECHO OFF

REM Defino propiedades de la ventana

TITLE Herramienta de ADB y Fastboot
COLOR 17
MODE 105,38

REM Defino una propiedad para evitar una vulnerabilidad con el comando SET

SETLOCAL EnableDelayedExpansion

REM Inicializo las variables a usar en todo el script

SET ADBDISPONIBLE=
SET DESCARGA=
SET CHOICE=
SET RUTA1=
SET RUTA2=
SET RUTA3=
SET RUTA4=
SET RUTA5=
SET ID=
SET CLAVE=
SET COMANDOPERS=

SET ARCHIVO1=!USERPROFILE!\Desktop\Apps.txt
SET ARCHIVO2=!USERPROFILE!\Desktop\AppsDes.txt
SET ARCHIVO3=!USERPROFILE!\Desktop\AppsClave.txt

REM Defino la primer ventana del script, que permite establecer si ADB esta descargado

:: Chequear si ADB esta disponible, y de lo contrario llevar a descargar
adb.exe /? >NUL 2>&1
IF ERRORLEVEL 1 (
    SET ADBDISPONIBLE=No
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO Este script requiere que esten instalados en el sistema los binarios de ADB y Fastboot.
    SET /P DESCARGA="Desea instalarlos ahora? [S/N] "
)

:: Si se confirma la eleccion, iniciar la descarga
IF /I "!DESCARGA!"=="S" (
    START https://dl.google.com/android/repository/platform-tools-latest-windows.zip
    ECHO.
    ECHO Descargue el archivo y descomprimalo. Luego, incluya la carpeta resultante en su variable PATH o, copie
    ECHO el script a su carpeta "platform-tools" e inicielo desde ahi.
    ECHO -------------------------------------------------------------------------------------------------------
    PAUSE
)

:: Abortar la operacion si los binarios no estan instalados
IF "!ADBDISPONIBLE!"=="No" GOTO:EOF

REM Defino el menu de opciones a utilizar

:MENU
CLS

ECHO.
ECHO -------------------------------------------------------------------------------------------------------
ECHO Bienvenido a mi herramienta para usar ADB y Fastboot.
ECHO Espero que encuentres esta herramienta de utilidad y te haga el uso de ADB mas facil.
ECHO -------------------------------------------------------------------------------------------------------
ECHO Fecha:
date /t
ECHO Hora:
time /t
ECHO -------------------------------------------------------------------------------------------------------
ECHO.
ECHO ADB
ECHO ---
ECHO.
ECHO 1. Comprobar si el ordenador reconoce el dispositivo.    (adb devices)
ECHO 2. Reiniciar el dispositivo.                             (adb reboot)
ECHO 3. Reiniciar el dispositivo en modo Recovery.            (adb reboot recovery)
ECHO 4. Reiniciar el dispositivo en modo Fastboot/Descarga.   (adb reboot bootloader)
ECHO 5. Realizar operaciones con archivos.
ECHO.
ECHO FASTBOOT
ECHO --------
ECHO.
ECHO 6. Comprobar si el ordenador reconoce el dispositivo.    (fastboot devices)
ECHO 7. Reiniciar el dispositivo.                             (fastboot reboot)
ECHO 8. Reiniciar el dispositivo en modo Recovery.            (fastboot reboot recovery)
ECHO 9. Formatear particiones del dispositivo.                (fastboot format)
ECHO.
ECHO MISCELANEO
ECHO ----------
ECHO.
ECHO 10. Elegir mas opciones.
ECHO 11. Creditos.
ECHO 12. SALIR.
ECHO.

:: Creo una entrada para recibir un valor elegido por el usuario
ECHO -------------------------------------------------------------------------------------------------------
SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "
ECHO.

REM Determino la opcion a ejecutar segun el numero elegido por el usuario
        
IF !CHOICE!==1 GOTO ADB
IF !CHOICE!==2 GOTO REBOOT-ADB
IF !CHOICE!==3 GOTO REBOOT-RECOVERY-ADB
IF !CHOICE!==4 GOTO REBOOT-FASTBOOT-ADB
IF !CHOICE!==5 GOTO FILEMAN
IF !CHOICE!==6 GOTO FASTBOOT
IF !CHOICE!==7 GOTO REBOOT-FASTBOOT
IF !CHOICE!==8 GOTO REBOOT-RECOVERY-FASTBOOT
IF !CHOICE!==9 GOTO FASTBOOT-FORMAT
IF !CHOICE!==10 GOTO EXTRA
IF !CHOICE!==11 GOTO CREDITS
IF !CHOICE!==12 GOTO EXIT

:: Defino las opciones a utilizar
:ADB
adb devices
pause
CLS
GOTO MENU

:REBOOT-ADB
adb reboot
ECHO Reiniciando.
ECHO.
pause
CLS
GOTO MENU

:REBOOT-RECOVERY-ADB
adb reboot recovery
ECHO Reiniciando.
ECHO.
pause
CLS
GOTO MENU

:REBOOT-FASTBOOT-ADB
adb reboot bootloader
ECHO Reiniciando.
ECHO.
pause
CLS
GOTO MENU

:FILEMAN
CLS
ECHO.
ECHO -------------------------------------------------------------------------------------------------------
ECHO En este apartado, usted podra optar por copiar archivos desde o hacia su dispositivo movil.
ECHO -------------------------------------------------------------------------------------------------------
ECHO.
ECHO 1. Copiar archivos hacia el dispositivo.                      (adb push)
ECHO 2. Copiar archivos desde el dispositivo hacia el ordenador.   (adb pull)
ECHO 3. Volver al menu principal.
ECHO.

SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "

IF !CHOICE!==1 GOTO ADBPUSH
IF !CHOICE!==2 GOTO ADBPULL
IF !CHOICE!==3 GOTO MENU

    :ADBPUSH
    CLS
    ECHO.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO Para copiar un archivo hacia el dispositivo, por favor, indique su ubicacion incluyendo el nombre de
    ECHO este, y la ubicacion en el dispositivo a la cual le gustaria copiarlo.
    ECHO.
    ECHO Ejemplo: "adb push C:\Users\foopsss\Desktop\Texto.txt\ /sdcard/Textos/".
    ECHO -------------------------------------------------------------------------------------------------------
    
    SET /P RUTA1="Ubicacion del archivo: "
    SET /P RUTA2="Ubicacion a la cual copiar: "
    
    ECHO.
    adb push !RUTA1! !RUTA2!
    ECHO -------------------------------------------------------------------------------------------------------
    SET /P CHOICE="Necesita copiar otro archivo? [S/N]: "
    
    IF /I !CHOICE!==S GOTO ADBPUSH
    IF /I !CHOICE!==N GOTO FILEMAN

    :ADBPULL
    CLS
    ECHO.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO Para copiar un archivo desde el dispositivo, por favor, indique su ubicacion incluyendo el nombre de
    ECHO este, y la ubicacion en el ordenador a la cual le gustaria copiarlo.
    ECHO.
    ECHO Ejemplo: "adb pull /sdcard/Textos/Texto.txt/ C:\Users\foopsss\Desktop\".
    ECHO -------------------------------------------------------------------------------------------------------
    
    SET /P RUTA1="Ubicacion del archivo: "
    SET /P RUTA2="Ubicacion a la cual copiar: "
    
    ECHO.
    adb pull !RUTA1! !RUTA2!
    ECHO -------------------------------------------------------------------------------------------------------
    SET /P CHOICE="Necesita copiar otro archivo? [S/N]: "
    
    IF /I !CHOICE!==S GOTO ADBPULL
    IF /I !CHOICE!==N GOTO FILEMAN

:FASTBOOT
fastboot devices
pause
CLS
GOTO MENU

:REBOOT-FASTBOOT
fastboot reboot
pause
CLS
GOTO MENU

:REBOOT-RECOVERY-FASTBOOT
fastboot reboot recovery
pause
CLS
GOTO MENU

:FASTBOOT-FORMAT
CLS
ECHO.
ECHO -------------------------------------------------------------------------------------------------------
ECHO En este apartado, usted podra optar por formatear ciertas particiones de su dispositivo utilizando el
ECHO modo Fastboot.
ECHO -------------------------------------------------------------------------------------------------------
ECHO.
ECHO 1. Formatear la particion /system.   (fastboot format system)
ECHO 2. Formatear la particion /data.     (fastboot format userdata)
ECHO 3. Formatear la particion /cache.    (fastboot format cache)
ECHO 4. Volver al menu principal.
ECHO.
ECHO -------------------------------------------------------------------------------------------------------
SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "
ECHO.

IF !CHOICE!==1 GOTO FASTBOOT-FORMAT-SYSTEM
IF !CHOICE!==2 GOTO FASTBOOT-FORMAT-DATA
IF !CHOICE!==3 GOTO FASTBOOT-FORMAT-CACHE
IF !CHOICE!==4 GOTO MENU
    
    :FASTBOOT-FORMAT-SYSTEM
    fastboot format system
    pause
    CLS
    GOTO MENU
    
    :FASTBOOT-FORMAT-DATA
    fastboot format userdata
    pause
    CLS
    GOTO MENU
    
    :FASTBOOT-FORMAT-CACHE
    fastboot format cache
    pause
    CLS
    GOTO MENU

:EXTRA
CLS
ECHO.
ECHO -------------------------------------------------------------------------------------------------------
ECHO En este apartado, usted podra optar por elegir entre una serie de comandos adicionales para ejecutar.
ECHO -------------------------------------------------------------------------------------------------------
ECHO.
ECHO 1. Administrar las aplicaciones instaladas.
ECHO 2. Instalar un archivo .zip utilizando el recovery.   (adb sideload)
ECHO 3. Ejecutar un comando propio.
ECHO 4. Volver al menu principal.
ECHO.

SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "

IF !CHOICE!==1 GOTO APPMAN
IF !CHOICE!==2 GOTO SIDELOAD
IF !CHOICE!==3 GOTO CUSTCOMM
IF !CHOICE!==4 GOTO MENU

    :APPMAN
    CLS
    ECHO.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO En este apartado, usted podra optar por realizar una serie de operaciones para administrar las
    ECHO aplicaciones del dispositivo.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO.
    ECHO 1. Instalar una aplicacion.
    ECHO 2. Desinstalar una aplicacion para el usuario actual.    (adb shell pm uninstall)
    ECHO 3. Restaurar una aplicacion desinstalada previamente.    (adb shell cmd package install-existing)
    ECHO 4. Deshabilitar una aplicacion.                          (adb shell pm disable-user)
    ECHO 5. Habilitar una aplicacion deshabilitada previamente.   (adb shell pm enable)
    ECHO 6. Obtener informacion de las aplicaciones instaladas.
    ECHO 7. Volver al menu de opciones adicionales.
    ECHO.
    
    SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "
    
    IF !CHOICE!==1 GOTO APPINSTALL
    IF !CHOICE!==2 GOTO APPUNINSTALL
    IF !CHOICE!==3 GOTO APPREINSTALL
    IF !CHOICE!==4 GOTO APPDISABLE
    IF !CHOICE!==5 GOTO APPENABLE
    IF !CHOICE!==6 GOTO APPINFO
    IF !CHOICE!==7 GOTO EXTRA

       :APPINSTALL
       CLS
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO En este apartado, usted podra optar por elegir entre distintas opciones para instalar aplicaciones en
       ECHO su dispositivo mediante archivos APK.
       ECHO.
       ECHO Si la instalacion tiene exito usted podra ver la palabra "Success".
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.
       ECHO 1. Instalar una aplicacion.                           (adb install)
       ECHO 2. Instalar una aplicacion por partes (split APKs).   (adb install-multiple)
       ECHO 3. Instalar multiples aplicaciones.                   (adb install-multi-package)
       ECHO 4. Volver al menu de manejo de aplicaciones.
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.
    
       IF !CHOICE!==1 GOTO SINGLEAPP
       IF !CHOICE!==2 GOTO SPLITAPKS
       IF !CHOICE!==3 GOTO MULTIPLEAPPS
       IF !CHOICE!==4 GOTO APPMAN

          :SINGLEAPP
          ECHO Introduzca en el campo correspondiente la ubicacion del archivo APK a instalar.
          ECHO.

          SET /P RUTA1="Ubicacion del archivo: "

          ECHO.
          adb install !RUTA1!
          ECHO.

          PAUSE
          CLS
          GOTO APPINSTALL

          :SPLITAPKS
          ECHO Introduzca en los campos correspondientes las ubicaciones de los archivos APK correspondientes a la
          ECHO aplicacion a instalar. Se pueden instalar 3 partes al mismo tiempo.
          ECHO.

          SET /P RUTA1="Ubicacion del primer archivo: "
          SET /P RUTA2="Ubicacion del segundo archivo: "
          SET /P RUTA3="Ubicacion del tercer archivo: "

          ECHO.
          adb install-multiple !RUTA1! !RUTA2! !RUTA3!
          ECHO.

          PAUSE
          CLS
          GOTO APPINSTALL

          :MULTIPLEAPPS
          ECHO Introduzca en los campos correspondientes las ubicaciones de los archivos APK correspondientes a las
          ECHO aplicaciones a instalar. Se pueden instalar hasta 5 aplicaciones al mismo tiempo.
          ECHO.

          SET /P RUTA1="Ubicacion del primer archivo: "
          SET /P RUTA2="Ubicacion del segundo archivo: "
          SET /P RUTA3="Ubicacion del tercer archivo: "
          SET /P RUTA4="Ubicacion del cuarto archivo: "
          SET /P RUTA5="Ubicacion del quinto archivo: "

          ECHO.
          adb install-multi-package !RUTA1! !RUTA2! !RUTA3! !RUTA4! !RUTA5!
          ECHO.

          PAUSE
          CLS
          GOTO APPINSTALL

       :APPUNINSTALL
       CLS
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO En este apartado, usted podra optar por "desinstalar" aplicaciones de su dispositivo. Tenga en cuenta
       ECHO que no es posible borrar completamente una aplicacion del dispositivo, sino para el usuario actual, por
       ECHO lo que esta puede ser restaurada con un reseteo, o utilizando la siguiente opcion de este apartado.
       ECHO.
       ECHO Para esto, se requiere el "ID" de la aplicacion que quiera desinstalar. Para obtenerlo, puede descargar
       ECHO alguna aplicacion de la Play Store o la Web, como "Package Name Viewer 2.0", o utilizar alguna de las
       ECHO opciones del sexto apartado del conjunto de opciones extra.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.

       SET /P ID="ID de la aplicacion: "

       ECHO.
       adb shell pm uninstall --user 0 !ID!
       ECHO -------------------------------------------------------------------------------------------------------
       SET /P CHOICE="Necesita desinstalar otra aplicacion? [S/N]: "

       IF /I !CHOICE!==S GOTO APPUNINSTALL
       IF /I !CHOICE!==N GOTO APPMAN

       :APPREINSTALL
       CLS
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO En este apartado, usted podra optar por "reinstalar" aquellas aplicaciones que haya removido de su
       ECHO dispositivo utilizando la opcion anterior.
       ECHO.
       ECHO Se requiere el ID de la aplicacion desinstalada.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.

       SET /P ID="ID de la aplicacion: "

       ECHO.
       adb shell cmd package install-existing !ID!
       ECHO -------------------------------------------------------------------------------------------------------
       SET /P CHOICE="Necesita reinstalar otra aplicacion? [S/N]: "

       IF /I !CHOICE!==S GOTO APPREINSTALL
       IF /I !CHOICE!==N GOTO APPMAN

       :APPDISABLE
       CLS
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO En este apartado, usted podra optar por desactivar aplicaciones de su dispositivo. Tenga en cuenta que
       ECHO a diferencia de la supresion de aplicaciones mediante el sistema operativo, las que son desactivadas
       ECHO mediante este metodo solo pueden ser devueltas a la normalidad a traves del mismo.
       ECHO.
       ECHO Se requiere el ID de la aplicacion a desactivar.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.

       SET /P ID="ID de la aplicacion: "

       ECHO.
       adb shell pm disable-user --user 0 !ID!
       ECHO -------------------------------------------------------------------------------------------------------
       SET /P CHOICE="Necesita desactivar otra aplicacion? [S/N]: "

       IF /I !CHOICE!==S GOTO APPDISABLE
       IF /I !CHOICE!==N GOTO APPMAN
       
       :APPENABLE
       CLS
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO En este apartado, usted podra optar por reactivar aquellas aplicaciones que haya desactivado utilizando
       ECHO la opcion anterior.
       ECHO.
       ECHO Se requiere el ID de la aplicacion a reactivar.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.

       SET /P ID="ID de la aplicacion: "

       ECHO.
       adb shell pm enable !ID!
       ECHO -------------------------------------------------------------------------------------------------------
       SET /P CHOICE="Necesita desactivar otra aplicacion? [S/N]: "

       IF /I !CHOICE!==S GOTO APPENABLE
       IF /I !CHOICE!==N GOTO APPMAN

       :APPINFO
       CLS
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO En este apartado, usted podra optar por obtener cierta informacion de las aplicaciones instaladas en su
       ECHO dispositivo.
       ECHO.
       ECHO Para la primera opcion, se requiere el ID de aplicacion.
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.
       ECHO 1. Obtener la ruta de una aplicacion.                               (adb shell pm path)
       ECHO 2. Obtener un listado de aplicaciones y sus rutas.                  (adb shell pm list packages -f)
       ECHO 3. Obtener un listado de aplicaciones desactivadas y sus rutas.     (adb shell pm list packages -d -f)
       ECHO 4. Obtener un listado de aplicaciones buscando por palabra clave.   (adb shell pm list packages -f)
       ECHO 5. Volver al menu de manejo de aplicaciones.
       ECHO.
       ECHO -------------------------------------------------------------------------------------------------------
       SET /P CHOICE="Escriba el numero correspondiente a la operacion que desee realizar y presione ENTER: "
       ECHO -------------------------------------------------------------------------------------------------------
       ECHO.
    
       IF !CHOICE!==1 GOTO ONEPACKAGE
       IF !CHOICE!==2 GOTO MULTIPLEPACKAGES
       IF !CHOICE!==3 GOTO DISABLEDPACKAGES
       IF !CHOICE!==4 GOTO KEYWORDPACKAGES
       IF !CHOICE!==5 GOTO APPMAN

          :ONEPACKAGE
          ECHO Introduzca en el campo correspondiente la ID de la aplicacion cuya ruta quiere averiguar.
          ECHO.

          SET /P ID="ID de la aplicacion: "

          ECHO.
          adb shell pm path !ID!
          ECHO.

          PAUSE
          CLS
          GOTO APPINFO

          :MULTIPLEPACKAGES
          ECHO A continuacion, obtendra una lista de las aplicaciones instaladas en su dispositivo tanto por el
          ECHO fabricante como por usted mismo. Los directorios escaneados son system/app, /priv-app/ y data/app.
          ECHO.
          ECHO Una vez que presione cualquier tecla, se imprimira la lista y se la guardara en un archivo de texto en
          ECHO su escritorio, ya que sera extensa.
          ECHO.

          PAUSE

          ECHO.
          adb shell pm list packages -f > !ARCHIVO1!
          if exist !ARCHIVO1! (
             ECHO El archivo se encuentra en el escritorio.
          )
          ECHO.
             
          PAUSE
          CLS
          GOTO APPINFO

          :DISABLEDPACKAGES
          ECHO A continuacion, obtendra una lista de las aplicaciones de su dispositivo que se encuentran suprimidas.
          ECHO.
          ECHO Una vez que presione cualquier tecla, se imprimira la lista y se la guardara en un archivo de texto en
          ECHO su escritorio, ya que sera extensa.
          ECHO.

          PAUSE

          ECHO.
          adb shell pm list packages -d -f > !ARCHIVO2!
          if exist !ARCHIVO2! (
             ECHO El archivo se encuentra en el escritorio.
          )
          ECHO.
             
          PAUSE
          CLS
          GOTO APPINFO

          :KEYWORDPACKAGES
          ECHO Introduzca en el campo correspondiente alguna palabra que quiera utilizar para poder identificar el ID
          ECHO de alguna aplicacion, junto con su ruta.
          ECHO.
          ECHO Una vez que introduzca la palabra, se imprimira la lista y se la guardara en su escritorio. De estar
          ECHO vacio el archivo, es porque no se encontro nada y debera probar con otra clave.
          ECHO.

          SET /P CLAVE="Palabra clave: "
          adb shell pm list packages -f "!CLAVE!" > !ARCHIVO3!
          if exist !ARCHIVO3! (
             ECHO El archivo se encuentra en el escritorio.
          )
          ECHO.

          PAUSE
          CLS
          GOTO APPINFO

    :SIDELOAD
    CLS
    ECHO.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO En este apartado, usted podra optar por instalar un archivo .zip mediante el modo Recovery.
    ECHO.
    ECHO Para ello, por favor, indique su ubicacion incluyendo el nombre de este.
    ECHO Ejemplo: "C:\Users\foopsss\Desktop\Example.zip\".
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO.
    
    SET /P RUTA1="Ubicacion del archivo: "
    
    ECHO.
    adb sideload !RUTA1!
    ECHO -------------------------------------------------------------------------------------------------------
    SET /P CHOICE="Necesita instalar otro archivo? [S/N]: "
    
    IF /I !CHOICE!==S GOTO SIDELOAD
    IF /I !CHOICE!==N GOTO EXTRA

    :CUSTCOMM
    CLS
    ECHO.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO En este apartado, usted podra optar por ejecutar cualquier otro tipo de comando no incluido en esta
    ECHO herramienta.
    ECHO.
    ECHO Para ello, por favor, indique el comando a ejecutar en el campo correspondiente.
    ECHO -------------------------------------------------------------------------------------------------------
    ECHO.
    
    SET /P COMANDOPERS="Comando a ejecutar: "
    
    ECHO.
    !COMANDOPERS!
    ECHO -------------------------------------------------------------------------------------------------------
    SET /P CHOICE="Necesita ejecutar otro comando? [S/N]: "
    
    IF /I !CHOICE!==S GOTO CUSTCOMM
    IF /I !CHOICE!==N GOTO EXTRA

:EXIT
adb kill-server
exit
