$parent = Split-Path -Path $pwd -Parent
$onedrive_win = "C:\Users\$([Environment]::UserName)\OneDrive\Backups\Zips"
$zips = Join-Path -Path $parent -ChildPath 'Zips'

function Test-WindowsOS {
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
Export-ModuleMember -Variable onedrive_win
Export-ModuleMember -Variable zips
Export-ModuleMember -Function Test-WindowsOS
Export-ModuleMember -Function Test-DoubleExistence
Export-ModuleMember -Function Test-SingleExistence
Export-ModuleMember -Function Read-Key