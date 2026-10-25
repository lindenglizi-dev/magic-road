# road_feature_blocks_client specification

## Scope and preserved interface

当前候选从../../frozen_attempt2/rtl/road_feature_blocks_client.v机械复制扩展。
同名模块每个编译闭包只纳入本候选一份，保留原CSP2/3/4固定case并新增block_id=5 SPPF。
一个FSM、一份3072B byte工作缓存、一份24×192bit权重bank、一个外部旧算术owner。
没有私有MAC/SiLU/完整ROM、新大数组、任意图描述符或PAN支持；6及以上ID仍非法。

完整端口定义见同目录road_feature_blocks_client.v，端口与冻结CSP共享客户相同。
i_block_id/o_block_id、parameter_response_block_id、barrier_block_id各4bit；
参数channel7bit/group5bit/layer3bit/window3bit；逻辑byte地址32bit、读返回128bit。
旧核元数据端口、II、signed33/RNE、量化/SiLU/残差语义保持。

100MHz同域，只有i_start && o_start_ready锁存block_id；busy期间ID/start忽略。
o_block_id在busy和FINISH稳定，到下一接受start或共同reset才更新。
参数响应握手核对block/layer/channel/group/window及同组量化一致性，
屏障握手核对block/layer。各valid等待ready时payload保持。
最终匹配屏障进入FINISH一拍done1/busy1/start_ready0，下一拍IDLE才可启动。
非法ID、错身份/读地址/核结果、cancel/core_fault粘滞FAULT，占有到共同reset。
i_rstn低有效异步断言，上级共同同步释放；服务共同撤销旧响应、旧owner重装SiLU。
控制/身份/linevalid复位，两个大数组不reset；不保证独立热复位或晚返回排空。

## SPPF fixed graph

H18/W32，逻辑INT8。每个stage完成全部真实写后等待block5及本stage匹配的可见性屏障。

| local stage | operation | input | output base | output channels |
|---|---|---|---|---|
| 0 | squeeze PW | csp4.out 0376b000，Cin96 | 0377a000 | 24 |
| 1 | signed maxpool5×5 | squeeze，C24 | 0377e000 | 24 |
| 2 | signed maxpool5×5 | pool00，C24 | 03782000 | 24 |
| 3 | signed maxpool5×5 | pool01，C24 | 03786000 | 24 |
| 4 | out PW | squeeze,pool00,pool01,pool02四C24 concat | 0378a000 | 96 |

地址均hex，tile4x4_hwc沿冻结graph，通道不补8。两个PW都12个8输入组、
window0、无残差。out的四路concat按固定base解析，没有实体concat张量。
所有新增除数和stride均常量，最后tile起点y16只写y16/17，禁止y18/19。
原CSP2的Cin12 mask0f及final4分类、CSP3/4七阶段和原地址case保留。

## Prefetch and byte port

各SPPF stage预取1536B到同一工作缓存。PW为16×96；
pool为8×8×24 halo，覆盖4×4输出窗口所需空间并集。
pool全图外逻辑样本不读内存，缓存填8'h80(-128)；
PW物理尾行缓存填0。存储服务里的y18/19物理padding0不能作为池化逻辑样本。

PW预取按pixel外/channel内；pool按halo row/column/channel。
linevalid在start和stage转换清，tile间保留一条16B行。
单在途对齐16B逻辑读，响应必须匹配完整地址。
独立CPU调度参考的stage0..4行请求数为3456/3060/3060/3060/4608；
这是待RTL实测核对的参考值，不是本角色测量值。out每个源分支C24跨16B行并切base，
不能按连续96B物理布局估算。

byte数组访问互斥：PREFETCH写一byte，CACHE_ACTIVATION读一byte，
CACHE_BYPASS读一byte，新增POOL_READ读一byte；其它状态不访问byte数组。
每tile完整覆盖全部后续读取范围，每输出组完整覆盖全部使用weight槽。
仅新增sample8bit、max8bit、sample_index5bit、pool_address32bit控制/工作寄存器。
原3072+576+31+16=3695B数据账不含这些寄存器及其它原控制/activation。
4ERAM是目标，资源/端口映射/时序仍UNKNOWN。

## Pool state and retirement

复用ST_TASK_SETUP(7)冻结一个池化写地址、sample_index=0、max=-128，
不会清/更新core_written或core_addresses。随后新增三个状态：

- ST_POOL_READ(17)：每拍从唯一byte口捕获一个样本。
- ST_POOL_COMPARE(18)：显式signed8比较sample与max；不是末样本则index加1回READ，
  第25个样本比较后转WRITE，确保最后样本已进入max。
- ST_POOL_WRITE(19)：独立输出pool_address、pool_max和符号扩展signed9 sum，
  保持到o_write_valid && i_write_ready，再转原ADVANCE。

每个pool输出为setup1+read25+compare25+write等待+advance1；
pool不走核心SEND/WRITE_WAIT/RETIRE，不发参数或核组。
输出遍历沿旧ADVANCE：tile内channel外、pixel内；pool channel逐1，PW逐3。
每个pool stage有13824个真实结果，25个样本/结果；全幅实际周期由root测量。
池化写握手flag_pool_write_accept独立于原flag_write_accept，不能更新core_written、
核心任务done或消费核输出。pool任何阶段出现i_core_output_valid触发fault，
POOL_WRITE同拍禁止写，o_core_output_ready保持0。
池化未释放外部owner，整个block5由同一busy覆盖。

原CSP/PW状态周期保持；状态计数互斥，流水活动计数不能叠加当总周期。
无timeout推断DDR写可见性，屏障仍由外部服务明确确认。

## Verification and current evidence

参考sppf_manifest.json的46个artifact本角色只读核对全部hash一致。
CPU报告PASS_CPU_SPPF_REFERENCE含两卷积全scalar、三pool各13824值；
pad0与unsigned真实数值反例已拒绝。CPU证据不代替RTL或DDR。

root先测同实例CSP4实际写回→SPPF，不重装CPU csp4输出冒充链路。
比较PW全部acc/pre/SiLU/post/sum/地址、pool全部值/signed9 sum及地址、
请求数、25次单口读/比较、stage屏障、尾行禁止写、busy ID/start扰动和背压稳定。
pool负边界、混合signed极值、错block屏障、pool阶段旧core输出、共同复位重装表；
原CSP2/3及CSP4候选回归由root统一执行。

本角色仅执行严格静态门禁，结果见static_gate.json/md；没有ModelSim/TD。
strict失败保留，不能宣称八门全通过或物理映射成立。
PAN未实现，down3/down4/连续骨干等范围未因本候选扩展而闭合。

## Timing diagram

固定一个窗口的最后两样本与写反压：WRITE在最后COMPARE之后才有效。

```json
{
 "signal": [
  {"name":"i_clk","wave":"p......."},
  {"name":"state","wave":"=====..=","data":["READ23","COMPARE23","READ24","COMPARE24","WRITE","ADVANCE"]},
  {"name":"cache_read","wave":"1010...."},
  {"name":"sample_index","wave":"=.=.....","data":["23","24"]},
  {"name":"o_write_valid","wave":"0...1..0"},
  {"name":"i_write_ready","wave":"0.....10"},
  {"name":"o_write_data","wave":"x...=...","data":["signed max of all25"]},
  {"name":"o_write_sum","wave":"x...=...","data":["sign extended max"]},
  {"name":"o_core_output_ready","wave":"0......."},
  {"name":"o_block_id","wave":"=.......","data":["5"]}
 ]
}
```
