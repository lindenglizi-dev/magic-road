module road_stem_ddr_sequence
#(
	parameter [26:0] C_TIMEOUT = 27'h7ffffff // 无进展看门狗，不充当DDR屏障
)
(
	input i_clk, // 100MHz计算时钟
	input i_rstn, // 与整个DDR共同断言并在本域同步释放
	input i_phy_ready, // 已同步到本域的初始化许可
	input i_ddr_fault, // 邮箱的本域粘滞故障
	input i_req_ready, // 邮箱可保管唯一请求
	input i_rsp_valid, // 完整响应已跨域冻结
	input [127:0]i_rsp_data, // 实际DDR返回字
	input [3:0]i_rsp_error, // 写接受或读请求错误
	output o_req_valid, // 载荷保持到本域接受
	output o_req_write, // 写接受与读返回分型
	output [24:0]o_req_addr, // 按冻结布局转换的native地址
	output [127:0]o_req_data, // 实际核导出打包的128位字
	output o_rsp_ready, // 完整响应只消费一次
	output [1:0]o_status, // 零等待、一通过、二失败
	output [3:0]o_error, // 首个失败类型
	output [4:0]o_phase, // 可观测调度状态
	output [8:0]o_writes, // 已收到接受回执的唯一写字数
	output [8:0]o_reads, // 实际已消费的读响应数
	output [10:0]o_output_bytes, // 已核对的最终PW字节数
	output [31:0]o_cycles, // 含初始化的端点总周期
	output [319:0]o_cycle_bins, // 十项互斥分类，低32位为初始化
	output [24:0]o_address, // 当前读写的完整native地址
	output [127:0]o_expected, // 最近比较的完整期望字
	output [127:0]o_actual // 最近比较的完整实读或导出字
);
endmodule
module road_paxi_mailbox #(
	parameter [26:0] C_TIMEOUT = 27'h7ffffff // DDR端点一次事务的最大等待拍数
)(
	//-----------------全局信号-----------------//
	input i_clk,                                // 100MHz请求源时钟
	input i_rstn,                               // 源域低有效复位，必须与DDR域共同断言
	input i_ddr_clk,                            // 约133.33MHz的DDR用户时钟
	input i_ddr_rstn,                           // DDR域低有效复位，必须与源域共同断言
	input i_phy_ready,                          // DDR PHY已完成初始化且持续可用

	//----------------源请求接口----------------//
	input i_req_valid,                          // 请求有效，等待ready期间载荷由上游保持
	input i_req_write,                          // 高电平选择写事务，低电平选择读事务
	input [24:0] i_req_addr,                    // 原生PAXI地址，合法步长为八
	input [127:0] i_req_data,                   // 单拍写入的完整128位载荷
	output o_req_ready,                         // 无在途事务且无故障时允许接收

	//----------------源响应接口----------------//
	output o_rsp_valid,                         // 完整响应已复制并保持至源端消费
	output [127:0] o_rsp_data,                  // 单拍读数据，写响应固定为零
	output [3:0] o_rsp_error,                   // 地址、PHY、RLAST、协议或超时分类
	input i_rsp_ready,                          // 源端确认已消费冻结响应
	output o_fault,                             // 任一端点错误的源域粘滞观测

	//---------------PAXI写地址通道-------------//
	input i_awready,                            // DDR控制器写地址接收条件
	output [24:0] o_awaddr,                     // 冻结请求中的原生写地址
	output o_awvalid,                           // 写地址持续呈现至独立握手

	//---------------PAXI写数据通道-------------//
	input i_wready,                             // DDR控制器写数据接收条件
	output [127:0] o_wdata,                     // 冻结请求中的128位写数据
	output [15:0] o_wstrb,                      // 当前控制器约定的全零高有效掩码
	output o_wvalid,                            // 写数据持续呈现至独立握手
	output o_wlast,                             // 唯一写数据拍的末拍标志

	//---------------PAXI读地址通道-------------//
	input i_arready,                            // DDR控制器读地址接收条件
	output [24:0] o_araddr,                     // 冻结请求中的原生读地址
	output o_arvalid,                           // 读地址持续呈现至真实握手

	//---------------PAXI读返回通道-------------//
	input i_rvalid,                             // DDR控制器返回一拍128位数据
	input i_rlast,                              // 单拍读返回必须同时声明末拍
	input [127:0] i_rdata,                      // 原生PAXI读返回载荷
	output o_rready                             // 预留返回槽后允许接收读数据
);
endmodule
