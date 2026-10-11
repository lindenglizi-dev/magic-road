# ccl_raw_run_table 行交接接口

隔离副本来自生产raw_run_table，参数、RAM、run写入、行切换、row_release和同步rd_req/rd_valid行为保持原样。仅模块名改为ccl_raw_run_table，并增加输出row_write_ready：当前run写银行未full时为1。不是像素银行empty，不表示所有银行已排空。

单clk上升沿、异步低有效rst_n；frame_clear同步清行状态。row_end上升沿被接收并标记当前银行full、翻转写银行；run_valid不得与row_end同拍。row_release释放消费者持有的原始run银行，与像素最后读不同。运行gold为原CCL现有参考；本副本不增加算法行为或容量。ADDR_WIDTH=6只适用于MAX_RUN≤64，本轮保持64。

验证：组合测试实际使用显式ready，core的row_input_commit连接detector_row_end，该边沿原始run表接收行结束。未综合或更改生产文件。

```json
{"signal":[{"name":"clk","wave":"p...."},{"name":"row_end","wave":"010.."},{"name":"row_write_ready","wave":"1.0.1"},{"name":"row_release","wave":"...10"}]}
```

相对时序声明未渲染，不是实际波形证据。完整端口与参数以同名.v及运行收据为准。
