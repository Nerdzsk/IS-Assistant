# PowerShell skript na automatické zapínanie aplikácie ak spadne
# Spustí Flask a monitoruje ho - ak spadne, zapne ho znova

$appPath = "e:\AI\IS- Assistent\IS-Assistant"
$pythonExe = "$appPath\.venv\Scripts\python.exe"
$webappPy = "$appPath\webapp.py"
$logFile = "$appPath\app_monitor.log"

function Log {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMsg = "[$timestamp] $message"
    Write-Host $logMsg
    Add-Content -Path $logFile -Value $logMsg
}

function Start-App {
    Log "Zapínam Flask aplikáciu..."
    Set-Location $appPath
    & $pythonExe $webappPy
}

# Vymaž starý log
if (Test-Path $logFile) { Remove-Item $logFile }

Log "=== Aplikácia Monitor Spustená ==="
Log "Adresár: $appPath"
Log "Python: $pythonExe"

# Spusti aplikáciu
Start-App
