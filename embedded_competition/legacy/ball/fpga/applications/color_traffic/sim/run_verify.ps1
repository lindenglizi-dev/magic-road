param([string]$VivadoBin='E:/Xilinx/Vivado/2022.2/bin',[string]$Python='E:/anaconda3/python.exe')
$ErrorActionPreference='Stop'
Push-Location $PSScriptRoot
try {
 $sources=@(Get-ChildItem '../rtl/*.v' | ForEach-Object FullName)
 & "$VivadoBin/xvlog.bat" @sources --log compile.log
 if($LASTEXITCODE -ne 0){throw 'RTL compile failed'}
 & "$VivadoBin/xvlog.bat" --sv tb_color_traffic.sv
 if($LASTEXITCODE -ne 0){throw 'Test compile failed'}
 & "$VivadoBin/xelab.bat" tb_color_traffic -s color_traffic --debug typical
 if($LASTEXITCODE -ne 0){throw 'Elaboration failed'}
 & "$VivadoBin/xsim.bat" color_traffic --runall --log result.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path result.log -SimpleMatch 'PASS color traffic') -or (Select-String -Path result.log -Pattern 'Fatal:|Error:')){throw 'Simulation failed'}
 & $Python make_osd_vectors.py
 if($LASTEXITCODE -ne 0){throw 'OSD vector generation failed'}
 & "$VivadoBin/xvlog.bat" --sv tb_osd_runtime.sv
 if($LASTEXITCODE -ne 0){throw 'OSD test compile failed'}
 & "$VivadoBin/xelab.bat" tb_osd_runtime -s osd_runtime --debug typical
 if($LASTEXITCODE -ne 0){throw 'OSD elaboration failed'}
 & "$VivadoBin/xsim.bat" osd_runtime --runall --log osd_result.log
 if($LASTEXITCODE -ne 0 -or !(Select-String -Path osd_result.log -SimpleMatch 'PASS OSD runtime') -or (Select-String -Path osd_result.log -Pattern 'Fatal:|Error:')){throw 'OSD simulation failed'}
 & $Python render_osd_preview.py
 if($LASTEXITCODE -ne 0){throw 'OSD preview render failed'}
} finally {Pop-Location}
