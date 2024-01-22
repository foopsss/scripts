Import-Module $pwd/CommonResources.psm1

function Show-Menu {
    Write-Host "----------------------------------------------------------------------------"
    Write-Host "Bienvenido!" -ForegroundColor Green
    Write-Host "Por favor, seleccione de que desearia realizar una copia"
    Write-Host "----------------------------------------------------------------------------"
    Write-Host "Fecha:"
    Get-Date -Format "dd/MM/yyyy"
    Write-Host "Hora:"
    Get-Date -Format "hh:mm"
    Write-Host "----------------------------------------------------------------------------"
    Write-Host "1. Hacer copia del mundo de Minecraft."
    Write-Host "2. Hacer copia de los datos de partida de Call of Duty: World at War."
    Write-Host "3. Hacer copia de los datos de partida de Grand Theft Auto: San Andreas."
    Write-Host "4. SALIR."
    Write-Host " "
}

function New-Copy {
	param
	(
		[Parameter(Mandatory=$true, Position=0)]
		[string] $origin,
		[Parameter(Mandatory=$true, Position=1)]
		[string] $first_file,
		[Parameter(Mandatory=$true, Position=2)]
		[string] $second_file
	)
	
	Clear-Host
	Write-Host "Creando archivo zip!" -ForegroundColor Gray
	Compress-Archive -Path "$origin" -DestinationPath "$first_file" -Update -CompressionLevel Optimal
	Copy-Item "$first_file" -Destination "$second_file" -Force
	Test-Existence -arch1 "$first_file" -arch2 "$second_file"
}

do
 {
    Show-Menu
    $selection =
    Read-Host "Escriba el numero que corresponda a la opcion que desee y presione ENTER"
    Write-Host " "

    switch ($selection)
    {
        '1' {
            $minecraft = "I:\Minecraft\Instalaciones\Fabric\saves\Lucas3\"
            New-Copy -origin "$minecraft" -first_file "$onedrive_win\Lucas3.zip" -second_file "$parent\Zips\Lucas3.zip"
        }
        
        '2' {
            $codwaw = "C:\Users\Lucas\AppData\Local\Activision\CoDWaW\"
			New-Copy -origin "$codwaw" -first_file "$onedrive_win\Call of Duty World at War.zip" -second_file "$parent\Zips\Call of Duty World at War.zip"
        }

        '3' {
            $gtasa = "C:\Users\Lucas\Documents\GTA San Andreas User Files"
			New-Copy -origin "$gtasa" -first_file "$onedrive_win\Grand Theft Auto San Andreas.zip" -second_file "$parent\Zips\Grand Theft Auto San Andreas.zip"
        }
    }
    
    Read-Key
 }

until ($selection -eq '4')
