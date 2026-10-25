param([switch]$Build)
$ErrorActionPreference = 'Stop'
$roadOldPythonPath = $env:PYTHONPATH
$roadOldCUDA = $env:CUDA_VISIBLE_DEVICES
$roadOldNVML = $env:PYTORCH_NVML_BASED_CUDA_CHECK
try {
    $env:PYTHONPATH='E:\project\qiansai\.tools\road_yolo_numpy_235_20261014;E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision'
    $env:CUDA_VISIBLE_DEVICES='-1'
    $env:PYTORCH_NVML_BASED_CUDA_CHECK='1'
    $roadArguments = @('-B', ($PSScriptRoot + '\golden.py'))
    if ($Build) { $roadArguments += '--build' }
    & 'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe' @roadArguments
    if ($LASTEXITCODE -ne 0) { throw ('CPU golden failed: exit ' + $LASTEXITCODE) }
} finally {
    $env:PYTHONPATH=$roadOldPythonPath
    $env:CUDA_VISIBLE_DEVICES=$roadOldCUDA
    $env:PYTORCH_NVML_BASED_CUDA_CHECK=$roadOldNVML
}
