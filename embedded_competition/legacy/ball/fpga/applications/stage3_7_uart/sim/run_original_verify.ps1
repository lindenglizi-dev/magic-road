param([string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 $sources=@(Get-ChildItem '../rtl/*.v' | ForEach-Object FullName)
 & "$VivadoBin/xvlog.bat" @sources ../user_source/hdl_source/awb.v ../user_source/hdl_source/signal_delay.v ../user_source/hdl_source/isp/data128_96/data128_96.v ../user_source/hdl_source/isp/isp_top.v
 if($LASTEXITCODE -ne 0){throw 'ISP compile failed'}
 & "$VivadoBin/xvlog.bat" --sv tb_awb_bypass.sv tb_official_original.sv
 if($LASTEXITCODE -ne 0){throw 'Colour test compile failed'}
 & "$VivadoBin/xelab.bat" tb_official_original -s official_original --debug typical --timescale 1ns/1ps
 if($LASTEXITCODE -ne 0){throw 'Colour test elaboration failed'}
 & "$VivadoBin/xsim.bat" official_original --runall --log official_original.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path official_original.log -SimpleMatch -Pattern 'PASS official-original colour regression') -or (Select-String -Path official_original.log -Pattern 'Fatal:|Error:')){throw 'Official original colour regression failed'}
}finally{Pop-Location}
