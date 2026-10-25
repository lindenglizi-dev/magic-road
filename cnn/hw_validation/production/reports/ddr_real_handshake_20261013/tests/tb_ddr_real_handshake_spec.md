# `tb_ddr_real_handshake` 验证规格

## 1. 目的与边界

本测试平台对未修改的 PH1P DDR2 原厂控制器执行一次启动和有限端口观察。它验证 PAXI 请求是否被真实 `READY` 接受，并观察控制器公开层次中的 B、DHI 命令和 DDR2 命令脚。

测试不包含 DDR2 器件模型，不检查写入是否落存，不把 `BVALID`、DHI 命令或 DDR 命令脚解释为存储提交，也不把任意 `RDATA` 解释为正确数据。所有结果必须带 `memory_model=ABSENT` 和 `memory_pass=0`。

## 2. 模块合同

- 模块：`tb_ddr_real_handshake`
- 源码：`tests/tb_ddr_real_handshake.v`
- 端口：无；这是仿真顶层。
- 参考时钟：`ref_clk`，周期 10000 ps。
- 复位：`sys_rst_n` 低电平保持 2000000 ps，随后在 `ref_clk` 负边沿释放。
- 用户时钟：原厂 IP 输出 `dhi_clk`。
- 全局看门狗：1000000000 ps。
- 单通道等待上限：2048 个 `dhi_clk` 周期。
- 写后观察窗口：64 个 `dhi_clk` 周期，仅用于观察，不代表提交屏障。

## 3. 冻结激励

| case | 地址 | AW/W 呈现关系 | 数据 |
|---:|---:|---|---|
| 0 | 0 | 同一采样拍前有效 | `00112233445566778899aabbccddeeff` |
| 1 | 8 | AW 接受后第 1 个采样拍允许 W 接受 | `102132435465768798a9bacbdcedfe0f` |
| 2 | 16 | AW 接受后第 2 个采样拍允许 W 接受 | `ffeeddccbbaa99887766554433221100` |
| 3 | 0 | 三次 AW/W 接受及有限观察窗口后唯一一次 AR；不是写提交屏障 | 无期望数据 |

所有写均使用 `WSTRB=16'h0000` 和 `WLAST=1`。AW、W、AR 各自保持到本通道真实握手；一个通道的 READY 不得替代另一个通道的 READY。

若任一 AW/W/AR 在 2048 个用户时钟周期内没有接受，测试打印 `REAL_ERROR` 并终止，不复位或重发。AR 接受后最多等待 2048 周期；没有 RVALID 时打印 `REAL_READ_RETURN_NOT_OBSERVED`，保留未完成 owner 事实并停止继续发读。

## 4. 只读观察点

```text
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.u_alc_mc_top.paxi_bvalid
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.u_alc_mc_top.paxi_bresp
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.dhi_cmd_vld
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.dhi_cmd_code
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.dhi_wdata_en
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.dhi_wdata
dut.ph1p_ddrmc_wrapper.ph1p_ddrmc_top.dhi_wmask
```

DHI 命令类型取 `cmd_code[31:28]`：实际 `ph1p_ddrphy_cmd_decode.v` 使用 `4'hc` 写、`4'hd` 读。上层 `cmd_execution.v` 虽定义 WR=7/RD=8，却没有用这些枚举译码，不能拿它们作为线上编码。DDR2 命令脚在 `ddr_ck_p` 上升沿采样：`{RAS_N,CAS_N,WE_N}=3'b100` 是写，`3'b101` 是读。两者都只是命令发出证据。

`dhi_wdata_en` 是 PHY 请求控制器提供数据的信号；同沿观察的数据可能仍属先前值，不构成该请求的数据对拍。本轮不宣称 DHI 数据路径逐字节通过。

内部 B、DHI 和 DDR 脚事件的 `window_case` 只是当前观察窗口标签，不是控制器提供的事务 ID；迟到事件不能根据该字段强行归属。跨时钟事件以 `time_ps` 比较，不用可能同沿更新的 `dhi_cycle` 解释亚周期延迟。`last_bresp` 仅在 B 计数非零时才有意义。

加密 MC 的 B 端口虽在公开端口表中存在，但明文顶层没有连接。若 ModelSim 不能解析该只读层次，必须保留编译失败证据并在后续明确移除 B 观察；禁止修改原厂源、绑定替代实现或强制内部状态。

## 5. 协议检查

- AW 背压时地址保持。
- W 背压时数据、掩码和末拍保持。
- AR 背压时地址保持。
- VALID 有效时对应 READY 必须为确定的 0 或 1。
- 没有已接受读 owner 时出现 RVALID 属于显式错误。
- 驱动协议错误打印 `REAL_ERROR` 并 `$fatal`。
- `RDATA` 允许含 X；使用归约异或检查并原样记录。

## 6. 期望日志

- 每个底层事件：`REAL_EVENT`，包含 `dhi_cycle` 和以 `%0d` 打印的 `time_ps`。
- 每个激励：`REAL_CASE`。
- 无读返回：`REAL_READ_RETURN_NOT_OBSERVED`。
- 流程完成：`REAL_OBSERVATION_COMPLETE`。
- 最终统计：`REAL_SUMMARY`。

只有 `REAL_OBSERVATION_COMPLETE` 和 `REAL_SUMMARY`、无 `REAL_ERROR`/`$fatal`、工具正常退出且运行期间源码哈希不变，才表示本次观察流程完整；它不表示内存通过。握手在用户时钟有效沿采样，驱动在负沿更新。

## 7. 时序示意

```json
{
  "signal": [
    {"name": "dhi_clk", "wave": "p..........."},
    {"name": "AWVALID", "wave": "01.0..10...."},
    {"name": "AWREADY", "wave": "0.10..1....."},
    {"name": "WVALID gap0", "wave": "01.0........"},
    {"name": "WVALID gap1", "wave": "0..10......."},
    {"name": "WVALID gap2", "wave": "0....10....."}
  ],
  "head": {"text": "示意图；实际接受完全由原厂 READY 决定"}
}
```

## 8. 不允许事项

- 不使用 `force`。
- 不注入 DDR 器件模型或假读数据。
- 不修改原厂 RTL、参数、端口或内部状态。
- 不用固定延迟宣称提交。
- 不生成位流、不访问板卡或 Flash。
