# FPGA 道路视觉项目多智能体工作流

## 1. 配置状态

本文件把外部多智能体方案中可用的分工落到当前工程目录。外部方案中的总体算法只是参考，不是本工程规格；当前规格以 `CURRENT_ARCHITECTURE.md`、`REAL_DATA_WORKFLOW.md` 和 `evaluation/status.json` 为准。

Codex 的仓库级持久指令由根目录 `AGENTS.md` 提供。角色模型不是仓库内静态配置项，协调代理在每次创建子代理时必须显式传入下表中的 model 和 reasoning effort。这样可避免配置文件看似存在、运行时却没有生效。

当前环境包括协调代理在内最多四个并发代理，因此最多同时启动三个子代理。下面的六项是角色池，不表示六个代理必须同时运行。

## 2. 角色与模型

| 角色 | 模型 | 推理强度 | 主要职责 | 默认写入范围 |
|---|---|---:|---|---|
| `arch_lead` | `gpt-6-astra` | `medium` | 跨模块架构、接口契约、CDC、帧号、bank 所有权、吞吐和资源取舍 | 架构与接口文档；默认不写实现 |
| `py_reference` | `gpt-6.1-sol` | `high` | 数据导入、Python golden model、特征/定点/SVM、训练评估、可复现向量 | `tools/*.py`、Python 测试、数据与评估产物 |
| `rtl_frontend` | `gpt-6.1-sol` | `high` | 灰度分析流、背景差分、去噪、RLE-CCL、候选和跟踪前端 | 分配到的前端 RTL 与专属 testbench |
| `rtl_classifier` | `gpt-6.1-sol` | `high` | ROI 读取、HOG、定点 SVM、分类任务控制及经批准的接入逻辑 | 分配到的分类 RTL 与专属 testbench |
| `verify` | `gpt-6.1-sol` | `high` | Python/RTL 对拍、仿真、周期与边界测量、失败复现、回归检查 | `tests/`、测量脚本与验证报告；默认不改功能 RTL |
| `review` | `gpt-6.1-sol` | `high` | 独立审查接口、位宽、符号、越界、CDC、帧身份、证据边界 | 默认只读；输出问题清单和定位 |

模型名必须保持完整拼写。2026-10-15 用户明确要求：除当前总协调外，普通执行、参考、验证和审阅默认使用 `gpt-6.1-sol`/`high`，覆盖先前五个角色的 `gpt-5.6-sol` 选择。当前总协调配置不因该要求改变；另行委托的普通架构子任务也默认 `gpt-6.1-sol`/`high`。工具调用须显式指定 model/thinking 或 model/reasoning_effort，不能仅在提示词宣称已切换。正在进行的外部仿真不因切换模型重复启动。如果指定模型在某次运行中不可用，协调代理应报告实际限制，不静默换成别的模型。

## 3. 当前阶段的启用规则

当前阶段以真实数据闭环为先：

1. `py_reference` 负责公开数据转换、ROI 核查、训练、浮点/定点基线和失败样本。
2. `verify` 独立检查数据泄漏、输入映射、指标口径、真实向量对拍和现有仿真测量。
3. `review` 在一个交付批次完成后做只读审查，重点检查结论是否超出证据。
4. 只有出现跨模块接口选择时才启动 `arch_lead`。
5. `rtl_frontend` 和 `rtl_classifier` 保持待命；实际候选分类有收益且定点一致性通过后，才安排正式接入工作。

不要为了“让所有角色都有事做”而启动代理。短小、强依赖、会同时修改同一文件的步骤由协调代理串行完成。

## 4. 当前工程的职责边界

### 4.1 Python 与数据

`py_reference` 的主要范围：

- `tools/hog_reference.py`
- `tools/train_hog_svm.py`
- `tools/road_evaluation.py`
- `tools/prepare_public_video.py`
- `tools/import_public_rois.py`
- `tools/convert_*.py`
- `tools/roi_dataset_tool.py`
- `tools/ccl_roi_candidates.py`
- `tools/audit_roi_dataset.py`
- 对应的 Python 测试及 `evaluation/` 下可再生报告

它不得自行改变 RTL 接口。若 Python 结果要求改变 ROI 尺寸、特征维度、定点格式或拒识协议，应提交给 `arch_lead` 决策。

### 4.2 RTL 前端

`rtl_frontend` 的主要模块族：

