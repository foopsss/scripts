$parent = Split-Path -Path $pwd -Parent
$username_win = "liben"
$onedrive_win = "C:\Users\$username_win\OneDrive\Backups\Zips"
$zips_win = "$parent\Zips"
$onedrive_linux = "$HOME/Documentos/OneDrive/Backups/Zips"
$zips_linux = "$parent/Zips"

function is_windows {
	if ([System.Environment]::OSVersion.Platform -eq 'Win32NT') {
		return $true
	}
}

function Read-Key {
	Write-Host "Presione una tecla para continuar." -ForegroundColor Yellow
	[void][System.Console]::ReadKey($FALSE)
	Clear-Host
}

function Test-DoubleExistence {
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

function Test-SingleExistence {
	param
	(
		[Parameter(Mandatory=$true)]
		[string] $arch
	)

	if (Test-Path -Path $arch -PathType Leaf) {
		Write-Host "Operacion completada exitosamente." -ForegroundColor Green
	} else {
		Write-Error "La operacion no se pudo completar. Intente de nuevo."
	}
}

Export-ModuleMember -Variable parent
Export-ModuleMember -Variable username_win
Export-ModuleMember -Variable onedrive_win
Export-ModuleMember -Variable zips_win
Export-ModuleMember -Variable onedrive_linux
Export-ModuleMember -Variable zips_linux
Export-ModuleMember -Function is_windows
Export-ModuleMember -Function Test-DoubleExistence
Export-ModuleMember -Function Test-SingleExistence
Export-ModuleMember -Function Read-Key
