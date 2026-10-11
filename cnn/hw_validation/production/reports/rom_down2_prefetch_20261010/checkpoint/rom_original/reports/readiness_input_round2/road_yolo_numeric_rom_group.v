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
	parameter C_LANE_ALPHA_FILE = "NONE",      //最低五字节物理通道初始化文件
	parameter C_LANE_BETA_FILE = "NONE",       //次低五字节物理通道初始化文件
	parameter C_LANE_GAMMA_FILE = "NONE",      //次高五字节物理通道初始化文件
	parameter C_LANE_DELTA_FILE = "NONE"       //最高五字节物理通道初始化文件
)
(
	//-----------------全局信号-----------------//
	input i_clk,                               //物理ROM同步读时钟
	input i_rstn,                              //低有效拼接流水复位

	//-----------------用户接口-----------------//
	input [8:0]i_word_addr,                    //四路物理ROM共用字地址
	output [159:0]o_word_data                  //拼接完成的一百六十位字
);

	//--------------模块实例化信号--------------//
	//四路物理ROM读数据
	wire [39:0]lane_alpha_data;                //字节零至字节四读数据
	wire [39:0]lane_beta_data;                 //字节五至字节九读数据
	wire [39:0]lane_gamma_data;                //字节十至字节十四读数据
	wire [39:0]lane_delta_data;                //字节十五至字节十九读数据

	//---------------寄存器信号---------------//
	//两级输出拼接流水
	reg [79:0]reg_lower_pair = 0;              //合并最低十字节的寄存结果
	reg [79:0]reg_upper_pair = 0;              //合并最高十字节的寄存结果

	//-----------------输出信号-----------------//
	//用户接口
	reg [159:0]word_data_o = 0;                //完整ROM字输出桥寄存器

	//---------------输出信号连线---------------//
	//用户接口
	assign o_word_data = word_data_o;          //桥接已寄存的完整ROM字

	//-------------输出信号处理区域-------------//
	//用户接口
	//最终一级拼接形成完整ROM字
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			word_data_o <= 0;                  //复位清空完整字输出
		end else begin
			word_data_o <= {reg_upper_pair, reg_lower_pair}; //拼接高低各十字节
		end
	end

	//-------------主要任务处理区域-------------//
	//首级拼接最低两路物理ROM输出
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_lower_pair <= 0;               //复位清空低十字节
		end else begin
			reg_lower_pair <= {lane_beta_data, lane_alpha_data}; //合并低侧物理通道
		end
	end

	//首级拼接最高两路物理ROM输出
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_upper_pair <= 0;               //复位清空高十字节
		end else begin
			reg_upper_pair <= {lane_delta_data, lane_gamma_data}; //合并高侧物理通道
		end
	end

	//--------------模块实例化区域--------------//
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
	//实例化最低五字节物理ROM通道
	)PH1P_LOGIC_ERAM_Inst_alpha(
		.dia({40{1'b0}}),                      //低五字节固定A口写数据为零
		.addra(i_word_addr),                   //低五字节连接共用读地址
		.cea(1'b1),                            //低五字节持续使能A口访问
		.ocea(1'b0),                           //低五字节关闭A口输出时钟使能
		.clka(i_clk),                          //低五字节连接A口扫描时钟
		.wea(1'b0),                            //低五字节禁止A口写入
		.rsta(1'b0),                           //低五字节保持A口复位无效
		.bea(1'b0),                            //低五字节固定A口字节使能
		.dib({40{1'b0}}),                      //低五字节固定备用B口写数据为零
		.addrb({9{1'b0}}),                     //低五字节固定备用B口地址为零
		.ceb(1'b0),                            //低五字节关闭备用B口访问
		.oceb(1'b0),                           //低五字节关闭备用B口输出使能
		.clkb(i_clk),                          //低五字节连接备用B口时钟
		.web(1'b0),                            //低五字节禁止备用B口写入
		.rstb(1'b0),                           //低五字节保持备用B口复位无效
		.beb(1'b0),                            //低五字节固定备用B口字节使能
		.ecc_sbiterrinj(1'b0),                 //低五字节关闭单比特错误注入
		.ecc_dbiterrinj(1'b0),                 //低五字节关闭双比特错误注入
		.doa(lane_alpha_data),                 //低五字节接收A口通道读数据
		.dob(),                                //低五字节悬空备用B口读数据
		.ecc_sbiterr(),                        //低五字节悬空单比特错误状态
		.ecc_dbiterr()                         //低五字节悬空双比特错误状态
	);

	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),                     //低五字节配置A口四十位宽
		.DATA_WIDTH_B(40),                     //低五字节配置备用B口四十位宽
		.ADDR_WIDTH_A(9),                      //低五字节配置A口九位地址
		.ADDR_WIDTH_B(9),                      //低五字节配置备用B口九位地址
		.DATA_DEPTH_A(512),                    //低五字节配置A口五百一十二字深度
		.DATA_DEPTH_B(512),                    //低五字节配置备用B口同等深度
		.BYTE_ENABLE(0),                       //低五字节关闭字节写使能
		.BYTE_A(1),                            //低五字节保持A口单写使能位
		.BYTE_B(1),                            //低五字节保持备用B口单写使能位
		.MODE("SP"),                           //低五字节选择单端口存储模式
		.REGMODE_A("NOREG"),                   //低五字节选择A口无附加输出寄存
		.REGMODE_B("NOREG"),                   //低五字节选择备用B口无附加输出寄存
		.WRITEMODE_A("NORMAL"),                //低五字节保持A口正常写模式
		.WRITEMODE_B("NORMAL"),                //低五字节保持备用B口正常写模式
		.RESETMODE_A("ASYNC"),                 //低五字节选择A口异步复位模式
		.RESETMODE_B("ASYNC"),                 //低五字节选择备用B口异步复位模式
		.OREGSET_A("RESET"),                   //低五字节选择A口复位输出值
		.OREGSET_B("RESET"),                   //低五字节选择备用B口复位输出值
		.SSROVERCE("DISABLE"),                 //低五字节关闭同步复位优先
		.ECC_DECODE("DISABLE"),                //低五字节关闭纠错解码
		.ECC_ENCODE("DISABLE"),                //低五字节关闭纠错编码
		.ASYNC_RESET_RELEASE_A("ASYNC"),       //低五字节保持A口异步释放
		.ASYNC_RESET_RELEASE_B("ASYNC"),       //低五字节保持备用B口异步释放
		.CLKMODE("ASYNC"),                     //低五字节选择双口异步时钟模式
		.DEBUGGABLE("NO"),                     //低五字节关闭在线调试
		.PACKABLE("NO"),                       //低五字节关闭存储拼块
		.FORCE_KEEP("ON"),                     //低五字节保留物理存储实例
		.INIT_FILE(C_LANE_BETA_FILE),          //低五字节选择通道初始化文件
		.FILL_ALL("NONE"),                     //低五字节关闭统一填充值
		.IMPLEMENT("20K")                      //低五字节选择二十K物理实现
	//实例化次低五字节物理ROM通道
	)PH1P_LOGIC_ERAM_Inst_beta(
		.dia({40{1'b0}}),                      //次低五字节固定A口写数据为零
		.addra(i_word_addr),                   //次低五字节连接共用读地址
		.cea(1'b1),                            //次低五字节持续使能A口访问
		.ocea(1'b0),                           //次低五字节关闭A口输出时钟使能
		.clka(i_clk),                          //次低五字节连接A口扫描时钟
		.wea(1'b0),                            //次低五字节禁止A口写入
		.rsta(1'b0),                           //次低五字节保持A口复位无效
		.bea(1'b0),                            //次低五字节固定A口字节使能
		.dib({40{1'b0}}),                      //次低五字节固定备用B口写数据为零
		.addrb({9{1'b0}}),                     //次低五字节固定备用B口地址为零
		.ceb(1'b0),                            //次低五字节关闭备用B口访问
		.oceb(1'b0),                           //次低五字节关闭备用B口输出使能
		.clkb(i_clk),                          //次低五字节连接备用B口时钟
		.web(1'b0),                            //次低五字节禁止备用B口写入
		.rstb(1'b0),                           //次低五字节保持备用B口复位无效
		.beb(1'b0),                            //次低五字节固定备用B口字节使能
		.ecc_sbiterrinj(1'b0),                 //次低五字节关闭单比特错误注入
		.ecc_dbiterrinj(1'b0),                 //次低五字节关闭双比特错误注入
		.doa(lane_beta_data),                  //次低五字节接收A口通道读数据
		.dob(),                                //次低五字节悬空备用B口读数据
		.ecc_sbiterr(),                        //次低五字节悬空单比特错误状态
		.ecc_dbiterr()                         //次低五字节悬空双比特错误状态
	);

	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),                     //次低五字节配置A口四十位宽
		.DATA_WIDTH_B(40),                     //次低五字节配置备用B口四十位宽
		.ADDR_WIDTH_A(9),                      //次低五字节配置A口九位地址
		.ADDR_WIDTH_B(9),                      //次低五字节配置备用B口九位地址
		.DATA_DEPTH_A(512),                    //次低五字节配置A口五百一十二字深度
		.DATA_DEPTH_B(512),                    //次低五字节配置备用B口同等深度
		.BYTE_ENABLE(0),                       //次低五字节关闭字节写使能
		.BYTE_A(1),                            //次低五字节保持A口单写使能位
		.BYTE_B(1),                            //次低五字节保持备用B口单写使能位
		.MODE("SP"),                           //次低五字节选择单端口存储模式
		.REGMODE_A("NOREG"),                   //次低五字节选择A口无附加输出寄存
		.REGMODE_B("NOREG"),                   //次低五字节选择备用B口无附加输出寄存
		.WRITEMODE_A("NORMAL"),                //次低五字节保持A口正常写模式
		.WRITEMODE_B("NORMAL"),                //次低五字节保持备用B口正常写模式
		.RESETMODE_A("ASYNC"),                 //次低五字节选择A口异步复位模式
		.RESETMODE_B("ASYNC"),                 //次低五字节选择备用B口异步复位模式
		.OREGSET_A("RESET"),                   //次低五字节选择A口复位输出值
		.OREGSET_B("RESET"),                   //次低五字节选择备用B口复位输出值
		.SSROVERCE("DISABLE"),                 //次低五字节关闭同步复位优先
		.ECC_DECODE("DISABLE"),                //次低五字节关闭纠错解码
		.ECC_ENCODE("DISABLE"),                //次低五字节关闭纠错编码
		.ASYNC_RESET_RELEASE_A("ASYNC"),       //次低五字节保持A口异步释放
		.ASYNC_RESET_RELEASE_B("ASYNC"),       //次低五字节保持备用B口异步释放
		.CLKMODE("ASYNC"),                     //次低五字节选择双口异步时钟模式
		.DEBUGGABLE("NO"),                     //次低五字节关闭在线调试
		.PACKABLE("NO"),                       //次低五字节关闭存储拼块
		.FORCE_KEEP("ON"),                     //次低五字节保留物理存储实例
		.INIT_FILE(C_LANE_GAMMA_FILE),         //次低五字节选择通道初始化文件
		.FILL_ALL("NONE"),                     //次低五字节关闭统一填充值
		.IMPLEMENT("20K")                      //次低五字节选择二十K物理实现
	//实例化次高五字节物理ROM通道
	)PH1P_LOGIC_ERAM_Inst_gamma(
		.dia({40{1'b0}}),                      //次高五字节固定A口写数据为零
		.addra(i_word_addr),                   //次高五字节连接共用读地址
		.cea(1'b1),                            //次高五字节持续使能A口访问
		.ocea(1'b0),                           //次高五字节关闭A口输出时钟使能
		.clka(i_clk),                          //次高五字节连接A口扫描时钟
		.wea(1'b0),                            //次高五字节禁止A口写入
		.rsta(1'b0),                           //次高五字节保持A口复位无效
		.bea(1'b0),                            //次高五字节固定A口字节使能
		.dib({40{1'b0}}),                      //次高五字节固定备用B口写数据为零
		.addrb({9{1'b0}}),                     //次高五字节固定备用B口地址为零
		.ceb(1'b0),                            //次高五字节关闭备用B口访问
		.oceb(1'b0),                           //次高五字节关闭备用B口输出使能
		.clkb(i_clk),                          //次高五字节连接备用B口时钟
		.web(1'b0),                            //次高五字节禁止备用B口写入
		.rstb(1'b0),                           //次高五字节保持备用B口复位无效
		.beb(1'b0),                            //次高五字节固定备用B口字节使能
		.ecc_sbiterrinj(1'b0),                 //次高五字节关闭单比特错误注入
		.ecc_dbiterrinj(1'b0),                 //次高五字节关闭双比特错误注入
		.doa(lane_gamma_data),                 //次高五字节接收A口通道读数据
		.dob(),                                //次高五字节悬空备用B口读数据
		.ecc_sbiterr(),                        //次高五字节悬空单比特错误状态
		.ecc_dbiterr()                         //次高五字节悬空双比特错误状态
	);

	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40),                     //次高五字节配置A口四十位宽
		.DATA_WIDTH_B(40),                     //次高五字节配置备用B口四十位宽
		.ADDR_WIDTH_A(9),                      //次高五字节配置A口九位地址
		.ADDR_WIDTH_B(9),                      //次高五字节配置备用B口九位地址
		.DATA_DEPTH_A(512),                    //次高五字节配置A口五百一十二字深度
		.DATA_DEPTH_B(512),                    //次高五字节配置备用B口同等深度
		.BYTE_ENABLE(0),                       //次高五字节关闭字节写使能
		.BYTE_A(1),                            //次高五字节保持A口单写使能位
		.BYTE_B(1),                            //次高五字节保持备用B口单写使能位
		.MODE("SP"),                           //次高五字节选择单端口存储模式
		.REGMODE_A("NOREG"),                   //次高五字节选择A口无附加输出寄存
		.REGMODE_B("NOREG"),                   //次高五字节选择备用B口无附加输出寄存
		.WRITEMODE_A("NORMAL"),                //次高五字节保持A口正常写模式
		.WRITEMODE_B("NORMAL"),                //次高五字节保持备用B口正常写模式
		.RESETMODE_A("ASYNC"),                 //次高五字节选择A口异步复位模式
		.RESETMODE_B("ASYNC"),                 //次高五字节选择备用B口异步复位模式
		.OREGSET_A("RESET"),                   //次高五字节选择A口复位输出值
		.OREGSET_B("RESET"),                   //次高五字节选择备用B口复位输出值
		.SSROVERCE("DISABLE"),                 //次高五字节关闭同步复位优先
		.ECC_DECODE("DISABLE"),                //次高五字节关闭纠错解码
		.ECC_ENCODE("DISABLE"),                //次高五字节关闭纠错编码
		.ASYNC_RESET_RELEASE_A("ASYNC"),       //次高五字节保持A口异步释放
		.ASYNC_RESET_RELEASE_B("ASYNC"),       //次高五字节保持备用B口异步释放
		.CLKMODE("ASYNC"),                     //次高五字节选择双口异步时钟模式
		.DEBUGGABLE("NO"),                     //次高五字节关闭在线调试
		.PACKABLE("NO"),                       //次高五字节关闭存储拼块
		.FORCE_KEEP("ON"),                     //次高五字节保留物理存储实例
		.INIT_FILE(C_LANE_DELTA_FILE),         //次高五字节选择通道初始化文件
		.FILL_ALL("NONE"),                     //次高五字节关闭统一填充值
		.IMPLEMENT("20K")                      //次高五字节选择二十K物理实现
	//实例化最高五字节物理ROM通道
	)PH1P_LOGIC_ERAM_Inst_delta(
		.dia({40{1'b0}}),                      //高五字节固定A口写数据为零
		.addra(i_word_addr),                   //高五字节连接共用读地址
		.cea(1'b1),                            //高五字节持续使能A口访问
		.ocea(1'b0),                           //高五字节关闭A口输出时钟使能
		.clka(i_clk),                          //高五字节连接A口扫描时钟
		.wea(1'b0),                            //高五字节禁止A口写入
		.rsta(1'b0),                           //高五字节保持A口复位无效
		.bea(1'b0),                            //高五字节固定A口字节使能
		.dib({40{1'b0}}),                      //高五字节固定备用B口写数据为零
		.addrb({9{1'b0}}),                     //高五字节固定备用B口地址为零
		.ceb(1'b0),                            //高五字节关闭备用B口访问
		.oceb(1'b0),                           //高五字节关闭备用B口输出使能
		.clkb(i_clk),                          //高五字节连接备用B口时钟
		.web(1'b0),                            //高五字节禁止备用B口写入
		.rstb(1'b0),                           //高五字节保持备用B口复位无效
		.beb(1'b0),                            //高五字节固定备用B口字节使能
		.ecc_sbiterrinj(1'b0),                 //高五字节关闭单比特错误注入
		.ecc_dbiterrinj(1'b0),                 //高五字节关闭双比特错误注入
		.doa(lane_delta_data),                 //高五字节接收A口通道读数据
		.dob(),                                //高五字节悬空备用B口读数据
		.ecc_sbiterr(),                        //高五字节悬空单比特错误状态
		.ecc_dbiterr()                         //高五字节悬空双比特错误状态
	);

endmodule
