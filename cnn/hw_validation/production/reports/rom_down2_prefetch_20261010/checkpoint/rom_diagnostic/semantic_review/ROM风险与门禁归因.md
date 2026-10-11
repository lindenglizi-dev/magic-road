# schema2 ROM 数值、驱动与接口只读审查

日期：2026-10-10。角色：`review`。任务类别：`analyze`。

## 结论

**没有发现阻止独立 TD 综合的真实语义缺陷。** 当前候选可以继续做隔离 TD 综合/ERAM 映射诊断，不需要先为旧严格格式问题继续改 RTL。厂商 ModelSim 已用真实 PH1P 模型通过 7168 字/143360 B 全量读回、393 字段重构、CRC32=`1bbd0dce` 和复位中断后重启；两份 DUT RTL 未改。继续条件是：候选仍保持两份 RTL 字节级不变、`artifacts/` 保持与 `production/numeric_artifacts/` 一致，并在 TD 中确认 56 个 20K ERAM、56 个初始化文件均被接受，且没有影响已加载逻辑的无驱动输入。任何 ERAM 数量/深度/位宽错误或初始化文件未装载都立即阻断。

这不是严格交付放行。当前候选 strict gate 仍为 `delivery_ready=false`；也没有参数消费者、QAT、DDR、整网吞吐或板级证据。

## 1. 已证明的静态事实

### 1.1 schema1 到 schema2 只需替换 artifact 绑定

- 新候选 `rtl/road_yolo_numeric_rom_group.v` 与旧基线 SHA-256 均为 `a3eafe9e403a4292e4458c2fe0c30a77dce400ac00a3d52459b41fd8e4ce391c`。
- 新候选 `rtl/road_yolo_numeric_rom_probe.v` 与旧基线 SHA-256 均为 `74f00032df9fff02b45d3832534b668f8c53a395b53d34e6193abd290f3a7f83`。
- 候选 `artifacts/` 与 `production/numeric_artifacts/` 的 60 个文件逐文件 SHA-256 相同，无缺失、无额外文件。
- schema2 几何仍为 14 组 × 512 字 × 160 bit；每组四个 40-bit lane。旧 RTL 的参数、端口、状态、CRC 和流水逻辑不依赖 manifest 字段名，只依赖相对路径 `artifacts/group_XX_lane_Y.dath`。因此在每个独立工作目录内把 `artifacts/` 绑定到冻结 schema2 文件即可保持 RTL 行为合同，不应为了 schema2 改计数、接口、II 或复位。

schema2 当前仍是 `TEST_ONLY_NOT_TRAINED_NOT_ACCURACY_EVIDENCE`，物理包为 143360 B，CRC32 为 `1bbd0dce`。这只证明 TEST 包布局闭合，不是部署 QAT 包。

### 1.2 位宽和计数边界

| 对象 | RTL 位置 | 静态判断 |
| --- | --- | --- |
| 单 lane | `road_yolo_numeric_rom_group.v:119-174`，其余三例同构 | `DATA_WIDTH_A/B=40`、`ADDR_WIDTH_A/B=9`、`DATA_DEPTH_A/B=512`，恰为 20480 bit；四 lane 拼成 160 bit。 |
| 组索引 | `road_yolo_numeric_rom_probe.v:96,149-150,340-347` | 4 bit 可表示 0…13；仅非末组的组末字走 `GROUP_ADVANCE`，实际递增 0…12 到 1…13。 |
| 字地址 | `road_yolo_numeric_rom_probe.v:97,149,350-360` | 9 bit 可表示 0…511；仅普通字递增 0…510 到 1…511，组切换清零。 |
| bit 索引 | `road_yolo_numeric_rom_probe.v:98,363-374,398-406` | 8 bit 可表示 0…159；末位更新后成为 160，随后不再索引缓存，并在下一字捕获时清零。 |
| FSM | `road_yolo_numeric_rom_probe.v:62-76,183-294` | 15 个独热状态，复位进入 `ST_ISSUE`；三种收字分支分别可达字递增、组递增和结束。旧 VG098/VG122 不能直接解释为真实不可达或溢出。 |

最终字不会漏算：`ST_BIT_FETCH` 先锁存 bit159 和末位标志，`ST_BIT_UPDATE` 更新最终 CRC，之后才经 `ST_WORD_BRANCH` 到 `ST_FINISH`；`checksum_o <= ~reg_crc` 取得的是已经包含末位的余数（`road_yolo_numeric_rom_probe.v:170-178,226-258,435-443`）。

### 1.3 CRC 覆盖和 padding

