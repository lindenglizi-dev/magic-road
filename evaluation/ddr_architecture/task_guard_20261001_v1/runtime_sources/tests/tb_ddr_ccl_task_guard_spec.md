# `tb_ddr_ccl_task_guard` 验证合同

## 范围

本测试台仅验证单时钟、单在途任务的 `ccl_task_guard` 隔离合同。它使用 mock core 主动构造同拍、背压、非法流和取消边界；DDR、CDC、显示、综合、布局布线及识别准确率不在本测试范围内。

## 时钟与复位

- `clk`：100 MHz，周期 10 ns。
- `rst_n`：异步低有效。复位划分任务守恒统计区间；不声明复位前的外部 DDR 返回已排空。

## 可观察要求

1. 只有 `task_valid && task_ready` 接受任务；忙时保持 `task_valid` 是正常背压。
2. 已接受任务的流事件必须携带相同 `stream_task_id`；其他任务整段被拒绝且不能改变当前任务。
3. 任务内错误保持到终态；`core_done` 同拍错误优先于成功。
4. 最后对象与 `core_done` 同拍时，成功结果包含该对象。
5. 失败结果的 `result_object_count=0` 且 `rd_valid=0`；成功空结果同样 count=0，但 `result_success=1`。
6. `result_valid && !result_ready` 时身份、状态、计数和对象表保持稳定。
7. 取消进入排空态，只有 `drain_done` 后才清核心并发布明确取消终态。
8. 每个未跨复位的已接受任务恰好发生一次 `result_valid && result_ready`。

## 重点向量

- 单拍错误后延迟结束。
- 最后对象、结束和错误同拍。
- 最后对象与结束同拍的正常提交。
- 对象计数不符、重复 index、同一任务重复 SOF。
- A 执行时未接受 B 的完整流隔离。
- 成功空结果、取消等待排空、结果背压稳定和复位边界。

## 时序图

```json
{signal: [
  {name: 'clk', wave: 'p........'},
  {name: 'task_valid', wave: '010......'},
  {name: 'task_ready', wave: '10.......'},
  {name: 'core_frame_clear', wave: '010......'},
  {name: 'core_obj_valid', wave: '....10...'},
  {name: 'core_done', wave: '....10...'},
  {name: 'state', wave: '=.=.=....', data: ['IDLE', 'RUN', 'FLUSH/HOLD']},
  {name: 'result_valid', wave: '......1.0'},
  {name: 'result_ready', wave: '.......10'}
]}
```

最后对象与 `core_done` 同拍后先进入 `FLUSH`；对象表提交完成后才进入 `HOLD`。结果在下游握手前保持不变。
