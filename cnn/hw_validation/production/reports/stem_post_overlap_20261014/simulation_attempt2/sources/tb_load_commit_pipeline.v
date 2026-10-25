`timescale 1ns / 1ps

// 候选与冻结原版锁步；仅目标RAM允许存在一个已接收、尚未提交的差异。
module tb_load_commit_pipeline(output reg o_test_done);
	reg clk=1'b0;
	reg rstn=1'b0;
	reg table_loaded=1'b1;
	reg stem_load_valid=1'b0;
	reg [2:0]stem_load_kind=3'd0;
	reg [8:0]stem_load_addr=9'd0;
	reg signed [31:0]stem_load_data=32'sd0;
	reg stem_start=1'b0;
	reg down_load_valid=1'b0;
	reg [2:0]down_load_kind=3'd0;
	reg [10:0]down_load_addr=11'd0;
	reg signed [31:0]down_load_data=32'sd0;
	reg down_start=1'b0;
	wire stem_ready, stem_busy, stem_done, stem_fault, stem_mac_valid;
	wire old_stem_ready, old_stem_busy, old_stem_done, old_stem_fault, old_stem_mac_valid;
	wire [63:0]stem_mac_activation, old_stem_mac_activation;
	wire [191:0]stem_mac_weight, old_stem_mac_weight;
	wire [95:0]stem_mac_bias, old_stem_mac_bias;
	wire [7:0]stem_mac_mask, old_stem_mac_mask;
	wire down_ready, down_busy, down_done, down_fault, down_mac_valid;
	wire old_down_ready, old_down_busy, old_down_done, old_down_fault, old_down_mac_valid;
	wire [63:0]down_mac_activation, old_down_mac_activation;
	wire [191:0]down_mac_weight, old_down_mac_weight;
	wire [95:0]down_mac_bias, old_down_mac_bias;
	wire [7:0]down_mac_mask, old_down_mac_mask;
	reg signed [7:0]stem_expected[0:431];
	reg signed [7:0]down_expected[0:1295];
	reg stem_expected_valid[0:431];
	reg down_expected_valid[0:1295];
	reg stem_pending_model=1'b0;
	reg [8:0]stem_pending_address=9'd0;
	reg signed [7:0]stem_pending_data=8'sd0;
	reg down_pending_model=1'b0;
	reg [10:0]down_pending_address=11'd0;
	reg signed [7:0]down_pending_data=8'sd0;
	integer index;
	integer compare_index;
	integer checks=0;
	integer stem_accepts=0;
	integer down_accepts=0;
	time phase_start_time;
	reg stem_queue_expected;
	reg down_queue_expected;

	always #5 clk=~clk;

	road_stem_tile_scheduler stem(
		.i_clk(clk),.i_rstn(rstn),.i_table_loaded(table_loaded),
		.i_load_valid(stem_load_valid),.i_load_kind(stem_load_kind),
		.i_load_addr(stem_load_addr),.i_load_data(stem_load_data),.o_load_ready(stem_ready),
		.i_start(stem_start),.o_busy(stem_busy),.o_done(stem_done),.o_fault(stem_fault),
		.i_mac_ready(1'b0),.o_mac_valid(stem_mac_valid),.o_mac_mask(stem_mac_mask),
		.o_mac_activation(stem_mac_activation),.o_mac_weight(stem_mac_weight),.o_mac_bias(stem_mac_bias),
		.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
		.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),
		.i_pp_int16(1'b0),.i_pp_fault(1'b0),.i_commit_ready(1'b1),
		.i_export_start(1'b0),.i_output_ready(1'b1));

	reference_road_stem_tile_scheduler old_stem(
		.i_clk(clk),.i_rstn(rstn),.i_table_loaded(table_loaded),
		.i_load_valid(stem_load_valid),.i_load_kind(stem_load_kind),
		.i_load_addr(stem_load_addr),.i_load_data(stem_load_data),.o_load_ready(old_stem_ready),
		.i_start(stem_start),.o_busy(old_stem_busy),.o_done(old_stem_done),.o_fault(old_stem_fault),
		.i_mac_ready(1'b0),.o_mac_valid(old_stem_mac_valid),.o_mac_mask(old_stem_mac_mask),
		.o_mac_activation(old_stem_mac_activation),.o_mac_weight(old_stem_mac_weight),.o_mac_bias(old_stem_mac_bias),
		.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
		.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),
		.i_pp_int16(1'b0),.i_pp_fault(1'b0),.i_commit_ready(1'b1),
		.i_export_start(1'b0),.i_output_ready(1'b1));

	road_down2_tile_scheduler down(
		.i_clk(clk),.i_rstn(rstn),.i_table_loaded(table_loaded),
		.i_load_valid(down_load_valid),.i_load_kind(down_load_kind),
		.i_load_addr(down_load_addr),.i_load_data(down_load_data),.o_load_ready(down_ready),
		.i_start(down_start),.i_pw_only(1'b0),.i_commit_ready(1'b1),
		.o_busy(down_busy),.o_done(down_done),.o_fault(down_fault),
		.i_export_start(1'b0),.i_output_ready(1'b1),
		.i_mac_ready(1'b0),.o_mac_valid(down_mac_valid),.o_mac_mask(down_mac_mask),
		.o_mac_activation(down_mac_activation),.o_mac_weight(down_mac_weight),.o_mac_bias(down_mac_bias),
		.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
		.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),
		.i_pp_int16(1'b0),.i_pp_fault(1'b0),.i_pp_result_queue_count(2'd0),.i_pp_meta_count(4'd0),
		.i_pp_pre_busy(1'b0),.i_pp_silu_busy(1'b0),.i_pp_post_busy(1'b0),
		.i_pp_pre_accept(1'b0),.i_pp_silu_accept(1'b0),.i_pp_post_accept(1'b0));

	reference_road_down2_tile_scheduler old_down(
		.i_clk(clk),.i_rstn(rstn),.i_table_loaded(table_loaded),
		.i_load_valid(down_load_valid),.i_load_kind(down_load_kind),
		.i_load_addr(down_load_addr),.i_load_data(down_load_data),.o_load_ready(old_down_ready),
		.i_start(down_start),.i_pw_only(1'b0),.i_commit_ready(1'b1),
		.o_busy(old_down_busy),.o_done(old_down_done),.o_fault(old_down_fault),
		.i_export_start(1'b0),.i_output_ready(1'b1),
		.i_mac_ready(1'b0),.o_mac_valid(old_down_mac_valid),.o_mac_mask(old_down_mac_mask),
		.o_mac_activation(old_down_mac_activation),.o_mac_weight(old_down_mac_weight),.o_mac_bias(old_down_mac_bias),
		.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
		.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),
		.i_pp_int16(1'b0),.i_pp_fault(1'b0),.i_pp_result_queue_count(2'd0),.i_pp_meta_count(4'd0),
		.i_pp_pre_busy(1'b0),.i_pp_silu_busy(1'b0),.i_pp_post_busy(1'b0),
		.i_pp_pre_accept(1'b0),.i_pp_silu_accept(1'b0),.i_pp_post_accept(1'b0));

	// 接收沿后比较控制；RAM由软件pending模型检查，未写地址从不读取。
	always @(posedge clk)begin
		stem_queue_expected=stem_load_valid && stem_ready && old_stem.flag_load_legal &&
		                    (stem_load_kind==3'd2);
		down_queue_expected=down.flag_halo_load_write;
		if(stem_load_valid && stem_ready) stem_accepts=stem_accepts+1;
		if(down_load_valid && down_ready) down_accepts=down_accepts+1;
		#1;
		if({stem_ready,stem_busy,stem_done,stem_fault,stem.state_current,stem.flag_load_state_ready,
		    stem.reg_loaded,stem.cnt_halo_address,stem.cnt_weight_address,stem.cnt_bias_address,
		    stem.cnt_multiplier_address,stem.cnt_shift_address,stem.flag_post_address} !==
		   {old_stem_ready,old_stem_busy,old_stem_done,old_stem_fault,old_stem.state_current,
		    old_stem.flag_load_state_ready,old_stem.reg_loaded,old_stem.cnt_halo_address,
		    old_stem.cnt_weight_address,old_stem.cnt_bias_address,old_stem.cnt_multiplier_address,
		    old_stem.cnt_shift_address,old_stem.flag_post_address})
			$fatal(1,"Stem control/metadata changed at %0t",$time);
		if({down_ready,down_busy,down_done,down_fault,down.state_current,down.cnt_preload_writes,
		    down.cnt_expected_halo,down.cnt_expected_dw_cache,down.cnt_expected_dw_weight,
		    down.cnt_expected_dw_bias,down.cnt_expected_pw_weight,down.cnt_expected_pw_bias,
		    down.flag_halo_loaded,down.flag_dw_cache_loaded,down.flag_dw_weight_loaded,
		    down.flag_dw_bias_loaded,down.flag_pw_weight_loaded,down.flag_pw_bias_loaded,
		    down.cnt_expected_multiplier,down.cnt_expected_control,down.flag_multiplier_loaded,
		    down.flag_control_loaded} !==
		   {old_down_ready,old_down_busy,old_down_done,old_down_fault,old_down.state_current,
		    old_down.cnt_preload_writes,old_down.cnt_expected_halo,old_down.cnt_expected_dw_cache,
		    old_down.cnt_expected_dw_weight,old_down.cnt_expected_dw_bias,
		    old_down.cnt_expected_pw_weight,old_down.cnt_expected_pw_bias,
		    old_down.flag_halo_loaded,old_down.flag_dw_cache_loaded,old_down.flag_dw_weight_loaded,
		    old_down.flag_dw_bias_loaded,old_down.flag_pw_weight_loaded,old_down.flag_pw_bias_loaded,
		    old_down.cnt_expected_multiplier,old_down.cnt_expected_control,
		    old_down.flag_multiplier_loaded,old_down.flag_control_loaded})
			$fatal(1,"Down2 control/metadata changed at %0t",$time);
		if({stem_mac_valid,stem_mac_mask,stem_mac_activation,stem_mac_weight,stem_mac_bias} !==
		   {old_stem_mac_valid,old_stem_mac_mask,old_stem_mac_activation,old_stem_mac_weight,old_stem_mac_bias})
			$fatal(1,"Stem first/read datapath changed at %0t",$time);
		if({down_mac_valid,down_mac_mask,down_mac_activation,down_mac_weight,down_mac_bias} !==
		   {old_down_mac_valid,old_down_mac_mask,old_down_mac_activation,old_down_mac_weight,old_down_mac_bias})
			$fatal(1,"Down2 first/read datapath changed at %0t",$time);
		if(rstn)begin
			if(stem.flag_weight_write_pending !== stem_queue_expected)
				$fatal(1,"Stem pending flag changed at %0t",$time);
			if(down.flag_halo_write_pending !== down_queue_expected)
				$fatal(1,"Down2 pending flag changed at %0t",$time);
			if(stem_pending_model)begin
				stem_expected[stem_pending_address]=stem_pending_data;
				stem_expected_valid[stem_pending_address]=1'b1;
			end
			if(down_pending_model)begin
				down_expected[down_pending_address]=down_pending_data;
				down_expected_valid[down_pending_address]=1'b1;
			end
			if(stem_queue_expected)begin
				if(stem.reg_weight_write_address!==stem_load_addr ||
				   stem.reg_weight_write_data!==stem_load_data[7:0])
					$fatal(1,"Stem queued payload changed");
				stem_pending_address=stem_load_addr;
				stem_pending_data=stem_load_data[7:0];
			end
			if(down_queue_expected)begin
				if(down.reg_halo_write_address!==down_load_addr ||
				   down.reg_halo_write_data!==down_load_data[7:0])
					$fatal(1,"Down2 queued payload changed");
				down_pending_address=down_load_addr;
				down_pending_data=down_load_data[7:0];
			end
			stem_pending_model=stem_queue_expected;
			down_pending_model=down_queue_expected;
			for(compare_index=0;compare_index<432;compare_index=compare_index+1)begin
				if(stem_expected_valid[compare_index] && stem.reg_weight[compare_index]!==stem_expected[compare_index])
					$fatal(1,"Stem committed RAM mismatch address=%0d",compare_index);
			end
			for(compare_index=0;compare_index<1296;compare_index=compare_index+1)begin
				if(down_expected_valid[compare_index] && down.reg_halo[compare_index]!==down_expected[compare_index])
					$fatal(1,"Down2 committed RAM mismatch address=%0d",compare_index);
			end
		end else begin
			stem_pending_model=1'b0;
			down_pending_model=1'b0;
			if(stem.flag_weight_write_pending || down.flag_halo_write_pending)
				$fatal(1,"Reset did not cancel pending write");
		end
	end

	task reset_all;
		begin
			@(negedge clk);stem_load_valid=0;down_load_valid=0;stem_start=0;down_start=0;
			#2;rstn=0;stem_pending_model=0;down_pending_model=0;
			repeat(2) @(negedge clk);
			rstn=1;
		end
	endtask

	task stem_send;
		input [2:0]kind;
		input [8:0]address;
		input signed [31:0]data;
		begin
			stem_load_kind=kind;stem_load_addr=address;stem_load_data=data;stem_load_valid=1;
			#1;if(!stem_ready) $fatal(1,"Stem legal stream lost ready address=%0d",address);
			@(posedge clk);#2;if(stem_fault) $fatal(1,"Stem legal stream fault address=%0d",address);
			@(negedge clk);stem_load_valid=0;
		end
	endtask

	task down_send;
		input [2:0]kind;
		input [10:0]address;
		input signed [31:0]data;
		begin
			down_load_kind=kind;down_load_addr=address;down_load_data=data;down_load_valid=1;
			#1;if(!down_ready) $fatal(1,"Down2 legal stream lost ready address=%0d",address);
			@(posedge clk);#2;if(down_fault) $fatal(1,"Down2 legal stream fault address=%0d",address);
			@(negedge clk);down_load_valid=0;
		end
	endtask

	task load_stem_support;
		begin
			for(index=0;index<243;index=index+1) stem_send(3'd0,index,(index*29)%256);
			for(index=0;index<16;index=index+1) stem_send(3'd3,index,index-8);
			for(index=0;index<16;index=index+1) stem_send(3'd4,index,index+1);
			for(index=0;index<16;index=index+1) stem_send(3'd5,index,index%13);
			stem_send(3'd6,0,3);stem_send(3'd6,1,4);
		end
	endtask

	task load_down_support;
		begin
			for(index=0;index<144;index=index+1) down_send(3'd2,index,((index*17)%256)-128);
			for(index=0;index<16;index=index+1) down_send(3'd3,index,index-8);
			for(index=0;index<384;index=index+1) down_send(3'd4,index,((index*11)%256)-128);
			for(index=0;index<24;index=index+1) down_send(3'd5,index,index-12);
			for(index=0;index<40;index=index+1) down_send(3'd6,index,index+1);
			for(index=0;index<40;index=index+1) down_send(3'd7,index,index%13);
			down_send(3'd7,40,3);down_send(3'd7,41,5);down_send(3'd7,42,4);down_send(3'd7,43,6);
		end
	endtask

	task check_complete_memories;
		begin
			if(stem_pending_model || down_pending_model) $fatal(1,"Memory checked before pending drain");
			for(index=0;index<432;index=index+1)begin
				if(!stem_expected_valid[index] || stem.reg_weight[index]!==old_stem.reg_weight[index])
					$fatal(1,"Stem exhaustive mismatch address=%0d",index);
				checks=checks+1;
			end
			for(index=0;index<1296;index=index+1)begin
				if(!down_expected_valid[index] || down.reg_halo[index]!==old_down.reg_halo[index])
					$fatal(1,"Down2 exhaustive mismatch address=%0d",index);
				checks=checks+1;
			end
		end
	endtask

	initial begin
		o_test_done=1'b0;
		for(index=0;index<432;index=index+1) stem_expected_valid[index]=1'b0;
		for(index=0;index<1296;index=index+1) down_expected_valid[index]=1'b0;
		reset_all();

		// 连续II1与signed数据；最后权重pending和start同沿提交，下一沿才读取RAM。
		load_stem_support();
		phase_start_time=$time;
		for(index=0;index<432;index=index+1) stem_send(3'd2,index,((index*73+19)%256)-128);
		if($time-phase_start_time!=4320) $fatal(1,"Stem continuous load was not II1");
		stem_start=1;
		@(posedge clk);#2;
		if(!stem_busy || stem.state_current!==4'd1 || stem.flag_weight_write_pending)
			$fatal(1,"Stem last-commit/start boundary changed busy=%b state=%0d pending=%b loaded=%b fault=%b",
			       stem_busy,stem.state_current,stem.flag_weight_write_pending,stem.reg_loaded,stem_fault);
		@(negedge clk);stem_start=0;
		@(posedge clk);#2;
		if(!stem_mac_valid || ^stem_mac_weight===1'bx || ^stem_mac_activation===1'bx)
			$fatal(1,"Stem first real read invalid");

		reset_all();
		load_down_support();
		phase_start_time=$time;
		for(index=0;index<1296;index=index+1) down_send(3'd0,index,((index*47+23)%256)-128);
		if($time-phase_start_time!=12960) $fatal(1,"Down2 continuous load was not II1");
		down_start=1;
		@(posedge clk);#2;
		if(!down_busy || down.state_current!==4'd1 || down.flag_halo_write_pending)
			$fatal(1,"Down2 last-commit/start boundary changed busy=%b state=%0d pending=%b loaded=%b fault=%b",
			       down_busy,down.state_current,down.flag_halo_write_pending,down.flag_halo_loaded,down_fault);
		@(negedge clk);down_start=0;
		@(posedge clk);#2;
		if(!down_mac_valid || ^down_mac_activation===1'bx || ^down_mac_weight===1'bx)
			$fatal(1,"Down2 first real read invalid");

		reset_all();
		// 带气泡重装目标RAM，并在最后提交后逐字节穷举。
		for(index=0;index<1296;index=index+1)begin
			if(index<432) stem_send(3'd2,index,((index*31+7)%256)-128);
			down_send(3'd0,index,((index*59+3)%256)-128);
			if(index%17==5)begin
				stem_load_valid=0;down_load_valid=0;repeat((index%3)+1) @(negedge clk);
			end
		end
		@(posedge clk);#2;
		check_complete_memories();

		// 地址零重启后乱序；前一个合法pending必须在新非法项故障沿提交。
		reset_all();
		@(negedge clk);stem_load_valid=1;stem_load_kind=3'd2;stem_load_addr=0;stem_load_data=-17;
		down_load_valid=1;down_load_kind=3'd0;down_load_addr=0;down_load_data=-29;
		@(posedge clk);#2;
		@(negedge clk);stem_load_addr=2;stem_load_data=91;down_load_addr=2;down_load_data=83;
		@(posedge clk);#2;
		if(!stem_fault || !down_fault || stem.flag_weight_write_pending || down.flag_halo_write_pending)
			$fatal(1,"Invalid sequence boundary changed");
		if(stem.reg_weight[0]!==-8'sd17 || down.reg_halo[0]!==-8'sd29)
			$fatal(1,"Prior legal pending did not commit before fault");

		// fresh reset后的末地址非法，不能产生pending或写入。
		reset_all();
		@(negedge clk);stem_load_valid=1;stem_load_kind=3'd2;stem_load_addr=431;stem_load_data=77;
		down_load_valid=1;down_load_kind=3'd0;down_load_addr=1295;down_load_data=66;
		@(posedge clk);#2;
		if(!stem_fault || !down_fault || stem.flag_weight_write_pending || down.flag_halo_write_pending)
			$fatal(1,"Fresh-reset final address was accepted");

		// 已入队但未提交时异步复位；候选保留旧RAM，原版已写的新值不参与等值断言。
		reset_all();
		@(negedge clk);stem_load_valid=1;stem_load_kind=3'd2;stem_load_addr=0;stem_load_data=-99;
		down_load_valid=1;down_load_kind=3'd0;down_load_addr=0;down_load_data=-101;
		@(posedge clk);#2;
		if(!stem.flag_weight_write_pending || !down.flag_halo_write_pending)
			$fatal(1,"Reset case did not queue target writes");
		@(negedge clk);stem_load_valid=0;down_load_valid=0;#2;rstn=0;
		stem_pending_model=0;down_pending_model=0;#1;
		if(stem.reg_weight[0]===-8'sd99 || down.reg_halo[0]===-8'sd101)
			$fatal(1,"Cancelled pending write reached candidate RAM");
		repeat(2) @(posedge clk);#2;
		if(stem.flag_weight_write_pending || down.flag_halo_write_pending)
			$fatal(1,"Cancelled pending write leaked after reset");

		// 完整重装后检查start与valid的旧优先级：Stem两者都拒绝，down2接受start但拒绝load。
		@(negedge clk);rstn=1;
		load_stem_support();
		for(index=0;index<432;index=index+1) stem_send(3'd2,index,((index*13+1)%256)-128);
		@(posedge clk);#2;
		load_down_support();
		for(index=0;index<1296;index=index+1) down_send(3'd0,index,((index*7+9)%256)-128);
		@(posedge clk);#2;
		@(negedge clk);stem_load_valid=1;stem_load_kind=3'd2;stem_load_addr=0;stem_load_data=12;stem_start=1;
		down_load_valid=1;down_load_kind=3'd0;down_load_addr=0;down_load_data=13;down_start=1;
		#1;if(stem_ready || down_ready) $fatal(1,"start did not retain priority over load ready");
		@(posedge clk);#2;
		if(stem_busy || stem.state_current!==4'd0) $fatal(1,"Stem start+valid priority changed");
		if(!down_busy || down.state_current!==4'd1) $fatal(1,"Down2 one-cycle start pulse lost");
		@(negedge clk);stem_load_valid=0;down_load_valid=0;stem_start=1;down_start=0;
		@(posedge clk);#2;
		if(!stem_busy || stem.state_current!==4'd1) $fatal(1,"Stem one-cycle start pulse lost");
		@(negedge clk);stem_start=0;

		if(stem_accepts!=1886 || down_accepts!=5196)
			$fatal(1,"Accepted record count changed stem=%0d down2=%0d",stem_accepts,down_accepts);
		o_test_done=1'b1;
		$display("TB_PASS_LOAD_COMMIT checks=%0d stem_accepts=%0d down_accepts=%0d",checks,stem_accepts,down_accepts);
		$finish;
	end

	initial begin
		#5000000;$fatal(1,"Load commit comparison timeout");
	end
endmodule
