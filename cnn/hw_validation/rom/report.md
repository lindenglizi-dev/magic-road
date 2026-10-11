# H1-A ROM 首批实现报告

## 角色与边界

- 角色：`rtl_classifier`。
- 写入范围：仅 `cnn/hw_validation/rom/`。
- 仓库状态：工程目录不存在 `.git`，因此分支为 N/A。
- 未修改任何生产文件；本目录内容是独立验证交付。
- 本批不运行 TD、不生成或下载板上位流。父流程只有在本目录 strict gate 通过后才应继续真实映射；当前 gate 未通过。

## 数值包

该包状态固定为 `deterministic_test_fixture_not_trained_model_or_frozen_deployment_artifact`。它使用 seed 42 的 PCG64 随机测试数据、真实 67 层 shape/顺序和共享整数 LUT，但不是训练模型参数，也不是冻结部署结构包。

精确字节闭合：

```text
113100 weights int8
+ 2501 * 4 folded bias int32
+ 2501 * (4 + 1) output requant multiplier/shift
+ 61 * (4 + 1) pre-SiLU requant multiplier/shift
+ 4608 shared LUT bytes
= 140522 payload bytes
+ 2838 zero padding bytes
= 143360 bytes = 14 groups * 512 words * 20 bytes
```

关键产物：

- `artifacts/manifest.json`：393 个连续 segment 的 offset、长度、首末 word/group 和 SHA-256。
- `artifacts/numeric_test_seed42.bin`：140522B，SHA-256 `c02f7c959a329161dcf7adcf599fc7e97f0a4ef799d83c40708e6c1f570cfd45`。
- `artifacts/numeric_test_seed42_padded.bin`：143360B，SHA-256 `3ecaaad27cd06b3323e9f03c767334d93902341af61f245555193d7f457aab27`。
- `artifacts/group_00_lane_0.dath` 至 `group_13_lane_3.dath`：56 个独立 40-bit/512-word 初始化文件。
- `artifacts/numeric_test_seed42_words.dath`：7168 个 160-bit golden word。
- padded package 的 reflected IEEE CRC32：`0x60c88426`。

40-bit lane 每行把五个连续 package byte 解释为 little-endian 40-bit word；四 lane 依次覆盖 word 的 byte `[0:4]`、`[5:9]`、`[10:14]`、`[15:19]`。

## RTL 接口与 primitive 依据

顶层 `road_yolo_numeric_rom_probe` 只有：

```text
i_clk
i_rstn
o_done
o_checksum[31:0]
```

复位释放后自动扫描 14 组、每组 512 词、每词 160 bit。CRC32 每拍处理一 bit，全部 143360B（含 2838B padding）都会影响外部 checksum。14 组数据选择使用分层寄存 mux；每级合并不超过两路。单组四 lane 先形成两个 80-bit 寄存器，再形成 160-bit 寄存器。

生产 RTL 使用真实 `PH1P_LOGIC_ERAM` 名称和官方逻辑 wrapper 参数：`MODE="SP"`、A/B width 40、address width 9、depth 512、`IMPLEMENT="20K"`。没有伪造 `PDP20K` 逻辑模式；依据：

- `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_eram.v`
- `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_phy_eram.v`
- `E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/ip/depot/ROMF9F0D0P0_1.0/ROM/RTL/rom.v`

`tb_ph1p_logic_eram_sim.v` 只是 Icarus 的 primitive 模型替身：用 `$readmemh(INIT_FILE, ...)` 和同步 port-A read 对拍。它不是厂商加密模型验证证据，也不能替代 TD 的真实 56 块映射。

## 规范产物

`spec_input.json` 通过 canonical `write-spec` 生成四个模块 spec，以及每模块对应的 WaveJSON 与 SVG：

- `spec/road_yolo_numeric_rom_group_spec.md`
- `spec/road_yolo_numeric_rom_probe_spec.md`
- `spec/tb_ph1p_logic_eram_sim_spec.md`
- `spec/tb_road_yolo_numeric_rom_probe_spec.md`
- `spec/waveforms/`

## 验证命令与结果

Python golden：

```powershell
& 'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe' -B -X utf8 'cnn\hw_validation\rom\generate_numeric_package.py'
& 'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe' -B -X utf8 -m unittest discover -s 'cnn\hw_validation\rom' -p 'test_numeric_package.py' -v
```

结果：`4/4 OK`，最终复核耗时 `0.551s`。覆盖两次可重复生成、393 段 offset/hash 连续性、共享 LUT 原字节、56 lane 全重构、7168-word 文件全重构、padding 和 CRC32。

Icarus：

```powershell
& 'E:\project\qiansai\.tools\iverilog\bin\iverilog.exe' -g2012 -Wall -s tb_road_yolo_numeric_rom_probe -o "$env:TEMP\rom_probe.vvp" 'tb_ph1p_logic_eram_sim.v' 'road_yolo_numeric_rom_group.v' 'road_yolo_numeric_rom_probe.v' 'tb_road_yolo_numeric_rom_probe.v'
& 'E:\project\qiansai\.tools\iverilog\bin\vvp.exe' "$env:TEMP\rom_probe.vvp"
```

