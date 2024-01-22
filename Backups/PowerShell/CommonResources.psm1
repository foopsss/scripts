$parent = Split-Path -Path $pwd -Parent
$onedrive_win = "C:\Users\liben\OneDrive\Backups\Zips"
$onedrive_linux = "/home/lucas/Documentos/OneDrive/Backups/Zips"

function is_windows {
	if ([System.Environment]::OSVersion.Platform -eq 'Win32NT') {
		return $true
	}
}

function Test-Existence {
	param
	(
		[Parameter(Mandatory=$true, Position=0)]
		[string] $arch1,
		[Parameter(Mandatory=$true, Position=1)]
		[string] $arch2
	)

	if ( (Test-Path -Path $arch1 -PathType Leaf) -and (Test-Path -Path $arch2 -PathType Leaf) ) {
		Write-Host "Operacion completada exitosamente." -ForegroundColor Green
	} else {
		Write-Error "La operacion no se pudo completar. Intente de nuevo."
	}
}

function Read-Key {
	Write-Host "Presione una tecla para continuar." -ForegroundColor Yellow
	[void][System.Console]::ReadKey($FALSE)
	Clear-Host
}

Export-ModuleMember -Variable parent
Export-ModuleMember -Variable onedrive_win
Export-ModuleMember -Variable onedrive_linux
Export-ModuleMember -Function is_windows
Export-ModuleMember -Function Test-Existence
Export-ModuleMember -Function Read-Key
