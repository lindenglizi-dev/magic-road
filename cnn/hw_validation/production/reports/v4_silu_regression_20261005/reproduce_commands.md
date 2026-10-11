# SiLU 固定回归复现步骤

在有 ModelSim SE-64 2020.4 许可的本机使用下列固定目录。先核对 `evidence.json` 中的输入、工具和库映射哈希。原版和候选代码分别在 original/candidate 子目录，官方模型和数据快照分别在 vendor_sources/frozen_data；不修改生产源码。

**工作目录必须是本目录**，四个测试台均使用 `../../silu/generated/` 读取黄金文件。生成的黄金文件须与 frozen_data 快照哈希一致。不能只指定 modelsim.ini 就省略工作目录切换。

下列示例日志使用新的 `replay` 名称；如已存在，应换一个新名称，不能覆盖原失败或通过记录。

```powershell
Set-Location 'E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/v4_silu_regression_20261005'

# 冻结模型、RTL与测试台编译到已明确映射的独立库。
& 'D:/modeltech64_2020.4/win64/vlog.exe' -modelsimini modelsim.ini -work old_work -l replay_old_compile.log vendor_sources/ph1p_logic_eram.v vendor_sources/ph1p_phy_gsr.v original/silu_shared_unit.v tb_silu_vendor_stall.v tb_silu_vendor_contract.v
& 'D:/modeltech64_2020.4/win64/vlog.exe' -modelsimini modelsim.ini -work candidate_work -l replay_candidate_compile.log vendor_sources/ph1p_logic_eram.v vendor_sources/ph1p_phy_gsr.v candidate/silu_shared_unit.v tb_silu_vendor_stall.v tb_silu_vendor_contract.v tb_silu_shared_unit.v tb_silu_vendor_random.v

# 使用库限定top，不依赖默认work；不使用不受支持的-novopt。
& 'D:/modeltech64_2020.4/win64/vsim.exe' -c -modelsimini modelsim.ini -l replay_original_stall1.log -wlf replay_original_stall1.wlf old_work.PH1P_PHY_GSR old_work.tb_silu_vendor_contract +STALL=1 +TRACE=replay_original_stall1.csv -do 'run 2 ms; quit -f'
& 'D:/modeltech64_2020.4/win64/vsim.exe' -c -modelsimini modelsim.ini -l replay_candidate_stall1.log -wlf replay_candidate_stall1.wlf candidate_work.PH1P_PHY_GSR candidate_work.tb_silu_vendor_contract +STALL=1 +TRACE=replay_candidate_stall1.csv -do 'run 2 ms; quit -f'
& 'D:/modeltech64_2020.4/win64/vsim.exe' -c -modelsimini modelsim.ini -l replay_candidate_full.log -wlf replay_candidate_full.wlf candidate_work.PH1P_PHY_GSR candidate_work.tb_silu_shared_unit -do 'run 2 ms; quit -f'
& 'D:/modeltech64_2020.4/win64/vsim.exe' -c -modelsimini modelsim.ini -l replay_candidate_random.log -wlf replay_candidate_random.wlf candidate_work.PH1P_PHY_GSR candidate_work.tb_silu_vendor_random -do 'run 2 ms; quit -f'
```

如在新机器重建，先以 vlib 建立两个库，再用 `vmap -modelsimini modelsim.ini old_work <绝对库目录>` 和 candidate_work 的对应命令更新本地映射。不能直接沿用旧机器绝对目录。库 inventory 日志和 mapping 日志记录了本次实际绑定。

原版预期：`TB_ERROR RAM output changed on frozen edge`、`raw=4 lookup=513 got=4 expected=2`、`TB_FAIL_CONTRACT ... errors=2`。这是真实 DUT 负例，必须失败，不因进程退出 0 宣称通过。

候选预期：`TB_PASS_CONTRACT ... accepted=1033 received=1033 load_checks=1024 table_reads=1024 errors=0`；全域 `TB_PASS inputs=65536 latency=5 ii=1 ... legal_writes=3072 stale_output_errors=0`；随机 `TB_PASS_RANDOM seed=42 ... accepted=4096 received=4096 stall_cycles=1353 max_stall=7`。把 STALL 改为 16、32、64 可复现相应定向冻结检查。任何 TB_ERROR、TB_FAIL、超时、缺失 PASS 或数量不符都应阻断候选功能结论。

每次复现应另存源码、数据、工具哈希与日志，不能只保存进程码。周期契约图与真实波形分别保留。本步骤不运行 TD、不签核物理 RAM、不下载位流。
