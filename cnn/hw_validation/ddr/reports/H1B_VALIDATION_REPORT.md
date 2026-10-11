# H1-B DDR/PAXI 隔离原型验证报告

日期：2026-10-04  
结论：`integration_release=false`。**行为自检通过，但严格静态门禁未通过；禁止据此接入生产或生成 production READY。**

## 验证对象与边界

- 对象是 `cnn/hw_validation/ddr/` 下的全局单在途、单个 16 B 请求 PAXI 隔离原型，不是生产桥。
- 合法地址为 `[0x03400000, 0x04000000)` 且 16 B 对齐，PAXI 地址固定为 `byte_addr >> 1`。
- 写数据在 AW 前缓存；W 不先于 AW，AW 接受后一拍首次呈现 W；该“两拍”约束按**呈现期限**解释，不代表 WREADY 必须在两拍内接受。
- `i_commit_confirmed` 仅表示经外部证明的写提交事件。当前 vendor/controller 提交语义未知，因此生产连接必须保持未使能，不能把 AW/W 接受或 mock 事件冒充 committed。
- AR/AW 一旦呈现，即使本地取消也保持 VALID 和地址至真实 READY 握手；已接受请求保留 owner 到晚返/提交事件排空。取消后的终止事件只计丢弃，不发布成功。
- `i_cancel` 对已保持的结果是双方共享 flush 例外；它不是普通 ready/valid 可随意撤销 VALID 的规则。
- 未执行 TD、下载、烧录或板测；本文所有通过项均为本地模型/RTL mock controller 证据。

## 可复跑的本地行为证据

Python 行为参考：

```powershell
& 'E:\project\qiansai\.tools\road_yolo_venv\Scripts\python.exe' -B -X utf8 .\cnn\hw_validation\ddr\paxi_single_outstanding_model.py
```

实际结果：

```text
H1-B Python behavior reference: PASS
```

固定随机种子为 `0x51B`。覆盖地址上下界和对齐、AW/W 背压、高有效 mask、呈现前取消、AR 已呈现后取消、取消与 AR 接受同拍、晚返丢弃、缺失 RLAST、意外返回、过早 commit 和非法地址 fail-closed。

Icarus RTL 自检：

```powershell
iverilog -g2001 -Wall -s tb_paxi_single_outstanding_bridge -o .\cnn\hw_validation\ddr\h1b_final.vvp .\cnn\hw_validation\ddr\paxi_single_outstanding_bridge.v .\cnn\hw_validation\ddr\tb_paxi_single_outstanding_bridge.v
vvp .\cnn\hw_validation\ddr\h1b_final.vvp
```

实际结果：

```text
 > INFO: [Verilog] H1-B isolated PAXI bridge PASS
$finish called at 885000 (1ps)
```

自检 TB 验证了 AW/AR 在取消和背压下稳定、W 必须晚于 AW、数据/mask 稳定、写接受不等于提交、显式后续 commit 才能成功、取消后的读写晚终止丢弃、正常读结果背压保持、`accepted = success + cancelled_drained` 排空边界守恒，以及非法地址/缺失 RLAST/意外返回/W 握手同拍 commit 的 fail-closed 行为。

规范 JSON 已通过 canonical `write-spec` 的 RTL 端口交叉检查，并生成 Markdown 与两张 WaveDrom SVG。该项证明规范可以重建和渲染，不证明 vendor controller 语义。

## 继续修复后的最终冻结状态

本轮最多三次修复预算已经耗尽。attempt4 和 attempt5 均在静态组合锥分析中持续高 CPU 且未发布 JSON/Markdown；它们记录为**验证工具未终止**，不能表述为 RTL 失败，也不能表述为通过。attempt6 使用项目 venv、技能根 cwd 和全绝对输入路径，并在允许发布报告后正常终止。

最终 attempt6：`delivery_ready=False`，`errors=42`，`strict_warnings=0`，因此 `integration_release=false`。

| 门 | 状态 | 错误 | 警告 | 说明 |
| --- | --- | ---: | ---: | --- |
| compile | passed | 0 | 0 | 静态解析/编译检查通过 |
| ast | passed | 0 | 0 | formatter AST 解析及模板一致性通过 |
| readability | failed | 42 | 0 | 结构、FSM 与组合预算仍阻断 |
| comment | passed | 0 | 0 | 注释门通过 |
| naming | failed | 5 | 0 | 名称/区域归属相关门未通过 |
| profile | passed | 0 | 0 | 严格配置门通过 |
| testbench | not_requested | 0 | 0 | design-only 静态运行；Icarus 自检证据独立列出 |
| toolchain | not_requested | 0 | 0 | 未运行 TD/vendor controller 工具链 |

attempt6 finding 计数：`VG031=1`、`VG054=1`、`VG057=1`、`VG061=8`、`VG065=2`、`VG066=2`、`VG070=3`、`VG071=2`、`VG109=2`、`VG122=3`、`VG145=1`、`VG146=16`。

