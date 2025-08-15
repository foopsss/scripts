Import-Module $pwd/modules/CommonResources.psm1

function Show-Menu {
    Write-Host "-----------------------------------------------------------------------------------"
    Write-Host "Bienvenido!" -ForegroundColor Green
    Write-Host "Por favor, seleccione una opcion."
    Write-Host "-----------------------------------------------------------------------------------"
    Write-Host "Fecha:"
    Get-Date -Format "dd/MM/yyyy"
    Write-Host "Hora:"
    Get-Date -Format "hh:mm"
    Write-Host "-----------------------------------------------------------------------------------"
    Write-Host "1. Hacer copia del mundo de Minecraft."
    Write-Host "2. Hacer copia de los datos de partida de Call of Duty: World at War."
    Write-Host "3. Hacer copia de los datos de partida de Grand Theft Auto: San Andreas."
    Write-Host "4. Hacer copia de los datos de partida de The Walking Dead: The Definitive Edition."
    Write-Host "5. SALIR."
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
	Write-Host "Creando archivo!" -ForegroundColor Gray
	Compress-Archive -Path "$origin" -DestinationPath "$first_file" -Update -CompressionLevel Optimal
	Copy-Item "$first_file" -Destination "$second_file" -Force
	Test-DoubleExistence -arch1 "$first_file" -arch2 "$second_file"
}

$onedrive_zips_folder = Join-Path -Path $onedrive_folder -ChildPath 'Backups\Zips'

do
{
    Show-Menu
    $selection =
    Read-Host "Escriba el numero que corresponda a la opcion que desee y presione ENTER"
    Write-Host " "

    switch ($selection)
    {
        '1' {
            $minecraft = @{
				origin = "I:\Minecraft\Instalaciones\Fabric\saves\Lucas3"
				first_file = "$onedrive_zips_folder\Lucas3.zip"
				second_file = "$zips_usb\Lucas3.zip"
			}
            New-Copy @minecraft
        }
        
        '2' {
            $codwaw = @{
				origin = "C:\Users\liben\AppData\Local\Activision\CoDWaW"
				first_file = "$onedrive_zips_folder\Call of Duty World at War.zip"
				second_file = "$zips_usb\Call of Duty World at War.zip"
			}
			New-Copy @codwaw
        }

        '3' {
            $gtasa = @{
				origin = "C:\Users\$username_win\Documents\GTA San Andreas User Files"
				first_file = "$onedrive_zips_folder\Grand Theft Auto San Andreas.zip"
				second_file = "$zips_usb\Grand Theft Auto San Andreas.zip"
			}
			New-Copy @gtasa
        }

		'4' {
			$twd = @{
				origin = "C:\Users\$username_win\Documents\Telltale Games"
				first_file = "$onedrive_zips_folder\The Walking Dead Definitive Edition.zip"
				second_file = "$zips_usb\The Walking Dead Definitive Edition.zip"
			}
			New-Copy @twd
		}
    }
    
    Read-Key
}

until ($selection -eq '5')
