# Installs the switch on this Windows PC and starts it at every sign-in.
# Double-click setup_windows.bat, which runs this file. Run it again after updating the files.
#   setup_windows.bat              asks for this computer's channel
#   setup_windows.bat -Channel 2   this computer is channel 2 (the Easy-Switch slot it's paired on)
#   setup_windows.bat -Uninstall   stops it and removes it from startup
param([int]$Channel = 0, [switch]$Uninstall)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$shortcut = Join-Path ([Environment]::GetFolderPath("Startup")) "Keyboard mouse switch.lnk"

# stop a copy that is already running
Get-CimInstance Win32_Process -Filter "Name = 'pythonw.exe' OR Name = 'python.exe'" |
    Where-Object { $_.CommandLine -like "*listener.py*" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host "Stopped the running switch." }

if ($Uninstall) {
    if (Test-Path $shortcut) { Remove-Item $shortcut; Write-Host "Removed it from startup." }
    exit 0
}

while ($Channel -lt 1 -or $Channel -gt 3) {
    $answer = Read-Host "Which Easy-Switch channel is this computer on (1, 2 or 3)?"
    [int]::TryParse($answer, [ref]$Channel) | Out-Null
}

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Install it, then run this again:"
    Write-Host "  winget install Python.Python.3.12"
    Write-Host "  (or python.org, with 'py launcher' ticked)"
    exit 1
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating .venv ..."
    py -3 -m venv .venv
    if ($LASTEXITCODE) { throw "could not create .venv" }
}
Write-Host "Installing hidapi ..."
& .venv\Scripts\python.exe -m pip install --quiet --disable-pip-version-check -r requirements.txt
if ($LASTEXITCODE) { throw "pip install failed" }

$pythonw = Join-Path $here ".venv\Scripts\pythonw.exe"
$args_ = "`"$here\listener.py`" --channel $Channel --log `"$here\listener.log`""

$sh = New-Object -ComObject WScript.Shell
$lnk = $sh.CreateShortcut($shortcut)
$lnk.TargetPath = $pythonw
$lnk.Arguments = $args_
$lnk.WorkingDirectory = $here
$lnk.Description = "Logitech keyboard + mouse switch (channel $Channel)"
$lnk.Save()
Write-Host "Installed as channel $Channel. It starts at every sign-in: $shortcut"

Start-Process -FilePath $pythonw -ArgumentList $args_ -WorkingDirectory $here
Start-Sleep -Seconds 3
Write-Host ""
Write-Host "Running. Log ($here\listener.log):"
Get-Content "$here\listener.log" -ErrorAction SilentlyContinue
