$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$baseline = Join-Path (Split-Path -Parent $PSScriptRoot) 'v17_pw_prefetch_20261008'
$manifest = Get-Content -LiteralPath (Join-Path $baseline 'source_manifest.json') -Raw | ConvertFrom-Json
foreach ($entry in $manifest.files.PSObject.Properties) {
    if ((Get-FileHash -LiteralPath (Join-Path $baseline $entry.Name) -Algorithm SHA256).Hash.ToLower() -ne $entry.Value) {
        throw "Frozen baseline changed: $($entry.Name)"
    }
}
$log = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'closure_trace.log') -Raw
if ($log -match 'CLOSURE_ERROR|TB_FAIL' -or $log -notmatch 'TB_PASS_DOWN2_TILE cases=4') { throw 'Regression or observer failed' }
foreach ($pattern in @('age=5 final_valid=0001', 'age=6 final_valid=0010', 'age=7 final_valid=0100', 'age=8 final_valid=1000', 'age=9 final_valid=0000 output_valid=1', 'CLOSURE_ACK case=3 .* age=10 errors=0')) {
    if ($log -notmatch $pattern) { throw "Missing trace evidence: $pattern" }
}
foreach ($entry in $manifest.vectors.PSObject.Properties) {
    $expected = $entry.Value
    foreach ($path in @((Join-Path $baseline "verification/regression_candidate/vectors/$($entry.Name)"), (Join-Path $PSScriptRoot "vectors/$($entry.Name)"))) {
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower() -ne $expected) { throw "Vector changed: $path" }
    }
}
foreach ($name in @('down2_overlap_tile_runner.v','road_mac_probe.v','road_round_shift.v','silu_shared_unit.v','road_postprocess_stream.v','ph1p_logic_eram_runtime_model.v','tb_down2_overlap_tile_runner.v')) {
    if ((Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $name) -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath (Join-Path $baseline "verification/regression_candidate/$name") -Algorithm SHA256).Hash) { throw "Copied input changed: $name" }
}
Write-Output 'PASS: baseline 17 files, 20 vectors, 7 copied sources unchanged; closure trace and original regression passed.'
