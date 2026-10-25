# WIF1物理工作仓交接（本代理停止写入）

日期：2026-10-16。工程分支：work/roadyolo。范围仅新工作仓RTL、同名合同/规范/周期图、Python参考与本报告。未运行ModelSim/TD，未修改旧源、冻结核或WIF1。

## 交付与当前证据

- `rtl/road_feature_workstore.v`：唯一模块，四个显式PH1P_LOGIC_ERAM实例，没有寄存器存储array。两块2048×8字节bank逻辑开放3072B；两块512×40并行组成80bit权重word，24group×3word。
- `reference/workstore_reference.py`：先于RTL实现并运行。12,648项PASS，见`workstore_reference_report.json`。覆盖全部3072字节两轮写读、全部24组两轮写读、192位行走、末word高48位零、非法地址不改内容、reset保留内容但清任务覆盖资格。该参考不模拟native延迟，覆盖资格不是额外RTL硬件。
- `spec/road_feature_workstore_contract.json`及registered write-spec输出`spec/workstore/road_feature_workstore_spec.md`、两张WaveDrom SVG/JSON5：21端口交叉核验成功。含byte独立反压/退休图与weight三word图。
- 严格门禁两次均保留，第一次453错误，最终448错误；未新增例外、假驱动或降级。最终八门：compile passed；ast/readability/comment/naming failed；profile passed；testbench/toolchain not_requested。源仍是待真实模型验证与诊断集成候选，不是严格交付通过。

## native选择与接口周期

所有实例MODE=SP、REGMODE_A/B=NOREG、WRITEMODE_A/B=NORMAL、IMPLEMENT=20K、CLKMODE=ASYNC、BYTE_ENABLE=0、FORCE_KEEP=ON。B口CE/WE固定0；rsta/rstb固定0；INIT_FILE/FILL_ALL=NONE。FORCE_KEEP及源码四实例不证明TD映射的实际类型/数量。

配置参考：`user_source/hdl_source/road_vision/gray_frame_bank_ram.v`提供2048×8原语实例；`production/rom_two_client_20261015/rtl/road_yolo_numeric_rom_group.v`提供已实跑SP/NOREG 512×40模式。官方行为模型为`E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_eram.v`，行为受保护，公共参数可核验。选择SP避免40位DP模式可能拆块。本代理没有执行行为模型，不能宣称native延迟已实测。

沿定义：K0为WIF1请求握手沿；K1等为后续上升沿，响应valid指沿后稳定值，最早在下一沿消费。

| 通道 | native访问 | 捕获/完成 | rsp_valid | ready持续1时最早下一接受 |
|---|---|---|---|---|
| byte | K1一次 | K2取得读数据或确认写/错误 | K2后 | K3沿与旧响应退休同拍 |
| weight | K1/K2/K3三个word | K2/K3/K4取得前三沿数据；K4确认整组写/错误 | K4后 | K5沿与旧响应退休同拍 |

两通道独立。各最多一个未退休；valid反压时载荷/error保持。非法byte>=3072、weight>=24与合法请求同延迟，但CE/WE始终零，返回error/data0，fault在非法K0接受后置1并粘滞。