本轮已消除旧报告中的 `VG094`、`VG098`、`VG125`、`VG137`、`VG138` 和 `VG155`；尤其请求消费现已显式使用 `i_req_valid && o_req_ready`。剩余关键阻塞是：

- `state_next` 仍有 17 个源、63 个操作，超过 3 源/3 操作严格预算；安全修复需要多周期架构分解，不能在本轮为了评分改变可见协议时序。
- 请求载荷、owner、地址、数据与计数器的时序 D 锥仍超过操作预算。
- 三个 32 位诊断计数器加法仍被 VG122 判定结果宽于目标；尝试的显式 carry 网络使分析不终止，因此已回退为行为正确且可分析的 `+ 1'b1`。
- formatter 的输出镜像归属与同一缓存驱动多个接口输出产生区域/顺序冲突；不通过重命名端口或改变外部接口规避。

冻结文件哈希：

| 文件 | SHA-256 |
| --- | --- |
| `paxi_single_outstanding_bridge.v` | `364920D2E1D2C006C62F07A91CB8CDA95033B9F17CDFEB7CBAAC4CB293B4BD5F` |
| `tb_paxi_single_outstanding_bridge.v` | `D6BC4CA60DC44B415E18822C4BDB07E385E71DC8C34ACE13C7AF727C9DB440EF` |
| `paxi_single_outstanding_model.py` | `B3EE343BB0F3BD8B768D93C3E288EA4D574DBB46817F9CD58A8284F4ADB7CC2C` |
| `paxi_single_outstanding_bridge_spec.json` | `1EA27666B398CD8CAFCB0EC8CDB7ABB17AB8553CD896CB132C9FC79B7B57EF8C` |
| `strict_gate_attempt6.json` | `E04E479945F101548D7D77DFBD3B5AF306C1926B515ADB3686F492B4E5276B0F` |
| 生成的 `paxi_single_outstanding_bridge_spec.md` | `2B0003FF0D87111932C18287B0FE3C1D3F615A234314BF522DD1AA4604F94348` |

## 历史第 3 次严格静态门禁

原始证据：`strict_gate_attempt3.json` 和 `strict_gate_attempt3.md`。该历史结果保留用于对照，不覆盖 attempt6。

| 门 | 状态 | 错误 | 警告 | 说明 |
| --- | --- | ---: | ---: | --- |
| compile | passed | 0 | 0 | 静态门内部编译检查通过 |
| ast | failed | 1 | 0 | AST 质量门未通过 |
| readability | failed | 87 | 0 | 可读性/结构规则未通过 |
| comment | passed | 0 | 0 | 注释门通过 |
| naming | failed | 5 | 0 | 命名门未通过 |
| profile | passed | 0 | 0 | 配置门通过 |
| testbench | not_requested | 0 | 0 | 第 3 次为 design-only；真实 TB 结果见上方 Icarus 日志 |
| toolchain | not_requested | 0 | 0 | 未把 TD/vendor 工具链纳入该次门禁 |

汇总：`delivery_ready=False`，`errors=88`，`strict_warnings=0`。

最终 finding 计数：`VG031=1`、`VG057=1`、`VG061=8`、`VG065=1`、`VG066=7`、`VG070=3`、`VG071=2`、`VG094=1`、`VG098=10`、`VG122=3`、`VG125=3`、`VG137=1`、`VG138=27`、`VG145=1`、`VG146=16`、`VG155=2`。

主要未清项：端口顺序启发式、区域与声明分组、注释间距/重复、FSM 默认态与可达性分析、计数器算术/字面量规则、源文件与操作预算、以及输出 valid/ready 消费者识别。部分规则与 formatter 输出或本原型的 fail-closed 默认态存在冲突/分析局限；未通过并不被行为 PASS 抵消，也没有为了门禁通过而把默认故障态放宽。

第 1 次包含 TB 的静态运行曾把 testbench 子门报告为 passed，但同次整体有 933 个错误，且 TB 格式化解析报告“only single module sources are currently supported”；因此不把该子门状态当作完整静态通过证据。

## 未决风险与放行条件

1. 必须从 build-matched controller 文档或实测获得写提交可见性/排序事件，才能定义 `i_commit_confirmed`；在此之前 production READY 必须保持禁用。
2. 必须确认 controller 对 AW 接受后 WVALID 首次呈现时限的定义，以及 WREADY 可长期背压是否被允许。
3. 必须在真实 controller 上验证无 RREADY 返回、单拍 RLAST、复位协调与晚返边界；mock PASS 不等同于 controller PASS。
4. 严格静态门禁仍为失败，当前交付仅可作为隔离探针和协议讨论载体，**不具备集成放行资格**。
5. 未使用超时释放 owner/bank；后续不得用超时掩盖无法归属的返回。
