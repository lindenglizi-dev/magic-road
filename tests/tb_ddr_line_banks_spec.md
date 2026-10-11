# tb_ddr_line_banks 验证合同

测试台以 `WIDTH=5` 缩短仿真，但保持与默认 129 像素相同的握手、行末、银行和取消规则。测试输入只在 `in_valid && in_ready` 时计入；输出只在 `out_valid && out_ready` 时计入。

覆盖项：两行连续写满后停供；银行 0/1 顺序和 task/y tag 保留；输出背压期间全部 payload 稳定；末像素握手后才释放银行；双满取消；最后一个同步读返回拍取消；取消后无迟到输出；task 不一致、y 不一致、短行、末像素缺少 `in_last`；错误保持到复位；复位后正常恢复。

通过标志为 `PASS line banks checks=<N>`。测试不模拟 DDR 控制器、CDC、生产顶层、器件 RAM 映射、综合时序或 CCL 算法结果。

```json
{"signal":[{"name":"clk","wave":"p....."},{"name":"out_valid","wave":"0111.0"},{"name":"out_ready","wave":"0001.0"},{"name":"out_x","wave":"=...=.","data":["x0","x1"]},{"name":"stable","wave":"01..0."}],"head":{"text":"背压时held输出保持，握手后才推进"}}
```
