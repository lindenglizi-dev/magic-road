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
$temporary = Join-Path $env:TEMP ("hog_svm_training_{0}" -f $PID)
$simulation = Join-Path $temporary 'tb_hog_svm_generated.vvp'
$trainer = Join-Path $projectRoot 'tools\train_hog_svm.py'
$testbench = Join-Path $PSScriptRoot 'tb_hog_svm_generated.v'
$svm = Join-Path $projectRoot 'user_source\hdl_source\road_vision\hog_linear_svm.v'

New-Item -ItemType Directory -Path $temporary -Force | Out-Null
try {
    & $python $trainer --self-test --output $temporary
    if ($LASTEXITCODE -ne 0) { throw 'Synthetic SVM training/export failed.' }

    $rom = Join-Path $temporary 'hog_svm_weights.v'
    & $iverilog -g2012 -s tb_hog_svm_generated -o $simulation `
        $testbench $svm $rom
    if ($LASTEXITCODE -ne 0) { throw 'Generated SVM ROM RTL compile failed.' }

    $feature = (Join-Path $temporary 'svm_test_feature.hex').Replace('\', '/')
    $score = (Join-Path $temporary 'svm_test_score.hex').Replace('\', '/')
    $class = (Join-Path $temporary 'svm_test_class.hex').Replace('\', '/')
    & $vvp $simulation "+FEATURE=$feature" "+SCORE=$score" "+CLASS=$class"
    if ($LASTEXITCODE -ne 0) { throw 'Generated SVM ROM/RTL score mismatch.' }
} finally {
    Remove-Item -LiteralPath $temporary -Recurse -Force -ErrorAction SilentlyContinue
}
