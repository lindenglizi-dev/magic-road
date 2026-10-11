# RoadYOLO SiLU 时序复核与计算链准入报告

日期：2026-10-06，Asia/Shanghai。

## 当前未通过项

SiLU 在隔离探针中的数值、停顿行为与已报告路径时序有正面证据，但尚不能作为生产交付通过。主要阻塞是严格门仍有167条未闭合记录，以及 TD 报告剩余0.08%未覆盖对象尚未定位。当前没有已证明的负裕量路径，不应为了消除报告数字而改复位、加流水或放宽约束。

本次完成的是下一步的时序路径分类、时钟告警复核，以及进入计算链前的既有 MAC 回归；没有生成新的卷积/tile RTL、整网位流或板测结果。

## 实际执行与冻结范围

本次沿用 readable-verilog-generator 的验证与证据分离流程，按 ponytail 原则复用已有探针和测试，不新建解析 RTL 的工具，也不修改冻结设计。工程仍不是 Git 仓库，无分支、提交或推送。

- 冻结 CEA DUT SHA256：`5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938`。
- 原已路由 `pr.db` SHA256：`e92f620dfb966141bb04ce95dd6318655311b4053fec1200cf42111acb2067ef`。
- 器件 PH1P35MDG324、速度等级3，TD 6.2.168116，目标100 MHz。
- 用户已明确批准隔离诊断；本次只读导入数据库，没有重新综合或布局布线，没有改 SDC、DUT、生产工程、门禁规则、引脚或时序例外。
- 首次创建本次子目录及写日志遭沙箱权限拒绝；仅对明确的报告路径使用受审查的执行权限完成创建与日志保存，没有修改整个工程的 ACL。

主端独立路径审计和输入哈希见 [path_audit.json](timing_audit/path_audit.json)、[input_manifest.json](timing_audit/input_manifest.json)。审计程序含最小自检，重新运行退出0。

## 路径分类结果

下列值来自同一份已路由实现，不是新优化结果。路径详情中包含起终点、工艺角、逻辑及连线延迟、扇出；完整记录见路径审计 JSON 和原 TD 报告。

| 路径范围 | 检查 | 最差裕量 | 实际路径与说明 |
|---|---|---:|---|
| 全部已报告路径 | setup | +1.338 ns | `cnt_result_reg[3]_syn_2.clk` → `o_result_count[3]`，slow_m40c；探针输出 PAD 路径，不是 SiLU 内部算术路径 |
| 含 SiLU 的已报告路径 | setup | +3.121 ns | `reg_table_valid_reg_syn_3.clk` → ERAM `addra[4]`，slow_m40c；数据延迟6.435 ns，其中 cell 1.907、net 4.528，最大扇出21 |
| 全部已报告路径 | hold | +0.034 ns | `add4_syn_110.clk` → ERAM `dia[9]`，fast_m40c；数据延迟0.290 ns，其中 cell 0.065、net 0.225，时钟偏斜0.031 ns |
| 仅 get_regs 过滤路径 | setup | +4.262 ns | 表装载控制到探针地址寄存器 CE；数据延迟5.473 ns，最大扇出21 |
| 仅 get_regs 过滤路径 | hold | +0.054 ns | SiLU `flag_round_upper` → `flag_value_lower`，fast_m40c；数据延迟0.116 ns |
| 外部复位到寄存器 | recovery | +4.975 ns | slow_125c；数据延迟7.228 ns，复位最大扇出107 |
| 外部复位到寄存器 | removal | +0.053 ns | fast_125c；数据延迟1.463 ns，复位最大扇出107 |

`get_regs` 过滤集合不能替代全部内部路径：它没有完整覆盖 ERAM 端点。因此不能仅引用 +4.262/+0.054 ns 而忽略到 ERAM 的 +3.121/+0.034 ns。

全局 setup 的瓶颈是诊断外部边界；含 SiLU 的最长路径主要耗时在连线，但当前裕量为正，没有证据支持此时复制控制或加流水。hold 和 removal 余量很小，换 wrapper 或集成后必须重跑，不能沿用本探针裕量。

复位输入仍采用隔离探针零 I/O 延迟假设。正 recovery/removal 不证明实际板上异步释放安全，也不支持直接把所有异步复位改成同步复位。

## 时钟告警与覆盖率

本次实际只读导出：`import_db` 原 `pr.db`、`update_timing -mode final`、`get_clocks -include_generated_clocks -verbose`、`check_timing -verbose`、时钟端点/debug报告，以及含 ignored 的全部路径报告。原始命令日志见 [TD复核日志](coverage_followup/td_20261006_103438.log)。

新导出得到以下事实：

