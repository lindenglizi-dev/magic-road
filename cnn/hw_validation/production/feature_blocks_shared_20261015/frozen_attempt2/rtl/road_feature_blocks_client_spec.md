# road_feature_blocks_client specification

## Scope and interface

100MHz同域固定图客户，机械复用封存CSP2和CSP3/CSP4客户。一个FSM、一个3072B
byte工作缓存和一个24×192bit权重bank；外接唯一旧算术owner，没有私有MAC/SiLU/完整ROM。
首批只支持i_block_id=2/3/4；没有SPPF/PAN或任意形状/图描述符。
原核端口、II、signed33/RNE、SiLU和残差sat8不变。

完整端口定义在同目录road_feature_blocks_client.v。新增i_block_id/o_block_id、
i_parameter_response_block_id/i_barrier_block_id均4bit。parameter_channel7bit、
parameter_group5bit、layer/window各3bit。逻辑读地址32bit，16B对齐，128bit返回，单在途。

唯一start事件为i_start && o_start_ready，仅IDLE且表已加载、无fault时接受。
接受后锁存block_id；busy期间live ID/start扰动忽略，o_block_id保持到下一次接受start或复位。
参数请求身份和屏障身份以o_block_id为准。各valid等待ready期间payload保持。
参数响应实际消费时核对block/layer/channel/group/window、error和同输出组量化字段一致性。
屏障消费时核对block/layer。core写回必须合法tag0/1/2、匹配完整地址、未重复lane，
且与外部writer同拍握手退休。最后实际写退休后才推进任务。

## Reset and faults

i_rstn低有效异步断言；上级共同同步释放，服务共同取消旧响应，算术owner重装SiLU。
复位清控制/身份/行valid，不清大数组。每tile/输出组先覆盖所有随后使用的项。
非法ID接受后直接busy/fault占有，无读/参数/核/写/屏障活动。
错误身份、读地址/错误、非法core输出、cancel/core_fault均粘滞fault到共同复位。
独立热复位和晚返回取消未证明，不假定已经排空。

## Fixed stages and shapes

| block | H×W | half/full | stages | source | output |
|---|---|---|---|---|---|
| 2 | 72×128 | 12/24 | DW0 PW1 DW2 PW3 out4 | 035b4000 | 03656000 |
| 3 | 36×64 | 24/48 | DW0 PW1 DW2 PW3 DW4 PW5 out6 | 0369a000 | 03709000 |
| 4 | 18×32 | 48/96 | DW0 PW1 DW2 PW3 DW4 PW5 out6 | 0372c000 | 0376b000 |

地址均hex。遵循冻结graph tile4x4_hwc、真实通道不补8。三个固定ID case内
prefetch/任务地址/cache索引的除数和通道stride均常量化。
CSP2 final4先排除DW，half12 PW第1组读4byte、mask0f；
CSP4最后tile y16只有y16/17有效，禁止y18/19写。DW图外halo补0，物理尾行补0。
各中间地址、旁路生命周期见design_contract.txt。

## Cycle behavior

IDLE接受合法start后TILE_SETUP一拍初始化。PREFETCH每命中/补零拍写1byte，
miss转READ/READ_WAIT等匹配16B行响应；完整tile覆盖后才装参数。
PARAMETER/PARAMETER_WAIT逐槽握手，DW4槽两窗口；PW为ceil(Cin/8)槽。
TASK_SETUP一拍冻结元数据并清拼装寄存器。CACHE_ACTIVATION逐byte读，
残差首组再用CACHE_BYPASS三拍。SEND保持至core_ready，非末组返回拼装，
末组到WRITE_WAIT等待所有合法lane实际写接受。
最后写后RETIRE一拍读取注册凭据，再ADVANCE一拍推进空间/通道/tile。
完整层末才BARRIER等待可见性；中间层回TILE_SETUP。
最终匹配屏障后FINISH一拍done=1/busy=1/start_ready=0，下一拍IDLE才接新任务。
FAULT占有至共同reset。没有新流水级，保留旧任务节拍；状态互斥。
外部等待/反压不限，不以固定timeout推断DDR可见性；实际分层/状态/全幅周期待root测量。

## Storage

唯一byte数组3072B、权重576B、量化31B、读行16B，共3695B数据，
不含控制/tag/地址/activation/bypass。PREFETCH写、CACHE_ACTIVATION读、
CACHE_BYPASS读互斥，每拍至多一个byte访问。
start和层转换清行valid，每tile先覆盖全部使用byte，每输出组先覆盖全部使用weight槽。
3072B/24槽只是已批准PAN最大容量预留，未实现PAN功能。
4ERAM原始10240B是目标；数组物理映射、端口时序及资源/时序均UNKNOWN/UNPROVEN。

## Required verification and evidence

同实例无复位2→3→4，每块全部输出和acc/pre/SiLU/post/sum/地址一致；
busy扰动ID/start、随机背压、共同复位重装表重复；非法ID、错参数block、
错屏障block、真实acc检查器负例；CSP2 mask0f、C4尾行、访问互斥、
请求计数和阶段/状态周期。ModelSim/TD由root统一执行，本角色未运行。
CSP3/CSP4源由CPU跨未实现down3/down4生成，同实例顺序不是连续CNN依赖链。
初次严格静态结果保留在static_gate.json/md；最终结果在static_gate_final.json/md。
CPU selector PASS仅控制参考，不是RTL/DDR/物理PASS。

## Timing diagram

下图表示最终屏障采样后的状态，可见FINISH仍busy一拍，随后才ready；非测量波形。

```json
{
 "signal": [
  {"name":"i_clk","wave":"p....."},
  {"name":"o_barrier_valid","wave":"10...."},
  {"name":"i_barrier_ready","wave":"10...."},
  {"name":"o_block_id","wave":"=.....","data":["latched"]},
  {"name":"o_done","wave":"010..."},
  {"name":"o_busy","wave":"1.0..."},
  {"name":"o_start_ready","wave":"0.1..."},
  {"name":"i_start","wave":"01.0.."},
  {"name":"state","wave":"===...","data":["BARRIER","FINISH","IDLE"]}
 ]
}
```
