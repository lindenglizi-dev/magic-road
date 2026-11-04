param([string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 & "$VivadoBin/xvlog.bat" ../rtl/uart_mode_protocol.v ../user_source/hdl_source/awb.v ../user_source/hdl_source/signal_delay.v
 if($LASTEXITCODE -ne 0){throw 'Unit RTL compile failed'}
 & "$VivadoBin/xvlog.bat" --sv tb_protocol_v2.sv tb_awb_bypass.sv
 if($LASTEXITCODE -ne 0){throw 'Unit test compile failed'}
 foreach($top in @('tb_protocol_v2','tb_awb_bypass')){
  & "$VivadoBin/xelab.bat" $top -s $top --debug typical --timescale 1ns/1ps
  if($LASTEXITCODE -ne 0){throw 'Unit elaboration failed'}
  & "$VivadoBin/xsim.bat" $top --runall --log "$top.log"
  if($LASTEXITCODE -ne 0 -or !(Select-String "$top.log" -SimpleMatch 'PASS ') -or (Select-String "$top.log" -Pattern 'Fatal:|Error:')){throw "Unit verification failed: $top"}
 }
}finally{Pop-Location}
