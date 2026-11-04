param([switch]$Full,[string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin',[string]$Python='E:/anaconda3/python.exe')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 $sources=@(Get-ChildItem '../rtl/*.v' | ForEach-Object FullName)
 & "$VivadoBin/xvlog.bat" @sources --log compile.log
 if($LASTEXITCODE -ne 0){throw 'RTL compile failed'}
 $top='tb_runtime';$log='small_sim.log'
 if($Full){
  & $Python make_vectors.py 1280 720
  $top='tb_runtime_full';$log='full_sim.log'
  $s=(Get-Content tb_runtime.sv -Raw).Replace('module tb_runtime;','module tb_runtime_full;').Replace('parameter W=640,H=112;','parameter W=1280,H=720;')
  Set-Content tb_runtime_full.sv $s
 } else { & $Python make_vectors.py 640 112 }
 if($LASTEXITCODE -ne 0){throw 'Golden model failed'}
 & "$VivadoBin/xvlog.bat" --sv "$top.sv"
 if($LASTEXITCODE -ne 0){throw 'Testbench compile failed'}
 & "$VivadoBin/xelab.bat" $top -s $top --debug typical
 if($LASTEXITCODE -ne 0){throw 'Elaboration failed'}
 & "$VivadoBin/xsim.bat" $top --runall --log $log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path $log -SimpleMatch 'PASS runtime') -or (Select-String -Path $log -Pattern 'Fatal:|Error:')){throw 'Verification failed'}
 if(!$Full){
  & "$VivadoBin/xvlog.bat" ../user_source/hdl_source/video_in.v
  if($LASTEXITCODE -ne 0){throw 'video_in compile failed'}
  & "$VivadoBin/xvlog.bat" --sv tb_fifo_boundary.sv
  if($LASTEXITCODE -ne 0){throw 'FIFO test compile failed'}
  & "$VivadoBin/xelab.bat" tb_fifo_boundary -s fifo_boundary --debug typical --timescale 1ns/1ps
  if($LASTEXITCODE -ne 0){throw 'FIFO test elaboration failed'}
  & "$VivadoBin/xsim.bat" fifo_boundary --runall --log fifo_boundary.log
  if($LASTEXITCODE -ne 0 -or !(Select-String -Path fifo_boundary.log -SimpleMatch 'PASS original video_in') -or (Select-String -Path fifo_boundary.log -Pattern 'Fatal:|Error:')){throw 'FIFO boundary failed'}
 }
} finally {Pop-Location}
