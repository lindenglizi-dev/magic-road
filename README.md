# Magic Road：视觉世界模型与硬件加速

目标是先建立可复现的视觉预测任务，再研究小型学习模型及其多步状态预测加速器。当前已有 **P1 软件数据与解析基线**和 **P2 首轮视觉预测模型试训**；P2 图像预测尚未超过简单对照，下一步先改进视觉初始化和数据，尚无硬件实现。

## 运行

在项目根目录执行：

```powershell
python software/tabletop.py --out artifacts/tabletop-baseline
```

需要 Python、NumPy 和 Pillow。缺少库时可自行安装：

```powershell
python -m pip install numpy pillow
```

默认生成训练 24 条、验证 6 条、测试 6 条轨迹，每条最多 48 个动作，图像为 64×64 RGB。可调整种子和步数：

```powershell
python software/tabletop.py --seed 42 --steps 24 --out artifacts/tabletop-seed42
```

输出目录必须不存在或为空；程序拒绝覆盖已有结果。再次运行时请使用新的目录。

## 任务与数据

固定俯视相机观察桌面方块。二维动作的每个分量在 `[-1, 1]` 内，控制加速度；时间步长为 `0.1`，包含摩擦及无弹性的轴分离碰撞。场景中有矩形障碍，按目标中心距离与目标半径判断到达。

首次到达目标时结束，否则达到步数上限后截断。每条轨迹满足 **N 个动作对应 N+1 个状态和图像**。

训练、验证、测试按完整轨迹划分，使用各自的种子与程序素材实例，不将同一轨迹的相邻帧拆到不同集合。程序素材实例的隔离不等于已经验证真实场景泛化。

```text
artifacts/tabletop-baseline/
├── manifest.json
├── episodes/
│   ├── train/{episode_id}.json
│   ├── val/{episode_id}.json
│   └── test/{episode_id}.json
├── frames/{episode_id}/{index:03d}.png
├── baseline_report.json
└── preview.png
```

`manifest.json` 记录数据清单；轨迹文件记录状态与动作；`preview.png` 用于快速检查画面；`baseline_report.json` 保存基线评估结果。

## 怎样理解结果

基线直接读取仿真真值状态，在预测步长 `H=1、4、8` 上比较开环位置误差：

| 名称 | 含义 |
|---|---|
| `state_hold` | 预测位置保持不变 |
| `constant_velocity` | 按当前速度外推 |
| `action_prior_no_collision` | 使用模拟器参数和动作的解析预测，忽略碰撞 |

开环预测期间不使用后续真实状态纠正预测。这些是 **状态级解析基线**，不是从图像学习的世界模型；不能将低误差解读为模型训练成功。

默认种子 `20261021` 的首批数据实际生成 36 条轨迹、975 次状态转移和 1011 张图像。以下为 6 条测试轨迹的预测终点位置 RMSE，单位为像素：

| 基线 | 1 步 | 4 步 | 8 步 |
|---|---:|---:|---:|
| 保持位置 | 1.966 | 6.928 | 11.804 |
| 恒速度 | 1.105 | 5.881 | 13.396 |
| 带动作、忽略碰撞的解析预测 | 0.488 | 3.595 | 8.964 |

对应有效窗口数量分别为 195、177、153；窗口有重叠，不作为独立重复实验。复现环境为 Python 3.13.12、NumPy 2.4.6、Pillow 12.3.0；完整指标与数据哈希由运行命令保存。

候选硬件工作量估算只计算假设网络的 MAC 数、INT8 权重等静态规模，不代表模型已经训练、定点数值已经验证，也不是 FPGA 延迟、功耗或实际时序结果。

**Nano Banana 尚未调用。** 当前图像和素材全部由程序生成。后续如引入 Nano Banana 外观素材，先只替换背景；位置、动作和碰撞真值仍来自仿真。生成图片本身不作为物理真实性依据。

## P2：首轮视觉预测模型

模型使用两帧图像估计 `(x, y, vx, vy)`，再把这个估计和候选动作输入小型残差 MLP，连续预测未来状态。CNN 初始化器有 70,556 个参数；预测网络为 `6 → 64 → 64 → 4`，含 4,868 个参数。它是**受物理状态监督的紧凑预测模型**，尚非自监督 latent JEPA，也没有动作规划模块。

