# row_matcher 隔离优化合同

此模块仅用于本地差分验证，模块名和全部端口与生产 row_matcher 相同，不进入正式工程源列表。基线为 `user_source/hdl_source/road_vision/row_matcher.v`；行为金标为 `tools/ddr_ccl_scan_reference.py`。用户已批准已有 Icarus 路径，不安装远端或 WaveDrom 依赖。

clk 上升沿；rst_n 异步低有效，frame_clear 同步高有效且优先于任务。全部接口在同一时钟域，不新增 CDC。

start 拍检查 raw_locked 前置条件，并锁存 raw_run_count、prev_count 和 raw_row_y；raw_locked 本身不寄存。raw_rd_req/raw_rd_idx 请求对应 raw_rd_valid/raw_rd_start/raw_rd_end 返回。previous-row 请求无 ready，逐拍发出；返回保持原表顺序且数量与 prev_count 相同。全数返回后才解析，不按请求发完推断返回完成。start 忙时仍按生产规则报 matcher_error。

新增 match_label_limit 为 LABEL_WIDTH 位，最大值 MAX_LABEL。reset、frame_clear、新 run 载入时清零；仅合法且相交的 previous-row 原始标签参与 max。label_scan_index 保持 LABEL_WIDTH+1 位。扫描仍从 1 开始，bitmap 原始标签升序不变；解析上界由 MAX_LABEL 改为本 run 的 match_label_limit，保留上界外终止拍。union 根只更新 base_label，不改变上界或次序。

alloc_req/alloc_done/alloc_label、union_req/union_done/union_root、curr_wr_*、feature_update_*、row_commit、raw_release、row_done 的语义及相对事件顺序保持不变，绝对延迟会提前。无重叠直接走原分配路径；非法零/超界标签及分配失败处理不变。不回收标签，不压缩路径。

参数约束：MAX_LABEL≥1，MAX_LABEL < 2**LABEL_WIDTH；MAX_RUN≤2**ADDR_WIDTH。检查逐 run 坐标/标签/new 标志、union 次序、最终根/面积框/对象，记录实际总周期、扫描周期与 row/resolve/select 峰值。覆盖无重叠、最后返回最大标签、桥接、最高编号、溢出→空→正常、合法 valid 间隙。SOF 忙状态仅故障探针，不属正常输入。

相对时序声明如下；未经 WaveDrom 渲染，不是仿真证据。

```json
{"signal":[{"name":"clk","wave":"p...."},{"name":"prev_rd_valid","wave":"010.."},{"name":"prev_rd_label","wave":"x=x..","data":["MAX_LABEL"]},{"name":"match_label_limit","wave":"0.=..","data":["MAX_LABEL"]},{"name":"state","wave":"==...","data":["SCAN_PREV","RESOLVE_LABELS"]}],"head":{"text":"最后返回更新在下一解析拍可见"}}
```

本地编译/仿真不能替代综合、布局布线、实际 DDR/视频调度或全部风格门禁；风格门禁另行记录，不通过时禁止正式接入。
