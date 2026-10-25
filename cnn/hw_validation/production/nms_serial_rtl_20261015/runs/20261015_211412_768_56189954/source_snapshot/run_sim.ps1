param(
    [string]$ModelSimBin = 'D:\modeltech64_2020.4\win64',
    [string]$RunRoot = ''
)

$ErrorActionPreference = 'Stop'
$sourceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$rtl = Join-Path $sourceRoot 'road_nms_serial.v'
$testbench = Join-Path $sourceRoot 'tb_road_nms_serial.v'
$vectorRoot = Join-Path $sourceRoot 'vectors'
$manifest = Join-Path $vectorRoot 'manifest.txt'
$referenceResult = Join-Path $sourceRoot 'reference_result.json'
$extraManifest = Join-Path $sourceRoot 'extras\manifest.txt'
$referenceExtraResult = Join-Path $sourceRoot 'reference_extra_result.json'
$referenceExtraWorstResult = Join-Path $sourceRoot 'reference_extra_worst_result.json'
$vlib = Join-Path $ModelSimBin 'vlib.exe'
$vlog = Join-Path $ModelSimBin 'vlog.exe'
$vsim = Join-Path $ModelSimBin 'vsim.exe'

foreach ($required in @($rtl, $testbench, $manifest, $referenceResult, $extraManifest,
                        $referenceExtraResult, $referenceExtraWorstResult, $vlib, $vlog, $vsim)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required file not found: $required"
    }
}

if (-not $RunRoot) {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $RunRoot = Join-Path $sourceRoot ("runs\{0}_{1}" -f $stamp, [guid]::NewGuid().ToString('N').Substring(0, 8))
}
$RunRoot = [IO.Path]::GetFullPath($RunRoot)
if (Test-Path -LiteralPath $RunRoot) {
    throw "Run directory already exists: $RunRoot"
}
[IO.Directory]::CreateDirectory($RunRoot) | Out-Null
$snapshotDir = Join-Path $RunRoot 'source_snapshot'
[IO.Directory]::CreateDirectory($snapshotDir) | Out-Null
$snapshotRtl = Join-Path $snapshotDir 'road_nms_serial.v'
$snapshotTb = Join-Path $snapshotDir 'tb_road_nms_serial.v'
$snapshotRunner = Join-Path $snapshotDir 'run_sim.ps1'
Copy-Item -LiteralPath $rtl -Destination $snapshotRtl
Copy-Item -LiteralPath $testbench -Destination $snapshotTb
Copy-Item -LiteralPath $MyInvocation.MyCommand.Path -Destination $snapshotRunner
$sourceStartHashes = [ordered]@{
    'road_nms_serial.v' = (Get-FileHash -Algorithm SHA256 -LiteralPath $snapshotRtl).Hash.ToLowerInvariant()
    'tb_road_nms_serial.v' = (Get-FileHash -Algorithm SHA256 -LiteralPath $snapshotTb).Hash.ToLowerInvariant()
    'run_sim.ps1' = (Get-FileHash -Algorithm SHA256 -LiteralPath $snapshotRunner).Hash.ToLowerInvariant()
}

