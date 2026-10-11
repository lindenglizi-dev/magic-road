`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 16:00:00
// Design Name:     road_yolo_numeric_rom_probe
// Module Name:     road_yolo_numeric_rom_probe
// Description:     description/road_yolo_numeric_rom_probe_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_yolo_numeric_rom_probe
//
// Referrences:
// File Format      File Name
// 1.Book           cnn/contract.json
//
// Dependencies:
// Module Name      Version
// road_yolo_numeric_rom_group current
//
// Version:         V1.0
// Revision Date:   2026/10/04 16:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/04       V1.0        Codex             Create full-package CRC probe.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月04日
// 设计名称:        road_yolo_numeric_rom_probe
// 模块名称:        road_yolo_numeric_rom_probe
// 模块说明:        Description/road_yolo_numeric_rom_probe_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_yolo_numeric_rom_probe
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           cnn/contract.json
//
// 依赖文件:
// 模块名称         版本
// road_yolo_numeric_rom_group current
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Codex             创建全包CRC探针。

module road_yolo_numeric_rom_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 全包扫描工作时钟
	input i_rstn,                               // 低有效扫描复位

	//-----------------用户接口-----------------//
	output o_done,                              // 全部物理ROM扫描完成标志
	output [31:0]o_checksum                     // 全部字节的CRC校验结果
);

	//---------------状态参数区域---------------//
	localparam [14:0]ST_ISSUE = 15'b000000000000001;       // 发起当前ROM字读取
	localparam [14:0]ST_WAIT_PHY = 15'b000000000000010;    // 等待物理ROM同步读出
	localparam [14:0]ST_WAIT_GROUP = 15'b000000000000100;  // 等待组内两级拼接寄存
	localparam [14:0]ST_WAIT_PAIR = 15'b000000000001000;   // 等待首层组选择寄存
	localparam [14:0]ST_WAIT_QUAD = 15'b000000000010000;   // 等待次层组选择寄存
	localparam [14:0]ST_WAIT_OCT = 15'b000000000100000;    // 等待第三层组选择寄存
	localparam [14:0]ST_WAIT_SELECT = 15'b000000001000000; // 等待末层组选择寄存
	localparam [14:0]ST_CAPTURE = 15'b000000010000000;     // 捕获完整一百六十位字
	localparam [14:0]ST_BIT_FETCH = 15'b000000100000000;   // 取得当前待校验数据位
	localparam [14:0]ST_BIT_UPDATE = 15'b000001000000000;  // 更新逐位CRC余数
	localparam [14:0]ST_WORD_BRANCH = 15'b000010000000000; // 判定字地址或组地址推进
	localparam [14:0]ST_WORD_INCREMENT = 15'b000100000000000; // 推进同组字地址
	localparam [14:0]ST_GROUP_ADVANCE = 15'b001000000000000; // 切换下一物理ROM组
	localparam [14:0]ST_FINISH = 15'b010000000000000;      // 锁存最终校验结果
	localparam [14:0]ST_DONE = 15'b100000000000000;        // 保持完成状态

	//--------------模块实例化信号--------------//
	//road_yolo_numeric_rom_group--用户接口
	wire [159:0]group_alpha_data;               // 第零组完整ROM字数据
	wire [159:0]group_beta_data;                // 第一组完整ROM字数据
	wire [159:0]group_gamma_data;               // 第二组完整ROM字数据
	wire [159:0]group_delta_data;               // 第三组完整ROM字数据
	wire [159:0]group_epsilon_data;             // 第四组完整ROM字数据
	wire [159:0]group_zeta_data;                // 第五组完整ROM字数据
	wire [159:0]group_eta_data;                 // 第六组完整ROM字数据
	wire [159:0]group_theta_data;               // 第七组完整ROM字数据
	wire [159:0]group_iota_data;                // 第八组完整ROM字数据
	wire [159:0]group_kappa_data;               // 第九组完整ROM字数据
	wire [159:0]group_lambda_data;              // 第十组完整ROM字数据
	wire [159:0]group_mu_data;                  // 第十一组完整ROM字数据
	wire [159:0]group_nu_data;                  // 第十二组完整ROM字数据
	wire [159:0]group_xi_data;                  // 第十三组完整ROM字数据

	//----------------状态机信号----------------//
	reg [14:0]state_current;                    // 当前独热扫描状态
	reg [14:0]state_next;                       // 下一独热扫描状态
	reg [5:0]task_control;                      // 当前状态单周期任务控制

	//-----------------其他信号-----------------//
	//ROM扫描位置与数据缓存
	reg [3:0]group_index_reg;                   // 当前物理ROM组索引
	reg [8:0]word_addr_reg;                     // 当前组内字地址
	reg [7:0]bit_index_reg;                     // 当前字内位索引
	reg [159:0]word_buffer_reg;                 // 当前待校验完整字缓存
	reg data_bit_reg;                           // 当前待反馈CRC的数据位
	reg last_bit_reg;                           // 当前数据位是否为字末位
	reg [1:0]word_branch_reg;                   // 当前字完成后的推进分支

	//逐位CRC数据路径
	reg [31:0]crc_reg;                          // 当前CRC余数寄存器
	wire crc_bit_mix;                           // 输入位与余数低位异或结果
	wire [31:0]crc_shifted;                     // 右移后的CRC中间值
	wire [31:0]crc_updated;                     // 本拍反馈后的CRC结果
	wire last_word_flag;                        // 当前地址位于组末字
	wire last_group_flag;                       // 当前索引位于末组

	//分层组选择流水寄存器
	reg [159:0]pair_alpha_reg;                  // 首对ROM组选择结果
	reg [159:0]pair_beta_reg;                   // 第二对ROM组选择结果
	reg [159:0]pair_gamma_reg;                  // 第三对ROM组选择结果
	reg [159:0]pair_delta_reg;                  // 第四对ROM组选择结果
	reg [159:0]pair_epsilon_reg;                // 第五对ROM组选择结果
	reg [159:0]pair_zeta_reg;                   // 第六对ROM组选择结果
	reg [159:0]pair_eta_reg;                    // 第七对ROM组选择结果
	reg [159:0]quad_alpha_reg;                  // 低四组选择结果
	reg [159:0]quad_beta_reg;                   // 次低四组选择结果
	reg [159:0]quad_gamma_reg;                  // 高区首四组选择结果
	reg [159:0]quad_delta_reg;                  // 高区末两组选择结果
	reg [159:0]oct_lower_reg;                   // 低八组选择结果
	reg [159:0]oct_upper_reg;                   // 高六组选择结果
	reg [159:0]selected_word_reg;               // 当前组最终选择字

	//-----------------输出信号-----------------//
	//用户接口
	reg done_o;                                 // 扫描完成锁存标志
	reg [31:0]checksum_o;                       // 全包CRC校验结果

	//---------------其他信号连线---------------//
	//逐位CRC与边界判定
	assign crc_bit_mix = crc_reg[0] ^ data_bit_reg; // 合并余数低位与当前数据位
	assign crc_shifted = {1'b0, crc_reg[31:1]}; // 形成无符号右移余数
	assign crc_updated = crc_bit_mix ? (crc_shifted ^ 32'hEDB88320) : crc_shifted; // 选择多项式反馈结果
	assign last_word_flag = (word_addr_reg == 9'd511); // 识别当前组末字
	assign last_group_flag = (group_index_reg == 4'd13); // 识别整个包末组

	//---------------输出信号连线---------------//
	//用户接口
	assign o_done = done_o;                     // 输出锁存的完成标志
	assign o_checksum = checksum_o;             // 输出锁存的CRC结果

	//-------------输出信号处理区域-------------//
	//用户接口
	//扫描完成标志仅在结束任务时置位
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			done_o <= 1'b0;                       // 异步复位清除完成标志
		end else if(task_control[5] == 1'b1)begin
			done_o <= 1'b1;                       // 结束状态锁存扫描完成
		end else begin
			done_o <= done_o;                     // 其余状态保持完成标志
		end
	end

	//最终CRC只在结束任务时由稳定余数生成
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			checksum_o <= 32'b0;                  // 异步复位清除校验输出
		end else if(task_control[5] == 1'b1)begin
			checksum_o <= ~crc_reg;               // 对最终余数执行标准末异或
		end else begin
			checksum_o <= checksum_o;             // 扫描期间保持既有输出
		end
	end

	//----------------状态机区域----------------//
	//组合过程只决定下一独热状态
	always@(*)begin
		state_next = state_current;              // 默认保持当前状态
		case(state_current)
			//发起读取后等待物理存储器输出
			ST_ISSUE:begin
				state_next = ST_WAIT_PHY;           // 进入物理读延迟状态
			end
			//物理读延迟结束后等待组内拼接
			ST_WAIT_PHY:begin
				state_next = ST_WAIT_GROUP;         // 进入组字形成等待状态
			end
			//组字形成后启动分层选择流水
			ST_WAIT_GROUP:begin
				state_next = ST_WAIT_PAIR;          // 等待成对选择寄存
			end
			//首层选择结束后等待四组选择
			ST_WAIT_PAIR:begin
				state_next = ST_WAIT_QUAD;          // 等待四组聚合寄存
			end
			//四组选择结束后等待八组选择
			ST_WAIT_QUAD:begin
				state_next = ST_WAIT_OCT;           // 等待八组聚合寄存
			end
			//八组选择结束后等待最终组选择
			ST_WAIT_OCT:begin
				state_next = ST_WAIT_SELECT;        // 等待末级选择寄存
			end
			//末级组选择稳定后准备捕获
			ST_WAIT_SELECT:begin
				state_next = ST_CAPTURE;            // 进入完整字捕获状态
			end
			//捕获完成后取得字内首位
			ST_CAPTURE:begin
				state_next = ST_BIT_FETCH;          // 开始逐位CRC循环
			end
			//数据位寄存后执行CRC反馈
			ST_BIT_FETCH:begin
				state_next = ST_BIT_UPDATE;         // 进入余数更新状态
			end
			//根据已寄存的末位标志决定继续或收字
			ST_BIT_UPDATE:begin
				if(last_bit_reg == 1'b1)begin
					state_next = ST_WORD_BRANCH;     // 字末进入地址分支
				end else begin
					state_next = ST_BIT_FETCH;       // 非字末继续取得下一位
				end
			end
			//使用已寄存的边界编码选择推进动作
			ST_WORD_BRANCH:begin
				case(word_branch_reg)
					//普通字只推进组内地址
					2'b00:begin
						state_next = ST_WORD_INCREMENT; // 进入字地址递增状态
					end
					//组末字切换到下一物理组
					2'b01:begin
						state_next = ST_GROUP_ADVANCE; // 进入组地址切换状态
					end
					//包末字进入校验结果锁存
					default:begin
						state_next = ST_FINISH;        // 进入全包结束状态
					end
				endcase
			end
			//同组地址推进后重新发起读取
			ST_WORD_INCREMENT:begin
				state_next = ST_ISSUE;             // 返回ROM读取起点
			end
			//组地址推进后重新发起读取
			ST_GROUP_ADVANCE:begin
				state_next = ST_ISSUE;             // 返回下一组读取起点
			end
			//校验结果锁存后进入完成保持态
			ST_FINISH:begin
				state_next = ST_DONE;              // 进入完成保持状态
			end
			//完成状态保持到下一次复位
			ST_DONE:begin
				state_next = ST_DONE;              // 保持扫描完成状态
			end
			//非法状态恢复到读取起点
			default:begin
				state_next = ST_ISSUE;             // 独热状态异常时重新扫描
			end
		endcase
	end

	//独热状态寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_ISSUE;           // 异步复位进入首字读取
		end else begin
			state_current <= state_next;          // 每拍锁存组合下一状态
		end
	end

	//-------------状态任务处理区域-------------//
	//组合过程把当前状态译码为单一任务向量
	always@(*)begin
		task_control = 6'b000000;               // 默认不触发数据任务
		case(state_current)
			//捕获完整ROM字与边界信息
			ST_CAPTURE:begin
				task_control = 6'b000001;          // 使能字缓存任务
			end
			//取得当前CRC输入位
			ST_BIT_FETCH:begin
				task_control = 6'b000010;          // 使能位采样任务
			end
			//更新CRC与位计数
			ST_BIT_UPDATE:begin
				task_control = 6'b000100;          // 使能余数更新任务
			end
			//推进同组字地址
			ST_WORD_INCREMENT:begin
				task_control = 6'b001000;          // 使能字地址递增任务
			end
			//推进物理组地址
			ST_GROUP_ADVANCE:begin
				task_control = 6'b010000;          // 使能组地址递增任务
			end
			//锁存最终输出
			ST_FINISH:begin
				task_control = 6'b100000;          // 使能结束输出任务
			end
			//其余状态没有数据更新任务
			default:begin
				task_control = 6'b000000;          // 保持所有数据寄存器
			end
		endcase
	end

	//-------------主要任务处理区域-------------//
	//物理组索引仅在组切换任务中递增
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			group_index_reg <= 4'd0;             // 复位指向首个ROM组
		end else if(task_control[4] == 1'b1)begin
			group_index_reg <= group_index_reg + 4'd1; // 组末切换到下一ROM组
		end else begin
			group_index_reg <= group_index_reg;  // 非切换状态保持组索引
		end
	end

	//组内字地址按字或组推进任务更新
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			word_addr_reg <= 9'd0;               // 复位指向组内首字
		end else if(task_control[3] == 1'b1)begin
			word_addr_reg <= word_addr_reg + 9'd1; // 普通字完成后地址加一
		end else if(task_control[4] == 1'b1)begin
			word_addr_reg <= 9'd0;               // 切组时回到新组首字
		end else begin
			word_addr_reg <= word_addr_reg;      // 等待期间保持读地址
		end
	end

	//字内位索引在捕获或逐位更新任务中变化
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			bit_index_reg <= 8'd0;               // 复位指向字内最低位
		end else if(task_control[0] == 1'b1)begin
			bit_index_reg <= 8'd0;               // 捕获新字时重置位索引
		end else if(task_control[2] == 1'b1)begin
			bit_index_reg <= bit_index_reg + 8'd1; // CRC更新后推进一位
		end else begin
			bit_index_reg <= bit_index_reg;      // 非更新状态保持位索引
		end
	end

	//当前选择字在捕获任务中进入校验缓存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			word_buffer_reg <= 160'b0;            // 复位清空完整字缓存
		end else if(task_control[0] == 1'b1)begin
			word_buffer_reg <= selected_word_reg; // 捕获末级组选择结果
		end else begin
			word_buffer_reg <= word_buffer_reg;   // 扫描字内位时保持缓存
		end
	end

	//当前数据位在位采样任务中单独寄存
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			data_bit_reg <= 1'b0;                 // 复位清除CRC输入位
		end else if(task_control[1] == 1'b1)begin
			data_bit_reg <= word_buffer_reg[bit_index_reg]; // 采样当前字内数据位
		end else begin
			data_bit_reg <= data_bit_reg;         // 余数更新期间保持输入位
		end
	end

	//末位标志与数据位同时寄存以切断状态源锥
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			last_bit_reg <= 1'b0;                 // 复位清除字末标志
		end else if(task_control[1] == 1'b1)begin
			last_bit_reg <= (bit_index_reg == 8'd159); // 标记当前是否处理末位
		end else begin
			last_bit_reg <= last_bit_reg;         // CRC更新期间保持末位判定
		end
	end

	//字完成分支在捕获任务中由地址边界编码
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			word_branch_reg <= 2'b00;             // 复位选择普通字推进
		end else if(task_control[0] == 1'b1)begin
			case({last_group_flag, last_word_flag})
				//末组末字编码为全包结束
				2'b11:begin
					word_branch_reg <= 2'b10;        // 选择结果锁存分支
				end
				//任意非末组的组末字编码为切组
				2'b01:begin
					word_branch_reg <= 2'b01;        // 选择物理组推进分支
				end
				//其余地址编码为组内递增
				default:begin
					word_branch_reg <= 2'b00;        // 选择组内字推进分支
				end
			endcase
		end else begin
			word_branch_reg <= word_branch_reg;   // 当前字扫描期间保持分支
		end
	end

	//CRC余数仅在位更新任务中推进
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			crc_reg <= 32'hFFFFFFFF;              // 复位装载标准CRC初值
		end else if(task_control[2] == 1'b1)begin
			crc_reg <= crc_updated;               // 锁存本位反馈后的余数
		end else begin
			crc_reg <= crc_reg;                   // 非更新状态保持CRC余数
		end
	end

	//首层成对选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_alpha_reg <= 160'b0;             // 复位清空首对选择结果
		end else begin
			pair_alpha_reg <= group_index_reg[0] ? group_beta_data : group_alpha_data; // 选择第零或第一组
		end
	end

	//第二对组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_beta_reg <= 160'b0;              // 复位清空第二对结果
		end else begin
			pair_beta_reg <= group_index_reg[0] ? group_delta_data : group_gamma_data; // 选择第二或第三组
		end
	end

	//第三对组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_gamma_reg <= 160'b0;             // 复位清空第三对结果
		end else begin
			pair_gamma_reg <= group_index_reg[0] ? group_zeta_data : group_epsilon_data; // 选择第四或第五组
		end
	end

	//第四对组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_delta_reg <= 160'b0;             // 复位清空第四对结果
		end else begin
			pair_delta_reg <= group_index_reg[0] ? group_theta_data : group_eta_data; // 选择第六或第七组
		end
	end

	//第五对组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_epsilon_reg <= 160'b0;           // 复位清空第五对结果
		end else begin
			pair_epsilon_reg <= group_index_reg[0] ? group_kappa_data : group_iota_data; // 选择第八或第九组
		end
	end

	//第六对组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_zeta_reg <= 160'b0;              // 复位清空第六对结果
		end else begin
			pair_zeta_reg <= group_index_reg[0] ? group_mu_data : group_lambda_data; // 选择第十或第十一组
		end
	end

	//第七对组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			pair_eta_reg <= 160'b0;               // 复位清空第七对结果
		end else begin
			pair_eta_reg <= group_index_reg[0] ? group_xi_data : group_nu_data; // 选择第十二或第十三组
		end
	end

	//低四组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			quad_alpha_reg <= 160'b0;             // 复位清空低四组结果
		end else begin
			quad_alpha_reg <= group_index_reg[1] ? pair_beta_reg : pair_alpha_reg; // 选择低区成对结果
		end
	end

	//次低四组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			quad_beta_reg <= 160'b0;              // 复位清空次低四组结果
		end else begin
			quad_beta_reg <= group_index_reg[1] ? pair_delta_reg : pair_gamma_reg; // 选择中低区成对结果
		end
	end

	//高区首四组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			quad_gamma_reg <= 160'b0;             // 复位清空高区四组结果
		end else begin
			quad_gamma_reg <= group_index_reg[1] ? pair_zeta_reg : pair_epsilon_reg; // 选择中高区成对结果
		end
	end

	//高区末两组传递寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			quad_delta_reg <= 160'b0;             // 复位清空末两组结果
		end else begin
			quad_delta_reg <= pair_eta_reg;       // 传递第十二与第十三组选择值
		end
	end

	//低八组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			oct_lower_reg <= 160'b0;              // 复位清空低八组结果
		end else begin
			oct_lower_reg <= group_index_reg[2] ? quad_beta_reg : quad_alpha_reg; // 选择低半区四组结果
		end
	end

	//高六组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			oct_upper_reg <= 160'b0;              // 复位清空高六组结果
		end else begin
			oct_upper_reg <= group_index_reg[2] ? quad_delta_reg : quad_gamma_reg; // 选择高半区四组结果
		end
	end

	//最终组选择寄存器
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			selected_word_reg <= 160'b0;          // 复位清空末级选择字
		end else begin
			selected_word_reg <= group_index_reg[3] ? oct_upper_reg : oct_lower_reg; // 选择低八组或高六组结果
		end
	end

	//--------------模块实例化区域--------------//
	//实例化第0个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_00_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_00_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_00_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_00_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_alpha(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_alpha_data)
	);

	//实例化第1个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_01_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_01_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_01_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_01_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_beta(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_beta_data)
	);

	//实例化第2个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_02_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_02_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_02_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_02_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_gamma(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_gamma_data)
	);

	//实例化第3个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_03_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_03_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_03_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_03_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_delta(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_delta_data)
	);

	//实例化第4个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_04_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_04_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_04_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_04_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_epsilon(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_epsilon_data)
	);

	//实例化第5个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_05_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_05_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_05_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_05_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_zeta(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_zeta_data)
	);

	//实例化第6个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_06_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_06_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_06_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_06_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_eta(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_eta_data)
	);

	//实例化第7个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_07_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_07_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_07_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_07_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_theta(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_theta_data)
	);

	//实例化第8个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_08_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_08_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_08_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_08_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_iota(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_iota_data)
	);

	//实例化第9个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_09_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_09_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_09_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_09_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_kappa(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_kappa_data)
	);

	//实例化第10个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_10_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_10_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_10_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_10_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_lambda(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_lambda_data)
	);

	//实例化第11个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_11_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_11_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_11_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_11_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_mu(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_mu_data)
	);

	//实例化第12个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_12_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_12_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_12_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_12_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_nu(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_nu_data)
	);

	//实例化第13个物理ROM组
	road_yolo_numeric_rom_group #(
		.C_LANE_ALPHA_FILE("artifacts/group_13_lane_0.dath"),
		.C_LANE_BETA_FILE("artifacts/group_13_lane_1.dath"),
		.C_LANE_GAMMA_FILE("artifacts/group_13_lane_2.dath"),
		.C_LANE_DELTA_FILE("artifacts/group_13_lane_3.dath")
	)road_yolo_numeric_rom_group_Inst_xi(
		.i_clk(i_clk),
		.i_rstn(i_rstn),
		.i_word_addr(word_addr_reg),
		.o_word_data(group_xi_data)
	);

endmodule
