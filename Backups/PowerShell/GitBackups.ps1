Import-Module -Name $pwd/CommonResources.psm1

$main_only = @("foopsss", "gentoo-configs", "gentoo-overlay", "natural-gentoo-remastered", "specfiles")
$other_repos = @("algoritmos", "algoritmos-rs", "dotfiles", "scripts")
$branches = @()
$all_repos = @()

$url = "www.github.com"
$is_reachable = Test-Connection $url -Count 1 -Quiet

if (!$is_reachable) {
	Throw "No se puede acceder a GitHub por el momento, o no hay conexion."
} else {
	Write-Host "GitHub esta disponible!" -ForegroundColor Green
	Write-Host "Procediendo a descargar los repositorios..." -ForegroundColor Gray 
}

foreach ($repo in $main_only) {
	Invoke-WebRequest -Uri "https://github.com/foopsss/$repo/archive/refs/heads/main.zip" -OutFile "$repo.zip"
}

foreach($repo in $other_repos) {
	# Averiguo el nombre de las ramas disponibles con una solicitud GET.
	# Utilizo la API de GitHub.
	$branches = Invoke-RestMethod -Uri "https://api.github.com/repos/foopsss/$repo/branches" -Method GET
	
	# Guardo en una variable el nombre de cada rama y la utilizo para descargarlas.
	# Luego modifico el nombre en el arreglo $branches para darle el nombre de su archivo correspondiente.
	foreach($branch in $branches) {
		$branch_name = $branch.name
		$branch.name = $branch.name | ForEach-Object {"$repo-$_.zip"}
		Invoke-WebRequest -Uri "https://github.com/foopsss/$repo/archive/refs/heads/$branch_name.zip" -OutFile "$repo-$branch_name.zip"
	}
	
	# Comprimo en un solo archivo las multiples ramas de un repositorio.
	Compress-Archive -LiteralPath $branches.name -DestinationPath "$repo.zip"
	Remove-Item -LiteralPath $branches.name
}

# Modifico los arreglos de entrada con los repositorios.
# La idea es añadirles un sufijo, la extension ".zip".
# Luego comprimo todos los archivos indicados en uno solo.
$main_only = $main_only | ForEach-Object {"$_.zip"}
$other_repos = $other_repos | ForEach-Object {"$_.zip"}
$all_repos = $main_only + $other_repos

if (is_windows) {
	Compress-Archive -LiteralPath $all_repos -DestinationPath "$onedrive_win\GitHub.zip" -Force
	Copy-Item "$onedrive_win\GitHub.zip" -Destination "$zips_win\GitHub.zip" -Force
	Test-Existence -arch1 "$onedrive_win\GitHub.zip" -arch2 "$zips_win\GitHub.zip"
} else {
	# La funcion "is_windows" solo devuelve "Unix" si no uso Windows.
	# Sin embargo, me es suficiente para el uso que le voy a dar en Linux.
	Compress-Archive -LiteralPath $all_repos -DestinationPath "$onedrive_linux/GitHub.zip" -Force
	Copy-Item "$onedrive_linux/GitHub.zip" -Destination "$zips_linux/GitHub.zip" -Force
	Test-Existence -arch1 "$onedrive_linux/GitHub.zip" -arch2 "$zips_linux/GitHub.zip"
}

Remove-Item -LiteralPath $all_repos

Read-Key