function Invoke-LoggedProcess {
    param(
        [string]$Executable,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [string]$LogBase
    )
    $stdout = "$LogBase.stdout.log"
    $stderr = "$LogBase.stderr.log"
    $process = Start-Process -FilePath $Executable -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory -Wait -PassThru -NoNewWindow `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $combined = @()
    if (Test-Path -LiteralPath $stdout) { $combined += Get-Content -LiteralPath $stdout }
    if (Test-Path -LiteralPath $stderr) { $combined += Get-Content -LiteralPath $stderr }
    [IO.File]::WriteAllLines("$LogBase.log", [string[]]$combined)
    return $process.ExitCode
}

$manifestLines = @(Get-Content -LiteralPath $manifest | Where-Object { $_.Trim() })
if ($manifestLines[0] -match '^case_count=(\d+)$') {
    $caseCount = [int]$Matches[1]
} else {
    $caseCount = [int]$manifestLines[0]
}
if ($caseCount -ne 16 -or $manifestLines.Count -ne 17) {
    throw "Expected 16 vector cases in manifest, found $caseCount"
}

$cases = @()
foreach ($line in $manifestLines[1..16]) {
    $field = @($line -split '\s+' | Where-Object { $_ })
    if ($field.Count -ne 8) { throw "Malformed manifest row: $line" }
    $cases += [pscustomobject]@{
        Id = [int]$field[0]
        Person = [int]$field[1]
        Vehicle = [int]$field[2]
        Outputs = [int]$field[3]
        Comparisons = [int]$field[4]
        Decisions = [int]$field[5]
        Frozen = [int]$field[6]
        Analytic = [int]$field[7]
    }
}

$work = Join-Path $RunRoot 'work'
$compileExit = Invoke-LoggedProcess $vlib @('work') $RunRoot (Join-Path $RunRoot 'vlib')
if ($compileExit -ne 0) { throw "vlib failed; logs preserved at $RunRoot" }
$compileExit = Invoke-LoggedProcess $vlog @('-work', 'work', $snapshotRtl, $snapshotTb) $RunRoot (Join-Path $RunRoot 'compile')
if ($compileExit -ne 0) { throw "vlog failed; logs preserved at $RunRoot" }
$compileLog = Get-Content -Raw -LiteralPath (Join-Path $RunRoot 'compile.log')
if ($compileLog -match '(?m)\*\* Warning|Warnings:\s*[1-9]') {
    throw "vlog reported warnings; logs preserved at $RunRoot"
}

$results = [Collections.Generic.List[object]]::new()
$failure = $null

function Invoke-NmsCase {
    param(
        [pscustomobject]$Case,
        [int]$Pause,
        [int]$TestKind,
        [string]$Name
    )
    $caseName = 'case_{0:d2}' -f $Case.Id
    $caseDir = if ($Case.PSObject.Properties.Name -contains 'Directory') {
        $Case.Directory
    } else {
        Join-Path $vectorRoot $caseName
    }
    $candidateFile = Join-Path $caseDir 'candidate.hex'
    $expectedFile = Join-Path $caseDir 'expected.hex'
    $comparisonFile = Join-Path $caseDir 'comparisons.hex'
    $decisionFile = Join-Path $caseDir 'decisions.hex'
    foreach ($vectorFile in @($candidateFile, $expectedFile, $comparisonFile, $decisionFile)) {
        if (-not (Test-Path -LiteralPath $vectorFile -PathType Leaf)) {
            throw "Vector file not found: $vectorFile"
        }
    }
    $simDir = Join-Path $RunRoot $Name
    [IO.Directory]::CreateDirectory($simDir) | Out-Null
    $doFile = Join-Path $simDir 'run.do'
    [IO.File]::WriteAllLines($doFile, [string[]]@(
        'onbreak {quit -code 2}'
        'onerror {quit -code 2}'
        'run -all'
        'quit -code 0'
    ))
    $slash = { param($Path) ([IO.Path]::GetFullPath($Path) -replace '\\', '/') }
    $simArgs = @(
        '-c', '-quiet', '-voptargs=+acc', '-onfinish', 'exit',
        '-l', (Join-Path $simDir 'transcript.log'), 'work.tb_road_nms_serial',
        "+CANDIDATE=$(& $slash $candidateFile)",
        "+EXPECTED=$(& $slash $expectedFile)",
        "+COMPARISONS=$(& $slash $comparisonFile)",
        "+DECISIONS=$(& $slash $decisionFile)",
        "+COUNT_PERSON=$($Case.Person)", "+COUNT_VEHICLE=$($Case.Vehicle)",
        "+OUTPUT_COUNT=$($Case.Outputs)", "+COMPARISON_COUNT=$($Case.Comparisons)",
        "+DECISION_COUNT=$($Case.Decisions)", "+CASE_ID=$($Case.Id)",
        "+PAUSE=$Pause", "+TEST_KIND=$TestKind", '-do', $doFile
    )
    $exitCode = Invoke-LoggedProcess $vsim $simArgs $RunRoot (Join-Path $simDir 'vsim')
    $log = Get-Content -Raw -LiteralPath (Join-Path $simDir 'vsim.log')
    $passed = $exitCode -eq 0 -and $log -match 'TB_PASS_NMS' -and
              $log -notmatch 'Failed to open readmem' -and
              $log -notmatch '(?m)\*\* Warning|Warnings:\s*[1-9]'
    $metric = @([regex]::Matches($log, '(?m)^#?\s*CASE_RESULT .+$') | ForEach-Object { $_.Value.Trim() })
    $results.Add([pscustomobject]@{
        name = $Name
        case_id = $Case.Id
        pause = $Pause
        test_kind = $TestKind
        exit_code = $exitCode
        passed = $passed
        metrics = $metric
        directory = $simDir
    })
    if (-not $passed) {
        throw "Simulation failed: $Name; logs preserved at $simDir"
    }
}

$started = Get-Date
try {
    foreach ($case in $cases) {
        Invoke-NmsCase $case 0 0 ('vector_{0:d2}_normal' -f $case.Id)
        Invoke-NmsCase $case 1 0 ('vector_{0:d2}_random' -f $case.Id)
    }

    $faultCase = $cases | Where-Object Id -eq 1
    $faultKinds = [ordered]@{
        1 = 'wrong_response_class'
        2 = 'wrong_response_index'
        3 = 'wrong_data_class'
        4 = 'response_error'
        5 = 'out_of_range_index'
        6 = 'count_over_128'
        7 = 'coordinate_out_of_range'
        8 = 'reserved_bits_nonzero'
    }
    foreach ($entry in $faultKinds.GetEnumerator()) {
        Invoke-NmsCase $faultCase 1 ([int]$entry.Key) ("protocol_{0}" -f $entry.Value)
    }

    $recoveryCase = $cases | Where-Object Id -eq 10
    Invoke-NmsCase $recoveryCase 1 9 'protocol_late_error_after_output'
    $abortKinds = [ordered]@{
        20 = 'cancel_request_wait'
        21 = 'cancel_response_wait'
        22 = 'cancel_multiply'
        23 = 'cancel_partial_output'
        24 = 'reset_request_wait'
        25 = 'reset_response_wait'
        26 = 'reset_multiply'
        27 = 'reset_partial_output'
    }
    foreach ($entry in $abortKinds.GetEnumerator()) {
        Invoke-NmsCase $recoveryCase 1 ([int]$entry.Key) ("recovery_{0}" -f $entry.Value)
    }
    Invoke-NmsCase $recoveryCase 0 28 'protocol_output_backpressure_128'
    $extraCase = [pscustomobject]@{
        Id = 16
        Person = 4
        Vehicle = 4
        Outputs = 4
        Comparisons = 4
        Decisions = 8
        Frozen = 0
        Analytic = 1
        Directory = Join-Path $sourceRoot 'extras\full_frame_area'
    }
    Invoke-NmsCase $extraCase 0 0 'extra_full_frame_area_normal'
    Invoke-NmsCase $extraCase 1 0 'extra_full_frame_area_random'
    $extraWorstCase = [pscustomobject]@{
        Id = 17
        Person = 128
        Vehicle = 128
        Outputs = 64
        Comparisons = 6944
        Decisions = 256
        Frozen = 0
        Analytic = 1
        Directory = Join-Path $sourceRoot 'extras\worst_comparisons_full_output'
    }
    Invoke-NmsCase $extraWorstCase 0 0 'extra_worst_full_output_normal'
    Invoke-NmsCase $extraWorstCase 1 0 'extra_worst_full_output_random'
} catch {
    $failure = $_.Exception.Message
}

$sourceUnchanged = $true
foreach ($entry in $sourceStartHashes.GetEnumerator()) {
    $currentPath = if ($entry.Key -eq 'road_nms_serial.v') { $rtl } elseif ($entry.Key -eq 'tb_road_nms_serial.v') { $testbench } else { $MyInvocation.MyCommand.Path }
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $currentPath).Hash.ToLowerInvariant() -ne $entry.Value) {
        $sourceUnchanged = $false
        if (-not $failure) { $failure = "Bound source changed during run: $($entry.Key)" }
    }
}

$hashes = [ordered]@{}
$hashInputs = [ordered]@{
    'road_nms_serial.v' = $snapshotRtl
    'tb_road_nms_serial.v' = $snapshotTb
    'run_sim.ps1' = $snapshotRunner
    'vectors/manifest.txt' = $manifest
    'reference_result.json' = $referenceResult
    'extras/manifest.txt' = $extraManifest
    'reference_extra_result.json' = $referenceExtraResult
    'reference_extra_worst_result.json' = $referenceExtraWorstResult
}
foreach ($entry in $hashInputs.GetEnumerator()) {
    $hashes[$entry.Key] = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Value).Hash.ToLowerInvariant()
}
$finished = Get-Date
$summary = [ordered]@{
    status = if ($failure) { 'FAIL_MODELSIM_NMS' } else { 'PASS_MODELSIM_NMS' }
    source_root = $sourceRoot
    run_root = $RunRoot
    started = $started.ToString('o')
    finished = $finished.ToString('o')
    vector_cases = 16
    frozen_cases = @($cases | Where-Object Frozen -eq 1).Count
    analytic_cases = @($cases | Where-Object Analytic -eq 1).Count
    worst_comparisons = ($cases | Measure-Object Comparisons -Maximum).Maximum
    simulations_requested = 54
    simulations_completed = $results.Count
    simulations_passed = @($results | Where-Object passed).Count
    hashes = $hashes
    source_unchanged_during_run = $sourceUnchanged
    source_snapshot = $snapshotDir
    failure = $failure
    results = $results
    training_run = $false
    synthesis_run = $false
    bitstream_or_board = $false
}
$summaryPath = Join-Path $RunRoot 'summary.json'
[IO.File]::WriteAllText($summaryPath, ($summary | ConvertTo-Json -Depth 8) + [Environment]::NewLine)

if ($failure) {
    throw "$failure`nSummary: $summaryPath"
}
Write-Host "PASS_MODELSIM_NMS runs=$($results.Count) frozen=11 analytic=7 worst_comparisons=6944"
Write-Host "SUMMARY=$summaryPath"
