# tb_road_postprocess_joint 测试台规格

本模块没有外部端口且不可综合。`tb_spec.json` 保存完整意图合同。受管 `write-spec` 对真实的空端口列表返回 `modules[0].interfaces.ports must be non-empty`，因此本伴随文档为人工补充，不能标记为受管规格门通过；不为迁就文档工具新增虚假端口。

测试台在 100 MHz 时钟上把 12096 个冻结的 112 位 head 字完整送入 C2 `road_head_decode_topk`。C2 的内部 `road_candidate_ram_Inst_store` 是唯一功能候选表；C2 的 sealed/read/response/finish 握手直接连接 C9 `road_nms_serial`。测试台只保存期望 FINAL97 表用于核对，不实现第二份候选 RAM 或后处理算法。

LUT 端点一次只允许一个未决请求，回显 kind/address/tag/frame/model，并可注入确定性延迟。成功运行逐项检查所有 FINAL97、frame token、候选计数、done 时 C2 finish-ready、握手停顿期间稳定性，以及 sealed 后 `o_ram_write_words` 不再增长。

22 个计划运行由 `run_joint.ps1` 执行：7 个保存的 12096-head 用例各正常/随机一次；真实图后连续空表；SCAN、SORT、DECODE、NMS 乘法和 held-output 五处复位后完整恢复；至少 128 拍输出反压；已有输出后注入响应错误，禁止 done/完整发布，再共同 cancel 并完整重跑。随机模式覆盖输入、LUT 和输出停顿。实际通过情况以冻结 run 的 `summary.json` 为准。

周期窗口采用单一 posedge 监视器：start 接受至 seal、seal 后第一拍至包含 done 的周期、start 至最后输出/done。NMS 请求、响应、乘法、输出与其他控制类别互斥，其和必须等于 `done_cycle - seal_accept_cycle`；stall 是上述占用的子计数，不能再次相加。decode+TopK+NMS 必须不超过 2,000,000 拍；100,000,000 拍只是整帧 1 FPS 规划额度，不能由本测试宣称整网达标。

此测试不含生产 C8 collector，所以“部分输出后错误”只证明 C9 不产生 done/完整表并可共同取消恢复，不宣称生产 collector 已完成回滚集成。也不运行 CNN、训练、综合、TD、布局布线、位流、板卡或 Flash。

周期示意见 `spec/postprocess_joint/waveforms/tb_road_postprocess_joint_joint_flow.svg`。该图由受管 WaveDrom renderer 独立生成，不代表 portless spec 交叉检查通过。
