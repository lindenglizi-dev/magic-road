param([string]$ModelSimBin = 'D:\modeltech64_2020.4\win64')

$ErrorActionPreference = 'Stop'
$traceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$publisherPath = Join-Path (Split-Path -Parent $traceRoot) 'rtl\road_result_publisher.v'
$expectedPublisherHash = 'c9b25968c51827f0a1856a5bcf5618c64742c04641629ac0c3ca4412847939f0'
if ((Get-FileHash -LiteralPath $publisherPath).Hash.ToLowerInvariant() -ne $expectedPublisherHash) {
    throw 'Publisher differs from the exact confirmed RTL source'
}
$vectorReceipt = Get-Content -Raw -LiteralPath (Join-Path $traceRoot 'trace_vector_receipt.json') | ConvertFrom-Json
foreach ($property in $vectorReceipt.sha256.PSObject.Properties) {
    $filePath = Join-Path $traceRoot $property.Name
    if ($property.Name -in @('reference.py', 'publisher_spec.json')) {
        $filePath = Join-Path (Split-Path -Parent $traceRoot) $property.Name
    }
    if ((Get-FileHash -LiteralPath $filePath).Hash.ToLowerInvariant() -ne $property.Value) {
        throw "Trace input closure changed: $($property.Name)"
    }
}
$runPath = Join-Path $traceRoot ('trace_runs\' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))
New-Item -ItemType Directory -Path $runPath | Out-Null
$tbPath = Join-Path $traceRoot 'tb_road_result_publisher_trace.v'
$vectorPath = (Join-Path $traceRoot 'publisher_trace.hex').Replace('\', '/')
$receipt = [ordered]@{
    status = 'FAIL'; scope = 'Python golden versus exact publisher RTL only'; cycles = 500; cases = 33
    preedge_output_fields = 13; postedge_internal_fields = @('state_current', 'cnt_entry')
    publisher_sha256 = $expectedPublisherHash
    vector_sha256 = (Get-FileHash -LiteralPath (Join-Path $traceRoot 'publisher_trace.hex')).Hash.ToLowerInvariant()
    testbench_sha256 = (Get-FileHash -LiteralPath $tbPath).Hash.ToLowerInvariant()
    runner_sha256 = (Get-FileHash -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant()
    tool_sha256 = [ordered]@{}; run_path = $runPath; error = $null
}
foreach ($tool in @('vlib', 'vlog', 'vsim')) {
    $receipt.tool_sha256[$tool] = (Get-FileHash -LiteralPath (Join-Path $ModelSimBin ($tool + '.exe'))).Hash.ToLowerInvariant()
}
function Invoke-TraceProcess {
    param([string]$Tool, [string[]]$ToolArguments, [string]$LogName)
    $logPath = Join-Path $runPath $LogName
    $process = Start-Process -FilePath (Join-Path $ModelSimBin ($Tool + '.exe')) -ArgumentList $ToolArguments -WorkingDirectory $runPath -WindowStyle Hidden -Wait -PassThru -RedirectStandardOutput $logPath -RedirectStandardError ($logPath + '.stderr')
    if ($process.ExitCode -ne 0) { throw "$Tool exit $($process.ExitCode)" }
}
Push-Location $runPath
try {
    Invoke-TraceProcess 'vlib' @('work') 'vlib.log'
    Invoke-TraceProcess 'vlog' @('-work', 'work', $publisherPath, $tbPath) 'compile.log'
    Invoke-TraceProcess 'vsim' @('-c', '-quiet', '-voptargs=+acc', '-onfinish', 'exit', 'work.tb_road_result_publisher_trace', "+vectors=$vectorPath", '-do', (Join-Path $traceRoot 'trace_sim.do')) 'simulation.log'
    $simulationText = (Get-Content -Raw -LiteralPath (Join-Path $runPath 'simulation.log')) + (Get-Content -Raw -LiteralPath (Join-Path $runPath 'simulation.log.stderr'))
    if ($simulationText -notmatch 'TRACE_PASS cycles=500 cases=33' -or $simulationText -match 'TRACE_ERROR|\*\* Error|\*\* Fatal') {
        throw 'Simulation did not provide the complete full-output PASS marker'
    }
    if ((Get-FileHash -LiteralPath $publisherPath).Hash.ToLowerInvariant() -ne $expectedPublisherHash) {
        throw 'Publisher source changed during the simulation'
    }
    $receipt.status = 'PASS'
} catch {
    $receipt.error = $_.Exception.Message
} finally {
    Pop-Location
    $receipt | ConvertTo-Json -Depth 8 | Set-Content -Encoding utf8 -LiteralPath (Join-Path $runPath 'result.json')
    $receipt | ConvertTo-Json -Depth 8
}
if ($receipt.status -ne 'PASS') { exit 1 }