- 地址顺序为 group 0…13，每组 word 0…511，共 7168 字；每字 bit 0…159，共 1,146,880 bit = 143360 B。
- `{lane_delta,lane_gamma,lane_beta,lane_alpha}` 使 package byte0 位于 `reg_word_buffer[7:0]`（group RTL `69-72,94,104,113`）；CRC 从 bit0 向 bit159 扫描（probe RTL `388-405`），对应 reflected IEEE CRC32 的逐字节低位优先次序。
- schema2 payload 为 140522 B，物理包为 143360 B，末尾 2838 B 为 padding。偏移 140522 位于 absolute word 7026 的第 2 个 byte 后；扫描固定覆盖完整 7168 字，因此自然包含该字剩余 18 B 及后续全部 padding。
- 当前 `package_check.json` 已记录 56 lane 全量重构成功，`words.dath` 为 7168 行且重构物理包 SHA-256 `bc04290dd840e78713c0e576e754bd203ea7df88e7991c71dd93de8fdaf13017`。这是文件布局证据，不替代 primitive 读回。

## 2. 流水等待与 primitive 边界

### 2.1 最小等待是否足够

在 `REGMODE_A="NOREG"` 且 A 口为一拍同步读的合同下，现有等待足够，并多留了清晰的寄存边界：

1. `ST_ISSUE → ST_WAIT_PHY`：等待 primitive 同步读；
2. group 内两个 80-bit pair 和一个 160-bit 输出寄存器各占一拍（group RTL `90-115`）；
3. 14 选 1 的 pair/quad/oct/final 四级寄存 mux 各占一拍（probe RTL `447-570`）；
4. `ST_CAPTURE` 再把稳定的 `reg_selected_word` 锁入 CRC 缓存（probe RTL `376-385`）。

地址从发起到捕获始终稳定；字/组计数只在完成当前字 CRC 后变化。因此不存在由本地流水导致的最小间隔不足。

官方 `ph1p_logic_eram.v` 的行为区被加密，完整接口抽取本身只证明 30 个参数和 22 个端口，不能单独证明读延迟、初始化或综合映射。但当前 `vendor_simulation/receipt.json` 明确记录 `vendor_model=true`、`standin_used=false`、`all_passed=true`；全量逐字读回和最终 CRC 已确认现有最小等待对该厂商仿真模型足够。尚未由此证明的是 TD 综合后的物理映射和实际 silicon 时序。

### 2.2 primitive 输入/输出风险

| 位置 | 判断 | 保护条件 / 是否阻断本轮 TD |
| --- | --- | --- |
| group RTL `119-149` 及三处同构实例 | `MODE="SP"`、40×512、`IMPLEMENT="20K"` 与官方 logical wrapper 参数集合相容；官方 physical model 明列 40-bit 支持。 | 目标应为 4 ERAM/组、共 56；不是 56 即阻断。 |
| group RTL `152-173` 及三处同构实例 | A 口 `cea=1,wea=0`；ECC 关闭；B 口 `ceb=0,web=0`，输出悬空，符合只读用途。`ocea=0` 在 `NOREG` 下也与官方 ROM 模板的 `OUTREG_DISA` 接法一致。 | 不阻断；TD 若报告写口或 ECC 逻辑被保留，需追查。 |
| group RTL `164,222,280,338` | 禁用的 B 口仍接 `clkb=i_clk`，而官方 ROM 模板在 SP 分支把 `clkb` 接常 0。当前没有证据说明它改变数据，但可能造成额外时钟负载或检查器噪声。 | 不先改；若 TD 显示 B 口时钟被实际加载、额外时钟资源或相关未解释路径，则停止并做单点修复。 |
| group RTL `158,166` 等 | primitive `rsta/rstb` 恒 0，复位只清本地拼接/选择/CRC寄存器；ROM 内容依赖 INIT_FILE，而非运行时复位。 | 必须在上电后实际断言 `i_rstn`；顶层应提供异步断言、同步释放后的 `i_rstn`。没有可靠复位时不能使用 checksum。 |
| group RTL `147,205,263,321`，probe RTL `575-760` | 56 个 INIT_FILE 名称覆盖 group00…13、lane0…3，当前候选工作目录内均存在；厂商 ModelSim 已确认仿真侧全部文件装入且逐字一致。 | TD 的综合侧路径解析仍需报告确认；任一文件未读取、退回 `NONE`、被截断或重排都阻断。 |

完整 pure interface 能消除“端口名字不存在/方向未知”的数据缺口，但不能当作输出驱动行为模型。当前 checker 对 `doa` 及 14 个 group 输出仍保守报 `read_without_driver/unresolved_instance_output`；官方明文声明确认这些端口方向为 output，厂商 ModelSim 已进一步证明仿真中的实际驱动、时序和内容。综合后的唯一驱动与保留性仍由本轮 TD 报告闭合。

## 3. 严格门禁与真实风险分离

当前候选门禁（来自本目录已生成的 `gate_candidate/gate.json`，本角色未重跑）：

| compile | ast | readability | comment | naming | profile | testbench | toolchain |
| --- | --- | --- | --- | --- | --- | --- | --- |
| passed | failed | failed | failed | failed | passed | not_requested | not_requested |

`441 errors / 0 strict warnings` 与同目录 baseline 完全相同，说明 schema2 artifact 绑定没有新增 RTL 门禁差异。主要归因：