- `awb96_analysis_adapter.v`
- `background_model.v`
- `binary_cleanup_3x3.v`
- `run_detector.v`、`row_matcher.v`、`label_manager.v`
- `raw_run_table.v`、`labeled_run_table.v`、`rle_ccl_top.v`、`foreground_ccl_top.v`
- `top4_selector.v`、`object_frame_store.v`、`object_tracker.v`、`track_event_detector.v`

涉及候选框快照、帧号或算法域任务入口时，它必须与 `arch_lead` 和 `rtl_classifier` 对齐接口后再写代码。

### 4.3 ROI 与分类链

`rtl_classifier` 的主要模块族：

- `gray_frame_bank_ram.v`、`gray_frame_pingpong.v`
- `roi_object_snapshot_cdc.v`、`roi_frame_reader.v`
- `hog_sobel_gradient.v`、`hog_cell_histogram.v`
- `feature_table.v`、`hog_linear_svm.v`

分类任务的完成、RAM 最后一次读取和 bank 释放必须分别定义。`ack` 的具体时机要由接口契约说明，不得用“流水已经进入”这类无法观察的推断代替硬件事件。

### 4.4 显示与快照边界

`track_snapshot_cdc.v`、`road_box_overlay.v`、`road_status_overlay.v` 牵涉分析帧与 HDMI 帧的关系，归为架构边界文件。修改前由 `arch_lead` 明确：

- 发布的源帧号；
- HDMI 端采用该表的生效帧；
- 一帧显示期间是否冻结；
- 视频主链总延迟的测量方法；
- 复位和丢更新时的行为。

## 5. Python 到 RTL 的实现顺序

对新的算法或难以直接证明的 RTL 行为采用以下顺序：

1. 写最小 Python 参考，定义输入、输出、边界条件和异常输入。
2. 固定整数位宽、符号、舍入、截断、饱和或回绕规则。
3. 生成小型确定性向量，覆盖零值、极值、边界框、负数乘加和溢出附近。
4. 再写 RTL，并在模块边界导出中间值。
5. 先逐级对拍，再比较最终分类；最终分类相同不能掩盖中间数值不一致。
6. `verify` 独立复跑命令并记录输入哈希、源码哈希、周期和失败样本。

对于现有 RTL 的纯接线、命名、文档或明确的机械修复，可直接修改并运行针对性验证，无需人为增加 Python 模型。

## 6. 协作波次

### 真实数据阶段

- 波次 A：`py_reference` 处理数据与模型；`verify` 检查数据和测量入口。二者文件必须拆开。
- 波次 B：`review` 审查 A 的交付；若发现跨模块决策，再由 `arch_lead` 给出最小决策。

### 硬件接入阶段

- 波次 A：`arch_lead` 冻结任务、帧号、CDC、bank 释放和 HDMI 生效接口。
- 波次 B：`rtl_frontend` 与 `rtl_classifier` 在不重叠的模块上实现；`verify` 同时准备基于冻结接口的 testbench。
- 波次 C：`review` 只读审查，协调代理集成和修复。

由于共享同一文件系统，任何两个并行代理都不得编辑同一文件。2026-10-11 已按用户要求初始化 Git；分支与文件纳管范围见 `GIT_WORKFLOW.md`。同一目录中的分支切换会影响所有代理，实际需要隔离时再从同一基线提交创建 worktree。

## 7. 交接格式

每个子代理结束时至少报告：

```text
角色：
任务边界：
修改文件：
关键结论或接口：
执行的验证命令与结果：
没有覆盖的风险/测量边界：
需要下一角色读取的文件：
```

接口提案还要逐项写清：时钟域、有效条件、payload 稳定窗口、源端保持条件、目标端采样条件、ack 时机、复位状态、同拍冲突优先级、帧号含义和 bank 释放事件。

## 8. 完成门槛

- Python/数据任务：来源、许可链接、哈希、场景分组、帧号和框可追溯；相邻帧不跨集合；人工框与 CCL 框分开报告。
- 分类任务：浮点与定点差异、溢出、每类 precision/recall、invalid 误接受和失败清单齐全；分数不解释为概率。
- RTL 任务：接口与参考模型一致，关键中间值可对拍，仿真覆盖复位、背压、边界和连续任务。
- CDC/缓存任务：发布、复制、ack、最后读、释放和复位均有可观察事件与断言，不采用未经测量的 N+2 超时。
- 评审任务：按严重级别给出文件与行号，区分已证明缺陷、证据不足和改进建议。

协调代理汇总时必须说明测量边界。四对象 4176 周期/41.76 us 目前只是计算夹具结果，不包含真实采集、完整 CDC 和连续帧 bank 占用，不能据此宣布双 bank 吞吐已经满足。
