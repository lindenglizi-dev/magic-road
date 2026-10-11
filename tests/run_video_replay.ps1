param(
    [Parameter(Mandatory = $true)]
    [string]$FrameDir,
    [string]$ResultDir = '',
    [int]$Frames = 0,
    [ValidateRange(1, 255)]
    [int]$Threshold = 20,
    [ValidateRange(0, 100000)]
    [int]$RowGap = 1280
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$workspaceRoot = Split-Path (Split-Path $projectRoot -Parent) -Parent
$framePath = (Resolve-Path -LiteralPath $FrameDir).Path
$manifestPath = Join-Path $framePath 'manifest.json'
if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "manifest.json not found in $framePath. Run video_to_gray_frames.py first."
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($Frames -eq 0) {
    $Frames = [int]$manifest.frame_count
}
if ($Frames -lt 1 -or $Frames -gt [int]$manifest.frame_count) {
    throw "Frames must be between 1 and $($manifest.frame_count)."
}

if ([string]::IsNullOrWhiteSpace($ResultDir)) {
    $resultPath = Join-Path $framePath 'rtl_results'
} else {
    $resultPath = [System.IO.Path]::GetFullPath($ResultDir)
}
New-Item -ItemType Directory -Path $resultPath -Force | Out-Null

$localIverilog = Join-Path $workspaceRoot '.tools\iverilog\bin\iverilog.exe'
$localVvp = Join-Path $workspaceRoot '.tools\iverilog\bin\vvp.exe'
$systemIverilog = 'C:\iverilog\bin\iverilog.exe'
$systemVvp = 'C:\iverilog\bin\vvp.exe'
if ((Test-Path -LiteralPath $localIverilog) -and (Test-Path -LiteralPath $localVvp)) {
    $iverilog = $localIverilog
    $vvp = $localVvp
} elseif ((Test-Path -LiteralPath $systemIverilog) -and (Test-Path -LiteralPath $systemVvp)) {
    $iverilog = $systemIverilog
    $vvp = $systemVvp
} else {
    throw 'Icarus Verilog not found in workspace .tools or C:\iverilog.'
}

$roadSource = Join-Path $projectRoot 'user_source\hdl_source\road_vision'
$sources = Get-ChildItem -LiteralPath $roadSource -Filter '*.v' |
    Sort-Object Name | ForEach-Object { $_.FullName }
$testbench = Join-Path $PSScriptRoot 'tb_video_replay.v'
$output = Join-Path $env:TEMP ("tb_video_replay_{0}.vvp" -f $PID)
$frameArg = $framePath.Replace('\', '/')
$resultArg = $resultPath.Replace('\', '/')

try {
    & $iverilog -g2012 -s tb_video_replay -o $output $testbench $sources
    if ($LASTEXITCODE -ne 0) {
        throw "Icarus compile failed with exit code $LASTEXITCODE."
    }
    & $vvp $output "+FRAME_DIR=$frameArg" "+RESULT_DIR=$resultArg" "+FRAMES=$Frames" "+THRESHOLD=$Threshold" "+ROW_GAP=$RowGap"
    if ($LASTEXITCODE -ne 0) {
        throw "RTL replay failed with exit code $LASTEXITCODE."
    }
} finally {
    Remove-Item -LiteralPath $output -Force -ErrorAction SilentlyContinue
}

Write-Output "RTL results: $resultPath"
