`timescale 1ns / 1ps

// Independent 100 MHz regression for the once-only Stem -> DDR -> down2 sequence.
module tb_stem_ddr_sequence;
	localparam [26:0] C_TB_TIMEOUT = 27'd20000;
	localparam integer ST_RUN = 6;
	localparam integer ST_STEM_BYTE = 8;
	localparam integer ST_WRITE = 10;
	localparam integer ST_READ = 16;
	localparam integer ST_HALO_BYTE = 19;
	localparam integer ST_OUTPUT_BYTE = 21;

	reg clk = 1'b0;
	reg rstn = 1'b0;
	reg phy_ready = 1'b0;
	reg ddr_fault = 1'b0;
	reg req_ready = 1'b0;
	reg rsp_valid = 1'b0;
	reg [127:0]rsp_data = 128'd0;
	reg [3:0]rsp_error = 4'd0;
	wire req_valid;
	wire req_write;
	wire [24:0]req_addr;
	wire [127:0]req_data;
	wire rsp_ready;
	wire [1:0]status;
	wire [3:0]error_code;
	wire [4:0]phase;
	wire [6:0]writes;
	wire [6:0]reads;
	wire [8:0]output_bytes;
	wire [31:0]cycles;
	wire [319:0]cycle_bins;
	wire [24:0]address_debug;
	wire [127:0]expected_debug;
	wire [127:0]actual_debug;

	reg [63:0]program [0:4095];
	reg [127:0]stem_golden [0:63];
	reg [31:0]stem_addresses [0:63];
	reg [7:0]halo_map [0:127];
	reg [7:0]pw_golden [0:511];
	reg [31:0]stem_acc [0:1023];
	reg [31:0]dw_acc [0:255];
	reg [31:0]pw_acc [0:383];
	reg [15:0]silu_table [0:1023];
	reg [127:0]endpoint_mem [0:63];
	reg write_seen [0:63];
	reg read_seen [0:63];
	reg output_seen [0:383];
	integer read_order [0:63];

	reg pending = 1'b0;
	reg pending_write = 1'b0;
	reg pending_drop = 1'b0;
	integer pending_slot = 0;
	integer response_delay = 0;
	integer long_wait = 0;
	reg [15:0]random_bits = 16'hace1;
	reg held_request = 1'b0;
	reg [153:0]held_request_payload = 154'd0;
	reg reset_done = 1'b0;
	reg started = 1'b0;
	reg reset_target_seen = 1'b0;
	reg [4095:0]vector_dir;
	reg [4095:0]path;

	integer case_id = 0;
	integer ticks = 0;
	integer i;
	integer j;
	integer slot;
	integer map_index;
	integer lane;
	integer family;
	integer value_index;
	integer channel;
	integer write_requests;
	integer write_responses;
	integer read_requests;
	integer read_responses;
	integer stem_exports;
	integer halo_bytes;
	integer padding_pixels;
	integer final_exports;
	integer accumulator_checks;
	integer pre_checks;
	integer silu_checks;
	integer post_checks;
	integer generation = 0;
	integer sum_bins;
	reg signed [15:0]expected_stage;
	reg signed [15:0]expected_silu;
	reg [30:0]stage_multiplier;
	reg [5:0]stage_shift;
	reg [30:0]post_multiplier;
	reg [5:0]post_shift;
	reg signed [31:0]stage_accumulator;

	always #5 clk = !clk;

	road_stem_ddr_sequence #(.C_TIMEOUT(C_TB_TIMEOUT)) dut(
		.i_clk(clk),.i_rstn(rstn),.i_phy_ready(phy_ready),.i_ddr_fault(ddr_fault),
		.i_req_ready(req_ready),.i_rsp_valid(rsp_valid),.i_rsp_data(rsp_data),
		.i_rsp_error(rsp_error),.o_req_valid(req_valid),.o_req_write(req_write),
		.o_req_addr(req_addr),.o_req_data(req_data),.o_rsp_ready(rsp_ready),
		.o_status(status),.o_error(error_code),.o_phase(phase),.o_writes(writes),
		.o_reads(reads),.o_output_bytes(output_bytes),.o_cycles(cycles),
		.o_cycle_bins(cycle_bins),.o_address(address_debug),
		.o_expected(expected_debug),.o_actual(actual_debug)
	);

	function integer find_slot;
		input [24:0]candidate;
		integer search;
		begin
			find_slot = -1;
			for(search=0;search<64;search=search+1)
				if(candidate === stem_addresses[search][24:0]) find_slot = search;
		end
	endfunction

	function signed [15:0]round_model;
		input signed [31:0]accumulator;
		input [30:0]multiplier;
		input [5:0]shift;
		reg signed [63:0]product;
		reg signed [63:0]rounded;
		reg [63:0]magnitude;
		reg [63:0]quotient;
		reg [63:0]remainder;
		reg [63:0]half;
		begin
			product = accumulator * $signed({1'b0,multiplier});
			magnitude = product[63] ? -product : product;
			quotient = magnitude >> shift;
			if(shift == 0) begin remainder = 0; half = 0; end
			else begin
				remainder = magnitude & ~(64'hffffffffffffffff << shift);
				half = 64'd1 << (shift-1);
			end
			if(shift != 0 && (remainder > half || (remainder == half && quotient[0])))
				quotient = quotient + 1'b1;
			rounded = product[63] ? -$signed(quotient) : $signed(quotient);
			if(rounded < -64'sd32768) round_model = -16'sd32768;
			else if(rounded > 64'sd32767) round_model = 16'sd32767;
			else round_model = rounded[15:0];
		end
	endfunction

	function signed [15:0]silu_model;
		input signed [15:0]sample;
		integer quotient;
		integer remainder;
		integer table_address;
		begin
			if(sample <= -16'sd2048) silu_model = 16'sd0;
			else if(sample >= 16'sd2048) silu_model = sample;
			else begin
				quotient = $signed(sample) >>> 2;
				remainder = sample[1:0];
				if(remainder == 3 || (remainder == 2 && quotient[0])) quotient = quotient + 1;
				table_address = quotient + 512;
				if(table_address == 1024) silu_model = 16'sd2047;
				else silu_model = $signed(silu_table[table_address]);
			end
		end
	endfunction

	task resolve_stage;
		input [15:0]internal_tag;
		input integer ordinal;
		output integer resolved_family;
		output integer resolved_index;
		output integer resolved_channel;
		reg [47:0]tags;
		reg [15:0]external_tag;
		integer position;
		begin
			if(internal_tag[15:5] !== 11'd0 || internal_tag[1:0] > 2)
				$fatal(1,"Invalid internal postprocess tag");
			tags = dut.u_core.u_pp.reg_retire_tags[internal_tag[4:2]];
			external_tag = tags >> (internal_tag[1:0]*16);
			if(!dut.u_core.flag_owner_down2) begin
				if(external_tag[15:8] !== 8'd0) $fatal(1,"Invalid Stem tag");
				resolved_family = 0;
				resolved_channel = external_tag[3:0];
				resolved_index = (ordinal/256)*256 + external_tag[7:0];
				if(resolved_index < 0 || resolved_index >= 1024) $fatal(1,"Stem stage index");
			end else begin
				position = external_tag[14:11];
				resolved_channel = external_tag[10:6];
				resolved_family = external_tag[15] ? 2 : 1;
				resolved_index = external_tag[15] ? position*24+resolved_channel :
				                                      position*16+resolved_channel;
				if((resolved_family==1 && resolved_index>=256) ||
				   (resolved_family==2 && resolved_index>=384)) $fatal(1,"Down2 stage index");
			end
		end
	endtask

	task stage_parameters;
		input integer selected_family;
		input integer selected_index;
		input integer selected_channel;
		begin
			if(selected_family == 0) begin
				stage_accumulator = $signed(stem_acc[selected_index]);
				stage_multiplier = dut.u_core.u_stem.reg_multiplier[selected_channel][30:0];
				stage_shift = dut.u_core.u_stem.reg_shift[selected_channel];
				post_multiplier = dut.u_core.u_stem.reg_post_multiplier[30:0];
				post_shift = dut.u_core.u_stem.reg_post_shift;
			end else if(selected_family == 1) begin
				stage_accumulator = $signed(dw_acc[selected_index]);
				stage_multiplier = dut.u_core.u_down2.reg_pre_multiplier[selected_channel][30:0];
				stage_shift = dut.u_core.u_down2.reg_pre_shift[selected_channel];
				post_multiplier = dut.u_core.u_down2.reg_post_multiplier[0][30:0];
				post_shift = dut.u_core.u_down2.reg_post_shift[0];
			end else begin
				stage_accumulator = $signed(pw_acc[selected_index]);
				stage_multiplier = dut.u_core.u_down2.reg_pre_multiplier[16+selected_channel][30:0];
				stage_shift = dut.u_core.u_down2.reg_pre_shift[16+selected_channel];
				post_multiplier = dut.u_core.u_down2.reg_post_multiplier[1][30:0];
				post_shift = dut.u_core.u_down2.reg_post_shift[1];
			end
		end
	endtask

	// The endpoint owns only accepted requests. Golden values never feed read data.
	always @(posedge clk or negedge rstn) begin
		if(!rstn) begin
			rsp_valid <= 1'b0;
			rsp_data <= 128'd0;
			rsp_error <= 4'd0;
			pending <= 1'b0;
			pending_write <= 1'b0;
			pending_drop <= 1'b0;
			pending_slot <= 0;
			response_delay <= 0;
			long_wait <= 0;
			random_bits <= 16'hace1;
			held_request <= 1'b0;
			held_request_payload <= 154'd0;
			write_requests <= 0;
			write_responses <= 0;
			read_requests <= 0;
			read_responses <= 0;
			for(i=0;i<64;i=i+1) begin
				endpoint_mem[i] <= 128'd0;
				write_seen[i] <= 1'b0;
				read_seen[i] <= 1'b0;
			end
		end else begin
			random_bits <= {random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
			if(held_request && (!req_valid || {req_write,req_addr,req_data} !== held_request_payload))
				$fatal(1,"Request payload changed under backpressure case=%0d",case_id);
			held_request <= req_valid && !req_ready;
			held_request_payload <= {req_write,req_addr,req_data};

			if(req_valid && req_ready) begin
				slot = find_slot(req_addr);
				if(slot < 0) $fatal(1,"Request address outside 64-vector set: %h",req_addr);
				pending <= 1'b1;
				pending_write <= req_write;
				pending_slot <= slot;
				pending_drop <= case_id==11 && !req_write && read_requests==0;
				response_delay <= case_id==2 ? 80 : case_id==1 ? random_bits[6:3] : 1;
				rsp_data <= req_write ? 128'd0 :
					(endpoint_mem[slot] ^ ((case_id==3 && read_requests==17) ? 128'd1 : 128'd0));
				rsp_error <= case_id==4 && req_write && write_requests==0 ? 4'h4 : 4'd0;
				if(req_write) begin
					if(write_requests >= 64 || slot != write_requests || write_seen[slot])
						$fatal(1,"Write identity/duplicate failure request=%0d slot=%0d",write_requests,slot);
					if(req_addr !== stem_addresses[write_requests][24:0] ||
					   req_data !== stem_golden[write_requests]) $fatal(1,"Write payload mismatch %0d",write_requests);
					endpoint_mem[slot] <= req_data;
					write_seen[slot] <= 1'b1;
					write_requests <= write_requests + 1;
				end else begin
					if(write_responses != 64 || read_requests >= 64 ||
					   slot != read_order[read_requests] || read_seen[slot])
						$fatal(1,"Read order/uniqueness failure request=%0d slot=%0d writes=%0d",read_requests,slot,write_responses);
					read_seen[slot] <= 1'b1;
					read_requests <= read_requests + 1;
				end
			end

			if(pending && !rsp_valid && !pending_drop) begin
				if(response_delay == 0) rsp_valid <= 1'b1;
				else response_delay <= response_delay - 1;
			end
			if(rsp_valid && rsp_ready) begin
				if(pending_write) write_responses <= write_responses + 1;
				else read_responses <= read_responses + 1;
				rsp_valid <= 1'b0;
				pending <= 1'b0;
				rsp_error <= 4'd0;
			end

			if(req_valid && !req_ready) long_wait <= long_wait + 1;
			else long_wait <= 0;
		end
	end

	// Drive request backpressure between active edges so reset-wait cases cannot accept once.
	always @(negedge clk or negedge rstn) begin
		if(!rstn) req_ready <= 1'b0;
		else if(pending || rsp_valid) req_ready <= 1'b0;
		else if(case_id==6 && !reset_done && req_valid && req_write) req_ready <= 1'b0;
		else if(case_id==7 && !reset_done && req_valid && !req_write) req_ready <= 1'b0;
		else if(case_id==2 && req_valid && long_wait<80) req_ready <= 1'b0;
		else if(case_id==1) req_ready <= random_bits[0] && random_bits[2];
		else req_ready <= 1'b1;
	end

	// Independent arithmetic, export, halo, and final-output scoreboards.
	always @(posedge clk or negedge rstn) begin
		if(!rstn) begin
			stem_exports <= 0;
			halo_bytes <= 0;
			padding_pixels <= 0;
			final_exports <= 0;
			accumulator_checks <= 0;
			pre_checks <= 0;
			silu_checks <= 0;
			post_checks <= 0;
			for(j=0;j<384;j=j+1) output_seen[j] <= 1'b0;
		end else begin
			if(phase==ST_STEM_BYTE && dut.core_output_valid && dut.flag_output_ready) begin
				if(stem_exports>=1024 || dut.core_output_index !== stem_exports[7:0] ||
				   dut.core_output_data !== stem_golden[stem_exports/16][(stem_exports%16)*8 +: 8])
					$fatal(1,"Stem export mismatch byte=%0d",stem_exports);
				stem_exports = stem_exports + 1;
			end

			if(dut.flag_halo_load && dut.core_load_ready) begin
				map_index = halo_bytes/16;
				if(map_index>=81) $fatal(1,"Halo overflow");
				if(halo_map[map_index][7]) begin
					if(dut.wire_load_data[7:0] !== 8'd0) $fatal(1,"Nonzero padding byte=%0d",halo_bytes);
					if((halo_bytes%16)==0) padding_pixels = padding_pixels + 1;
				end else if(dut.wire_load_data[7:0] !==
				            endpoint_mem[halo_map[map_index][5:0]][(halo_bytes%16)*8 +: 8])
					$fatal(1,"Halo byte did not come from endpoint byte=%0d",halo_bytes);
				halo_bytes = halo_bytes + 1;
			end

			if(phase==ST_OUTPUT_BYTE && dut.core_output_valid && dut.flag_output_ready) begin
				if(dut.core_output_index>=384 || output_seen[dut.core_output_index] ||
				   dut.core_output_data !== pw_golden[dut.core_output_index])
					$fatal(1,"Final export mismatch index=%0d",dut.core_output_index);
				output_seen[dut.core_output_index] <= 1'b1;
				final_exports = final_exports + 1;
			end

			if(!dut.u_core.flag_owner_down2 && dut.u_core.s_pp_valid && dut.u_core.s_pp_ready) begin
				for(lane=0;lane<3;lane=lane+1) if(dut.u_core.s_pp_mask[lane]) begin
					value_index=(accumulator_checks/256)*256+
						dut.u_core.u_stem.cnt_position*16+dut.u_core.u_stem.cnt_channel+lane;
					if(value_index>=1024 || $signed(dut.u_core.s_mac_result[lane*32+:32]) !== $signed(stem_acc[value_index]))
						$fatal(1,"Stem accumulator mismatch index=%0d",value_index);
					accumulator_checks = accumulator_checks + 1;
				end
			end else if(dut.u_core.flag_owner_down2 && dut.u_core.u_down2.flag_pp_input_accept) begin
				for(lane=0;lane<3;lane=lane+1) if(dut.u_core.u_down2.wire_result_lane_mask[lane]) begin
					value_index=dut.u_core.u_down2.wire_pp_position*16+
						dut.u_core.u_down2.wire_result_channel_base+lane;
					if(dut.u_core.u_down2.flag_layer_pw) begin
						value_index=dut.u_core.u_down2.wire_pp_position*24+
							dut.u_core.u_down2.wire_result_channel_base+lane;
						if($signed(dut.u_core.u_down2.wire_pp_result_data[lane*32+:32]) !== $signed(pw_acc[value_index]))
							$fatal(1,"PW accumulator mismatch index=%0d",value_index);
					end else if($signed(dut.u_core.u_down2.wire_pp_result_data[lane*32+:32]) !== $signed(dw_acc[value_index]))
						$fatal(1,"DW accumulator mismatch index=%0d",value_index);
					accumulator_checks = accumulator_checks + 1;
				end
			end

			if(dut.u_core.u_pp.flag_silu_accept) begin
				resolve_stage(dut.u_core.u_pp.pre_result_tag,pre_checks,family,value_index,channel);
				stage_parameters(family,value_index,channel);
				expected_stage=round_model(stage_accumulator,stage_multiplier,stage_shift);
				if($signed(dut.u_core.u_pp.pre_result_data) !== expected_stage)
					$fatal(1,"Pre mismatch family=%0d index=%0d",family,value_index);
				pre_checks = pre_checks + 1;
			end
			if(dut.u_core.u_pp.flag_post_accept) begin
				resolve_stage(dut.u_core.u_pp.reg_meta_tags[dut.u_core.u_pp.reg_meta_read],silu_checks,
				              family,value_index,channel);
				stage_parameters(family,value_index,channel);
				expected_stage=round_model(stage_accumulator,stage_multiplier,stage_shift);
				expected_silu=silu_model(expected_stage);
				if($signed(dut.u_core.u_pp.silu_output_data) !== expected_silu)
					$fatal(1,"SiLU mismatch family=%0d index=%0d",family,value_index);
				silu_checks = silu_checks + 1;
			end
			if(dut.u_core.u_pp.flag_post_complete) begin
				resolve_stage(dut.u_core.u_pp.post_result_tag,post_checks,family,value_index,channel);
				stage_parameters(family,value_index,channel);
				expected_stage=round_model(stage_accumulator,stage_multiplier,stage_shift);
				expected_silu=silu_model(expected_stage);
				expected_stage=round_model({{16{expected_silu[15]}},expected_silu},post_multiplier,post_shift);
				if($signed(dut.u_core.u_pp.post_result_data) !== expected_stage)
					$fatal(1,"Post mismatch family=%0d index=%0d",family,value_index);
				post_checks = post_checks + 1;
			end
		end
	end

	// Reset cases cancel the endpoint and core together, then run from command zero.
	initial begin
		wait(started);
		if(case_id>=5 && case_id<=10) begin
			case(case_id)
				5: wait(rstn && phase==ST_RUN && !dut.u_core.flag_owner_down2 && dut.u_core.s_busy);
				6: wait(rstn && phase==ST_WRITE && req_valid && !req_ready);
				7: wait(rstn && phase==ST_READ && req_valid && !req_ready);
				8: wait(rstn && phase==ST_HALO_BYTE);
				9: wait(rstn && phase==ST_RUN && dut.u_core.flag_owner_down2 && dut.u_core.d_busy);
				10: wait(rstn && phase==ST_OUTPUT_BYTE);
			endcase
			reset_target_seen = 1'b1;
			repeat(4) @(posedge clk);
			#1 rstn = 1'b0;
			repeat(4) @(negedge clk);
			reset_done = 1'b1;
			rstn = 1'b1;
			@(posedge clk);
			if(rsp_valid || pending || req_valid || rsp_ready) $fatal(1,"Old transaction survived common reset");
		end
	end

	task check_success;
		begin
			if(writes!==64 || reads!==64 || output_bytes!==384 ||
			   write_requests!=64 || write_responses!=64 || read_requests!=64 || read_responses!=64)
				$fatal(1,"Endpoint conservation W=%0d/%0d/%0d R=%0d/%0d/%0d O=%0d",
				       write_requests,write_responses,writes,read_requests,read_responses,reads,output_bytes);
			if(stem_exports!=1024 || halo_bytes!=1296 || padding_pixels!=17 || final_exports!=384)
				$fatal(1,"Data path counts Stem=%0d halo=%0d pad=%0d final=%0d",
				       stem_exports,halo_bytes,padding_pixels,final_exports);
			if(accumulator_checks!=1664 || pre_checks!=1664 || silu_checks!=1664 || post_checks!=1664)
				$fatal(1,"Arithmetic coverage acc=%0d pre=%0d silu=%0d post=%0d",
				       accumulator_checks,pre_checks,silu_checks,post_checks);
			for(i=0;i<64;i=i+1)
				if(!write_seen[i] || !read_seen[i]) $fatal(1,"Endpoint hole slot=%0d",i);
			for(i=0;i<384;i=i+1)
				if(!output_seen[i]) $fatal(1,"Final output hole=%0d",i);
			sum_bins=0;
			for(i=0;i<10;i=i+1) sum_bins=sum_bins+cycle_bins[i*32 +: 32];
			if(sum_bins!==cycles) $fatal(1,"Cycle bins do not close sum=%0d cycles=%0d",sum_bins,cycles);
			if(case_id>=5 && case_id<=10 && (!reset_done || !reset_target_seen))
				$fatal(1,"Requested reset phase not covered");
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=0;
		if(!$value$plusargs("VECTORS=%s",vector_dir)) $fatal(1,"Missing +VECTORS=<absolute path>");
		if(case_id<0 || case_id>12) $fatal(1,"CASE must be 0..12");
		$sformat(path,"%0s/program.hex",vector_dir); $readmemh(path,program);
		$sformat(path,"%0s/stem_golden.hex",vector_dir); $readmemh(path,stem_golden);
		$sformat(path,"%0s/stem_addresses.hex",vector_dir); $readmemh(path,stem_addresses);
		$sformat(path,"%0s/halo_map.hex",vector_dir); $readmemh(path,halo_map);
		$sformat(path,"%0s/pw_golden.hex",vector_dir); $readmemh(path,pw_golden);
		$sformat(path,"%0s/stem_acc.hex",vector_dir); $readmemh(path,stem_acc);
		$sformat(path,"%0s/dw_acc.hex",vector_dir); $readmemh(path,dw_acc);
		$sformat(path,"%0s/pw_acc.hex",vector_dir); $readmemh(path,pw_acc);
		for(i=0;i<1024;i=i+1) silu_table[i]=program[i][15:0];
		j=0;
		for(i=0;i<81;i=i+1) if(!halo_map[i][7]) begin
			read_order[j]=halo_map[i][5:0];
			j=j+1;
		end
		if(j!=64) $fatal(1,"Halo map expected 64 real pixels, got %0d",j);
		for(i=0;i<64;i=i+1) begin
			if(stem_addresses[i][31:25]!==0 || stem_addresses[i][2:0]!==0)
				$fatal(1,"Invalid native address vector %0d",i);
			for(j=0;j<i;j=j+1)
				if(stem_addresses[i]===stem_addresses[j]) $fatal(1,"Duplicate vector address %0d/%0d",j,i);
		end
		repeat(8) @(negedge clk);
		phy_ready=1'b1;
		rstn=1'b1;
		started=1'b1;
		while(status==0) begin
			@(posedge clk);
			ticks=ticks+1;
			if(ticks>500000) $fatal(1,"TB timeout case=%0d phase=%0d",case_id,phase);
		end
		if(case_id==3) begin
			if(status!==2 || error_code!==5) $fatal(1,"Read corruption expected error 5, got %0d",error_code);
		end else if(case_id==4) begin
			if(status!==2 || error_code!==7) $fatal(1,"Response error expected error 7, got %0d",error_code);
		end else if(case_id==11) begin
			if(status!==2 || error_code!==9) $fatal(1,"Dropped read expected timeout 9, got %0d",error_code);
		end else begin
			if(status!==1) $fatal(1,"Unexpected failure case=%0d error=%0d phase=%0d",case_id,error_code,phase);
			check_success;
			if(case_id==12) begin
				@(negedge clk); ddr_fault=1'b1;
				wait(status==2); @(posedge clk);
				if(error_code!==1) $fatal(1,"Post-PASS DDR fault expected error 1, got %0d",error_code);
			end
		end
		$display("TB_PASS_STEM_DDR_SEQUENCE case=%0d status=%0d error=%0d generation=%0d cycles=%0d W=%0d R=%0d Stem=%0d halo=%0d pad=%0d PW=%0d acc/pre/silu/post=%0d/%0d/%0d/%0d",
		         case_id,status,error_code,generation,cycles,write_requests,read_requests,
		         stem_exports,halo_bytes,padding_pixels,final_exports,
		         accumulator_checks,pre_checks,silu_checks,post_checks);
		$finish;
	end

	always @(negedge rstn) generation = generation + 1;
endmodule
