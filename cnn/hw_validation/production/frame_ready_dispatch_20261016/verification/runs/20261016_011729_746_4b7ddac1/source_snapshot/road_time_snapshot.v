`timescale 1ns / 1ps

// Company: RoadYOLO project
// Engineer: Codex
// Create Date: 2026/10/15
// Design Name: Independent millisecond snapshot
// Module Name: road_time_snapshot
// Description: Frozen epoch/time payload with request and acknowledgement
// Simulations: tests/tb_road_time_snapshot.v
// Referrences: reference/contract.json
// Dependencies: Shared 100MHz and template 75MHz clocks
// Version: V1.0
// Revision Date: 2026/10/15
// History: 2026/10/15 V1.0 Codex Create file
// 版权归属: RoadYOLO project
// 开发人员: Codex
// 创建日期: 2026年10月15日
// 设计名称: 独立毫秒时间快照
// 模块名称: road_time_snapshot
// 模块说明: 源时间载荷冻结至目标稳定捕获确认
// 仿真工程: tests/tb_road_time_snapshot.v
// 参考资料: reference/contract.json
// 依赖文件: 同一PLL配置的计算与HDMI时钟
// 当前版本: V1.0
// 修订日期: 2026年10月15日
// 修订历史: 2026年10月15日 V1.0 Codex 创建文件
module road_time_snapshot
(
	input i_src_clk,                         // 同源100MHz时间时钟
	input i_dst_clk,                         // 模板75MHz显示时钟
	input i_rstn,                            // 两域共同取消复位
	input [31:0]i_src_epoch,                 // 共同复位之间保持的代次
	output [63:0]o_src_now_ms,               // 给摄像头与计算侧使用的唯一时间
	output o_src_tick,                       // 每100000个本域有效时钟一拍
	output o_src_busy,                       // 冻结快照尚未收到确认
	output [63:0]o_dst_now_ms,               // 安全捕获的时间快照
	output [31:0]o_dst_epoch,                // 与时间同时捕获的代次
	output o_dst_time_valid,                 // 首次更新后且未失联才有效
	output o_dst_update                      // 本拍接收完整新时间快照
);
	//---------------计数信号---------------//
	reg [16:0]cnt_source_tick = 0;           // 100MHz下累计零至99999
	reg [17:0]cnt_snapshot_silence = 0;      // 目标域累计距上次更新的周期

	//--------------寄存器信号--------------//
	(* async_reg = "true" *) reg [1:0]reg_source_release = 0; // 源域复位同步释放
	(* async_reg = "true" *) reg [1:0]reg_destination_release = 0; // 显示域独立同步释放
	reg [95:0]reg_held_snapshot = 0;         // 高64时间、低32代次，确认前冻结

	//---------------标志信号---------------//
	reg flag_request_toggle = 0;            // 每次完整时间快照翻转一次
	(* async_reg = "true" *) reg flag_ack_meta = 0; // 返回确认的首级隔离寄存器
	(* async_reg = "true" *) reg flag_ack_sync = 0; // 源域使用的第二级确认
	(* async_reg = "true" *) reg flag_request_meta = 0; // 请求进入显示域的首级
	(* async_reg = "true" *) reg flag_request_sync = 0; // 请求的第二级稳定观察
	reg flag_request_seen = 0;              // 已启动稳定捕获的请求代次
	reg flag_capture_pending = 0;           // 多等一拍再采样冻结时间总线
	reg flag_ack_toggle = 0;                // 捕获完成才回送的确认代次
	wire flag_source_tick;                  // 终值判定，不依赖异域信号
	wire flag_source_busy;                  // 请求与同步确认不一致
	wire flag_publish;                      // 本毫秒机会能建立新冻结快照
	wire flag_new_request;                  // 目标域观察到尚未捕获的请求

	//---------------其他信号---------------//
	wire source_rstn;                       // 异步断言且源域同步释放的功能复位
	wire destination_rstn;                  // 异步断言且目标域同步释放的功能复位

	//---------------输出信号---------------//
	reg [63:0]src_now_ms_o = 0;             // 源域绝对毫秒计数器
	reg src_tick_o = 0;                     // 当前毫秒递增事件
	reg [63:0]dst_now_ms_o = 0;             // 目标域已确认的冻结时间值
	reg [31:0]dst_epoch_o = 0;              // 对应时间值的复位代次
	reg dst_time_valid_o = 0;               // 时间新鲜性许可
	reg dst_update_o = 0;                   // 目标捕获完成脉冲

	//-------------其他信号连线-------------//
	assign source_rstn = reg_source_release[1]; // 下游只使用同步释放的复位
	assign destination_rstn = reg_destination_release[1]; // 不共享同步器首级
	assign flag_source_tick = (cnt_source_tick == 17'd99999); // 精确一毫秒分频终值
	assign flag_source_busy = (flag_request_toggle != flag_ack_sync); // 确认前禁止覆写
	assign flag_publish = flag_source_tick && !flag_source_busy; // 忙时跳过本次发布机会
	assign flag_new_request = (flag_request_sync != flag_request_seen); // 一个请求仅捕获一次

	//-------------输出信号连线-------------//
	assign o_src_now_ms = src_now_ms_o;      // 导出同源绝对时间
	assign o_src_tick = src_tick_o;          // 导出毫秒机会脉冲
	assign o_src_busy = flag_source_busy;    // 导出时间握手占用而非表占用
	assign o_dst_now_ms = dst_now_ms_o;      // 导出本域稳定快照
	assign o_dst_epoch = dst_epoch_o;        // 导出原子捕获代次
	assign o_dst_time_valid = dst_time_valid_o; // 失联后撤销绘制许可
	assign o_dst_update = dst_update_o;      // 导出本拍完整时间更新事件

	//-----------输出信号处理区域-----------//
	// 时间递增不被请求确认或框表复制反压停住。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			src_now_ms_o <= 64'd0;
		end else if(flag_source_tick)begin
			src_now_ms_o <= src_now_ms_o + 64'd1;
		end
	end

	// 同域消费者可用这一拍记录毫秒边界，时间载荷用递增后的值。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			src_tick_o <= 1'b0;
		end else begin
			src_tick_o <= flag_source_tick;
		end
	end

	// 仅在额外稳定等待拍后读取高64位，绝非动态总线两级同步。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			dst_now_ms_o <= 64'd0;
		end else if(flag_capture_pending)begin
			dst_now_ms_o <= reg_held_snapshot[95:32];
		end
	end

	// 代次与时间同拍来自同一个源端冻结载荷。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			dst_epoch_o <= 32'd0;
		end else if(flag_capture_pending)begin
			dst_epoch_o <= reg_held_snapshot[31:0];
		end
	end

	// 首次捕获才有效，经过150001个无更新像素拍后失效。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			dst_time_valid_o <= 1'b0;
		end else if(flag_capture_pending)begin
			dst_time_valid_o <= 1'b1;
		end else if(cnt_snapshot_silence >= 18'd150000)begin
			dst_time_valid_o <= 1'b0;
		end
	end

	// 完整捕获事件供看门狗与集成计数，正常持续一像素拍。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			dst_update_o <= 1'b0;
		end else begin
			dst_update_o <= flag_capture_pending;
		end
	end

	//-----------主要任务处理区域-----------//
	// 原始共同复位异步清零，源域两个上升沿后才允许功能启动。
	always@(posedge i_src_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_source_release <= 2'b00;
		end else begin
			reg_source_release <= {reg_source_release[0], 1'b1};
		end
	end

	// 显示域独立释放，同一原始复位同时取消两条握手链。
	always@(posedge i_dst_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_destination_release <= 2'b00;
		end else begin
			reg_destination_release <= {reg_destination_release[0], 1'b1};
		end
	end

	// 毫秒计数器只在终值回零，不受跨域忙信号影响。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			cnt_source_tick <= 17'd0;
		end else if(flag_source_tick)begin
			cnt_source_tick <= 17'd0;
		end else begin
			cnt_source_tick <= cnt_source_tick + 17'd1;
		end
	end

	// 包含代次的96位快照保持到同步确认，表pending满不影响它。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			reg_held_snapshot <= 96'd0;
		end else if(flag_publish)begin
			reg_held_snapshot <= {src_now_ms_o + 64'd1, i_src_epoch};
		end
	end

	// 发布与快照写入同一源时钟，目标还将经历同步和稳定等待。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			flag_request_toggle <= 1'b0;
		end else if(flag_publish)begin
			flag_request_toggle <= !flag_request_toggle;
		end
	end

	// 确认首级仅进入同步器，不分发到功能逻辑。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			flag_ack_meta <= 1'b0;
		end else begin
			flag_ack_meta <= flag_ack_toggle;
		end
	end

	// 第二级确认解除源端payload保持要求。
	always@(posedge i_src_clk or negedge source_rstn)begin
		if(!source_rstn)begin
			flag_ack_sync <= 1'b0;
		end else begin
			flag_ack_sync <= flag_ack_meta;
		end
	end

	// 请求首级只驱动下一级，避免亚稳态首级扇出。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			flag_request_meta <= 1'b0;
		end else begin
			flag_request_meta <= flag_request_toggle;
		end
	end

	// 目标功能仅观察第二级请求代次。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			flag_request_sync <= 1'b0;
		end else begin
			flag_request_sync <= flag_request_meta;
		end
	end

	// 记录已观察代次，使同一冻结请求不会重复捕获。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			flag_request_seen <= 1'b0;
		end else if(flag_new_request)begin
			flag_request_seen <= flag_request_sync;
		end
	end

	// 同步请求出现后再稳定等待一个完整目标周期。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			flag_capture_pending <= 1'b0;
		end else begin
			flag_capture_pending <= flag_new_request;
		end
	end

	// 捕获目标寄存器的同拍才确认，不能提前释放源载荷。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			flag_ack_toggle <= 1'b0;
		end else if(flag_capture_pending)begin
			flag_ack_toggle <= flag_request_seen;
		end
	end

	// 以目标本地周期判定失联，饱和后不回绕伪装新鲜时间。
	always@(posedge i_dst_clk or negedge destination_rstn)begin
		if(!destination_rstn)begin
			cnt_snapshot_silence <= 18'd0;
		end else if(flag_capture_pending)begin
			cnt_snapshot_silence <= 18'd0;
		end else if(cnt_snapshot_silence < 18'd150001)begin
			cnt_snapshot_silence <= cnt_snapshot_silence + 18'd1;
		end
	end
endmodule
