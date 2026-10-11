# ccl_pipeline_trial_top 统一出口接线参考

范围为单时钟、单源任务、可综合二值像素行缓存、候选保护层、原/优化CCL与同步候选读取适配。非生产接入；无摄像头、DDR/CDC、ROI像素读取、分类器、跟踪或HDMI实现。对应整数参考tools/ddr_pipeline_reference.py；银行的周期参考由ddr_line_bank_reference.py维护。所有参数/端口以同名源码为准，默认129×8、X8/Y4、ID32、L128/LABEL8、MAX_RUN64、面积16bit、min-run/area1。要求WIDTH可由X_WIDTH表达，HEIGHT可由Y_WIDTH表达，L+1可由LABEL_WIDTH及内部扩展计数表示。

## 阶段与字段

task_valid/task_ready接受task_id、task_frame_id并锁定至最终终态ACK。下一拍才供数；in_valid/in_ready接受像素，事件身份在行银行填充首像素确定，并随读请求/返回保持，禁止用当前任务号给旧返回重新贴标签。in_y行内不变、in_last恰在WIDTH-1；in_frame_last恰为HEIGHT-1行末。

candidate_valid/success仅表示候选处理完整，不代表已分类。表只含检测域闭区间框、标签与面积；同步response_*仍是候选字段，没有合法类别字段。宽高由该检测域框xmax-xmin+1、ymax-ymin+1推导。映射720p/半开裁剪由未来ROI适配负责，不能将两个域尺寸混用。未分类不是class=0；本接口完全不提供class_valid或class数据。

processed_valid/ready是外部ROI/分类消费者的完整处理报告，须带匹配task/frame身份、完成数量、接受数量及硬件/数据错误。完成数量须等于全部候选数量，接受数量≤完成数量；全部正常拒识仍可处理成功。processed_error指处理过程失败，不指模型预测错误。当前顶层只校验合同，不自行验证真实ROI返回和分类结果，因此正式消费者必须兑现此前提。

final_valid/success表示完整处理结果具备发布资格，保持至终态握手。成功只接受display_commit_ack（图像及结果实际切换的外部ACK）；失败只接受failure_ack，不产生显示切换。测试台模拟ACK，不是HDMI实现。algorithm_release只释放算法占用；RGB帧释放仍须帧管理器确认显示持有和最后DDR读取结束，不能由此单信号决定。

## 候选读取与释放

候选表在candidate_valid/success时即可读取，不能等待candidate_release才开始读。read_valid/read_ready按index0～count-1顺序接受，最多1个未完成请求；请求后1拍捕获store组合表，response_valid保持至response_ready。返回含原task/frame身份、index、label、检测域框及面积。请求、等待返回、返回背压期间不允许表释放。

candidate_release的语义是所有所需表数据已实际接收；最后返回ACK后read_count等于候选数且无pending/held响应才允许交接。提前release通过candidate_release_blocked显式拒绝，不覆盖数据。零候选及失败候选无需读取。局部guard空闲后完整顶层仍处PROCESS/FINAL，禁止新源任务；不添加队列或复制第二候选表。

## 行交接与取消

先等待显式row_input_ready，再通过真实像素握手送完整行；最后像素返回被接受后发送EOL，等待row_input_commit再进入下一行，非逐行等待row_done。完成行计数确认最后一行已处理才发送EOF一次；无固定EOL flush等待，无功能RTL层级访问。

RUN中cancel、银行/输入协议错误或core_error优先停止新输入和行事件。取消银行处理自身同步pending返回并丢弃held输出，empty只在该模块所有缓存/返回失效后成立。本轮无外部DDR请求，故此empty仅证明本地输入路径。随后RESET_CORE对核心和银行执行受控复位；RECOVER检查banks_empty、core_idle且core_error=0，再产生guard drain_done。该路径不等正常ccl_done，可恢复半行协议错误。协议错误采用带错误原因的内部取消，终态不是正常空成功。

复位划分账本区间；异步硬件复位不证明未来DDR请求已排空。既已到候选/处理/最终阶段的取消不撤销发布或已接受的表读取；本实验取消仅对RUN有效。错身份输入不ready且rejected_input=1，上游必须保持payload，不得把旧A改号为B。

## 验证

原/优化CCL分别运行确定性17×4矩形/条纹gold。交叉场景：双银行占用取消、最后RAM返回与取消同拍、候选消费者延迟/最后返回背压/提前ACK、新任务禁止提前启动、半行故障受控复位、A残余身份隔离、完整处理失败、全部拒识正常成功与恢复。已有exact32/33等模块测试保留，非本组合首次覆盖。

```json
{"signal":[{"name":"clk","wave":"p......."},{"name":"read_valid","wave":"010....."},{"name":"response_valid","wave":"0..1110."},{"name":"response_ready","wave":"0....10."},{"name":"candidate_release","wave":"0.1...10"},{"name":"candidate_release_blocked","wave":"0.1....."}]}
```

相对WaveJSON未渲染；实际编译、执行、源文件哈希和参数记录见运行收据。Verilog-2001编译不等于器件RAM推断/综合、严格风格门禁、板上时序或识别正确率。