权重：word0=data[79:0]，word1=data[159:80]，word2={48'd0,data[191:160]}；地址3group/3group+1/3group+2；每word lower实例存[39:0]，upper实例存[79:40]。末word只回读lower[31:0]，不使用未有效位。

共同reset异步清控制与响应，不复位RAM内容；释放后首个上升沿置flag_running，随后允许握手。中途权重写可能部分提交；client必须重新覆盖整组及本任务所有所用范围，不承诺回滚、外部DDR排空或初值有效。

## 静态风险逐项解释

最终门禁原件`reference/workstore_gate_attempt2.json/.md`保留，不改写为通过。

- VG097四实例参数/端口解析不确定，继发VG153四读结果无可确认驱动、VG132八个clka/clkb被视为非时钟。实际源码四个doa分别独占驱动dec_byte_lower_data/upper_data及dec_weight_lower_data/upper_data；每块clka/clkb只接i_clk，B口始终关闭。纯接口文件只用于静态门，不用于仿真/综合。这些原语边界必须由真实厂商模型编译/运行和TD进一步确认，未豁免门禁。
- VG122计数加法潜在进位：phase仅0→1→2→3→4→0，加1只在1..3；9bit native地址从3group开始，合法最大69，只在phase1/2各加1，最大71。非法组号最大起点93、最大95但CE/WE关闭。可达值均不溢出。
- VG125是显式3bit/9bit常量大于最小表示位数；这些常量按目标寄存器位宽声明，不改变数值。VG138主要为风格要求的`reg = 0`及复位0/1无尺寸字面量，当前失败保留。
- VG155仍报告两响应valid过程；实际清valid条件显式为`byte_rsp_valid_o && i_byte_rsp_ready`及weight对应条件，生成新valid优先于消费，且新请求只可能在已完成且旧响应可消费时握手。由独立TB测长反压与同拍退休接受；不以人工解释替代门禁。
- VG145/146/147组合来源/操作预算失败，包括ready与合法访问的控制解码和原语解析不确定；没有通过切断来源或额外流水绕过。其实际延迟/资源/路径仍需诊断综合，100MHz时序未测。
- 其余ast、注释布局、相似注释、header模板及region失败均原样保留。未扩展到整库格式改写。

真实碰撞风险：SP A口一次只读或写，B口从不访问，通道内请求完全序列化；字节bank与weight物理实例不同。写时doa不参与读结果；同地址读必须在前一写响应退休后接纳，预期无同沿碰撞。reset沿恰逢native写是否已提交不作回滚保证，client覆盖前提消除对旧内容的依赖。

## 独立TB监视信号

byte：flag_byte_pending、flag_byte_capture、flag_byte_native_enable、flag_byte_native_write、flag_byte_lower_enable/upper_enable、reg_byte_addr[11:0]、reg_byte_data[7:0]。
weight：cnt_weight_phase[2:0]、flag_weight_native_enable、flag_weight_native_write、reg_weight_native_addr[8:0]、reg_weight_native_data[79:0]（组合选择，phase3高48位必须零）。
实例：PH1P_LOGIC_ERAM_Inst_byte_lower/byte_upper/weight_lower/weight_upper。

## 已执行命令与边界

1. `python -B -X utf8 production/workstore_feature_20261016/reference/workstore_reference.py --report production/workstore_feature_20261016/reference/workstore_reference_report.json`（cwd=cnn/hw_validation）：PASS。
2. skill dependency check：required_ok=true、WaveDrom3.6.1存在；recommended context-engineering缺失，不安装。
3. registered `scripts.python.workflow.cli main(['write-spec',...,'--no-state'])`：项目目录作为workspace，源交叉核验与两图生成成功。普通隔离执行Windows严格Path.resolve报WinError5；同一已授权路径的提升执行成功，没有修改技能或扩大输出范围。
4. `python -m scripts.python.validation.generated_deliverable_gate <RTL> --external-interface-source <interfaces/ph1p_eram_interface_complete.v> --json <attemptN.json> --markdown <attemptN.md>`：两次exit1，原始八门失败保留。
5. 未运行外部仿真、TD、package整套回归、训练、push、布局布线或板卡动作。下一步由总协调运行独立真实模型TB，符合功能及语义风险条件后才安排诊断综合。

## SHA256（交接时）

- RTL：0d9f78544ce6e726a8ff042d7be0f5a2aee7d717bfbde0495a98a78dea25eb1c
- Python参考：5665a577064637de42ad19a1d413d70363aff9f9be779b90e8a473271de93c38
- 合同：86628c020db6f81ada488b56b34d5ac0354383a394ae1ecc1384fc1cd0f834c3
- 生成spec：3a3063bc8f883d55c824e6a463c35e6c224dee355b84512f42cb4d382e20527b
- 真实厂商模型：70d89b70bdd51812ad86b91e88526b4604ebb117516efda5af976fcddb2e69af

本代理交接后停止所有写入；总协调可将以上RTL/ref作为独立storage冻结闭包。Python与静态证据不证明全网吞吐、精度、真实4ERAM映射或板测。
