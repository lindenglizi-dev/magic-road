param(
    [string]$ModelSimBin = 'D:\modeltech64_2020.4\win64',
    [string]$RunRoot = '',
    [switch]$Smoke
)

$ErrorActionPreference = 'Stop'
$sourceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [IO.Path]::GetFullPath((Join-Path $sourceRoot '..\..\..\..\..'))
$oldRoot = [IO.Path]::GetFullPath((Join-Path (Split-Path -Parent $sourceRoot) '..\postprocess_joint_1fps_20261015'))
$manifestPath = Join-Path $oldRoot 'vector_manifest.json'
$verifierPath = Join-Path $oldRoot 'verify_vectors.py'
$bindingChecker = Join-Path (Split-Path -Parent $sourceRoot) 'check_inputs.py'
$actualClosure = Join-Path (Split-Path -Parent $sourceRoot) 'vendor_rom'
$actualArtifacts = Join-Path $actualClosure 'artifacts'
$actualManifest = Join-Path $actualArtifacts 'manifest.json'
if (-not (Test-Path -LiteralPath (Join-Path $actualClosure 'source_receipt.json') -PathType Leaf)) {
    throw 'Stable actual ROM closure has not been handed off; controlled verification remains separate.'
}
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $actualManifest).Hash.ToLowerInvariant() -ne '93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b') {
    throw 'Actual ROM manifest is not the frozen true G10 package'
}
$laneFiles = @(Get-ChildItem -LiteralPath $actualArtifacts -File -Filter 'group_*_lane_*.dath')
if ($laneFiles.Count -ne 56) { throw 'Actual ROM needs exactly 56 frozen lane files' }
$actualReceipt = Get-Content -Raw -LiteralPath (Join-Path $actualClosure 'source_receipt.json') | ConvertFrom-Json
if ($actualReceipt.status -ne 'PASS' -or -not $actualReceipt.snapshot_unchanged) {
    throw 'Actual ROM source receipt is not a stable passed C2 snapshot'
}
foreach ($file in Get-ChildItem -LiteralPath $actualClosure -Recurse -File) {
    $relative = $file.FullName.Substring($actualClosure.Length + 1).Replace('\','/')
    if ($relative -eq 'source_receipt.json') { continue }
    $expectedHash = $actualReceipt.closure_sha256.PSObject.Properties[$relative].Value
    if (-not $expectedHash -or (Get-FileHash -LiteralPath $file.FullName).Hash.ToLowerInvariant() -ne $expectedHash) {
        throw "Frozen C2 actual ROM closure mismatch: $relative"
    }
}
$tbPath = Join-Path $sourceRoot 'tb_road_postprocess_real_rom.v'
$runnerPath = $MyInvocation.MyCommand.Path
$rtlPaths = [ordered]@{
    'road_candidate_ram.v' = Join-Path (Split-Path -Parent $sourceRoot) 'rtl\road_candidate_ram.v'
    'road_head_decode_topk.v' = Join-Path (Split-Path -Parent $sourceRoot) 'rtl\road_head_decode_topk.v'
    'road_numeric_rom_reader.v' = Join-Path $actualClosure 'rtl\road_numeric_rom_reader.v'
    'road_yolo_numeric_rom_group.v' = Join-Path $actualClosure 'rtl\road_yolo_numeric_rom_group.v'
    'ph1p_logic_eram.v' = Join-Path $actualClosure 'vendor\ph1p_logic_eram.v'
    'ph1p_phy_gsr.v' = Join-Path $actualClosure 'vendor\ph1p_phy_gsr.v'
    'road_shared_lut_service.v' = Join-Path (Split-Path -Parent $sourceRoot) 'rtl\road_shared_lut_service.v'
    'road_nms_serial.v' = Join-Path (Split-Path -Parent $sourceRoot) 'rtl\road_nms_serial.v'
}
$physicalPath = Join-Path $repoRoot 'cnn\hw_validation\production\shared_lut_service_1fps_20261015\verification\assets\physical_words_160.hex'
$python = [IO.Path]::GetFullPath((Join-Path $repoRoot '..\..\.tools\road_yolo_venv\Scripts\python.exe'))
$vlib = Join-Path $ModelSimBin 'vlib.exe'
$vlog = Join-Path $ModelSimBin 'vlog.exe'
$vsim = Join-Path $ModelSimBin 'vsim.exe'

foreach ($required in @($manifestPath, $verifierPath, $tbPath, $physicalPath, $bindingChecker,
                         $python, $rtlPaths.Values, $vlib, $vlog, $vsim)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required file not found: $required"
    }
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$allCases = @($manifest.cases) + @($manifest.joint_extra_cases)
$caseNames = @(
    'real_image', 'all_low_empty_complete_table',
    'top128_ties_and_each32_total64', 'same_class_duplicate_suppressed',
    'threshold_equal_inclusive_and_below', 'person_vehicle_same_box_not_suppressed',
    'worst_comparisons_full_output'
)
$caseMap = @{}
foreach ($caseName in $caseNames) {
    $match = @($allCases | Where-Object name -eq $caseName)
    if ($match.Count -ne 1) { throw "Manifest case is not unique: $caseName" }
    $caseMap[$caseName] = $match[0]
}

function Resolve-ManifestPath {
    param([string]$RelativePath)
    return [IO.Path]::GetFullPath((Join-Path $repoRoot ($RelativePath -replace '/', '\')))
}

$vectorFiles = [Collections.Generic.List[string]]::new()
foreach ($caseName in $caseNames) {
    $case = $caseMap[$caseName]
    foreach ($path in @((Resolve-ManifestPath $case.heads112.path),
                         (Resolve-ManifestPath $case.final97.path))) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Vector file not found: $path"
        }
        $vectorFiles.Add($path)
    }
}

if (-not $RunRoot) {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $RunRoot = Join-Path $sourceRoot ("runs\{0}_{1}" -f $stamp, [guid]::NewGuid().ToString('N').Substring(0, 8))
}
$RunRoot = [IO.Path]::GetFullPath($RunRoot)
if (Test-Path -LiteralPath $RunRoot) { throw "Run directory already exists: $RunRoot" }
[IO.Directory]::CreateDirectory($RunRoot) | Out-Null
Copy-Item -LiteralPath $actualArtifacts -Destination (Join-Path $RunRoot 'artifacts') -Recurse
$snapshotDir = Join-Path $RunRoot 'source_snapshot'
[IO.Directory]::CreateDirectory($snapshotDir) | Out-Null

$boundSources = [ordered]@{}
foreach ($entry in $rtlPaths.GetEnumerator()) {
    $destination = Join-Path $snapshotDir $entry.Key
    Copy-Item -LiteralPath $entry.Value -Destination $destination
    $boundSources[$entry.Key] = $destination
}
$snapshotTb = Join-Path $snapshotDir 'tb_road_postprocess_real_rom.v'
$snapshotRunner = Join-Path $snapshotDir 'run_vendor_rom.ps1'
Copy-Item -LiteralPath $tbPath -Destination $snapshotTb
Copy-Item -LiteralPath $runnerPath -Destination $snapshotRunner
$boundSources['tb_road_postprocess_real_rom.v'] = $snapshotTb
$boundSources['run_vendor_rom.ps1'] = $snapshotRunner

$watchedInputs = [ordered]@{}
foreach ($entry in $rtlPaths.GetEnumerator()) { $watchedInputs[$entry.Key] = $entry.Value }
$watchedInputs['tb_road_postprocess_real_rom.v'] = $tbPath
$watchedInputs['run_vendor_rom.ps1'] = $runnerPath
$watchedInputs['vector_manifest.json'] = $manifestPath
$watchedInputs['verify_vectors.py'] = $verifierPath
$watchedInputs['physical_words_160.hex'] = $physicalPath
$watchedInputs['check_inputs.py'] = $bindingChecker
foreach ($path in $vectorFiles | Select-Object -Unique) {
    $watchedInputs[('vector/' + [IO.Path]::GetFileName((Split-Path -Parent $path)) + '/' + [IO.Path]::GetFileName($path))] = $path
}
foreach ($file in Get-ChildItem -LiteralPath $actualClosure -Recurse -File) {
    $watchedInputs['actual_closure/' + $file.FullName.Substring($actualClosure.Length + 1).Replace('\','/')] = $file.FullName
}
$startHashes = [ordered]@{}
foreach ($entry in $watchedInputs.GetEnumerator()) {
    $startHashes[$entry.Key] = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Value).Hash.ToLowerInvariant()
}

function Invoke-LoggedProcess {
    param([string]$Executable, [string[]]$ArgumentList,
          [string]$WorkingDirectory, [string]$LogBase)
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

$bindingExit = Invoke-LoggedProcess $python @('-B', '-X', 'utf8', $bindingChecker) $repoRoot (Join-Path $RunRoot 'input_binding_before')
if ($bindingExit -ne 0) { throw "True-model input binding failed; logs preserved at $RunRoot" }
$verifyExit = Invoke-LoggedProcess $python @('-B', '-X', 'utf8', $verifierPath, '--check') $repoRoot (Join-Path $RunRoot 'vector_check')
if ($verifyExit -ne 0) { throw "Vector checker failed; logs preserved at $RunRoot" }
$verifyLog = Get-Content -Raw -LiteralPath (Join-Path $RunRoot 'vector_check.log')
if ($verifyLog -notmatch 'JOINT_VECTOR_CHECK_PASS') {
    throw "Vector checker did not report PASS; logs preserved at $RunRoot"
}

$vlibExit = Invoke-LoggedProcess $vlib @('work') $RunRoot (Join-Path $RunRoot 'vlib')
if ($vlibExit -ne 0) { throw "vlib failed; logs preserved at $RunRoot" }
$compileArgs = @('+define+USE_VENDOR_ROM', '-work', 'work', $boundSources['ph1p_logic_eram.v'],
                 $boundSources['ph1p_phy_gsr.v'], $boundSources['road_yolo_numeric_rom_group.v'],
                 $boundSources['road_numeric_rom_reader.v'], $boundSources['road_candidate_ram.v'],
                 $boundSources['road_head_decode_topk.v'], $boundSources['road_nms_serial.v'],
                 $boundSources['road_shared_lut_service.v'], $snapshotTb)
$compileExit = Invoke-LoggedProcess $vlog $compileArgs $RunRoot (Join-Path $RunRoot 'compile')
if ($compileExit -ne 0) { throw "vlog failed; logs preserved at $RunRoot" }
$compileLog = Get-Content -Raw -LiteralPath (Join-Path $RunRoot 'compile.log')
if ($compileLog -match '(?m)\*\* Warning|Warnings:\s*[1-9]') {
    throw "vlog reported warnings; logs preserved at $RunRoot"
}

$results = [Collections.Generic.List[object]]::new()
$failure = $null
$slash = { param($Path) ([IO.Path]::GetFullPath($Path) -replace '\\', '/') }

function Invoke-JointCase {
    param([string]$Name, [pscustomobject]$Case, [int]$Mode, [int]$Stall,
          [pscustomobject]$SecondCase = $null)
    $head = Resolve-ManifestPath $Case.heads112.path
    $expected = Resolve-ManifestPath $Case.final97.path
    if (-not $SecondCase) { $SecondCase = $Case }
    $head2 = Resolve-ManifestPath $SecondCase.heads112.path
    $expected2 = Resolve-ManifestPath $SecondCase.final97.path
    foreach ($required in @($head, $expected, $head2, $expected2)) {
        if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
            throw "Vector file not found: $required"
        }
    }
    $simDir = Join-Path $RunRoot $Name
    [IO.Directory]::CreateDirectory($simDir) | Out-Null
    $doFile = Join-Path $simDir 'run.do'
    [IO.File]::WriteAllLines($doFile, [string[]]@(
        'onbreak {quit -code 2}', 'onerror {quit -code 2}',
        'run -all', 'quit -code 0'
    ))
    $simArgs = @(
        '-c', '-quiet', '-voptargs=+acc', '-onfinish', 'exit',
        '-l', (Join-Path $simDir 'transcript.log'), 'work.PH1P_PHY_GSR', 'work.tb_road_postprocess_real_rom',
        "+MODE=$Mode", "+STALL=$Stall", "+HEAD=$(& $slash $head)",
        "+EXPECTED=$(& $slash $expected)",
        "+EXPECT_PERSON=$($Case.expected.person_candidates)",
        "+EXPECT_VEHICLE=$($Case.expected.vehicle_candidates)",
        "+EXPECT_OUTPUTS=$($Case.expected.final_entries)",
        "+HEAD2=$(& $slash $head2)", "+EXPECTED2=$(& $slash $expected2)",
        "+EXPECT2_PERSON=$($SecondCase.expected.person_candidates)",
        "+EXPECT2_VEHICLE=$($SecondCase.expected.vehicle_candidates)",
        "+EXPECT2_OUTPUTS=$($SecondCase.expected.final_entries)",
        "+PHYSICAL=$(& $slash $physicalPath)",
        '+MAX_CYCLES=30000000', '-do', $doFile
    )
    $exitCode = Invoke-LoggedProcess $vsim $simArgs $RunRoot (Join-Path $simDir 'vsim')
    $log = Get-Content -Raw -LiteralPath (Join-Path $simDir 'vsim.log')
    # Retain and classify the exact known encrypted-vendor diagnostic; do not suppress warnings.
    $warnings = @([regex]::Matches($log, '(?m)^#?\s*\*\* Warning[^\r\n]*') | ForEach-Object { $_.Value.Trim() })
    $knownVendorWarnings = @($warnings | Where-Object {
        $_ -match "ph1p_logic_eram\.v\(165\): \(vopt-2697\) (MSB 167999|LSB 167928) of part-select into 'INIT_FILE' is out of bounds\."
    })
    $unexpectedWarnings = @($warnings | Where-Object { $_ -notin $knownVendorWarnings })
    $cachedOptimization = $log -match '\(vsim-8009\) Loading existing optimized design _opt'
    $knownWarningClosure = $knownVendorWarnings.Count -eq 112 -or
                          ($knownVendorWarnings.Count -eq 0 -and $cachedOptimization)
    $passed = $exitCode -eq 0 -and $log -match 'TB_PASS_POSTPROCESS_REAL_ROM' -and
              $log -notmatch 'TB_ERROR|\*\* Fatal|\*\* Error|Failed to open readmem|\(vsim-7\)' -and
              $unexpectedWarnings.Count -eq 0 -and $knownWarningClosure
    $metrics = @([regex]::Matches($log, '(?m)^#?\s*(JOINT_RESULT|C2_RESULT|NMS_RESULT|ROM_RESULT) .+$') |
                 ForEach-Object { $_.Value.Trim() })
    $results.Add([pscustomobject]@{
        name = $Name; case = $Case.name; mode = $Mode; stall = $Stall
        second_case = $SecondCase.name; exit_code = $exitCode; passed = $passed
        metrics = $metrics; directory = $simDir
        budget_passed = $log -notmatch 'TB_BUDGET_FAIL'
        endpoint = 'actual_PH1P_true_G10_single_reader_56lanes'
        warning_status = 'UNRESOLVED_ENCRYPTED_VENDOR_INIT_FILE_BOUNDS'
        known_vendor_warnings = $knownVendorWarnings.Count
        cached_optimization = $cachedOptimization
        unexpected_warnings = $unexpectedWarnings
    })
    if (-not $passed) { throw "Simulation failed: $Name; logs preserved at $simDir" }
}

$started = Get-Date
try {
    if ($Smoke) {
        Invoke-JointCase 'real_image_smoke' $caseMap['real_image'] 0 0
    } else {
    foreach ($caseName in @('real_image', 'all_low_empty_complete_table',
                            'top128_ties_and_each32_total64', 'same_class_duplicate_suppressed',
                            'threshold_equal_inclusive_and_below',
                            'person_vehicle_same_box_not_suppressed',
                            'worst_comparisons_full_output')) {
        Invoke-JointCase ("{0}_normal" -f $caseName) $caseMap[$caseName] 0 0
        Invoke-JointCase ("{0}_random" -f $caseName) $caseMap[$caseName] 0 1
    }
    Invoke-JointCase 'consecutive_real_then_empty' $caseMap['real_image'] 1 1 $caseMap['all_low_empty_complete_table']
    Invoke-JointCase 'reset_scan_recover' $caseMap['real_image'] 2 1
    Invoke-JointCase 'reset_sort_recover' $caseMap['real_image'] 3 1
    Invoke-JointCase 'reset_decode_recover' $caseMap['real_image'] 4 1
    Invoke-JointCase 'reset_nms_multiply_recover' $caseMap['real_image'] 5 1
    Invoke-JointCase 'reset_held_output_recover' $caseMap['real_image'] 6 1
    Invoke-JointCase 'late_response_error_cancel_recover' $caseMap['real_image'] 7 1
    Invoke-JointCase 'output_backpressure_128' $caseMap['real_image'] 8 0
    Invoke-JointCase 'cancel_accepted_rom_late_drain_recover' $caseMap['real_image'] 9 1
    Invoke-JointCase 'reset_accepted_rom_recover' $caseMap['real_image'] 10 1
    }
} catch {
    $failure = $_.Exception.Message
}

$bindingExit = Invoke-LoggedProcess $python @('-B', '-X', 'utf8', $bindingChecker) $repoRoot (Join-Path $RunRoot 'input_binding_after')
if ($bindingExit -ne 0 -and -not $failure) { $failure = 'Input binding changed after run' }
$sourceUnchanged = $true
foreach ($entry in $watchedInputs.GetEnumerator()) {
    $endHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry.Value).Hash.ToLowerInvariant()
    if ($endHash -ne $startHashes[$entry.Key]) {
        $sourceUnchanged = $false
        if (-not $failure) { $failure = "Bound input changed during run: $($entry.Key)" }
    }
}

$finished = Get-Date
$summary = [ordered]@{
    status = if ($failure) { 'FAIL_MODELSIM_POSTPROCESS_VENDOR_ROM' } else { 'PASS_MODELSIM_POSTPROCESS_VENDOR_ROM' }
    run_root = $RunRoot
    started = $started.ToString('o')
    finished = $finished.ToString('o')
    simulations_requested = if ($Smoke) { 1 } else { 24 }
    endpoint = 'actual_PH1P_true_G10_single_reader_56lanes'
    warning_status = 'UNRESOLVED_ENCRYPTED_VENDOR_INIT_FILE_BOUNDS'
    budget_status = if (@($results | Where-Object { -not $_.budget_passed }).Count) { 'FAIL_POSTPROCESS_2M_BUDGET' } else { 'PASS_POSTPROCESS_2M_BUDGET' }
    simulations_completed = $results.Count
    simulations_passed = @($results | Where-Object passed).Count
    source_unchanged_during_run = $sourceUnchanged
    source_snapshot = $snapshotDir
    hashes = $startHashes
    tool_hashes = @{vlib=(Get-FileHash -LiteralPath $vlib).Hash; vlog=(Get-FileHash -LiteralPath $vlog).Hash; vsim=(Get-FileHash -LiteralPath $vsim).Hash; python=(Get-FileHash -LiteralPath $python).Hash}
    failure = $failure
    results = $results
    decode_topk_nms_allowance_cycles = 2000000
    whole_frame_planning_cycles = 100000000
    training_run = $false
    synthesis_run = $false
    timing_run = $false
    bitstream_or_board = $false
}
$summaryPath = Join-Path $RunRoot 'summary.json'
[IO.File]::WriteAllText($summaryPath, ($summary | ConvertTo-Json -Depth 8) + [Environment]::NewLine)
if ($failure) { throw "$failure`nSummary: $summaryPath" }
Write-Host "PASS_MODELSIM_POSTPROCESS_VENDOR_ROM runs=$($results.Count)"
Write-Host "SUMMARY=$summaryPath"



