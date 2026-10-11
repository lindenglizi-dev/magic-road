# v10 原始 RTL 风险与真实路径证据

## 冻结输入

- `road_postprocess_stream.v`: `63392A96003D24BA000A3B0ABAA7EAFA9C5E49A921E22D2E56949326F1040650`
- `down2_overlap_tile_runner.v`: `DF69AF9BAD06A76D5C2A72CAAB9DD556F6C0D21F1CBBCD2B0DAB4FB5C87E108D`
- v11 冻结清单: 4686 个文件，清单 SHA-256 为
  `7fa8cc8baa1cdd5451ae4eb3fa9953f36e6e46b5da4af97209bf1fd899616bb7`。

本记录只分析冻结输入，不把静态门禁占位诊断解释成已证明的语义错误。

## 七条内部 setup 违例

物理证据真源为 `physical/v10_internal_setup_paths.json`，其 SHA-256 为
`CBAFAA83D91F061962229F8BD30A96197E3C35FFE3BDFFBFF67340DDF504B0FB`。

其中五条端点具有同一真实锥：

1. 起点均为 `reg_group_mask_head[1]`；
2. 经过 lane 选择、符号扩展、固定系数乘法；
3. 进入冻结 `road_round_shift_Inst_pre` 的绝对值/取负逻辑；
4. 路径逻辑均包含选择 LUT、`DSPMULT`、`DSPTADD` 与 round 内加法器；
5. 最差 slack 为 -0.232 ns，其余为 -0.152/-0.074/-0.056/-0.004 ns。

因此，产品、shift、tag 的单项弹性寄存器位于乘法之后、冻结 round 之前，
能直接切断这五条路径。仅移动 valid 而不同时寄存 product/shift/tag 会破坏元数据同步，
因此不可接受。

另外两条路径从 SiLU 的 `table_fault_o_reg` 出发，分别到 runner 的
`cnt_output[2]` 和 MAC 的 `mult17.xa[1]`。它们的 net 占比分别为 82% 和 90%，
属于高扇出故障控制路径。冻结 runner 在 `pp_fault || flag_load_fault` 当拍保持/清理调度状态；
延迟或寄存该故障会改变 fatal 可见性与取消语义。因此首个候选不改这两条控制路径，
先用新布局确认产品切分带来的放置变化是否已消除它们。

## runner formatter-AST 覆盖缺口

冻结 v10 门禁报告为 `modules=0`、`parse_errors=1`，外层只给出
`FORMATTER_AST_PARSE`。v11 的 guarded exception-chain probe 定位到：

```text
case_normalization_violation: end
```

解析器在 `i_load_kind` case 中遇到以下单行形态后，把随后的 case-item `end`
误识别为新的 case item：

```verilog
end else begin flag_load_fault <= 1'b1; end
```

冻结源中共有六处，位于 489、496、503、510、517、524 行。它们均为合法
Verilog，问题是 formatter 对该紧凑形态的覆盖不足。v11 只把每处展开为：

```verilog
end else begin
    flag_load_fault <= 1'b1;
end
```

该修复不改 token 序列、控制条件、赋值目标或赋值值。候选的全文件非空白字符
顺序比较已 PASS，两侧 compact SHA-256 同为
`d7dd007566d7a6dccb7508921a23506f0ba75216990585aa5d5acf203c7e93be`。
formatter 复验不再报该 case normalization 错误，随后到达既有 FSM 结构检查并以
`state_machine_violation` 停止。该更深层失败被保留且未豁免；本任务不重写 runner FSM。

## 首个候选边界

- 仅在 pre-round 前加一个深度为 1 的弹性切分；
- 两个 `road_round_shift`、一个 `silu_shared_unit` 与 MAC 核均不修改；
- 外部端口、固定系数、数值位宽、lane 规则与 II=1 不修改；
- reset 或既有 sticky fault event 清除新增 valid；
- table global-empty、busy 与 inflight 计数必须包含新增 token；
- reload 请求只阻止新组 admission，已接收 token 继续排空；
- 两条 `table_fault` 控制路径在首个候选中保持完全不变。

具体可见延迟、最大未决 token 数与观察信号定义必须以先行 Python 接受模型和
deep review 的 PASS 结果为准；模型通过前不写候选 RTL。
