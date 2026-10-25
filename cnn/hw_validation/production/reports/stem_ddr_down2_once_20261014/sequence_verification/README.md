# Stem + DDR + down2 sequence verification

This verification instantiates `road_stem_ddr_sequence` directly at 100 MHz. Its request/response endpoint is a controllable 64-entry sparse memory indexed by `stem_addresses.hex`; it does not use the PAXI mailbox. Accepted Stem writes populate the endpoint, and later reads return those stored payloads. Golden data is used only by scoreboards.

The DUT instance uses `C_TIMEOUT=20000`. Cases are selected with `+CASE=0..12`; scoreboard vectors are selected with an absolute `+VECTORS=...` path. RTL-internal `$readmemh` names remain relative, so copy the vector `.hex` files into the simulation working directory before launch.

## ModelSim commands

Run these commands in PowerShell. Every generated file remains under `sequence_verification/case0`.

```powershell
$root = 'E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision\cnn\hw_validation\production\reports\stem_ddr_down2_once_20261014'
$model = 'D:\modeltech64_2020.4\win64'
$vendor = 'E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\sim_release\ph1p'
$run = Join-Path $root 'sequence_verification\case0'
$reused = (Get-ChildItem -LiteralPath (Join-Path $root 'reused') -Filter '*.v' | Sort-Object Name).FullName
Copy-Item -Path (Join-Path $root 'vectors\*.hex') -Destination $run -Force
Set-Location -LiteralPath $run
if (!(Test-Path -LiteralPath 'work')) { & "$model\vlib.exe" work }
& "$model\vlog.exe" -work work -l compile_final.log "+incdir+$root\rtl" "$vendor\ph1p_phy_gsr.v" "$vendor\ph1p_logic_eram.v" $reused "$root\rtl\road_stem_ddr_sequence.v" "$root\tests\tb_stem_ddr_sequence.v"
foreach ($case in 0..12) {
    & "$model\vsim.exe" -c -lib work PH1P_PHY_GSR tb_stem_ddr_sequence "+CASE=$case" "+VECTORS=$root\vectors" -l "case$case.log" -do 'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'
}
```

`tests/sequence_cases.json` defines the expected terminal status/error for each case. `receipts/case00.json` through `receipts/case12.json` capture the final observed counters, while `receipts/manifest.json` pins the source/vector hashes used for the run.

The preserved `case0_pre_parameter_kind_fix.log` is the first diagnostic failure. It localized a reference-program load-kind ordering error; the reference generator and vectors were corrected, with the DUT and frozen reused RTL unchanged.
