# `ddr_roi_byte_reader` 隔离规格

## 目的

从紧密 RGB888 帧的字节地址读取半开候选框，按像素中心最近邻规则产生 32×32 灰度 ROI。模块只允许一个已接受且尚未返回的 128-bit 请求。

## 接口合同

- `start_valid && start_ready` 接受任务，并锁存 task ID、frame ID、帧字节基址和半开框 `[x0,x1)×[y0,y1)`。
- `rd_req_addr_byte` 始终是16字节对齐的字节地址。`rd_req_valid` 在 `rd_req_ready` 前保持地址及 tag。
- `rd_rsp_valid/data` 没有 ready；本隔离合同假设每个已接受请求恰好返回一个128-bit拍，且返回至少晚于请求接受一个时钟。模块不支持请求接受同拍的零延迟返回。
- 一个像素占连续三个字节；最低字节地址对应 `rd_rsp_data[127:120]`。跨拍像素最多请求两拍。
- 灰度为 `(R>>2)+(G>>1)+(B>>2)`。
- `occupied_count + reserved_count <= 1`；返回槽兼作最近拍缓存。
- 取消立即停止新请求。已接受请求必须等真实返回并丢弃后才发 `cancel_done`；返回不来时 `busy=1`、`reserved_count=1`、`drained=0`。
- ROI 输出携带锁存的 task/frame tag。`roi_valid` 没有 ready；下游必须保证每个有效输出都写入 ROI RAM。最后一个有效像素与 `done` 同拍。
- 最近拍缓存以 frame ID 和帧基址作为内容身份。上游必须保证二者唯一对应尚未覆盖的同一帧内容；若复用 ID/基址或覆盖帧区，必须先使缓存失效。
- 异步复位会清除模块内的 `pending`，但这不能证明外部 DDR 已排空。正式接入需要协调复位并接收/丢弃旧返回；本测试只证明取消路径不会提前清除预留。

## 地址和 IP 边界

现工程 video_in/video_out 每128-bit命令地址加8，DDR配置为x16和BL8；候选适配是 `IP地址=字节地址>>1`。PAXI模式没有 `arlen/arsize/arburst` 端口，现有桥未传播 `rlast`，所以正式接入前仍须确认每命令的真实返回拍数及归属。

坐标和字节地址计算中的乘法是功能参考写法，尚无综合结果，不代表已完成低资源乘法器优化。

## 验证场景

- 全帧采样、跨拍偏移14/15、重复采样、右下角和最后一行。
- 请求随机背压，1024个ROI像素逐项对拍。
- 接受后晚取消，以及取消后无返回时保留 reserved/busy。
- 非法额外返回必须置 `protocol_error`。

## 时序示意

```json
{"signal":[
  {"name":"clk","wave":"p........."},
  {"name":"rd_req_valid","wave":"01..0....."},
  {"name":"rd_req_ready","wave":"0.1......."},
  {"name":"reserved_count","wave":"0.1...0..."},
  {"name":"rd_rsp_valid","wave":"0.....10.."},
  {"name":"roi_valid","wave":"0.......10"}
]}
```
