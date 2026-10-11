# 未解决事项

- 新顶层运行时加载每通道前乘数与统一后乘数的补丁被安全审查拒绝，因为会扩大当前外部接口契约；本轮保持冻结测试参数 `pre M=[1,3,5]`、`pre shift=[0,2,4]`、`post M=1`、`post shift=4`。后续资源证据仅代表这些测试系数，不能代表任意非负 31 位部署乘数的 DSP 或 LUT 预算。
- Icarus Verilog 无法解析官方 `PH1P_LOGIC_ERAM` 模型，报告 `ph1p_logic_eram.v:107 syntax error`，因此真实 RAM 功能回归使用项目既有的 ModelSim SE-64 2020.4 路径。该解析失败不解释为 DUT 失败。
- ModelSim 优化阶段从官方加密 RAM 模型 `inputs/ph1p_logic_eram.v` 第 165 行（SHA-256 `70d89b70bdd51812ad86b91e88526b4604ebb117516efda5af976fcddb2e69af`）逐字报告两条告警：`** Warning: inputs/ph1p_logic_eram.v(165): (vopt-2697) MSB 172095 of part-select into 'INIT_FILE' is out of bounds.` 与 `** Warning: inputs/ph1p_logic_eram.v(165): (vopt-2697) LSB 172024 of part-select into 'INIT_FILE' is out of bounds.`。模型参数 `INIT_FILE` 为 `NONE`；链在 `o_table_loaded` 置位前禁止输入，TB 每次复位后通过 ready-valid 显式写满 1024 项真实表，随后才运行并逐级对拍冻结向量，因此功能结果不依赖告警所涉上电初始化路径。两条告警仍原样保留在 ModelSim 日志中，未归零或隐藏，历史 SiLU strict 167 项也未宣称闭合。
- registered strict 门禁保留失败状态：`delivery_ready=false`、374 errors、0 strict warnings。compile/profile/testbench 子门通过，AST/readability/comment/naming 子门失败；370 条结构化 findings 以 VG060=131、VG146=74、VG147=66 为主。自动 formatter 因缓存实体写 always 块无复位而拒绝安全结构化写回，本轮不为排版门禁扩大到功能结构重写。
- 顶层宽诊断接口实测预算为 414 I/O，大于目标器件约 160 个可用 I/O。本阶段不制作窄 I/O 物理 wrapper，不运行 TD，不改变引脚、时序例外、冻结核接口或生产 RTL。
