param([ValidateSet('build', 'verify', 'self-test')][string]$Mode = 'verify')
$ErrorActionPreference = 'Stop'
$roadRoot = 'E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision'
$roadOldPythonPath = $env:PYTHONPATH
$roadOldCUDA = $env:CUDA_VISIBLE_DEVICES
$roadOldNVML = $env:PYTORCH_NVML_BASED_CUDA_CHECK
try {
    $env:PYTHONPATH = 'E:\project\qiansai\.tools\road_yolo_numpy_235_20261014;' + $roadRoot
    $env:CUDA_VISIBLE_DEVICES = '-1'
    $env:PYTORCH_NVML_BASED_CUDA_CHECK = '1'
    $roadArguments = @('-B', ($PSScriptRoot + '\handoff.py'))
    if ($Mode -eq 'verify') { $roadArguments += '--verify' }
    if ($Mode -eq 'self-test') { $roadArguments += '--self-test' }
    & 'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe' @roadArguments
    if ($LASTEXITCODE -ne 0) { throw ('CPU handoff failed: exit ' + $LASTEXITCODE) }
} finally {
    $env:PYTHONPATH = $roadOldPythonPath
    $env:CUDA_VISIBLE_DEVICES = $roadOldCUDA
    $env:PYTORCH_NVML_BASED_CUDA_CHECK = $roadOldNVML
}
