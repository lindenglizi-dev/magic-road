# ccl_rle_stream_core 显式行入口

生产rle_ccl_top的隔离接线副本；算法和CCL子模块保持原样。raw_run_table换为同逻辑的ccl_raw_run_table以接出真实写银行ready；新增row_input_ready、row_input_commit、core_idle。MIN_RUN、MIN_AREA、MAX_LABEL及标签位宽由组合顶层参数指定，本轮回归两种row_matcher。

- row_input_ready：phase为SCAN且原始run写银行可用。发一行前获得ready后，行像素顺序交接，不能把它当逐像素ready或RAM返回ACK。
- row_input_commit：detector_row_end；上升沿是run表实际接收完整行的时刻。尾run会由run_detector先发出，不能固定等待四拍猜测commit。
- row_done_debug：matcher一行完整处理结束；顶层累计完成行数，末行EOF等待全部输入行处理完毕，避免错认上一行done。
- core_idle：SCAN、matcher/resolver/selector/label_manager不busy且raw未锁定。用于受控复位后确认重新就绪，不独立证明任意正常任务的全部外部活动已排空。

单时钟上升沿、异步低有效复位。部分run_detector错误只复位清除，组合恢复对整个核心施加一个完整时钟的受控复位，并检查core_idle/error后才ACK；复位持续时间是定义的复位协议，不是固定拍数排空。生产路径未修改。

```json
{"signal":[{"name":"clk","wave":"p......"},{"name":"analysis_eol","wave":"010...."},{"name":"row_input_commit","wave":"0..10.."},{"name":"row_done_debug","wave":"0....10"}]}
```

波形只声明相对事件顺序，尾run可改变EOL到commit延迟；未渲染。接口以同名源码为准。
