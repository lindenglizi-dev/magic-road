`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 16:00:00
// Design Name:     road_yolo_numeric_rom_group
// Module Name:     road_yolo_numeric_rom_group
// Description:     description/road_yolo_numeric_rom_group_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_yolo_numeric_rom_group
//
// Referrences:
// File Format      File Name
// 1.Book           PH1P_LOGIC_ERAM official
//
// Dependencies:
// Module Name      Version
// PH1P_LOGIC_ERAM official
//
// Version:         V1.0
// Revision Date:   2026/10/04 16:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/04       V1.0        Codex             Create physical ROM group.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月04日
// 设计名称:        road_yolo_numeric_rom_group
// 模块名称:        road_yolo_numeric_rom_group
// 模块说明:        Description/road_yolo_numeric_rom_group_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_yolo_numeric_rom_group
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           PH1P_LOGIC_ERAM official
//
// 依赖文件:
// 模块名称         版本
// PH1P_LOGIC_ERAM official
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Codex             创建物理ROM组。

module road_yolo_numeric_rom_group
#(
	parameter C_LANE_ALPHA_FILE = "NONE",       // 最低五字节物理通道初始化文件
	parameter C_LANE_BETA_FILE = "NONE",        // 次低五字节物理通道初始化文件
	parameter C_LANE_GAMMA_FILE = "NONE",       // 次高五字节物理通道初始化文件
	parameter C_LANE_DELTA_FILE = "NONE"        // 最高五字节物理通道初始化文件
)
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 物理ROM同步读时钟
	input i_rstn,                               // 低有效拼接流水复位

	//-----------------用户接口-----------------//
	input [8:0]i_word_addr,                     // 四路物理ROM共用字地址
	output [159:0]o_word_data                   // 拼接完成的一百六十位字
);

	//--------------模块实例化信号--------------//
	//四路物理ROM读数据
	wire [39:0]lane_alpha_data;                 // 字节零至字节四读数据
	wire [39:0]lane_beta_data;                  // 字节五至字节九读数据
	wire [39:0]lane_gamma_data;                 // 字节十至字节十四读数据
	wire [39:0]lane_delta_data;                 // 字节十五至字节十九读数据

	//-----------------其他信号-----------------//
	//两级输出拼接流水
	reg [79:0]lower_pair_reg;                   // 合并最低十字节的寄存结果
	reg [79:0]upper_pair_reg;                   // 合并最高十字节的寄存结果

	//-----------------输出信号-----------------//
	//用户接口
	reg [159:0]word_data_o;                     // 完整ROM字输出桥寄存器

	//---------------输出信号连线---------------//
	//用户接口
	assign o_word_data = word_data_o;           // 桥接已寄存的完整ROM字

	//-------------输出信号处理区域-------------//
	//最终一级拼接形成完整ROM字
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			word_data_o <= 160'b0;                  // 复位清空完整字输出
		end else begin
			word_data_o <= {upper_pair_reg, lower_pair_reg}; // 拼接高低各十字节
		end
	end

	//-------------主要任务处理区域-------------//
	//首级拼接最低两路物理ROM输出
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			lower_pair_reg <= 80'b0;                // 复位清空低十字节
		end else begin
			lower_pair_reg <= {lane_beta_data, lane_alpha_data}; // 合并低侧物理通道
		end
	end

	//首级拼接最高两路物理ROM输出
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			upper_pair_reg <= 80'b0;                // 复位清空高十字节
		end else begin
			upper_pair_reg <= {lane_delta_data, lane_gamma_data}; // 合并高侧物理通道
		end
	end

	//--------------模块实例化区域--------------//
	//实例化最低五字节物理ROM通道
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),
		.DATA_WIDTH_B(40),
		.ADDR_WIDTH_A(9),
		.ADDR_WIDTH_B(9),
		.DATA_DEPTH_A(512),
		.DATA_DEPTH_B(512),
		.BYTE_ENABLE(0),
		.BYTE_A(1),
		.BYTE_B(1),
		.MODE("SP"),
		.REGMODE_A("NOREG"),
		.REGMODE_B("NOREG"),
		.WRITEMODE_A("NORMAL"),
		.WRITEMODE_B("NORMAL"),
		.RESETMODE_A("ASYNC"),
		.RESETMODE_B("ASYNC"),
		.OREGSET_A("RESET"),
		.OREGSET_B("RESET"),
		.SSROVERCE("DISABLE"),
		.ECC_DECODE("DISABLE"),
		.ECC_ENCODE("DISABLE"),
		.ASYNC_RESET_RELEASE_A("ASYNC"),
		.ASYNC_RESET_RELEASE_B("ASYNC"),
		.CLKMODE("ASYNC"),
		.DEBUGGABLE("NO"),
		.PACKABLE("NO"),
		.FORCE_KEEP("ON"),
		.INIT_FILE(C_LANE_ALPHA_FILE),
		.FILL_ALL("NONE"),
		.IMPLEMENT("20K")
	)PH1P_LOGIC_ERAM_Inst_alpha(
		.dia(40'b0),
		.addra(i_word_addr),
		.cea(1'b1),
		.ocea(1'b0),
		.clka(i_clk),
		.wea(1'b0),
		.rsta(1'b0),
		.bea(1'b0),
		.dib(40'b0),
		.addrb(9'b0),
		.ceb(1'b0),
		.oceb(1'b0),
		.clkb(i_clk),
		.web(1'b0),
		.rstb(1'b0),
		.beb(1'b0),
		.ecc_sbiterrinj(1'b0),
		.ecc_dbiterrinj(1'b0),
		.doa(lane_alpha_data),
		.dob(),
		.ecc_sbiterr(),
		.ecc_dbiterr()
	);

	//实例化次低五字节物理ROM通道
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),
		.DATA_WIDTH_B(40),
		.ADDR_WIDTH_A(9),
		.ADDR_WIDTH_B(9),
		.DATA_DEPTH_A(512),
		.DATA_DEPTH_B(512),
		.BYTE_ENABLE(0),
		.BYTE_A(1),
		.BYTE_B(1),
		.MODE("SP"),
		.REGMODE_A("NOREG"),
		.REGMODE_B("NOREG"),
		.WRITEMODE_A("NORMAL"),
		.WRITEMODE_B("NORMAL"),
		.RESETMODE_A("ASYNC"),
		.RESETMODE_B("ASYNC"),
		.OREGSET_A("RESET"),
		.OREGSET_B("RESET"),
		.SSROVERCE("DISABLE"),
		.ECC_DECODE("DISABLE"),
		.ECC_ENCODE("DISABLE"),
		.ASYNC_RESET_RELEASE_A("ASYNC"),
		.ASYNC_RESET_RELEASE_B("ASYNC"),
		.CLKMODE("ASYNC"),
		.DEBUGGABLE("NO"),
		.PACKABLE("NO"),
		.FORCE_KEEP("ON"),
		.INIT_FILE(C_LANE_BETA_FILE),
		.FILL_ALL("NONE"),
		.IMPLEMENT("20K")
	)PH1P_LOGIC_ERAM_Inst_beta(
		.dia(40'b0),
		.addra(i_word_addr),
		.cea(1'b1),
		.ocea(1'b0),
		.clka(i_clk),
		.wea(1'b0),
		.rsta(1'b0),
		.bea(1'b0),
		.dib(40'b0),
		.addrb(9'b0),
		.ceb(1'b0),
		.oceb(1'b0),
		.clkb(i_clk),
		.web(1'b0),
		.rstb(1'b0),
		.beb(1'b0),
		.ecc_sbiterrinj(1'b0),
		.ecc_dbiterrinj(1'b0),
		.doa(lane_beta_data),
		.dob(),
		.ecc_sbiterr(),
		.ecc_dbiterr()
	);

	//实例化次高五字节物理ROM通道
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),
		.DATA_WIDTH_B(40),
		.ADDR_WIDTH_A(9),
		.ADDR_WIDTH_B(9),
		.DATA_DEPTH_A(512),
		.DATA_DEPTH_B(512),
		.BYTE_ENABLE(0),
		.BYTE_A(1),
		.BYTE_B(1),
		.MODE("SP"),
		.REGMODE_A("NOREG"),
		.REGMODE_B("NOREG"),
		.WRITEMODE_A("NORMAL"),
		.WRITEMODE_B("NORMAL"),
		.RESETMODE_A("ASYNC"),
		.RESETMODE_B("ASYNC"),
		.OREGSET_A("RESET"),
		.OREGSET_B("RESET"),
		.SSROVERCE("DISABLE"),
		.ECC_DECODE("DISABLE"),
		.ECC_ENCODE("DISABLE"),
		.ASYNC_RESET_RELEASE_A("ASYNC"),
		.ASYNC_RESET_RELEASE_B("ASYNC"),
		.CLKMODE("ASYNC"),
		.DEBUGGABLE("NO"),
		.PACKABLE("NO"),
		.FORCE_KEEP("ON"),
		.INIT_FILE(C_LANE_GAMMA_FILE),
		.FILL_ALL("NONE"),
		.IMPLEMENT("20K")
	)PH1P_LOGIC_ERAM_Inst_gamma(
		.dia(40'b0),
		.addra(i_word_addr),
		.cea(1'b1),
		.ocea(1'b0),
		.clka(i_clk),
		.wea(1'b0),
		.rsta(1'b0),
		.bea(1'b0),
		.dib(40'b0),
		.addrb(9'b0),
		.ceb(1'b0),
		.oceb(1'b0),
		.clkb(i_clk),
		.web(1'b0),
		.rstb(1'b0),
		.beb(1'b0),
		.ecc_sbiterrinj(1'b0),
		.ecc_dbiterrinj(1'b0),
		.doa(lane_gamma_data),
		.dob(),
		.ecc_sbiterr(),
		.ecc_dbiterr()
	);

	//实例化最高五字节物理ROM通道
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),
		.DATA_WIDTH_B(40),
		.ADDR_WIDTH_A(9),
		.ADDR_WIDTH_B(9),
		.DATA_DEPTH_A(512),
		.DATA_DEPTH_B(512),
		.BYTE_ENABLE(0),
		.BYTE_A(1),
		.BYTE_B(1),
		.MODE("SP"),
		.REGMODE_A("NOREG"),
		.REGMODE_B("NOREG"),
		.WRITEMODE_A("NORMAL"),
		.WRITEMODE_B("NORMAL"),
		.RESETMODE_A("ASYNC"),
		.RESETMODE_B("ASYNC"),
		.OREGSET_A("RESET"),
		.OREGSET_B("RESET"),
		.SSROVERCE("DISABLE"),
		.ECC_DECODE("DISABLE"),
		.ECC_ENCODE("DISABLE"),
		.ASYNC_RESET_RELEASE_A("ASYNC"),
		.ASYNC_RESET_RELEASE_B("ASYNC"),
		.CLKMODE("ASYNC"),
		.DEBUGGABLE("NO"),
		.PACKABLE("NO"),
		.FORCE_KEEP("ON"),
		.INIT_FILE(C_LANE_DELTA_FILE),
		.FILL_ALL("NONE"),
		.IMPLEMENT("20K")
	)PH1P_LOGIC_ERAM_Inst_delta(
		.dia(40'b0),
		.addra(i_word_addr),
		.cea(1'b1),
		.ocea(1'b0),
		.clka(i_clk),
		.wea(1'b0),
		.rsta(1'b0),
		.bea(1'b0),
		.dib(40'b0),
		.addrb(9'b0),
		.ceb(1'b0),
		.oceb(1'b0),
		.clkb(i_clk),
		.web(1'b0),
		.rstb(1'b0),
		.beb(1'b0),
		.ecc_sbiterrinj(1'b0),
		.ecc_dbiterrinj(1'b0),
		.doa(lane_delta_data),
		.dob(),
		.ecc_sbiterr(),
		.ecc_dbiterr()
	);

endmodule
