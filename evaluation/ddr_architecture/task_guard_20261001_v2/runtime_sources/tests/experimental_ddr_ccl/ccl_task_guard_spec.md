# ccl_task_guard：单任务接受与整帧结果资格合同

隔离实验，尚未接入生产 FPGA 工程。行为参考为 `tools/ddr_ccl_task_guard_reference.py`，测试与生产 CCL、现有 object_frame_store 串联。全部端口定义以同名 Verilog 为准，参数 ID_WIDTH=32、X_WIDTH=8、Y_WIDTH=8、LABEL_WIDTH=6、AREA_WIDTH=16；不新增 CDC，不包含 DDR 读请求或返回缓存。

## 接受和供数

clk 上升沿；rst_n 异步低有效。task_valid/task_ready 同时为真接受 task_id/task_frame_id；valid 等待 ready 是正常背压，源端保持描述稳定。只在 IDLE 接受，不支持抢占，不在结果接收的同拍接受下一任务。task_id 在不跨复位的账本区间内由调用者保持唯一。

core_frame_clear 只在接受新任务或显式取消排空完成时为真，接核心 analysis_sof 和对象缓存 frame_clear。数据从接受后下一拍开始；不能在接受拍同时供首像素。stream_event 表示像素、SOF、EOL、EOF 中任一事件，stream_task_id 每个事件都携带所属任务。RUN 只对匹配任务号且未取消的事件给 core_stream_enable；核心 valid/EOL/EOF 均须与此相与。原始流 SOF 不得再直接连核心清帧端。首次 SOF 允许作为元数据，重复 SOF 是输入错误且被屏蔽。

未接受的 B 的全部事件按任务号隔离；rejected_stream 为诊断指示，不使正常 A 失败。上游若不能提供每事件身份，必须先建立整帧丢弃/银行所有权机制，不能假装仅屏蔽 SOF 就完成保护。该实验不暂停摄像头。

## 输出和错误

core_obj_valid/index/label/xmin/xmax/ymin/ymax/center_x/center_y/area 是内部诊断流；只在 RUN 暂存。复用生产 object_frame_store 的 stage/front 表，没有再建一套候选 RAM。几何分类辅助字段 width/height/fill/class 在此层为零，分类仅允许结果资格确认后启动。

任务错误只在下一任务接受时清零，core_error_reason 按位累积。reason bit0=输入重复 SOF；bit1=标签溢出；bit2=run 溢出；bit3=其他核心错误；bit4=对象重复、数量不符、缓存协议或 done 后额外对象；bit5=显式取消。核心全体错误必须由集成方完整编码，不能仅连接标签错误。

core_done 捕获 core_object_count 并进入 FLUSH；延迟一个时钟才向 store 提交，故最后对象与 done 同拍时先进入 stage。FLUSH 使用已锁存错误或当拍新错误，错误优先；数量必须≤4且等于唯一对象接收数，索引必须恰为0～count-1，不能让缺失索引冒充完整表。失败也产生 result_valid，但 result_success=0、reason 非零、count=0，rd_valid=0。成功空帧 result_success=1/count=0，与失败不同。

结果进入 HOLD 后，result_valid、task_id、frame_id、success、cancelled、reason、count 和对象表冻结至 result_valid/result_ready 握手。任务描述和锁存错误寄存器直接复用，不另复制一套结果描述；唯一对象索引 bitmap 也兼做数量完整性判断，不增加重复的对象计数寄存器。rd_index 可变，rd_* 数据按索引读取；同索引数据保持稳定。rd_valid 仅在 HOLD 且 success 时可能为真，其他时刻不能当有效对象。不存在公共逐项投机输出端。

## 取消与复位

cancel_valid 只对 RUN 当前任务有效；core_done 同拍时取消优先。进入 CANCEL_DRAIN 后 abort_request 保持，禁止新输入和新任务，忽略晚到诊断对象。调用者必须停止发新操作、排空已接受活动与行缓存，并在真实排空后给 drain_done；guard 不自动猜测排空时间。此时清核心、发布 cancelled=1/reason bit5/count0 的唯一终态。core_done 已接受后的 FLUSH/HOLD 不再撤销发布资格，不能用取消撤销已发布显示提交。

rst_n 复位使结果失效并开始新的账本边界；不能证明外部 DDR 在途返回已被排空。复位后外部供数必须丢弃旧身份/旧缓存，才能接受新描述。

## 验证门槛

不跨复位时 `accepted = success_taken + failure_taken + cancelled_taken + pending`，pending包括运行、排空和等待结果接收，完全排空后为0。每次接受只许一个终态；等待/拒绝的任务不计接受。覆盖 last-object/done/error 同拍、脉冲错误保持、空成功、数量错、结果背压、B 等待且整段隔离、取消等待真实排空、溢出→空→正常、原/优化 CCL 合法结果一致。

下面为未渲染的相对时序声明，不作为仿真证据：

```json
{"signal":[{"name":"clk","wave":"p...."},{"name":"core_obj_valid","wave":"010.."},{"name":"core_done","wave":"010.."},{"name":"state","wave":"==.=.","data":["RUN","FLUSH","HOLD"]},{"name":"result_valid","wave":"0..1."}],"head":{"text":"最后对象同拍DONE，下一提交拍后公开结果"}}
```

本地功能仿真与严格风格/AST、器件综合、布局布线、DDR/CDC/显示验证分别报告，不因某一项通过概括全部通过。
