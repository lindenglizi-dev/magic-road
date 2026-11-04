param([string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 & "$VivadoBin/xvlog.bat" ../rtl/uart_rx.v ../rtl/uart_frame_rx.v ../rtl/uart_frame_tx.v ../rtl/vision_video_control.v ../rtl/vision_uart_control.v ../rtl/image_upload_engine.v ../rtl/color_traffic_core.v
 if($LASTEXITCODE -ne 0){throw 'Vision control compile failed'}
 & "$VivadoBin/xvlog.bat" --sv tb_vision_roi.sv
 if($LASTEXITCODE -ne 0){throw 'ROI test compile failed'}
 & "$VivadoBin/xelab.bat" tb_vision_roi -s vision_roi --debug typical --timescale 1ns/1ps
 if($LASTEXITCODE -ne 0){throw 'ROI elaboration failed'}
 & "$VivadoBin/xsim.bat" vision_roi --runall --log vision_roi.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path vision_roi.log -SimpleMatch -Pattern 'PASS vision ROI:') -or (Select-String -Path vision_roi.log -Pattern 'Fatal:|Error:')){throw 'Vision ROI test failed'}
}finally{Pop-Location}
