$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir
$python = "python"
Start-Process -FilePath $python -ArgumentList 'server.py' -WorkingDirectory $scriptDir -WindowStyle Hidden
Write-Output "Serveur lancé en arrière-plan. Ouvrez http://localhost:8000"
Pop-Location
