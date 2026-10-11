# 验证命令

以下命令均从本报告目录执行；未运行 TD、综合、布局布线、上板或 Flash。

```powershell
vlog -modelsimini modelsim.ini -work chain_work -l modelsim_chain_compile_final.log inputs/ph1p_logic_eram.v inputs/ph1p_phy_gsr.v inputs/road_mac_probe.v inputs/road_round_shift.v inputs/silu_shared_unit.v road_onchip_chain.v
vlog -modelsimini modelsim.ini -work chain_work -l modelsim_chain_tb_compile_final.log tb_road_onchip_chain.v
vsim -c -modelsimini modelsim.ini -l modelsim_chain_run_final.log -wlf modelsim_chain_run_final.wlf chain_work.PH1P_PHY_GSR chain_work.tb_road_onchip_chain -do "run 2 ms; quit -f"
```

同名规范和 WaveDrom 从工程根目录生成：

```powershell
$env:PYTHONPATH='C:\Users\lenovo\.codex\skills\readable-verilog-generator'
python -m scripts.python.workflow.cli write-spec --spec cnn/hw_validation/production/reports/v7_onchip_chain_20261006/road_onchip_chain.contract.json --out-dir cnn/hw_validation/production/reports/v7_onchip_chain_20261006/spec --source cnn/hw_validation/production/reports/v7_onchip_chain_20261006/road_onchip_chain.v --language zh --no-state
```

strict 门禁从工程根目录执行，完整结果保存在 `strict_gate.json` 与 `strict_gate.md`：

```powershell
$env:PYTHONPATH='C:\Users\lenovo\.codex\skills\readable-verilog-generator'
python -m scripts.python.validation.generated_deliverable_gate cnn/hw_validation/production/reports/v7_onchip_chain_20261006/road_onchip_chain.v --spec cnn/hw_validation/production/reports/v7_onchip_chain_20261006/road_onchip_chain.contract.json --external-interface-source cnn/hw_validation/production/reports/v7_onchip_chain_20261006/inputs/road_mac_probe.v --external-interface-source cnn/hw_validation/production/reports/v7_onchip_chain_20261006/inputs/road_round_shift.v --external-interface-source cnn/hw_validation/production/reports/v7_onchip_chain_20261006/inputs/silu_shared_unit.v --comment-language zh --include-testbench --json cnn/hw_validation/production/reports/v7_onchip_chain_20261006/strict_gate.json --markdown cnn/hw_validation/production/reports/v7_onchip_chain_20261006/strict_gate.md
```
