# ccl_pixel_line_banks：双银行像素行缓存合同

该模块仅用于隔离实验，未接入生产 FPGA 顶层。默认参数为 `WIDTH=129`、`X_WIDTH=8`、`Y_WIDTH=8`、`ID_WIDTH=32`。所有接口位于 `clk` 单时钟域，`rst_n` 为异步低有效复位。

## 输入与银行所有权

`in_valid && in_ready` 才接受像素。首个已接受像素把 `in_task_id` 和 `in_y` 固定到当前写银行；同行后续像素必须保持相同身份。内部 x 从 0 连续递增，只有 x=`WIDTH-1` 的已接受像素必须带 `in_last=1`，`in_frame_last` 只允许随该末像素出现。身份、y、行长或末帧标志错误会置位 `protocol_error`、丢弃当前行；错误保持到复位。

两银行按 0、1 交替写入和读出。银行只在末像素输出握手后释放。两个银行均被占用时 `in_ready=0`；源端须保持输入 payload，直到握手或取消。输出的任务号、y 和末帧标志来自银行锁存元数据，不使用当前输入身份。

## 同步读与背压

每次读请求保存银行、地址、x 和元数据；下一上升沿从 `pixel_mem` 读取到 held 返回寄存器。`out_valid && out_ready` 才推进输出。held 未被接受时全部输出保持稳定。本实现最多一个 read pending 和一个 held 返回；为保持最小且无溢出的读管线，不在 pending 返回拍同时再发下一读请求。

`empty=1` 要求两个银行均为空、没有 pending 读且 held 无效。它表示本模块内部已经排空，不表示外部 DDR 或其他模块已经排空。

## 取消、复位与同拍优先级

`cancel=1` 的时钟沿优先于输入、输出和读请求：该拍不接受输入、不确认输出，未发送银行被清除，held 被丢弃，正在返回的 pending 数据也被明确丢弃。取消结束后不会出现旧任务迟到输出；新任务身份由上层控制。`protocol_error` 不因取消清零。

复位清空两银行、pending、held、读写指针和 `protocol_error`。像素 RAM 内容不复位，因为有效性完全由银行状态限定。

## 时序声明

```json
{"signal":[{"name":"clk","wave":"p......"},{"name":"in_valid","wave":"0111100"},{"name":"in_ready","wave":"0111100"},{"name":"in_last","wave":"0000100"},{"name":"bank_state","wave":"=.=..=.","data":["EMPTY","FILL","FULL"]},{"name":"read_pending","wave":"0000010"},{"name":"out_valid","wave":"0000001"}],"head":{"text":"完整行进入银行，读请求后一拍进入held输出"}}
```

## 验证范围

`tools/ddr_line_bank_reference.py` 是周期级合同模型。`tests/tb_ddr_line_banks.v` 覆盖输出背压稳定、两银行交替、双满停供、双满取消、末返回取消、错误 task/y/行长、错误粘滞和银行 tag 保留。Icarus 仿真只证明该隔离模块的单时钟行为；不证明器件 RAM 推断、综合时序、DDR 返回或生产接入。
