param([switch]$SynthesisOnly,[string]$TdBin='E:/TD/6.2.1/bin')
$ErrorActionPreference='Stop'
$stages=@('syn_1');if(!$SynthesisOnly){$stages+= 'phy_1'}
foreach($stage in $stages){
 $settings="$PSScriptRoot/td_project/camera_to_dsi_display_Runs/$stage/settings.cfg"
 if(!(Test-Path -LiteralPath $settings)){
  Copy-Item -LiteralPath "$PSScriptRoot/td_project/run_settings/$stage.cfg" -Destination $settings
 }
 Push-Location "$PSScriptRoot/td_project/camera_to_dsi_display_Runs/$stage"
 try {
  $started=Get-Date
  & "$TdBin/td_commands_prompt.exe" ./camera_to_dsi_display.tcl *> console.log
  $marker=if($stage -eq 'syn_1'){'.opt_gate.end.f'}else{'.bitgen.end.f'}
  if($LASTEXITCODE -ne 0 -or !(Test-Path $marker) -or (Get-Item $marker).LastWriteTime -lt $started){throw "TD $stage failed; inspect console.log"}
 } finally {Pop-Location}
}
if(!$SynthesisOnly){
 $timing=Get-Content "$PSScriptRoot/td_project/camera_to_dsi_display_Runs/phy_1/camera_to_dsi_display_pr.timing" -Raw
 foreach($kind in @('SWNS','HWNS')){
  $m=[regex]::Match($timing,"${kind}:\s*([-\d.]+)ns")
  if(!$m.Success -or [double]$m.Groups[1].Value -lt 0){throw "Final $kind timing failed"}
 }
}
Write-Output 'PASS fresh TD run'
