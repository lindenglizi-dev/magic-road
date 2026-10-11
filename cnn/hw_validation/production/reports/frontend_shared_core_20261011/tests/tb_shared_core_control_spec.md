# tb_shared_core_control 验证规格

## 目的

用最小零值 Stem tile 覆盖装表中复位、非法 Stem 高地址、故障命令封锁、写回长反压期间复位，以及完整重装后的恢复运行。

## 通过条件

- 装表中复位后，旧参数、旧 halo 和部分旧表不得让 `start` 进入 busy。
- Stem 地址 512 不得截断成地址 0；必须置 fault，并封锁 select/load/start。
- 写回结果在 `commit_ready=0` 下保持时复位，`busy`、MAC/PP valid 和导出 valid 均立即清除。
- 阶段所有权回到 Stem，`table_loaded` 清零；完整重装后一个 4x4 Stem tile 输出 256 项零值且无故障。
- select提前保持valid时，旧任务计算和导出必须继续，导出后自动完成选择握手，再返回Stem。
- table提前保持valid时，旧任务继续使用原表并导出；只有排空后接受第一项，完整1024项重装后loaded恢复。
- 三次恢复/持续请求测试各导出256项，共768项，逐项核对编号和零值。

```json
{"signal":[
  {"name":"clk","wave":"p......"},
  {"name":"rstn","wave":"1..0.1."},
  {"name":"busy","wave":"01.0..."},
  {"name":"table_loaded","wave":"1..0..."},
  {"name":"selected_down2","wave":"0......"},
  {"name":"select_ready","wave":"0....1."}
]}
```

该测试证明控制取消和恢复后的零值fixture，不代替非零极值数值验证；全量冻结数值由 `tb_frontend_shared` 覆盖。
