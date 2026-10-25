# 摄像头2 FPS采集组件 ModelSim 验证报告

## 结论

冻结 `road_area_resize` 哈希 `4a0a23239d9870dfbfebee45c61bff8e08d519f8bd2b0848385ea1bde7e3a5c0`、`road_capture_slots` 哈希 `746065b5c61393ceda8dc24b782f2d9984cbcb736a4d91ba05c3178569bb2cca` 下，五个 scaler case 与四个 slot case 全部得到正式 PASS 收据。结论是 **PASS_COMPONENT_FUNCTIONAL_CONTROLLED_EVENTS_PHYSICAL_NOT_RUN**。

## Scaler 完整帧

| Case | 结果 | TB总周期 | 像素/beat/bytes | 首输出 | 末输出 | frame error |
|---|---|---:|---|---:|---:|---:|
| numbered bars | PASS | 576,004 | 147,456 / 147,456 / 442,368 | 1,606 | 575,717 | 0 |
| random seed20261015 | PASS | 576,004 | 147,456 / 147,456 / 442,368 | 1,606 | 575,717 | 0 |
| all255 | PASS | 576,004 | 147,456 / 147,456 / 442,368 | 1,606 | 575,717 | 0 |
| fault/reset then all255 recovery | PASS | 576,573 | 147,456 / 147,456 / 442,368 | 1,606 | 575,717 | 3 expected |
| no-line-gap overload | PASS | 381 | 0 / 0 / 0 | — | — | 1 expected |

首/末输出以最后一次完整帧首个输入 valid 为相对第0拍。CPU串行调度参考为1,600/575,711，实际RTL与两个厂商ERAM流水固定多6拍。每行输入连续320拍、空闲480拍，行周期800；首到末输入 valid 的索引范围为0..575,519。末输出在最后输入后198拍出现。当前 RTL 选择串行输出，所有完整帧均为 mask01；接口允许但本实现未使用 mask11。

三张完整帧均对147,456个像素逐项核对，不是抽样。编号帧覆盖AWB96高lane优先、RGB低byte顺序、四边及行边界；随机帧覆盖一般数值；全255覆盖二维和最大6375以及最终255。SOF/EOL/EOF位置和总输出442,368 bytes同时核对。

128×67-bit变长record CPU队列证明：普通320+480与最短320+192的最大record数均为120，深度128保留8条余量，最大待处理像素192；无行间空闲在证明cycle342首次溢出。RTL过载 case 在TB相对口径343拍明确 `frame_error`，未输出像素或EOF；一拍差异来自参考cycle0与TB首valid后计数方式。

## Slot 控制

| Case | 结果 | TB周期 | 核心覆盖 |
|---|---|---:|---|
| lifecycle | PASS | 19 | 双槽、442,368-byte结束、visible发布、claim、末读释放、同拍结束+visible。 |
| protection | PASS | 29 | 无FREE跳帧、CAPTURING/READING保护、重入SOF、同拍SOF中断capture并释放另一reading槽。 |
| protocol | PASS | 25 | 早/旧/重复visible、非法claim、错身份/重复release不污染状态。 |
| malformed/reset | PASS | 25 | 短帧、溢出、显式错误隔离，无FREE跳过，复位无残留。 |

槽 READY 只由完整442,368-byte捕获后身份匹配的受控 `write_visible` 驱动；capture end/EOF 本身不会 READY。READING 只由身份匹配的受控 `last_read_consumed` 释放，非CNN done。这里两个事件均为TB外部合同，不是实际PAXI可见性或退休证据。

首轮 protection/protocol/malformed 三目录保留失败：TB在posedge NBA更新前统计registered pulse，导致计数落后一拍；状态掩码并未失败。夹具只改为negedge采样后重跑通过，并再次重跑全部slot正式case，使九份正式收据绑定完全相同的最终源码闭包。

## 工具与RAM证据

九例均使用 ModelSim SE-64 2020.4，编译为0 error/0 warning。scaler实际编译和运行安路 `PH1P_PHY_GSR`、`PH1P_LOGIC_ERAM` 厂商模型，RTL包含两个 `PH1P_LOGIC_ERAM` 实例；仿真优化阶段每实例产生两条固定 `INIT_FILE` 越界 warning，共4条。slot不触发ERAM优化warning。没有使用纯行为假RAM代替。

最终仅TB八门报告：`compile=passed`、`ast=passed`、`readability=passed`、`comment=failed(160)`、`naming=passed`、`profile=passed`、`testbench=not_requested`、`toolchain=not_requested`。160项是参数、信号、实例、always、task/port未逐项添加规定邻接注释；如实保留，未为门禁刷绿而改动已验证夹具。实际ModelSim证据由各case收据单列，不被静态门的`not_requested`代替。

## 边界

本报告不证明真实摄像头、真实PAXI写可见/读退休、DDR时序、CDC、500ms帧触发、持续实板2 FPS、综合资源、TD时序、位流、Flash或训练。物理实现未运行。
