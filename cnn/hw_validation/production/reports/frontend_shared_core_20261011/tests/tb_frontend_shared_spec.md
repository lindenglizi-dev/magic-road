# tb_frontend_shared 验证规格

## 目的

端口为空的仿真顶层复用旧全量向量，验证 2304 个 Stem tile 与 576 个 down2 tile 经 `road_frontend_shared_core` 的唯一 `u_mac`、唯一 `u_pp` 连续运行。Stem 的实际导出数据填充 `input_tensor`，down2 halo 不得由黄金张量驱动。

## 时钟、复位与接口

- `clk` 为 100 MHz；`rstn` 为低有效异步复位，正常全量序列只在开头释放一次。
- SiLU 表经公共表口装载一次；Stem 导出完成后切到 down2，不复位、不重装表。
- Stem 与 down2 保留各自 testbench 驱动变量，由 `selected_down2` 只在顶层公共入口前选择；testbench 不直接驱动所有权状态。
- `commit_ready` 与 `output_ready` 分别制造内部写回和导出反压。

## 检查项

1. 表只装 1023 项时 `start` 不得进入 busy；第 1024 项后才允许任务。
2. Stem 忙、done 后尚未导出、导出有效且被反压时，阶段切换均必须拒绝。
3. `done` 为高的同拍，以及下一拍 IDLE 但未导出的状态，都必须拒绝切换。
4. 最后一次 Stem 导出握手清空未导出状态后，下一空闲边界接受切到 down2，且 `table_loaded` 保持。
5. Stem 的 MAC、pre、SiLU、post、commit、export 全量对拍；实际 589824 字节导出填充下游输入。
6. down2 的 MAC、pre、SiLU、post、commit、export 全量对拍；检查重复、空洞、halo、padding 和周期分类闭合。
7. `normal` 与 `stalls` 两种模式都必须完成；本测试不代表 DDR、整网、物理时序或部署 QAT 通过。
8. 每拍验证两个调度器各自 `load_ready -> !mac_valid`，证明空闲判定不需要反馈读取发射 valid；结构无环仍须实际综合核实。

## 时序示意

```json
{"signal":[
  {"name":"clk","wave":"p........."},
  {"name":"stem_busy","wave":"01..0....."},
  {"name":"stem_done","wave":"0...10...."},
  {"name":"output_valid","wave":"0.....1.0."},
  {"name":"output_ready","wave":"1.....01.."},
  {"name":"select_valid","wave":"0.10.10.10"},
  {"name":"select_ready","wave":"0........1"},
  {"name":"selected_down2","wave":"0........1"}
]}
```

示意图压缩了真实计算和 256 项导出周期；前三次选择请求分别代表 busy、未导出和导出反压拒绝，最后一次在完全排空后接受。
