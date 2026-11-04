$ErrorActionPreference='Stop'
$project=Split-Path $PSScriptRoot -Parent
$python=Join-Path $project '.venv/Scripts/python.exe'
if(!(Test-Path -LiteralPath $python)){throw '请先运行根目录安装环境.cmd'}
& $python (Join-Path $PSScriptRoot 'main.py')
exit $LASTEXITCODE
