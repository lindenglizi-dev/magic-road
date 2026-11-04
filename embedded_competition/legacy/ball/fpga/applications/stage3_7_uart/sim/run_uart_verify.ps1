param([switch]$Full,[string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin',[string]$Python='E:/anaconda3/python.exe')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 $top='tb_uart_modes';$snapshot='uart_modes'
 if($Full){
  & $Python make_vectors.py 1280 720
  $top='tb_uart_modes_full';$snapshot='uart_modes_full'
  $source=(Get-Content tb_uart_modes.sv -Raw).Replace('module tb_uart_modes;','module tb_uart_modes_full;').Replace('parameter W=640,H=112;','parameter W=1280,H=720;')
  Set-Content "$top.sv" $source
 } else { & $Python make_vectors.py 640 112 }
 if($LASTEXITCODE -ne 0){throw 'Golden model failed'}
 $sources=@(Get-ChildItem '../rtl/*.v' | ForEach-Object FullName)
 & "$VivadoBin/xvlog.bat" @sources
 if($LASTEXITCODE -ne 0){throw 'RTL compile failed'}
 & "$VivadoBin/xvlog.bat" --sv "$top.sv"
 if($LASTEXITCODE -ne 0){throw 'Test compile failed'}
 & "$VivadoBin/xelab.bat" $top -s $snapshot --debug typical
 if($LASTEXITCODE -ne 0){throw 'Elaboration failed'}
 & "$VivadoBin/xsim.bat" $snapshot --runall --log "$snapshot.log"
 if($LASTEXITCODE -ne 0 -or !(Select-String "$snapshot.log" -SimpleMatch 'PASS UART') -or (Select-String "$snapshot.log" -Pattern 'Fatal:|Error:')){throw 'UART verification failed'}
} finally {Pop-Location}
