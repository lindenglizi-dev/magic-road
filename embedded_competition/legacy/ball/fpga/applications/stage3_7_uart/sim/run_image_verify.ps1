param([string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 & "$VivadoBin/xvlog.bat" ../rtl/image_ddr_bridge.v ../rtl/image_upload_engine.v ../rtl/pc_image_replay.v
 if($LASTEXITCODE -ne 0){throw 'Image RTL compile failed'}
 & "$VivadoBin/xvlog.bat" --sv tb_image_path.sv tb_replay_1080.sv tb_source_select.sv
 if($LASTEXITCODE -ne 0){throw 'Image test compile failed'}
 & "$VivadoBin/xelab.bat" tb_image_path -s image_path --debug typical --timescale 1ns/1ps
 if($LASTEXITCODE -ne 0){throw 'Image elaboration failed'}
 & "$VivadoBin/xsim.bat" image_path --runall --log image_path.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path image_path.log -SimpleMatch -Pattern 'PASS image path:') -or (Select-String -Path image_path.log -Pattern 'Fatal:|Error:')){throw 'Image path test failed'}
 & "$VivadoBin/xelab.bat" tb_replay_1080 -s native_replay --debug typical --timescale 1ns/1ps
 if($LASTEXITCODE -ne 0){throw 'Native replay elaboration failed'}
 & "$VivadoBin/xsim.bat" native_replay --runall --log native_replay.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path native_replay.log -SimpleMatch -Pattern 'PASS native 1080 DDR replay:') -or (Select-String -Path native_replay.log -Pattern 'Fatal:|Error:')){throw 'Native replay test failed'}
 & "$VivadoBin/xelab.bat" tb_source_select -s source_select --debug typical --timescale 1ns/1ps
 if($LASTEXITCODE -ne 0){throw 'Source select elaboration failed'}
 & "$VivadoBin/xsim.bat" source_select --runall --log source_select.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path source_select.log -SimpleMatch -Pattern 'PASS source select:') -or (Select-String -Path source_select.log -Pattern 'Fatal:|Error:')){throw 'Source select test failed'}
}finally{Pop-Location}
