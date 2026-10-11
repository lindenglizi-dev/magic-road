# `tb_ddr_roi_bytes` 验证规格

测试台为 `ddr_roi_byte_reader` 提供抽象的单拍 128-bit 内存返回模型。模型使用确定性的坐标颜色公式，最低字节地址放在 `[127:120]`；请求 ready 使用 LFSR 插入背压，返回延迟为1至5拍。

检查四个完整任务，每个任务逐项核对1024个灰度像素和 task/frame tag：全帧、偏移15跨拍重复采样、右下角最后一行、偏移14跨拍重复采样。另检查接受后的晚取消，以及取消后20拍无返回仍保持 `busy=1,reserved=1,drained=0`，随后释放返回才完成排空。

测试台每拍断言 `occupied_count+reserved_count<=1`，并检查字节请求地址16字节对齐、请求 tag 不变、取消任务不产生 ROI 输出。

```json
{"signal":[
  {"name":"clk","wave":"p..........."},
  {"name":"req_valid","wave":"01...0......"},
  {"name":"req_ready","wave":"0..1........"},
  {"name":"cancel","wave":"0....10....."},
  {"name":"rsp_valid","wave":"0.......10.."},
  {"name":"cancel_done","wave":"0........10."}
]}
```
