$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path $PSScriptRoot -Parent
$workspaceRoot = Split-Path (Split-Path $projectRoot -Parent) -Parent
$localIverilog = Join-Path $workspaceRoot '.tools\iverilog\bin\iverilog.exe'
$localVvp = Join-Path $workspaceRoot '.tools\iverilog\bin\vvp.exe'
$systemIverilog = 'C:\iverilog\bin\iverilog.exe'
$systemVvp = 'C:\iverilog\bin\vvp.exe'

if ((Test-Path -LiteralPath $localIverilog) -and
    (Test-Path -LiteralPath $localVvp)) {
    $iverilog = $localIverilog
    $vvp = $localVvp
} elseif ((Test-Path -LiteralPath $systemIverilog) -and
          (Test-Path -LiteralPath $systemVvp)) {
    $iverilog = $systemIverilog
    $vvp = $systemVvp
} else {
    throw 'Icarus Verilog not found.'
}

$python = Get-Command python -ErrorAction Stop | Select-Object -ExpandProperty Source
$generated = Join-Path $env:TEMP ("hog_crosscheck_{0}" -f $PID)
$roi = Join-Path $generated 'hog_roi.hex'
$expected = Join-Path $generated 'hog_expected.hex'
$actual = Join-Path $generated 'hog_actual.hex'
$simulation = Join-Path $env:TEMP ("tb_hog_crosscheck_{0}.vvp" -f $PID)
$reference = Join-Path $projectRoot 'tools\hog_reference.py'
$gradient = Join-Path $projectRoot 'user_source\hdl_source\road_vision\hog_sobel_gradient.v'
$histogram = Join-Path $projectRoot 'user_source\hdl_source\road_vision\hog_cell_histogram.v'
$testbench = Join-Path $PSScriptRoot 'tb_hog_crosscheck.v'

New-Item -ItemType Directory -Path $generated -Force | Out-Null

try {
    & $python $reference --generate --roi $roi --expected $expected
    if ($LASTEXITCODE -ne 0) { throw 'HOG reference generation failed.' }

    & $iverilog -g2012 -s tb_hog_crosscheck -o $simulation `
        $testbench $gradient $histogram
    if ($LASTEXITCODE -ne 0) { throw 'HOG cross-check RTL compile failed.' }

    $roiArg = $roi.Replace('\', '/')
    $actualArg = $actual.Replace('\', '/')
    & $vvp $simulation "+ROI=$roiArg" "+OUT=$actualArg"
    if ($LASTEXITCODE -ne 0) { throw 'HOG cross-check RTL simulation failed.' }

    & $python $reference --roi $roi --expected $expected --actual $actual
    if ($LASTEXITCODE -ne 0) { throw 'HOG software/RTL comparison failed.' }
} finally {
    Remove-Item -LiteralPath $simulation -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $generated -Recurse -Force -ErrorAction SilentlyContinue
}