结果：`PASS: 7168 words / 143360 bytes checked, CRC32=60c88426`。逐词比较全部 160 bit，显式检查 absolute word `0/511/512/7025/7026/7167`；7026 含 payload→padding 的字内边界。

最终 strict gate 使用只含两份生产 RTL 的冻结目录，并把从官方明文模型机械抽取的完整 30 参数/端口 pure interface 仅作为静态接口事实：

```powershell
& 'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe' -B -X utf8 -m scripts.python.validation.generated_deliverable_gate `
  'cnn\hw_validation\rom\reports\readiness_input_round3' `
  --external-interface-source 'cnn\hw_validation\interfaces\ph1p_eram_interface_complete.v' `
  --comment-language zh `
  --json 'cnn\hw_validation\rom\reports\final_readiness.json' `
  --markdown 'cnn\hw_validation\rom\reports\final_readiness.md'
```

结果：退出码 `1`，`delivery_ready=false`，`427 errors / 0 strict warnings`。未通过，必须阻断 TD 接续。pure interface 不是 primitive 行为模型，未进入 Icarus 或综合源集合。

| 门禁项 | 实际状态 | 证据 |
|---|---|---|
| compile | passed | 冻结目录 2 files / 2 modules；静态 parser 无 compile error |
| ast | failed | formatter/AST 严格检查未闭合 |
| readability | failed | 包含本地位宽/运算锥和 vendor 边界未决项 |
| comment | failed | 只扫描两份生产 RTL；仍有 instance 布局与重复语义注释错误 |
| naming | failed | 严格命名/结构规则仍未闭合 |
| profile | passed | Erie strict profile 选择有效 |
| testbench | not_requested | production gate 未使用 `--include-testbench`；完整动态 TB 单独通过 |
| toolchain | not_requested | 本 gate 未请求外部综合；Icarus 动态证据单列 |

最终主要阻断项按报告统计为：`VG146` 90 inconclusive、`VG147` 90 inconclusive、`VG066` 80 failed、`VG138` 58 failed、`VG063` 18 failed、`VG097` 18 inconclusive、`VG153` 18 failed、`VG060` 8 failed、`VG132` 8 failed、`VG151` 5 inconclusive、`VG098` 4 failed，另有少量 `VG122/VG125/VG084/VG065`。其中 PH1P 输出驱动、时钟角色和组合锥的边界事实无法由 pure interface 证明；本地注释、literal/FSM 等失败也真实存在，不能把全部失败归因于 vendor boundary。按最多三轮证据修复边界冻结，不追加第四轮，也不改用无法在本轮证明 56 ERAM 映射的推断 ROM。

冻结闭包与哈希：

- gate root：`reports/readiness_input_round3/`，目录中只有两份 `.v`。
- `road_yolo_numeric_rom_group.v`：SHA-256 `a3eafe9e403a4292e4458c2fe0c30a77dce400ac00a3d52459b41fd8e4ce391c`。
- `road_yolo_numeric_rom_probe.v`：SHA-256 `74f00032df9fff02b45d3832534b668f8c53a395b53d34e6193abd290f3a7f83`。
- 两份冻结副本与原源逐字节相同；绑定文件为 `reports/final_source_binding.json`。
- `final_readiness.json`：SHA-256 `b25b7552c9b1861feb7408889ae5e198e069721a799398a70941cc427f44483d`。
- 完整 PH1P pure interface：SHA-256 `9348dec7d1294218c0fd609a06b12739c9c83d33ec555203cabf3a0a66c04245`；来源证明在 `cnn/hw_validation/interfaces/complete_provenance.json`。

## 限制与后续

- 当前不可宣称 strict Verilog 交付就绪；严格 gate 的 3 次修复预算已耗尽，不应启动 TD ROM 映射。
- 当前不可宣称厂商 PH1P 模型仿真通过；只有 Icarus 替身对拍通过。
- 未执行 TD 综合、布局布线、ERAM 使用率核对、烧录或板上关键字节读回。
- 用户没有板卡，本批明确不下载。
- required dependency 由父流程报告为可用；推荐 context 组件仍缺失，因此总体 dependency `ok` 仍为 false。
- catalog 中没有 `readable-python-generator` 和 `readable-script-generator`；Python golden 有单元测试证据，但不能宣称完整 Python/script skill governance 就绪。
- 下一角色应先读取 `requirements.json`、`codegen_plan.json`、`artifacts/manifest.json`、两份生产 RTL、本报告、`reports/final_readiness.json` 和 `reports/final_source_binding.json`。后续若获新一轮明确修复授权，必须保持官方 primitive 端口名，并先治理有证据的 vendor clock/output boundary 与本地静态规则，不得以 pure interface 冒充行为模型。
