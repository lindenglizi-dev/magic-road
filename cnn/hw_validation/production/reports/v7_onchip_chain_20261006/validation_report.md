# v7 最小片上链功能验证报告

## 结论

本目录是隔离的功能候选，不是生产合入件。ModelSim 功能门禁通过；registered strict 门禁未通过，因此整体 `delivery_ready=false`，未进入 TD。

## 功能结果

- 当前 `road_onchip_chain.v` 与冻结 MAC、round、真实 SiLU/PH1P 模型重新全量编译：0 error、0 warning。
- 最终仿真仅出现 2 条保留的官方 RAM 模型 `INIT_FILE` 优化告警；DUT/TB 结果为唯一一条 `TB_PASS_CHAIN`，日志中无 `TB_ERROR` 或 `TB_FAIL_CHAIN`。
- 覆盖为 MAC 终点 9 次、pre/SiLU/post 逐级断言各 27 次、实体缓存读回 27 次、alpha/beta 提前不可见观察 18 次、阶段复位 6 例、参考模型定向饱和 1 例。
- base16 为 482 周期，tail13 为 503 周期；起点是首个 MAC 输入握手，终点是末个缓存响应消费，1024 次运行时装表不计入。tail13 包含 3 周期和 20 周期缓存响应反压。
- 六个链内复位点覆盖 MAC 在途、PRE_WAIT、SILU_WAIT、POST_WAIT、两个提交间隙；另测缓存响应长反压时复位。各例均检查 valid、位置/通道/phase 元数据、cache-valid、在途核输出取消、20 周期无 ghost 写/读、外读故障，以及重装 1024 项表后恢复。
- 定向例的 golden 由冻结 `v7_minimal_chain_20261006/reference.py` 生成：pre 正饱和 32767、pre 负饱和 -32768、2.5 最近偶数舍入为 2，完整链正 INT8 饱和为 127。固定 SiLU 和 post 比例下负 INT8 饱和不可达，未虚构全链覆盖；该边界只由冻结独立 round/saturation 参考覆盖。
- `cycle_trace.csv` 写入实际整数，但数值裁决来自 TB 对冻结 stage vectors、feature vectors 与定向 golden 的逐级断言，不以 CSV 作为黄金模型。

## 保留边界

- 乘法操作数是 signed INT32 数据与“带零符号位、由 signed32 承载的非负 31 位 magnitude”，完整结果为 signed64。当前系数固定为 pre M=[1,3,5]、pre shift=[0,2,4]、post M=1、post shift=4；未来物理资源不能外推为任意部署 M 的 DSP/LUT 预算。
- 新顶层宽诊断接口为 414 I/O，超过目标器件约 160 个可用 I/O；本轮未擅自制作窄物理壳。TD 需未来单独授权低 I/O wrapper。
- Icarus 无法解析官方加密 PH1P 模型；真实 RAM 回归使用 ModelSim SE-64 2020.4。
- 未训练、未上板、未写 Flash、未修改冻结核接口/II/约束例外、未修改生产 RTL。

## Strict 门禁

strict 报告为 `delivery_ready=false`、374 errors、0 strict warnings。compile/profile/testbench 子门通过；AST/readability/comment/naming 子门失败。结构化 findings 共 370 条，主要为 VG060=131、VG146=74、VG147=66，其余详见 `strict_gate.json`。自动 formatter 预检因缓存实体写块没有复位分支而拒绝结构化改写；该缓存由独立 valid 位控制，不能仅为排版门禁擅改功能结构。按本轮“只做窄机械修复、不做宽重构”的边界，保留原始 strict 证据并停止在 TD 之前。

## 官方 RAM 模型告警

最终 ModelSim 优化阶段逐字报告：

```text
** Warning: inputs/ph1p_logic_eram.v(165): (vopt-2697) MSB 172095 of part-select into 'INIT_FILE' is out of bounds.
** Warning: inputs/ph1p_logic_eram.v(165): (vopt-2697) LSB 172024 of part-select into 'INIT_FILE' is out of bounds.
```

来源模型 SHA-256 为 `70d89b70bdd51812ad86b91e88526b4604ebb117516efda5af976fcddb2e69af`。模型 `INIT_FILE=NONE`；链在 `o_table_loaded` 前禁止推理，TB 每次复位后显式 ready-valid 写满 1024 个真实表项并逐级对拍，因此功能结果不依赖该出错初始化路径。告警仍保留，历史 SiLU strict 167 项未宣称闭合。
