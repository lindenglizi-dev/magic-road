# tb_stem_weight_address 验证契约

非综合、无端口白盒测试台，仅枚举组合权重地址，不改变被测调度器接口。

- clk保持0，rstn初始0、1ns后释放；不测时序/亚稳态。
- 两次装填432项权重，分别为地址低8位、高8位。两次合起来区分全部地址。
- 遍历16个position、6个channel组、4个归约组、8个lane、3个输出，共18,432项。
- 每次改变索引后等待1ns；有效项与原始OIHW公式比较，无效输入/输出lane必须为0。
- 失败立即fatal；成功必须打印TB_PASS_STEM_WEIGHT_ADDRESS checks=18432。
- 只读next_weight，不替代正常/背压/复位/缓存导出的冻结全帧测试。

原时序关系：t0修改group，t0+1ns采样next_weight；不推进时钟、不声称额外周期或吞吐。

文档工具限制：canonical write-spec要求ports非空，不支持此类无端口测试台。
失败保留于specifications_attempt3/write_tb_spec.log，未添加假端口绕过检查。
本文件为人工补充契约，不宣称该测试台通过canonical规格生成；设计RTL的同名规格和WaveDrom已由canonical入口生成。
