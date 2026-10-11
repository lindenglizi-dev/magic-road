# `tb_ddr_ccl_banked_feed` 验证规格

## 用途与边界

该测试台用两个测试专用像素行银行向现有 `rle_ccl_top` 供数。它验证合法背压下的行顺序、银行交替、生产者停顿和 CCL 语义，不表示生产 RTL 已经包含该输入缓存，也不模拟 DDR、CDC 或取消管线。

## 接口与时序合同

- 时钟为 100 MHz 仿真时钟，复位为低有效异步复位。
- 生产者只写空银行；写完整行后置 `full`。
- 消费者按银行顺序读行，且仅在 `dut.u_raw_runs.write_bank_full==0` 时开始发送下一行。
- 每行像素坐标连续，`analysis_valid` 可按 `PIXEL_GAP` 插入合法空拍。
- EOL 与最后像素分离；EOL 后观察固定 flush 周期。只有最后一行等待 `row_done_debug` 后才发送 EOF。
- 两银行均满时生产者停止接受新行并记录停顿。末行只发送一次，EOF 只发送一次。
- `BANK_SUMMARY` 必须显示填充/发送行数等于帧高，且填充及发送银行交替错误均为零。

## 检查场景

1. 129 像素宽、每行 64 个 run 的压力 Mask。
2. 基线和扫描优化 `row_matcher` 分别运行。
3. `PIXEL_GAP=0/1` 的逐事件语义、最终分区和候选与 Python 整数参考一致。
4. 至少出现一次生产者停顿，且 `run_overflow`、`label_overflow`、`protocol_error`、`ccl_error` 均为零。

## 时序示意

```json
{
  "signal": [
    {"name": "clk", "wave": "p........"},
    {"name": "bank0_full", "wave": "01....0.."},
    {"name": "bank1_full", "wave": "0.1....0."},
    {"name": "producer_stall", "wave": "0.1..0..."},
    {"name": "analysis_valid", "wave": "0.1110..."},
    {"name": "analysis_eol", "wave": "0....10.."},
    {"name": "raw_write_bank_full", "wave": "0.....1.0"}
  ]
}
```