使用项目局部环境，可复用 P1 已安装的 NumPy/Pillow：

```powershell
python -m venv --system-site-packages .venv
python -m pip --python .venv/Scripts/python.exe install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe software/visual_predictor.py --data artifacts/tabletop-baseline --out artifacts/visual-pilot --epochs 80 --seed 20261022
```

若受限运行环境中的 `ensurepip` 失败，可先用 `python -m venv --without-pip --system-site-packages .venv` 创建环境，再执行上面的 `pip --python` 命令。输出目录同样要求新建或为空。

本轮为 CPU、2 线程、固定种子、80 轮试训。按验证集 8 步终点位置误差选择第 21 轮 checkpoint，然后评估 6 条测试轨迹。训练有 609 个窗口，验证 141 个窗口；测试各步长的结果如下，单位均为终点位置 RMSE 像素：

| 初态来源与预测方法 | 1 步 | 4 步 | 8 步 |
|---|---:|---:|---:|
| 两帧 CNN 初态＋学习转移 | 14.249 | 13.739 | 12.537 |
| 同一 CNN 初态＋保持位置 | 13.959 | 12.913 | 11.862 |
| 真值初态＋学习转移（诊断） | 1.883 | 4.972 | 8.058 |
| 真值初态＋已知动作公式、忽略碰撞（诊断） | 0.496 | 3.644 | 9.044 |

所有方法均使用同一批 `t ≥ 1` 窗口，数量依次为 189、171、147，所以不能直接与 P1 的 `t ≥ 0` 总表比较。完整报告还包含图像初态＋恒速度／已知动作公式、真值初态＋保持位置／恒速度，以及逐轨迹和碰撞窗口结果。

**本轮未通过视觉预测的性能关卡。** 图像初始化的位置 RMSE 为 14.469 像素，完整视觉链路没有超过同图像初态的保持位置基线；真实初态下的结果仅用于定位瓶颈。测试集仅 6 条轨迹、单个训练种子，不构成广泛泛化证据。

训练期间允许使用初始与未来真值状态作为监督，并额外从训练真值初态展开预测；正式图像推理只读取 `image[t-1]、image[t]` 与待执行动作，不读取未来图像、真值状态，也不调用物理仿真器代替网络展开。checkpoint 选择只看验证集。

输出位于 `artifacts/visual-pilot/`：

- `checkpoint.pt`：验证集选出的模型权重。
- `history.json`：全部训练损失与验证误差。
- `report.json`：相同窗口的 8 种对照、逐窗口误差、数据与源码哈希、环境及参数规模。

仓库中的 [reports/visual-pilot.json](reports/visual-pilot.json) 保存本轮精简报告；生成数据和权重留在本地，可通过命令重建。本轮实测环境为 PyTorch `2.14.1+cpu`，其余库版本同 P1。报告中的 `training_seconds` 包含训练、验证和最终测试评估，不代表纯训练性能。预测核的乘加计数只是工作量统计，尚未完成量化或 FPGA 性能验证。

## 检查

```powershell
python software/test_tabletop.py
.\.venv\Scripts\python.exe software/test_visual_predictor.py
node test-world-model.cjs
```

第二条命令检查图像与监督对齐、梯度、checkpoint、相同对照窗口、无未来真值回灌、连续递推与数据完整性。第三条命令对应历史迷宫教学示例。`world-model.html` 展示表格转移学习和规划，与当前视觉世界模型及硬件加速主线分开。

## 后续关卡

1. 先改进图像初始化和数据覆盖，在独立轨迹上验证预测优势；当前只有预测评估，动作选择和任务成功率仍待实现。
2. 根据实际算子、耗时和访存分析选择硬件范围，再建立定点参考并检查误差累积。
3. 实现 RTL，验证数值、握手、资源与实际时序；有设备后再报告实测性能和能耗。

当前先完成软件验证，不要求 FPGA，也不声称已经获得芯片加速收益。
