`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO
// Engineer:        Codex
// Create Date:     2026/10/16
// Design Name:     WIF1 physical feature and weight workstore
// Module Name:     road_feature_workstore
// Description:     description/road_feature_workstore_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_feature_workstore
// Referrences:     PH1P_LOGIC_ERAM public contract, gray_frame_bank_ram.
// Dependencies:    PH1P_LOGIC_ERAM official vendor primitive.
// Version:         V1.0
// Revision Date:   2026/10/16
// History:
// Time             Version     Revised by        Contents
// 2026/10/16       V1.0        Codex             Create workstore.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO
// 开发人员:        Codex
// 创建日期:        2026年10月16日
// 设计名称:        特征字节与权重物理工作仓
// 模块名称:        road_feature_workstore
// 模块说明:        Description/road_feature_workstore_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_feature_workstore
// 参考资料:        PH1P_LOGIC_ERAM与gray_frame_bank_ram。
// 依赖文件:        官方PH1P_LOGIC_ERAM。
// 当前版本:        V1.0
// 修订日期:        2026年10月16日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月16日   V1.0        Codex             创建工作仓。

module road_feature_workstore
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 唯一一百MHz工作时钟
	input i_rstn,                               // 共同低有效复位并取消旧事务

	//-----------------用户接口-----------------//
	input i_byte_req_valid,                     // 字节请求在握手沿被接受
	input i_byte_req_write,                     // 字节操作方向一写零读
	input [11:0]i_byte_req_addr,                 // 字节逻辑地址仅零至3071合法
	input [7:0]i_byte_req_data,                  // 字节写入的八位原样数据
	input i_byte_rsp_ready,                     // 字节响应消费许可
	input i_weight_req_valid,                   // 权重请求在独立通道握手
	input i_weight_req_write,                   // 权重操作方向一写零读
	input [4:0]i_weight_req_group,               // 权重组号仅零至23合法
	input [191:0]i_weight_req_data,              // 权重整组载荷低位先存
	input i_weight_rsp_ready,                   // 权重完成响应的消费许可
	output o_byte_req_ready,                    // 字节仓空闲或旧响应同拍退休
	output o_byte_rsp_valid,                    // 字节native提交或取得后的响应
	output [7:0]o_byte_rsp_data,                 // 字节读结果写及错误返回零
	output o_byte_rsp_error,                    // 字节越界请求的完成错误
	output o_weight_req_ready,                  // 权重仓无未完成native操作
	output o_weight_rsp_valid,                  // 三个word完成后的整组响应
	output [191:0]o_weight_rsp_data,             // 三word拼接的原始权重载荷
	output o_weight_rsp_error,                  // 权重非法组号的完成错误
	output o_fault                              // 任一接受的越界请求粘滞至复位
);

	//--------------模块实例化信号--------------//
	//四块物理存储的同步读结果
	wire [7:0]dec_byte_lower_data;              // 第一字节块A口读出值
	wire [7:0]dec_byte_upper_data;              // 第二字节块A口读出值
	wire [39:0]dec_weight_lower_data;           // 每个权重word的低四十位
	wire [39:0]dec_weight_upper_data;           // 每个权重word的高四十位

	//---------------计数信号---------------//
	//权重连续三word访问与末拍捕获
	reg [2:0]cnt_weight_phase = 0;              // 零空闲一至三访问四完成

	//---------------寄存器信号---------------//
	//握手锁存后保持至本事务完成
	reg [11:0]reg_byte_addr = 0;                // 锁存字节bank及块内地址
	reg [7:0]reg_byte_data = 0;                 // native写沿使用的字节载荷
	reg reg_byte_write = 0;                    // 字节请求方向跨同步读流水
	reg reg_byte_illegal = 0;                  // 越界字节事务禁止物理访问
	reg [8:0]reg_weight_native_addr = 0;        // 三倍组号起始并逐word递增
	reg [191:0]reg_weight_data = 0;             // 当前权重写请求的完整载荷
	reg reg_weight_write = 0;                  // 三个native沿共同的操作方向
	reg reg_weight_illegal = 0;                // 非法组号只完成错误响应
	reg [79:0]reg_weight_native_data = 0;       // 组合选择本拍八十位写入片

	//---------------标志信号---------------//
	//两通道握手与native访问资格
	wire flag_byte_accept;                    // 字节valid及ready同时成立
	reg flag_byte_pending = 0;                 // 字节接受后等待native沿
	reg flag_byte_capture = 0;                 // native沿后的读数据捕获资格
	wire flag_byte_native_enable;             // 共同复位外的合法字节访问
	wire flag_byte_native_write;              // 合法字节访问中的写许可
	wire flag_byte_lower_enable;              // 零至2047选择第一字节块
	wire flag_byte_upper_enable;              // 2048至3071选择第二字节块
	wire flag_weight_accept;                  // 权重valid及ready同时成立
	wire flag_weight_native_enable;           // 合法组号的一至三word访问
	wire flag_weight_native_write;            // 三个权重写沿的共同写许可
	reg flag_running = 0;                     // 共同复位释放一拍后允许请求

	//---------------输出信号---------------//
	//端点响应在反压时保持全部载荷
	wire byte_req_ready_o;                    // 字节单未退休槽位准入
	reg byte_rsp_valid_o = 0;                 // 字节完成资格由消费者退休
	reg [7:0]byte_rsp_data_o = 0;              // 取得的字节结果寄存值
	reg byte_rsp_error_o = 0;                 // 与字节响应同行的错误位
	wire weight_req_ready_o;                  // 权重单未退休槽位准入
	reg weight_rsp_valid_o = 0;               // 末word取得后发布的资格
	reg [191:0]weight_rsp_data_o = 0;           // 逐word捕获并保持的权重结果
	reg weight_rsp_error_o = 0;               // 与权重响应同行的错误位
	reg fault_o = 0;                          // 双通道共同的越界锁存告警

	//-------------其他信号连线-------------//
	//单未退休事务与原子访问选择
	assign byte_req_ready_o = flag_running && !flag_byte_pending && !flag_byte_capture && (!byte_rsp_valid_o || i_byte_rsp_ready); // native等待完成且旧响应可退休时准入
	assign weight_req_ready_o = flag_running && (cnt_weight_phase == 3'd0) && (!weight_rsp_valid_o || i_weight_rsp_ready); // 三word空闲并留有响应槽时准入
	assign flag_byte_accept = i_byte_req_valid && byte_req_ready_o; // 仅字节请求真实握手触发锁存
	assign flag_weight_accept = i_weight_req_valid && weight_req_ready_o; // 仅权重请求真实握手启动三word
	assign flag_byte_native_enable = flag_byte_pending && !reg_byte_illegal; // 复位清pending且非法事务不产生字节CE
	assign flag_byte_native_write = flag_byte_native_enable && reg_byte_write; // 字节WE只随有效访问的写方向
	assign flag_byte_lower_enable = flag_byte_native_enable && !reg_byte_addr[11]; // 低地址bank选择保留至取得
	assign flag_byte_upper_enable = flag_byte_native_enable && reg_byte_addr[11]; // 高地址bank只开放合法半块
	assign flag_weight_native_enable = (cnt_weight_phase[0] || cnt_weight_phase[1]) && !reg_weight_illegal; // 复位清阶段且第四阶段关闭CE
	assign flag_weight_native_write = flag_weight_native_enable && reg_weight_write; // 权重WE与三word合法访问一致

	//-------------输出信号连线-------------//
	//准确WIF1端口桥接
	assign o_byte_req_ready = byte_req_ready_o; // 输出字节请求接纳资格
	assign o_byte_rsp_valid = byte_rsp_valid_o; // 输出字节完成的寄存有效位
	assign o_byte_rsp_data = byte_rsp_data_o; // 输出字节完成的寄存载荷
	assign o_byte_rsp_error = byte_rsp_error_o; // 输出字节完成的寄存错误
	assign o_weight_req_ready = weight_req_ready_o; // 输出权重请求接纳资格
	assign o_weight_rsp_valid = weight_rsp_valid_o; // 输出权重完成的寄存有效位
	assign o_weight_rsp_data = weight_rsp_data_o; // 输出完整权重的寄存载荷
	assign o_weight_rsp_error = weight_rsp_error_o; // 输出整组权重的寄存错误
	assign o_fault = fault_o; // 输出共同复位清除的粘滞告警

	//-----------输出信号处理区域-----------//
	//字节完成必须晚于native提交沿
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			byte_rsp_valid_o <= 0; // 取消复位之前的字节完成
		end else if(flag_byte_capture)begin
			byte_rsp_valid_o <= 1; // K2发布K1已提交的字节事务
		end else if(byte_rsp_valid_o && i_byte_rsp_ready)begin
			byte_rsp_valid_o <= 0; // 已消费的字节响应退出槽位
		end
	end

	//字节数据只能在native读沿后一拍采样
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			byte_rsp_data_o <= 0; // 复位清空端点结果而非RAM
		end else if(flag_byte_capture)begin
			if(reg_byte_illegal || reg_byte_write)begin
				byte_rsp_data_o <= 0; // 错误及写确认均返回确定零
			end else begin
				byte_rsp_data_o <= reg_byte_addr[11] ? dec_byte_upper_data : dec_byte_lower_data; // bank元数据选择同步读值
			end
		end
	end

	//错误状态与字节响应同拍完成
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			byte_rsp_error_o <= 0; // 清除已取消的字节错误
		end else if(flag_byte_capture)begin
			byte_rsp_error_o <= reg_byte_illegal; // 非法标志保持到响应消费
		end
	end

	//权重完成统一使用第四阶段收尾
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			weight_rsp_valid_o <= 0; // 取消旧整组权重响应
		end else if(cnt_weight_phase == 3'd4)begin
			weight_rsp_valid_o <= 1; // K4确认三word已提交或取得
		end else if(weight_rsp_valid_o && i_weight_rsp_ready)begin
			weight_rsp_valid_o <= 0; // 权重消费者消费后释放响应槽
		end
	end

	//同步读每个word在访问后一拍拼接
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			weight_rsp_data_o <= 0; // 复位只清空整组响应寄存器
		end else if(reg_weight_illegal || reg_weight_write)begin
			if(cnt_weight_phase == 3'd4)begin
				weight_rsp_data_o <= 0; // 全组写完成及错误完成返回零
			end
		end else begin
			case(cnt_weight_phase)
				3'd2:begin
					weight_rsp_data_o[79:0] <= {dec_weight_upper_data, dec_weight_lower_data}; // 取得首word的八十位
				end
				3'd3:begin
					weight_rsp_data_o[159:80] <= {dec_weight_upper_data, dec_weight_lower_data}; // 取得中word的八十位
				end
				3'd4:begin
					weight_rsp_data_o[191:160] <= dec_weight_lower_data[31:0]; // 尾word只取有效三十二位
				end
				default:begin
					weight_rsp_data_o <= weight_rsp_data_o; // 非捕获阶段保留响应载荷
				end
			endcase
		end
	end

	//权重错误从锁存组号保留到完成
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			weight_rsp_error_o <= 0; // 复位取消先前组号错误
		end else if(cnt_weight_phase == 3'd4)begin
			weight_rsp_error_o <= reg_weight_illegal; // 第四阶段将错误与valid对齐
		end
	end

	//任一越界接受永久告警至共同复位
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			fault_o <= 0; // 共同复位清除越界历史
		end else if((flag_byte_accept && (i_byte_req_addr >= 12'd3072)) || (flag_weight_accept && (i_weight_req_group >= 5'd24)))begin
			fault_o <= 1; // 只对真实握手的非法请求粘滞置位
		end
	end

	//-----------主要任务处理区域-----------//
	//共同复位释放后启用同域端点
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_running <= 0; // 复位期间请求保持未就绪
		end else begin
			flag_running <= 1; // 首个正常沿后开放握手
		end
	end

	//字节请求经一个native沿后进入捕获阶段
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_byte_pending <= 0; // 复位禁止未提交字节访问
		end else begin
			flag_byte_pending <= flag_byte_accept; // 接受后只生成一次native访问资格
		end
	end

	//字节同步读延迟与请求方向共同保持
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_byte_capture <= 0; // 取消复位前native取得资格
		end else begin
			flag_byte_capture <= flag_byte_pending; // K1访问后的K2才采样读值
		end
	end

	//锁存字节块选择和块内地址
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_byte_addr <= 0; // 清空控制地址不触及存储内容
		end else if(flag_byte_accept)begin
			reg_byte_addr <= i_byte_req_addr; // 地址稳定覆盖提交与捕获窗口
		end
	end

	//锁存字节写载荷以承受源端变化
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_byte_data <= 0; // 清空待写字节寄存值
		end else if(flag_byte_accept)begin
			reg_byte_data <= i_byte_req_data; // 真实写沿只使用握手时数据
		end
	end

	//记录字节读写方向
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_byte_write <= 0; // 复位默认无写请求
		end else if(flag_byte_accept)begin
			reg_byte_write <= i_byte_req_write; // 请求方向保持至完成
		end
	end

	//字节越界只保留错误元数据
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_byte_illegal <= 0; // 复位清除待响应越界位
		end else if(flag_byte_accept)begin
			reg_byte_illegal <= i_byte_req_addr >= 12'd3072; // 未实现的高半块禁止CE
		end
	end

	//固定四阶段计数独立于响应反压
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			cnt_weight_phase <= 0; // 中断三word序列且取消旧valid
		end else if(flag_weight_accept)begin
			cnt_weight_phase <= 3'd1; // K0接受后从首word开始
		end else if(cnt_weight_phase == 3'd4)begin
			cnt_weight_phase <= 0; // 完成时回空闲并由响应占槽
		end else if(cnt_weight_phase != 3'd0)begin
			cnt_weight_phase <= cnt_weight_phase + 3'd1; // 三word逐拍访问而后统一收尾
		end
	end

	//权重组号乘三后只在前两次访问递增
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_weight_native_addr <= 0; // 清空native地址控制寄存
		end else if(flag_weight_accept)begin
			reg_weight_native_addr <= {4'd0, i_weight_req_group} + {3'd0, i_weight_req_group, 1'b0}; // 九位无符号精确计算组起点
		end else if((cnt_weight_phase == 3'd1) || (cnt_weight_phase == 3'd2))begin
			reg_weight_native_addr <= reg_weight_native_addr + 9'd1; // 合法末组最后地址为71
		end
	end

	//权重只保留当前整组操作数
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_weight_data <= 0; // 清空未提交权重载荷
		end else if(flag_weight_accept)begin
			reg_weight_data <= i_weight_req_data; // 三word均来自同一次握手
		end
	end

	//保存整组操作方向
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_weight_write <= 0; // 取消复位前整组写方向
		end else if(flag_weight_accept)begin
			reg_weight_write <= i_weight_req_write; // 方向跨越三个实际提交沿
		end
	end

	//在发出任何word前完成合法性锁存
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_weight_illegal <= 0; // 复位取消待响应组号错误
		end else if(flag_weight_accept)begin
			reg_weight_illegal <= i_weight_req_group >= 5'd24; // 非法组号三阶段均关闭CE
		end
	end

	//八十位word低位先存且尾word高四十八位清零
	always@(*)begin
		reg_weight_native_data = 80'd0; // 空闲与完成阶段不提供有效写片
		case(cnt_weight_phase)
			3'd1:begin
				reg_weight_native_data = reg_weight_data[79:0]; // 首word承载最低十字节
			end
			3'd2:begin
				reg_weight_native_data = reg_weight_data[159:80]; // 中word承载中间十字节
			end
			3'd3:begin
				reg_weight_native_data = {48'd0, reg_weight_data[191:160]}; // 尾word只写最高四字节
			end
			default:begin
				reg_weight_native_data = 80'd0; // 其余阶段固定空写入片
			end
		endcase
	end

	//------------模块实例化区域------------//
	//低地址字节块独占一个PH1P存储原语
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(8), // 低地址字节块A口数据位宽
		.DATA_WIDTH_B(8), // 低地址字节块停用B口数据位宽
		.ADDR_WIDTH_A(11), // 低地址字节块A口块内地址位数
		.ADDR_WIDTH_B(11), // 低地址字节块停用B口地址位数
		.DATA_DEPTH_A(2048), // 低地址字节块A口物理深度
		.DATA_DEPTH_B(2048), // 低地址字节块B口匹配的物理深度
		.BYTE_ENABLE(0), // 低地址字节块整字写入禁用字节掩码
		.BYTE_A(1), // 低地址字节块A口单个未使用掩码位
		.BYTE_B(1), // 低地址字节块B口单个未使用掩码位
		.MODE("SP"), // 低地址字节块读写序列化的单口模式
		.REGMODE_A("NOREG"), // 低地址字节块同步读无额外输出寄存级
		.REGMODE_B("NOREG"), // 低地址字节块备用输出不加寄存级
		.WRITEMODE_A("NORMAL"), // 低地址字节块写时输出无需参与数据判断
		.WRITEMODE_B("NORMAL"), // 低地址字节块备用写模式保持默认
		.RESETMODE_A("ASYNC"), // 低地址字节块A口输出复位模式保持异步
		.RESETMODE_B("ASYNC"), // 低地址字节块B口输出复位模式保持异步
		.OREGSET_A("RESET"), // 低地址字节块A口输出复位设定为零
		.OREGSET_B("RESET"), // 低地址字节块B口输出复位设定为零
		.SSROVERCE("DISABLE"), // 低地址字节块关闭同步复位优先
		.ECC_DECODE("DISABLE"), // 低地址字节块不启用纠错读出
		.ECC_ENCODE("DISABLE"), // 低地址字节块不启用纠错写入
		.ASYNC_RESET_RELEASE_A("ASYNC"), // 低地址字节块A口无额外复位释放流水
		.ASYNC_RESET_RELEASE_B("ASYNC"), // 低地址字节块B口无额外复位释放流水
		.CLKMODE("ASYNC"), // 低地址字节块沿用已验证SP时钟模式
		.DEBUGGABLE("NO"), // 低地址字节块关闭额外调试接口
		.PACKABLE("NO"), // 低地址字节块禁止与其他逻辑打包
		.FORCE_KEEP("ON"), // 低地址字节块保留此实际物理块
		.INIT_FILE("NONE"), // 低地址字节块不加载位流初始化文件
		.FILL_ALL("NONE"), // 低地址字节块不依赖上电填充内容
		.IMPLEMENT("20K") // 低地址字节块选择一块原生二十K模式
	)PH1P_LOGIC_ERAM_Inst_byte_lower(
		.dia(reg_byte_data), // 低地址字节块握手后保持的写入载荷
		.dib(8'd0), // 低地址字节块停用B口写数据置零
		.addra(reg_byte_addr[10:0]), // 低地址字节块当前提交或读取的块内地址
		.addrb(11'd0), // 低地址字节块停用B口地址固定零
		.cea(flag_byte_lower_enable), // 低地址字节块唯一有效访问口的CE
		.ceb(1'b0), // 低地址字节块B口从不访问存储
		.ocea(1'b0), // 低地址字节块无输出寄存级不使用OCE
		.oceb(1'b0), // 低地址字节块停用B口不使用OCE
		.clka(i_clk), // 低地址字节块工作仓共同A口时钟
		.clkb(i_clk), // 低地址字节块停用B口也连接同域时钟
		.wea(flag_byte_native_write), // 低地址字节块只有合法提交沿允许写入
		.web(1'b0), // 低地址字节块B口永远禁止写入
		.bea(1'b0), // 低地址字节块整字模式忽略A口字节选择
		.beb(1'b0), // 低地址字节块停用B口字节选择固定零
		.rsta(1'b0), // 低地址字节块不复位物理内容或输出
		.rstb(1'b0), // 低地址字节块停用B口复位保持无效
		.doa(dec_byte_lower_data), // 低地址字节块取得的A口同步读数据
		.dob(), // 低地址字节块停用B口读结果不接
		.ecc_sbiterr(), // 低地址字节块未启用单比特纠错状态
		.ecc_dbiterr(), // 低地址字节块未启用双比特纠错状态
		.ecc_sbiterrinj(1'b0), // 低地址字节块关闭单比特错误注入
		.ecc_dbiterrinj(1'b0) // 低地址字节块关闭双比特错误注入
	);

	//高地址字节块独占一个PH1P存储原语
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(8), // 高地址字节块A口数据位宽
		.DATA_WIDTH_B(8), // 高地址字节块停用B口数据位宽
		.ADDR_WIDTH_A(11), // 高地址字节块A口块内地址位数
		.ADDR_WIDTH_B(11), // 高地址字节块停用B口地址位数
		.DATA_DEPTH_A(2048), // 高地址字节块A口物理深度
		.DATA_DEPTH_B(2048), // 高地址字节块B口匹配的物理深度
		.BYTE_ENABLE(0), // 高地址字节块整字写入禁用字节掩码
		.BYTE_A(1), // 高地址字节块A口单个未使用掩码位
		.BYTE_B(1), // 高地址字节块B口单个未使用掩码位
		.MODE("SP"), // 高地址字节块读写序列化的单口模式
		.REGMODE_A("NOREG"), // 高地址字节块同步读无额外输出寄存级
		.REGMODE_B("NOREG"), // 高地址字节块备用输出不加寄存级
		.WRITEMODE_A("NORMAL"), // 高地址字节块写时输出无需参与数据判断
		.WRITEMODE_B("NORMAL"), // 高地址字节块备用写模式保持默认
		.RESETMODE_A("ASYNC"), // 高地址字节块A口输出复位模式保持异步
		.RESETMODE_B("ASYNC"), // 高地址字节块B口输出复位模式保持异步
		.OREGSET_A("RESET"), // 高地址字节块A口输出复位设定为零
		.OREGSET_B("RESET"), // 高地址字节块B口输出复位设定为零
		.SSROVERCE("DISABLE"), // 高地址字节块关闭同步复位优先
		.ECC_DECODE("DISABLE"), // 高地址字节块不启用纠错读出
		.ECC_ENCODE("DISABLE"), // 高地址字节块不启用纠错写入
		.ASYNC_RESET_RELEASE_A("ASYNC"), // 高地址字节块A口无额外复位释放流水
		.ASYNC_RESET_RELEASE_B("ASYNC"), // 高地址字节块B口无额外复位释放流水
		.CLKMODE("ASYNC"), // 高地址字节块沿用已验证SP时钟模式
		.DEBUGGABLE("NO"), // 高地址字节块关闭额外调试接口
		.PACKABLE("NO"), // 高地址字节块禁止与其他逻辑打包
		.FORCE_KEEP("ON"), // 高地址字节块保留此实际物理块
		.INIT_FILE("NONE"), // 高地址字节块不加载位流初始化文件
		.FILL_ALL("NONE"), // 高地址字节块不依赖上电填充内容
		.IMPLEMENT("20K") // 高地址字节块选择一块原生二十K模式
	)PH1P_LOGIC_ERAM_Inst_byte_upper(
		.dia(reg_byte_data), // 高地址字节块握手后保持的写入载荷
		.dib(8'd0), // 高地址字节块停用B口写数据置零
		.addra(reg_byte_addr[10:0]), // 高地址字节块当前提交或读取的块内地址
		.addrb(11'd0), // 高地址字节块停用B口地址固定零
		.cea(flag_byte_upper_enable), // 高地址字节块唯一有效访问口的CE
		.ceb(1'b0), // 高地址字节块B口从不访问存储
		.ocea(1'b0), // 高地址字节块无输出寄存级不使用OCE
		.oceb(1'b0), // 高地址字节块停用B口不使用OCE
		.clka(i_clk), // 高地址字节块工作仓共同A口时钟
		.clkb(i_clk), // 高地址字节块停用B口也连接同域时钟
		.wea(flag_byte_native_write), // 高地址字节块只有合法提交沿允许写入
		.web(1'b0), // 高地址字节块B口永远禁止写入
		.bea(1'b0), // 高地址字节块整字模式忽略A口字节选择
		.beb(1'b0), // 高地址字节块停用B口字节选择固定零
		.rsta(1'b0), // 高地址字节块不复位物理内容或输出
		.rstb(1'b0), // 高地址字节块停用B口复位保持无效
		.doa(dec_byte_upper_data), // 高地址字节块取得的A口同步读数据
		.dob(), // 高地址字节块停用B口读结果不接
		.ecc_sbiterr(), // 高地址字节块未启用单比特纠错状态
		.ecc_dbiterr(), // 高地址字节块未启用双比特纠错状态
		.ecc_sbiterrinj(1'b0), // 高地址字节块关闭单比特错误注入
		.ecc_dbiterrinj(1'b0) // 高地址字节块关闭双比特错误注入
	);

	//权重低位片独占一个PH1P存储原语
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40), // 权重低位片A口数据位宽
		.DATA_WIDTH_B(40), // 权重低位片停用B口数据位宽
		.ADDR_WIDTH_A(9), // 权重低位片A口块内地址位数
		.ADDR_WIDTH_B(9), // 权重低位片停用B口地址位数
		.DATA_DEPTH_A(512), // 权重低位片A口物理深度
		.DATA_DEPTH_B(512), // 权重低位片B口匹配的物理深度
		.BYTE_ENABLE(0), // 权重低位片整字写入禁用字节掩码
		.BYTE_A(1), // 权重低位片A口单个未使用掩码位
		.BYTE_B(1), // 权重低位片B口单个未使用掩码位
		.MODE("SP"), // 权重低位片读写序列化的单口模式
		.REGMODE_A("NOREG"), // 权重低位片同步读无额外输出寄存级
		.REGMODE_B("NOREG"), // 权重低位片备用输出不加寄存级
		.WRITEMODE_A("NORMAL"), // 权重低位片写时输出无需参与数据判断
		.WRITEMODE_B("NORMAL"), // 权重低位片备用写模式保持默认
		.RESETMODE_A("ASYNC"), // 权重低位片A口输出复位模式保持异步
		.RESETMODE_B("ASYNC"), // 权重低位片B口输出复位模式保持异步
		.OREGSET_A("RESET"), // 权重低位片A口输出复位设定为零
		.OREGSET_B("RESET"), // 权重低位片B口输出复位设定为零
		.SSROVERCE("DISABLE"), // 权重低位片关闭同步复位优先
		.ECC_DECODE("DISABLE"), // 权重低位片不启用纠错读出
		.ECC_ENCODE("DISABLE"), // 权重低位片不启用纠错写入
		.ASYNC_RESET_RELEASE_A("ASYNC"), // 权重低位片A口无额外复位释放流水
		.ASYNC_RESET_RELEASE_B("ASYNC"), // 权重低位片B口无额外复位释放流水
		.CLKMODE("ASYNC"), // 权重低位片沿用已验证SP时钟模式
		.DEBUGGABLE("NO"), // 权重低位片关闭额外调试接口
		.PACKABLE("NO"), // 权重低位片禁止与其他逻辑打包
		.FORCE_KEEP("ON"), // 权重低位片保留此实际物理块
		.INIT_FILE("NONE"), // 权重低位片不加载位流初始化文件
		.FILL_ALL("NONE"), // 权重低位片不依赖上电填充内容
		.IMPLEMENT("20K") // 权重低位片选择一块原生二十K模式
	)PH1P_LOGIC_ERAM_Inst_weight_lower(
		.dia(reg_weight_native_data[39:0]), // 权重低位片握手后保持的写入载荷
		.dib(40'd0), // 权重低位片停用B口写数据置零
		.addra(reg_weight_native_addr), // 权重低位片当前提交或读取的块内地址
		.addrb(9'd0), // 权重低位片停用B口地址固定零
		.cea(flag_weight_native_enable), // 权重低位片唯一有效访问口的CE
		.ceb(1'b0), // 权重低位片B口从不访问存储
		.ocea(1'b0), // 权重低位片无输出寄存级不使用OCE
		.oceb(1'b0), // 权重低位片停用B口不使用OCE
		.clka(i_clk), // 权重低位片工作仓共同A口时钟
		.clkb(i_clk), // 权重低位片停用B口也连接同域时钟
		.wea(flag_weight_native_write), // 权重低位片只有合法提交沿允许写入
		.web(1'b0), // 权重低位片B口永远禁止写入
		.bea(1'b0), // 权重低位片整字模式忽略A口字节选择
		.beb(1'b0), // 权重低位片停用B口字节选择固定零
		.rsta(1'b0), // 权重低位片不复位物理内容或输出
		.rstb(1'b0), // 权重低位片停用B口复位保持无效
		.doa(dec_weight_lower_data), // 权重低位片取得的A口同步读数据
		.dob(), // 权重低位片停用B口读结果不接
		.ecc_sbiterr(), // 权重低位片未启用单比特纠错状态
		.ecc_dbiterr(), // 权重低位片未启用双比特纠错状态
		.ecc_sbiterrinj(1'b0), // 权重低位片关闭单比特错误注入
		.ecc_dbiterrinj(1'b0) // 权重低位片关闭双比特错误注入
	);

	//权重高位片独占一个PH1P存储原语
	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(40), // 权重高位片A口数据位宽
		.DATA_WIDTH_B(40), // 权重高位片停用B口数据位宽
		.ADDR_WIDTH_A(9), // 权重高位片A口块内地址位数
		.ADDR_WIDTH_B(9), // 权重高位片停用B口地址位数
		.DATA_DEPTH_A(512), // 权重高位片A口物理深度
		.DATA_DEPTH_B(512), // 权重高位片B口匹配的物理深度
		.BYTE_ENABLE(0), // 权重高位片整字写入禁用字节掩码
		.BYTE_A(1), // 权重高位片A口单个未使用掩码位
		.BYTE_B(1), // 权重高位片B口单个未使用掩码位
		.MODE("SP"), // 权重高位片读写序列化的单口模式
		.REGMODE_A("NOREG"), // 权重高位片同步读无额外输出寄存级
		.REGMODE_B("NOREG"), // 权重高位片备用输出不加寄存级
		.WRITEMODE_A("NORMAL"), // 权重高位片写时输出无需参与数据判断
		.WRITEMODE_B("NORMAL"), // 权重高位片备用写模式保持默认
		.RESETMODE_A("ASYNC"), // 权重高位片A口输出复位模式保持异步
		.RESETMODE_B("ASYNC"), // 权重高位片B口输出复位模式保持异步
		.OREGSET_A("RESET"), // 权重高位片A口输出复位设定为零
		.OREGSET_B("RESET"), // 权重高位片B口输出复位设定为零
		.SSROVERCE("DISABLE"), // 权重高位片关闭同步复位优先
		.ECC_DECODE("DISABLE"), // 权重高位片不启用纠错读出
		.ECC_ENCODE("DISABLE"), // 权重高位片不启用纠错写入
		.ASYNC_RESET_RELEASE_A("ASYNC"), // 权重高位片A口无额外复位释放流水
		.ASYNC_RESET_RELEASE_B("ASYNC"), // 权重高位片B口无额外复位释放流水
		.CLKMODE("ASYNC"), // 权重高位片沿用已验证SP时钟模式
		.DEBUGGABLE("NO"), // 权重高位片关闭额外调试接口
		.PACKABLE("NO"), // 权重高位片禁止与其他逻辑打包
		.FORCE_KEEP("ON"), // 权重高位片保留此实际物理块
		.INIT_FILE("NONE"), // 权重高位片不加载位流初始化文件
		.FILL_ALL("NONE"), // 权重高位片不依赖上电填充内容
		.IMPLEMENT("20K") // 权重高位片选择一块原生二十K模式
	)PH1P_LOGIC_ERAM_Inst_weight_upper(
		.dia(reg_weight_native_data[79:40]), // 权重高位片握手后保持的写入载荷
		.dib(40'd0), // 权重高位片停用B口写数据置零
		.addra(reg_weight_native_addr), // 权重高位片当前提交或读取的块内地址
		.addrb(9'd0), // 权重高位片停用B口地址固定零
		.cea(flag_weight_native_enable), // 权重高位片唯一有效访问口的CE
		.ceb(1'b0), // 权重高位片B口从不访问存储
		.ocea(1'b0), // 权重高位片无输出寄存级不使用OCE
		.oceb(1'b0), // 权重高位片停用B口不使用OCE
		.clka(i_clk), // 权重高位片工作仓共同A口时钟
		.clkb(i_clk), // 权重高位片停用B口也连接同域时钟
		.wea(flag_weight_native_write), // 权重高位片只有合法提交沿允许写入
		.web(1'b0), // 权重高位片B口永远禁止写入
		.bea(1'b0), // 权重高位片整字模式忽略A口字节选择
		.beb(1'b0), // 权重高位片停用B口字节选择固定零
		.rsta(1'b0), // 权重高位片不复位物理内容或输出
		.rstb(1'b0), // 权重高位片停用B口复位保持无效
		.doa(dec_weight_upper_data), // 权重高位片取得的A口同步读数据
		.dob(), // 权重高位片停用B口读结果不接
		.ecc_sbiterr(), // 权重高位片未启用单比特纠错状态
		.ecc_dbiterr(), // 权重高位片未启用双比特纠错状态
		.ecc_sbiterrinj(1'b0), // 权重高位片关闭单比特错误注入
		.ecc_dbiterrinj(1'b0) // 权重高位片关闭双比特错误注入
	);

endmodule
