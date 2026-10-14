`timescale 1ns / 1ps

// 原源与候选同输入锁步；逐沿比较全部目标存储及完成/故障/许可。
module tb_load_bank_equivalence(output o_test_done);
	reg clk=0;
	reg rstn=0;
	reg stem_valid=0, halo_valid=0;
	reg [2:0]stem_kind=3'd2;
	reg [8:0]stem_addr=0;
	reg [10:0]halo_addr=0;
	reg signed [31:0]load_data=0;
	reg done_o=0;
	wire stem_ready, old_stem_ready, stem_fault, old_stem_fault;
	wire halo_ready, old_halo_ready, halo_fault, old_halo_fault;
	integer index, sample, pass, checks=0, accepted_stem=0, accepted_halo=0;
	assign o_test_done=done_o;
	always #5 clk=~clk;

	road_stem_tile_scheduler stem(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b1),
		.i_load_valid(stem_valid),.i_load_kind(stem_kind),.i_load_addr(stem_addr),.i_load_data(load_data),
		.o_load_ready(stem_ready),.o_fault(stem_fault),.i_start(1'b0),
		.i_mac_ready(1'b0),.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
		.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),
		.i_commit_ready(1'b1),.i_export_start(1'b0),.i_output_ready(1'b1));
	reference_stem_tile_scheduler old_stem(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b1),
		.i_load_valid(stem_valid),.i_load_kind(stem_kind),.i_load_addr(stem_addr),.i_load_data(load_data),
		.o_load_ready(old_stem_ready),.o_fault(old_stem_fault),.i_start(1'b0),
		.i_mac_ready(1'b0),.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
		.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),
		.i_commit_ready(1'b1),.i_export_start(1'b0),.i_output_ready(1'b1));
	road_down2_tile_scheduler halo(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b0),
		.i_load_valid(halo_valid),.i_load_kind(3'd0),.i_load_addr(halo_addr),.i_load_data(load_data),
		.o_load_ready(halo_ready),.o_fault(halo_fault),.i_start(1'b0),.i_pw_only(1'b0),.i_commit_ready(1'b1),
		.i_export_start(1'b0),.i_output_ready(1'b1),.i_mac_ready(1'b0),.i_mac_result_valid(1'b0),
		.i_mac_result(96'd0),.i_mac_fault(1'b0),.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),
		.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),.i_pp_result_queue_count(2'd0),.i_pp_meta_count(4'd0),
		.i_pp_pre_busy(1'b0),.i_pp_silu_busy(1'b0),.i_pp_post_busy(1'b0),
		.i_pp_pre_accept(1'b0),.i_pp_silu_accept(1'b0),.i_pp_post_accept(1'b0));
	reference_down2_tile_scheduler old_halo(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b0),
		.i_load_valid(halo_valid),.i_load_kind(3'd0),.i_load_addr(halo_addr),.i_load_data(load_data),
		.o_load_ready(old_halo_ready),.o_fault(old_halo_fault),.i_start(1'b0),.i_pw_only(1'b0),.i_commit_ready(1'b1),
		.i_export_start(1'b0),.i_output_ready(1'b1),.i_mac_ready(1'b0),.i_mac_result_valid(1'b0),
		.i_mac_result(96'd0),.i_mac_fault(1'b0),.i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),
		.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),.i_pp_result_queue_count(2'd0),.i_pp_meta_count(4'd0),
		.i_pp_pre_busy(1'b0),.i_pp_silu_busy(1'b0),.i_pp_post_busy(1'b0),
		.i_pp_pre_accept(1'b0),.i_pp_silu_accept(1'b0),.i_pp_post_accept(1'b0));

	// NBA写入后比较X/已知值，任何旁路写、延后写或旧事务泄漏均可见。
	always @(posedge clk)begin
		if(rstn && stem_valid && stem_ready) accepted_stem=accepted_stem+1;
		if(rstn && halo_valid && halo_ready) accepted_halo=accepted_halo+1;
		#1;
		if({stem_ready,stem_fault,stem.reg_loaded,stem.cnt_weight_address} !==
		   {old_stem_ready,old_stem_fault,old_stem.reg_loaded,old_stem.cnt_weight_address})
			$fatal(1,"Stem loader interface/metadata changed");
		if({halo_ready,halo_fault,halo.flag_halo_loaded,halo.cnt_expected_halo,halo.cnt_preload_writes} !==
		   {old_halo_ready,old_halo_fault,old_halo.flag_halo_loaded,old_halo.cnt_expected_halo,old_halo.cnt_preload_writes})
			$fatal(1,"Halo loader interface/metadata changed");
		for(sample=0;sample<432;sample=sample+1)begin
			if(stem.reg_weight[sample] !== old_stem.reg_weight[sample]) $fatal(1,"Stem memory mismatch %0d",sample);
			checks=checks+1;
		end
		for(sample=0;sample<1296;sample=sample+1)begin
			if(halo.reg_halo[sample] !== old_halo.reg_halo[sample]) $fatal(1,"Halo memory mismatch %0d",sample);
			checks=checks+1;
		end
	end

	// 复位在非时钟沿断言；内容不清空，资格/游标即时取消。
	task cancel;
		begin
			@(negedge clk);#2;rstn=0;#1;
			if(stem_ready || halo_ready) $fatal(1,"Reset failed immediate cancellation");
			repeat(2) @(negedge clk);
			stem_valid=0;halo_valid=0;rstn=1;
		end
	endtask

	initial begin
		cancel();
		for(pass=0;pass<2;pass=pass+1)begin
			for(index=0;index<1296;index=index+1)begin
				@(negedge clk);
				stem_valid=index<432;halo_valid=1;stem_addr=index;halo_addr=index;
				load_data=((index*73+19+pass*11)%256)-128;
				if(!halo_ready || (stem_valid && !stem_ready)) $fatal(1,"Continuous load lost II1");
				@(posedge clk);#2;
				if(stem_fault || halo_fault) $fatal(1,"Legal load faulted");
				if(pass==1 && index%7==3)begin
					@(negedge clk);stem_valid=0;halo_valid=0;repeat(index%3+1) @(negedge clk);
				end
			end
			@(negedge clk);stem_valid=0;halo_valid=0;#2;
			if(!stem.reg_loaded[1] || !halo.flag_halo_loaded || stem.cnt_weight_address!=0 || halo.cnt_expected_halo!=0)
				$fatal(1,"Last write completion edge changed");
			cancel();
		end
		// 原完成态在地址零重启沿清除；随后乱序、越界和非法类型逐一触发粘滞故障。
		for(pass=0;pass<4;pass=pass+1)begin
			@(negedge clk);stem_valid=1;halo_valid=1;stem_kind=2;stem_addr=0;halo_addr=0;load_data=7;
			@(posedge clk);#2;
			if(stem.cnt_weight_address!=1 || halo.cnt_expected_halo!=1) $fatal(1,"Address-zero restart changed");
			@(negedge clk);
			case(pass)
				0:begin stem_addr=432;halo_addr=1296;end
				1:begin stem_addr=2;halo_addr=2;end
				2:begin stem_kind=7;halo_addr=1296;end
				3:begin stem_addr=1;load_data=128;halo_addr=1296;end
			endcase
			@(posedge clk);#2;
			if(!stem_fault || !halo_fault || stem_ready || halo_ready) $fatal(1,"Illegal record fault edge changed");
			repeat(3) @(negedge clk);
			cancel();stem_kind=2;
		end
		// 装载未完时复位，保持的valid不能泄漏成恢复后的旧地址写。
		@(negedge clk);stem_valid=1;halo_valid=1;stem_addr=0;halo_addr=0;load_data=-3;
		@(posedge clk);#2;cancel();
		@(negedge clk);stem_valid=1;halo_valid=1;stem_addr=0;halo_addr=0;load_data=-9;
		@(posedge clk);#2;
		if(stem.reg_weight[0]!==8'hf7 || halo.reg_halo[0]!==8'hf7) $fatal(1,"Recovery write mismatch");
		@(negedge clk);stem_addr=9'bx;halo_addr=11'bx;
		@(posedge clk);#2;cancel();
		repeat(3) @(negedge clk);
		$display("TB_PASS_LOAD_BANK_EQ byte_checks=%0d stem_accepts=%0d halo_accepts=%0d",checks,accepted_stem,accepted_halo);
		done_o=1;$finish;
	end
	initial begin #1000000;$fatal(1,"Load bank comparison timeout");end
endmodule
