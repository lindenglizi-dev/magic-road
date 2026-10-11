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
    throw 'Icarus Verilog not found in workspace .tools or C:\iverilog.'
}

$roadSource = Join-Path $projectRoot 'user_source\hdl_source\road_vision'
$sources = Get-ChildItem -LiteralPath $roadSource -Filter '*.v' |
    Sort-Object Name |
    ForEach-Object { $_.FullName }
$sources += Join-Path $PSScriptRoot 'ph1p_logic_eram_sim.v'

$tests = @(
    @{ Top = 'tb_hog_linear_svm'; File = 'tb_hog_linear_svm.v' },
    @{ Top = 'tb_hog_frontend'; File = 'tb_hog_frontend.v' },
    @{ Top = 'tb_roi_object_snapshot_cdc'; File = 'tb_roi_object_snapshot_cdc.v' },
    @{ Top = 'tb_roi_frame_reader'; File = 'tb_roi_frame_reader.v' },
    @{ Top = 'tb_gray_frame_pingpong'; File = 'tb_gray_frame_pingpong.v' },
    @{ Top = 'tb_binary_cleanup_3x3'; File = 'tb_binary_cleanup_3x3.v' },
    @{ Top = 'tb_lab1_road_chain'; File = 'tb_lab1_road_chain.v' },
    @{ Top = 'tb_track_overlay'; File = 'tb_track_overlay.v' },
    @{ Top = 'tb_background_address_guard'; File = 'tb_background_address_guard.v' },
    @{ Top = 'tb_object_discard'; File = 'tb_object_discard.v' }
)

foreach ($test in $tests) {
    $testbench = Join-Path $PSScriptRoot $test.File
    $output = Join-Path $env:TEMP ("{0}_{1}.vvp" -f $test.Top, $PID)
    try {
        & $iverilog -g2012 -s $test.Top -o $output $testbench $sources
        if ($LASTEXITCODE -ne 0) {
            throw "Icarus compile failed for $($test.Top) with exit code $LASTEXITCODE."
        }

        & $vvp $output
        if ($LASTEXITCODE -ne 0) {
            throw "RTL simulation failed for $($test.Top) with exit code $LASTEXITCODE."
        }
    } finally {
        Remove-Item -LiteralPath $output -Force -ErrorAction SilentlyContinue
    }
}
