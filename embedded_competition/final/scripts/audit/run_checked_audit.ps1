$ErrorActionPreference='Stop'
$taskPython='python'
& $taskPython (Join-Path $PSScriptRoot 'audit_preflight.py') --require-checked
if($LASTEXITCODE -ne 0){throw 'PENDING: completed current route/qualification/source/flow evidence is required; no physical export or approval performed'}
$taskStarted=Get-Date
& $env:TD_EXEC ((Join-Path $PSScriptRoot 'run_checked_audit.tcl').Replace('\','/')) *> (Join-Path $PSScriptRoot 'checked_clock_audit.log')
$taskExit=$LASTEXITCODE
$taskLog=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'checked_clock_audit.log') -Raw
$taskMarker=$taskLog.Contains('CHECKED_CLOCK_EVIDENCE_EXPORTED_NOT_INDEPENDENTLY_APPROVED')
[ordered]@{started=$taskStarted.ToString('o');finished=(Get-Date).ToString('o');exit=$taskExit;export_marker=$taskMarker;scope='Native read-only checked DB report/netlist/constraint export; no independent approval, implementation, bitgen or board action'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'checked_export_receipt.json') -Encoding utf8
if($taskExit -ne 0 -or !$taskMarker){throw 'Native checked evidence collection incomplete; offline review remains pending'}
Write-Output 'EXPORTED_CURRENT_CHECKED_EVIDENCE_ONLY; independent offline reviews still required'
