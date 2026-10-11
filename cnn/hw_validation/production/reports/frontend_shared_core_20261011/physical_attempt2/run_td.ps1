param([switch]$Execute)

$physicalRoot = $PSScriptRoot
$python = Get-Command python -ErrorAction Stop
& $python.Source (Join-Path $physicalRoot 'physical_report.py') preflight
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not $Execute) {
    Write-Output 'PREPARED_ONLY: TD was not executed. Re-run with -Execute only after functional regression approval.'
    exit 0
}

$td = 'E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe'
if (-not (Test-Path -LiteralPath $td -PathType Leaf)) { throw "TD executable not found: $td" }
$started = Get-Date
Push-Location -LiteralPath $physicalRoot
try {
    & $td 'build.tcl' 2>&1 | Tee-Object -FilePath 'td_launcher.log'
    $returnCode = $LASTEXITCODE
    [ordered]@{
        command = @($td, 'build.tcl')
        cwd = $physicalRoot
        started = $started.ToString('o')
        finished = (Get-Date).ToString('o')
        returncode = $returnCode
    } | ConvertTo-Json | Set-Content -LiteralPath 'td.command.json' -Encoding utf8
    if ($returnCode -ne 0) { exit $returnCode }
    & $python.Source (Join-Path $physicalRoot 'physical_report.py') summarize
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