- **格式/强编码**：VG060/063/065/066、VG125/138、comment placement 等；不应为了本轮隔离映射无休止改写 RTL。
- **本地保守分析**：VG098 状态可达、VG122 计数加法和 VG084/VG137 表达式宽度；上述计数保护条件已能静态解释，但 strict 规则仍未通过。
- **vendor/interface 待证**：VG097、VG132、VG146/147、VG153。完整接口只提供声明，无法证明 primitive 行为和实例输出唯一驱动；其中 `clka` 是真实读时钟，不能因为 VG132 就断开。
- **参数合同**：VG151 对四个文件字符串参数及默认值未闭合；真实风险不是字符串“命名”，而是 TD 是否实际装入 56 个冻结文件。

用户已明确允许在 strict 未闭合时继续隔离诊断，因此这些项不阻断本轮 TD 资源筛查；它们继续阻断“严格交付完成”的表述。若 TD 出现与 vendor 待证项一致的真实异常，应按 stop condition 停止，而不是靠 pure interface 或格式修改放行。

测试平台的 `forever` 被检查器误判成 `for` 后，仅将等效时钟生成写法改为 `always #5`；DUT 未改。修正后 TB gate 为 `compile=passed`、parse errors=0、`testbench=passed`，但总体仍为 `351 errors / 2 strict warnings`，所以不把动态通过解释成 strict 放行。

## 4. 本轮 TD 门禁归因

允许继续的前置条件：

1. 顶层仅为 `road_yolo_numeric_rom_probe`，候选 RTL hash 保持上述两值；
2. 工具工作目录携带与 schema2 source 完全相同的 60 个 artifact 文件；
3. 不加入 timing exception，不改接口、II、计数、CRC、复位或 primitive 参数；
4. 报告把 0 输入/输出延迟标成隔离诊断，不冒充板级 IO timing。

本轮 TD 的阻断条件：

- ERAM 数不是 56，或不是 40×512 对应的 20K 映射；
- INIT_FILE 找不到、格式不接受、部分 ROM 被常量化/裁剪，或读回与 schema2 `words.dath` 不同；
- 已加载逻辑存在无法解释且会影响 CRC/地址/选择路径的无驱动输入；
- TD 网表/实现出现与已通过厂商 ModelSim 不一致的读延迟、字序、lane序或 group序；
- 为继续实现必须改变算术接口、II、数值/复位合同、真实 DDR 协议或增加时序例外。

非阻断但仍待证：禁用 B 口的时钟连接、异步复位释放必须由上层同步、真实 setup/hold、初始化在实现后的保留性。这些可在隔离 TD 中继续取证；无需先扩大成格式整治。

## 5. 证据边界

- 本角色未运行仿真、TD、综合、布局布线、训练、位流、板卡或 Flash；只读核对了主流程新生成的厂商 ModelSim 收据和日志。
- 厂商加密 PH1P 模型仿真已证明全量读回、CRC 和复位重启；未把 pure interface 当行为模型。该证据不替代综合映射、实现或板上行为。
- 未证明参数消费者已实现；ROM probe 只证明 TEST 包可能被逐字读出，不证明量化参数被正确解释或送入 MAC/后处理。
- 未证明部署 QAT、真实 DDR 闭环、67 层整网、5 FPS、检测精度或视频并发。

## 6. 只读来源

- `AGENTS.md`、`MULTI_AGENT_WORKFLOW.md`
- `cnn/hw_validation/plans/competition_framework_20261008/RoadYOLO_训练与RTL整体技术框架.md`
- `cnn/hw_validation/plans/competition_framework_20261008/证据索引与对话进度.md`
- `cnn/hw_validation/rom/road_yolo_numeric_rom_group.v`
- `cnn/hw_validation/rom/road_yolo_numeric_rom_probe.v`
- `cnn/hw_validation/rom/spec/road_yolo_numeric_rom_group_spec.md`
- `cnn/hw_validation/rom/spec/road_yolo_numeric_rom_probe_spec.md`
- `cnn/hw_validation/rom/reports/final_readiness.json`（仅提取头部、八门状态与按规则计数/定位）
- `cnn/hw_validation/interfaces/complete_provenance.json`
- `cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v`
- `cnn/hw_validation/production/reports/checker_fact_closure_20261009/三类误报修复与后续路线报告.md`
- `cnn/hw_validation/production/reports/checker_fact_closure_20261009/checker_overlay/`
- `cnn/hw_validation/production/reports/checker_fact_closure_20261009/inputs/interfaces/ph1p_eram_interface_complete.v`
- `cnn/hw_validation/production/numeric_artifacts/manifest.json` 及同目录冻结 artifact
- `cnn/hw_validation/production/reports/rom_schema2_mapping_20261010/{requirements.json,package_check.json,baseline/,rtl/,artifacts/,gate_candidate/gate.json}`
- `cnn/hw_validation/production/reports/rom_schema2_mapping_20261010/vendor_simulation/{receipt.json,vsim.log,observed_words.dath}`
- `cnn/hw_validation/production/reports/rom_schema2_mapping_20261010/gate_testbench_attempt2/gate.json`
- `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_eram.v`
- `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_phy_eram.v`
- `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/ip/depot/ROMF9F0D0P0_1.0/ROM/RTL/rom.v`
