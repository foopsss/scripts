Import-Module -Name $pwd/modules/CommonResources.psm1

$repos = @("dotfiles", "foopsss", "gentoo-configs", "gentoo-overlay", "scripts", "specfiles", "utn")
$branches = @()

$url = "www.github.com"
$is_reachable = Test-Connection $url -Count 1 -Quiet

if (!$is_reachable) {
	Throw "No se puede acceder a GitHub por el momento, o no hay conexion."
} else {
	Write-Host "GitHub esta disponible!" -ForegroundColor Green
	Write-Host "Procediendo a descargar los repositorios..." -ForegroundColor Gray 
}

foreach($repo in $repos) {
	# Averiguo el nombre de las ramas disponibles con una solicitud GET.
	# Utilizo la API de GitHub.
	$branches = Invoke-RestMethod -Uri "https://api.github.com/repos/foopsss/$repo/branches" -Method GET
	
	# Guardo en una variable el nombre de cada rama y la utilizo para descargarlas.
	# Luego modifico el nombre en el arreglo $branches para darle el nombre de su archivo correspondiente.
	foreach($branch in $branches) {
		$branch_name_var = $branch.name
		$branch.name = $branch.name | ForEach-Object {"$repo-$_.zip"}
		Invoke-WebRequest -Uri "https://github.com/foopsss/$repo/archive/refs/heads/$branch_name_var.zip" -OutFile "$repo-$branch_name_var.zip"
	}
	
	# Comprimo en un solo archivo las multiples ramas de un repositorio.
	Compress-Archive -LiteralPath $branches.name -DestinationPath "$repo.zip"
	Remove-Item -LiteralPath $branches.name
}

# Modifico el arreglo de entrada con los repositorios.
# La idea es añadirle la extension ".zip" a los elementos.
$repos = $repos | ForEach-Object {"$_.zip"}

# Comprimo los archivos obtenidos previamente en un solo archivo de salida.
$ruta_pendrive = Join-Path -Path $zips_usb -ChildPath 'GitHub.zip'
$ruta_onedrive = Join-Path -Path $onedrive_folder -ChildPath 'Backups/Zips/GitHub.zip'
Compress-Archive -LiteralPath $repos -DestinationPath $ruta_pendrive -Force

# Copio el archivo a OneDrive.
Copy-Item $ruta_pendrive -Destination $ruta_onedrive -Force
Test-DoubleExistence -arch1 $ruta_pendrive -arch2 $ruta_onedrive

# Limpio los archivos residuales innecesarios y salgo.
Remove-Item -LiteralPath $repos
Read-Key