- 只枚举到 `probe_clk` 一个时钟对象；时钟树标为 primary，源为 `i_clk`。
- 时钟树含108个时钟负载，nonclocks=0。
- 详细 `check_timing` 为0个 local clock、0个断开主时钟的 generated clock；无缺失时钟、悬空节点、无效约束、组合环和缺失 I/O delay。
- 原报告则记为1个 local clock和1个断开主时钟的 generated clock。两份报告的差异保留，没有修改约束，不能写成“已经修复”，也不能直接归因为 RTL 生成了错误时钟或厂商工具缺陷。
- 使用 `include_ignored` 后覆盖率仍为99.92%；ignored、exception、abnormal 报告未列出能解释该缺口的具体对象。

剩余0.08%不能根据四舍五入的百分比换算为确定的路径数量。当前可用导出没有给出未覆盖对象名单，故该项保持未定位。正式签核前需要 TD 对应版本支持的覆盖对象查询或厂商说明；不能加 false path/multicycle、删对象或改变统计口径来补齐。

新导出见 [详细时钟检查](coverage_followup/check_timing_verbose.rpt)、[时钟树摘要](coverage_followup/clock_summary_debug.rpt)、[完整路径含ignored](coverage_followup/all_paths_include_ignored.rpt)。原报告保持不变。

## MAC 计算链前置回归

复用已有 `road_mac_probe` 和动态输入 wrapper，没有修改算法或 RTL。本次 Python 10项测试通过；Icarus 使用 `-g2001 -Wall` 编译并执行1031组向量，日志实际出现：

```text
VERILOG-GEN-RESULT PASS cases=1031 errors=0 reset=1 dynamic_words=12 io=140
```

结果见 [Python回归](timing_audit/mac_python_recheck.log)、[RTL对拍](timing_audit/mac_rtl_recheck.log)。编译与仿真退出0。首次因目录权限失败的命令没有产生有效仿真结果，不计为 DUT 失败或通过。

该探针仍是单事务在途：历史冻结协议记录 continuation 接受间隔11拍，accept到terminal valid为9拍。它有24个乘法操作，不等于持续每拍24 MAC。以上协议周期本次没有重新测量，仍按历史证据引用。

因此，进入最小计算链应复用其数值契约和测试向量，不直接把该单事务控制器当作整网高吞吐计算核。后续最小链必须实际串联 MAC累加、重定标、SiLU、特征写入和读回，并测量输入接受间隔、最后一次读回、墙钟耗时及各类等待。当前还没有这条联合 RTL 链的通过记录。

## 验证状态与未运行项

| 验收类别 | 状态 |
|---|---|
| SiLU 功能 | 前一批官方模型全域、定向和随机反压证据通过；本批未重复该全部功能矩阵 |
| MAC Python及RTL | 本批10项Python测试、1031组RTL向量通过 |
| 隔离物理时序 | 同一已路由数据库复核，已报告路径裕量为正；覆盖缺口和告警差异未完全解释 |
| 生产严格交付 | 保持167条未闭合，不重新计数、不改成PASS、不合入生产 |
| 最小卷积/tile联合链 | 尚未生成或对拍 |
| 整网资源与5 FPS | 未验证 |
| 板级及Flash自主启动 | 未运行 |

本批未修改 Verilog，未重新运行八项严格门。`compile、ast、readability、comment、naming、profile、testbench、toolchain` 的生产门状态沿用已冻结报告，不将本批 Icarus 成功换算成全部门通过。新增 Python 文本报告审计仅使用标准库和可执行自检，专用 readable-python/script 技能不可用，未声称通过相应专用门。

依赖检查进程退出1：required_ok=true，缺失项是推荐的 context-engineering；WaveDrom 3.6.1与必需技能存在。本次静态工具预检退出0。未安装新依赖，也没有远程执行。原始结果见 [dependencies.json](timing_audit/dependencies.json)、[preflight.json](timing_audit/preflight.json)。

## 下一项具体工作

当前最限制生产交付的是检查规范未闭合和时序证据覆盖缺口，不是已经证实的 SiLU 数值故障或负裕量。整网方向的下一瓶颈是计算与存储联合吞吐，不能用现有单事务探针代替。

先保持冻结 SiLU，不做无依据时序优化。覆盖对象定位与严格门整改继续跟踪；在独立验证范围内可以先完成小张量 Python中间值、最小链模块接口和周期契约，再实现联合探针。接口必须包含有效/就绪保持、复位取消、偏置仅一次、累加块首末、特征写完成与最后读消费事件。每一项先有参考和向量，再写RTL；不得先宣称联合链或5 FPS完成。

本次不需要用户提供现场视频、不需要板子、不需要新的训练授权；板级引脚和真实复位来源只在实际集成签核时确认。若必须新增时序例外或改变SiLU可见延迟，再单独请求决定。
