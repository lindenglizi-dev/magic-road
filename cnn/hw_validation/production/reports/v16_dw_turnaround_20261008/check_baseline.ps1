$ErrorActionPreference = 'Stop'
$receipt = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'baseline_freeze.json') -Raw | ConvertFrom-Json
$baseline = Join-Path $PSScriptRoot $receipt.baseline
foreach ($entry in $receipt.files.PSObject.Properties) {
    $actual = (Get-FileHash -LiteralPath (Join-Path $baseline $entry.Name) -Algorithm SHA256).Hash.ToLower()
    if ($actual -ne $entry.Value) { throw "Frozen baseline changed: $($entry.Name)" }
    Write-Output "PASS $($entry.Name) $actual"
}
