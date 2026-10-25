`timescale 1ns / 1ps

// Independent controlled-memory check of the complete RGB -> Stem -> DW -> PW traversal.
module tb_frontend_ddr_tensor;
	localparam [26:0] C_DUT_TIMEOUT = 27'd500000;
	localparam integer ST_HALO_BYTE = 20;
	localparam integer ST_TABLE = 6;
	localparam integer ST_EXPORT_BYTE = 11;
	localparam integer ST_READ_RESPONSE = 19;
	localparam integer INPUT_WORDS = 27648;
	localparam integer STEM_WORDS = 36864;
	localparam integer PW_WORDS = 13824;
	localparam integer STEM_VALUES = 589824;
	localparam integer DW_VALUES = 147456;
	localparam integer PW_VALUES = 221184;
	localparam integer STEM_HALO = 559872;
	localparam integer DW_HALO = 746496;
	localparam integer STEM_READS = 51357;
	localparam integer DW_READS = 46207;

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
	wire [31:0]writes;
	wire [31:0]reads;
	wire [31:0]output_bytes;
	wire [31:0]cycles;
	wire [319:0]cycle_bins;
	wire [24:0]address_debug;
	wire [127:0]expected_debug;
	wire [127:0]actual_debug;

	reg [127:0]input_golden [0:INPUT_WORDS-1];
	reg [127:0]stem_golden [0:STEM_WORDS-1];
	reg [127:0]pw_golden [0:PW_WORDS-1];
	reg [127:0]input_mem [0:INPUT_WORDS-1];
	reg [127:0]stem_mem [0:STEM_WORDS-1];
	reg [127:0]pw_mem [0:PW_WORDS-1];
	reg input_write_seen [0:INPUT_WORDS-1];
	reg stem_write_seen [0:STEM_WORDS-1];
	reg pw_write_seen [0:PW_WORDS-1];

	reg [31:0]stem_acc [0:STEM_VALUES-1];
	reg [15:0]stem_pre [0:STEM_VALUES-1];
	reg [15:0]stem_silu [0:STEM_VALUES-1];
	reg [7:0]stem_post [0:STEM_VALUES-1];
	reg [31:0]dw_acc [0:DW_VALUES-1];
	reg [15:0]dw_pre [0:DW_VALUES-1];
	reg [15:0]dw_silu [0:DW_VALUES-1];
	reg [7:0]dw_post [0:DW_VALUES-1];
	reg [31:0]pw_acc [0:PW_VALUES-1];
	reg [15:0]pw_pre [0:PW_VALUES-1];
	reg [15:0]pw_silu [0:PW_VALUES-1];
	reg [7:0]pw_post [0:PW_VALUES-1];
	reg stem_acc_seen [0:STEM_VALUES-1];
	reg stem_pre_seen [0:STEM_VALUES-1];
	reg stem_silu_seen [0:STEM_VALUES-1];
	reg stem_post_seen [0:STEM_VALUES-1];
	reg dw_acc_seen [0:DW_VALUES-1];
	reg dw_pre_seen [0:DW_VALUES-1];
	reg dw_silu_seen [0:DW_VALUES-1];
	reg dw_post_seen [0:DW_VALUES-1];
	reg pw_acc_seen [0:PW_VALUES-1];
	reg pw_pre_seen [0:PW_VALUES-1];
	reg pw_silu_seen [0:PW_VALUES-1];
	reg pw_post_seen [0:PW_VALUES-1];

	reg [7:0]stem_halo_value [0:STEM_HALO-1];
	reg [31:0]stem_halo_addr [0:STEM_HALO-1];
	reg [7:0]dw_halo_value [0:DW_HALO-1];
	reg [31:0]dw_halo_addr [0:DW_HALO-1];
	reg [31:0]stem_read_trace [0:STEM_READS-1];
	reg [31:0]dw_read_trace [0:DW_READS-1];

	reg pending = 1'b0;
	reg pending_write = 1'b0;
	reg pending_drop = 1'b0;
	integer response_delay = 0;
	reg [15:0]random_bits = 16'hace1;
	reg held_request = 1'b0;
	reg [153:0]held_request_payload = 154'd0;
	reg [4095:0]vector_dir;
	reg [4095:0]generated_dir;
	reg [4095:0]path;
	integer case_id = 0;
	integer ticks = 0;
	integer i;
	integer lane;
	integer family;
	integer value_index;
	integer slot;
	integer write_requests = 0;
	integer write_responses = 0;
	integer read_requests = 0;
	integer read_responses = 0;
	integer halo_checks = 0;
	integer padding_checks = 0;
	integer acc_checks = 0;
	integer pre_checks = 0;
	integer silu_checks = 0;
	integer post_checks = 0;
	integer table_entries = 0;
	integer sum_bins = 0;
	integer stall_count = 0;
	integer reset_stage = 0;
	reg started = 1'b0;
	reg reset_done = 1'b0;
	reg injected_bad_data = 1'b0;
	reg [31:0]expected_halo_addr;
	reg [24:0]expected_native_addr;
	reg [47:0]tag_bundle;
	reg [15:0]external_tag;

	always #5 clk = !clk;

	road_stem_ddr_sequence #(.C_TIMEOUT(C_DUT_TIMEOUT)) dut(
		.i_clk(clk),.i_rstn(rstn),.i_phy_ready(phy_ready),.i_ddr_fault(ddr_fault),
		.i_req_ready(req_ready),.i_rsp_valid(rsp_valid),.i_rsp_data(rsp_data),.i_rsp_error(rsp_error),
		.o_req_valid(req_valid),.o_req_write(req_write),.o_req_addr(req_addr),.o_req_data(req_data),
		.o_rsp_ready(rsp_ready),.o_status(status),.o_error(error_code),.o_phase(phase),
		.o_writes(writes),.o_reads(reads),.o_output_bytes(output_bytes),.o_cycles(cycles),
		.o_cycle_bins(cycle_bins),.o_address(address_debug),.o_expected(expected_debug),.o_actual(actual_debug)
	);

	task decode_external_tag;
		input [15:0]tag;
		output integer resolved_family;
		output integer resolved_index;
		integer position;
		integer channel;
		begin
			if(!dut.u_core.flag_owner_down2) begin
				if(tag[15:8] !== 8'd0 || dut.cnt_stem_tile >= 2304) $fatal(1,"Stem tag range tag=%h tile=%0d",tag,dut.cnt_stem_tile);
				position = tag[7:4];
				channel = tag[3:0];
				resolved_family = 0;
				resolved_index = dut.cnt_stem_tile*256 + position*16 + channel;
			end else begin
				position = tag[14:11];
				channel = tag[10:6];
				resolved_family = tag[15] ? 2 : 1;
				resolved_index = dut.cnt_down_tile*(tag[15] ? 384 : 256) + position*(tag[15] ? 24 : 16) + channel;
				if(tag[5:0] !== 6'd0 || dut.cnt_down_tile >= 576 || position >= 16 ||
				   (resolved_family==1 && channel>=16) || (resolved_family==2 && channel>=24))
					$fatal(1,"Down tag range tag=%h tile=%0d",tag,dut.cnt_down_tile);
			end
		end
	endtask

	task resolve_internal_tag;
		input [15:0]tag;
		output integer resolved_family;
		output integer resolved_index;
		begin
			if(tag[15:5] !== 11'd0 || tag[1:0] > 2) $fatal(1,"Internal tag range %h",tag);
			tag_bundle = dut.u_core.u_pp.reg_retire_tags[tag[4:2]];
			external_tag = tag_bundle >> (tag[1:0]*16);
			decode_external_tag(external_tag,resolved_family,resolved_index);
		end
	endtask

	task clear_generation;
		begin
			write_requests=0; write_responses=0; read_requests=0; read_responses=0;
			halo_checks=0; padding_checks=0; acc_checks=0; pre_checks=0; silu_checks=0; post_checks=0; table_entries=0;
			for(i=0;i<INPUT_WORDS;i=i+1) begin input_write_seen[i]=1'b0; input_mem[i]=0; end
			for(i=0;i<STEM_WORDS;i=i+1) begin stem_write_seen[i]=1'b0; stem_mem[i]=0; end
			for(i=0;i<PW_WORDS;i=i+1) begin pw_write_seen[i]=1'b0; pw_mem[i]=0; end
			for(i=0;i<STEM_VALUES;i=i+1) begin stem_acc_seen[i]=0; stem_pre_seen[i]=0; stem_silu_seen[i]=0; stem_post_seen[i]=0; end
			for(i=0;i<DW_VALUES;i=i+1) begin dw_acc_seen[i]=0; dw_pre_seen[i]=0; dw_silu_seen[i]=0; dw_post_seen[i]=0; end
			for(i=0;i<PW_VALUES;i=i+1) begin pw_acc_seen[i]=0; pw_pre_seen[i]=0; pw_silu_seen[i]=0; pw_post_seen[i]=0; end
		end
	endtask

	// A request response is derived only from this endpoint's previously accepted writes.
	always @(posedge clk or negedge rstn) begin
		if(!rstn) begin
			rsp_valid <= 1'b0;
			rsp_data <= 128'd0;
			rsp_error <= 4'd0;
			pending <= 1'b0;
			pending_write <= 1'b0;
			pending_drop <= 1'b0;
			response_delay <= 0;
			random_bits <= 16'hace1;
			held_request <= 1'b0;
			held_request_payload <= 154'd0;
			write_requests <= 0; write_responses <= 0; read_requests <= 0; read_responses <= 0;
		end else begin
			random_bits <= {random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
			if(held_request && (!req_valid || {req_write,req_addr,req_data} !== held_request_payload))
				$fatal(1,"Request changed under backpressure ordinal=%0d",write_requests+read_requests);
			held_request <= req_valid && !req_ready;
			held_request_payload <= {req_write,req_addr,req_data};
			if(req_valid && req_ready) begin
				if(pending || rsp_valid) $fatal(1,"Endpoint accepted a second outstanding request");
				pending <= 1'b1;
				pending_write <= req_write;
				pending_drop <= case_id==5 && !req_write && read_requests==0;
				response_delay <= case_id==1 ? random_bits[5:3] : 1;
				if(req_write) begin
					if(req_addr>=25'h1a00000 && req_addr<25'h1a00000+INPUT_WORDS*8) begin
						slot=(req_addr-25'h1a00000)>>3;
						if(req_addr!==25'h1a00000+slot*8 || input_write_seen[slot] || req_data!==input_golden[slot])
							$fatal(1,"Input write mismatch ordinal=%0d slot=%0d addr=%h",write_requests,slot,req_addr);
						input_write_seen[slot]<=1'b1; input_mem[slot]<=req_data;
					end else if(req_addr>=25'h1a80000 && req_addr<25'h1a80000+STEM_WORDS*8) begin
						slot=(req_addr-25'h1a80000)>>3;
						if(req_addr!==25'h1a80000+slot*8 || stem_write_seen[slot] || req_data!==stem_golden[slot])
							$fatal(1,"Stem write mismatch ordinal=%0d slot=%0d addr=%h",write_requests,slot,req_addr);
						stem_write_seen[slot]<=1'b1; stem_mem[slot]<=req_data;
					end else if(req_addr>=25'h1b00000 && req_addr<25'h1b00000+PW_WORDS*8) begin
						slot=(req_addr-25'h1b00000)>>3;
						if(req_addr!==25'h1b00000+slot*8 || pw_write_seen[slot] || req_data!==pw_golden[slot])
							$fatal(1,"PW write mismatch ordinal=%0d slot=%0d addr=%h",write_requests,slot,req_addr);
						pw_write_seen[slot]<=1'b1; pw_mem[slot]<=req_data;
					end else $fatal(1,"Write address outside tensors: %h",req_addr);
					rsp_data <= 128'd0;
					rsp_error <= 4'd0;
					write_requests <= write_requests+1;
				end else begin
					if(read_requests<STEM_READS) begin
						if(req_addr!==stem_read_trace[read_requests]) $fatal(1,"RGB read order mismatch ordinal=%0d actual=%h expected=%h",read_requests,req_addr,stem_read_trace[read_requests]);
						slot=(req_addr-25'h1a00000)>>3;
						if(slot<0 || slot>=INPUT_WORDS || !input_write_seen[slot]) $fatal(1,"RGB read before accepted write ordinal=%0d",read_requests);
						rsp_data <= input_mem[slot] ^ ((case_id==7 && read_requests==0) ? {128{1'b1}} : 128'd0);
					end else begin
						if(read_requests>=STEM_READS+DW_READS || req_addr!==dw_read_trace[read_requests-STEM_READS])
							$fatal(1,"DW read order mismatch ordinal=%0d actual=%h expected=%h",read_requests,req_addr,dw_read_trace[read_requests-STEM_READS]);
						slot=(req_addr-25'h1a80000)>>3;
						if(slot<0 || slot>=STEM_WORDS || !stem_write_seen[slot]) $fatal(1,"DW read before accepted Stem write ordinal=%0d",read_requests);
						rsp_data <= stem_mem[slot];
					end
					read_requests <= read_requests+1;
					if(case_id==4 && read_requests==0) rsp_error<=4'h4;
					if(case_id==7 && read_requests==0) injected_bad_data<=1'b1;
				end
			end
			if(pending && !rsp_valid && !pending_drop) begin
				if(response_delay==0) rsp_valid<=1'b1;
				else response_delay<=response_delay-1;
			end
			if(rsp_valid && rsp_ready) begin
				if(pending_write) write_responses<=write_responses+1;
				else read_responses<=read_responses+1;
				rsp_valid<=1'b0; pending<=1'b0;
				rsp_error<=4'd0;
			end
		end
	end

	always @(negedge clk or negedge rstn) begin
		if(!rstn) req_ready<=1'b0;
		else if(pending || rsp_valid) req_ready<=1'b0;
		else if(case_id==2 && req_valid && write_requests==INPUT_WORDS && stall_count<512) begin req_ready<=1'b0; stall_count=stall_count+1; end
		else if(case_id==1) req_ready<=random_bits[0] || random_bits[3];
		else req_ready<=1'b1;
	end

	always @(posedge clk or negedge rstn) begin
		if(!rstn) table_entries=0;
		else if(dut.flag_table_accept) table_entries=table_entries+1;
	end

	// Compare every accepted halo entry against the independently converted binary contract.
	always @(posedge clk) begin
		if(rstn && case_id!=7 && phase==ST_HALO_BYTE && dut.flag_load_accept) begin
			if(dut.flag_halo_rgb) begin
				value_index=dut.cnt_stem_tile*243+dut.cnt_halo_address;
				if(value_index<0 || value_index>=STEM_HALO) $fatal(1,"Stem halo index %0d",value_index);
				expected_halo_addr=stem_halo_addr[value_index];
				if(expected_halo_addr===32'hffffffff) begin
					if(dut.wire_load_kind!==3'd1 || dut.wire_load_data!==32'd0 || stem_halo_value[value_index]!==8'd0)
						$fatal(1,"Stem padding mismatch index=%0d",value_index);
					padding_checks=padding_checks+1;
				end else begin
					expected_native_addr=(expected_halo_addr>>1)&25'h1fffff8;
					if(dut.wire_load_kind!==3'd0 || dut.reg_address!==expected_native_addr ||
					   (dut.wire_load_data[7:0]^8'h80)!==stem_halo_value[value_index])
						$fatal(1,"Stem halo value/address mismatch index=%0d addr=%h/%h raw=%h normalized=%h expected=%h",value_index,dut.reg_address,expected_native_addr,dut.wire_load_data[7:0],dut.wire_load_data[7:0]^8'h80,stem_halo_value[value_index]);
				end
			end else begin
				value_index=dut.cnt_down_tile*1296+dut.cnt_halo_address;
				if(value_index<0 || value_index>=DW_HALO) $fatal(1,"DW halo index %0d",value_index);
				expected_halo_addr=dw_halo_addr[value_index];
				if(expected_halo_addr===32'hffffffff) begin
					if(dut.wire_load_kind!==3'd0 || dut.wire_load_data!==32'd0 || dw_halo_value[value_index]!==8'd0)
						$fatal(1,"DW padding mismatch index=%0d",value_index);
					padding_checks=padding_checks+1;
				end else begin
					expected_native_addr=(expected_halo_addr>>1)&25'h1fffff8;
					if(dut.wire_load_kind!==3'd0 || dut.reg_address!==expected_native_addr ||
					   $signed(dut.wire_load_data)!==$signed({{24{dw_halo_value[value_index][7]}},dw_halo_value[value_index]}))
						$fatal(1,"DW halo value/address mismatch index=%0d addr=%h/%h actual=%h expected=%h",value_index,dut.reg_address,expected_native_addr,dut.wire_load_data,dw_halo_value[value_index]);
				end
			end
			halo_checks=halo_checks+1;
		end
	end

	// Compare every arithmetic retirement; duplicate tags fail before the value check can hide holes.
	always @(posedge clk) begin
		if(rstn && case_id!=7) begin
			if(!dut.u_core.flag_owner_down2 && dut.u_core.s_pp_valid && dut.u_core.s_pp_ready) begin
				for(lane=0;lane<3;lane=lane+1) if(dut.u_core.s_pp_mask[lane]) begin
					decode_external_tag(dut.u_core.s_pp_tags[lane*16+:16],family,value_index);
					if(family!=0 || stem_acc_seen[value_index] || $signed(dut.u_core.s_pp_acc[lane*32+:32])!==$signed(stem_acc[value_index])) $fatal(1,"Stem acc mismatch index=%0d",value_index);
					stem_acc_seen[value_index]=1'b1; acc_checks=acc_checks+1;
				end
			end else if(dut.u_core.flag_owner_down2 && dut.u_core.u_down2.flag_pp_input_accept) begin
				for(lane=0;lane<3;lane=lane+1) if(dut.u_core.d_pp_mask[lane]) begin
					decode_external_tag(dut.u_core.d_pp_tags[lane*16+:16],family,value_index);
					if(family==1) begin
						if(dw_acc_seen[value_index] || $signed(dut.u_core.d_pp_acc[lane*32+:32])!==$signed(dw_acc[value_index])) $fatal(1,"DW acc mismatch index=%0d",value_index);
						dw_acc_seen[value_index]=1'b1;
					end else if(family==2) begin
						if(pw_acc_seen[value_index] || $signed(dut.u_core.d_pp_acc[lane*32+:32])!==$signed(pw_acc[value_index])) $fatal(1,"PW acc mismatch index=%0d",value_index);
						pw_acc_seen[value_index]=1'b1;
					end else $fatal(1,"Down accumulator family");
					acc_checks=acc_checks+1;
				end
			end
			if(dut.u_core.u_pp.flag_silu_accept) begin
				resolve_internal_tag(dut.u_core.u_pp.pre_result_tag,family,value_index);
				if(family==0) begin if(stem_pre_seen[value_index] || dut.u_core.u_pp.pre_result_data!==stem_pre[value_index]) $fatal(1,"Stem pre mismatch index=%0d",value_index); stem_pre_seen[value_index]=1'b1; end
				else if(family==1) begin if(dw_pre_seen[value_index] || dut.u_core.u_pp.pre_result_data!==dw_pre[value_index]) $fatal(1,"DW pre mismatch index=%0d",value_index); dw_pre_seen[value_index]=1'b1; end
				else begin if(pw_pre_seen[value_index] || dut.u_core.u_pp.pre_result_data!==pw_pre[value_index]) $fatal(1,"PW pre mismatch index=%0d",value_index); pw_pre_seen[value_index]=1'b1; end
				pre_checks=pre_checks+1;
			end
			if(dut.u_core.u_pp.flag_post_accept) begin
				resolve_internal_tag(dut.u_core.u_pp.reg_meta_tags[dut.u_core.u_pp.reg_meta_read],family,value_index);
				if(family==0) begin if(stem_silu_seen[value_index] || dut.u_core.u_pp.silu_output_data!==stem_silu[value_index]) $fatal(1,"Stem silu mismatch index=%0d",value_index); stem_silu_seen[value_index]=1'b1; end
				else if(family==1) begin if(dw_silu_seen[value_index] || dut.u_core.u_pp.silu_output_data!==dw_silu[value_index]) $fatal(1,"DW silu mismatch index=%0d",value_index); dw_silu_seen[value_index]=1'b1; end
				else begin if(pw_silu_seen[value_index] || dut.u_core.u_pp.silu_output_data!==pw_silu[value_index]) $fatal(1,"PW silu mismatch index=%0d",value_index); pw_silu_seen[value_index]=1'b1; end
				silu_checks=silu_checks+1;
			end
			if(dut.u_core.u_pp.flag_post_complete) begin
				resolve_internal_tag(dut.u_core.u_pp.post_result_tag,family,value_index);
				if(family==0) begin if(stem_post_seen[value_index] || dut.u_core.u_pp.wire_post_saturated[7:0]!==stem_post[value_index]) $fatal(1,"Stem post mismatch index=%0d",value_index); stem_post_seen[value_index]=1'b1; end
				else if(family==1) begin if(dw_post_seen[value_index] || dut.u_core.u_pp.wire_post_saturated[7:0]!==dw_post[value_index]) $fatal(1,"DW post mismatch index=%0d",value_index); dw_post_seen[value_index]=1'b1; end
				else begin if(pw_post_seen[value_index] || dut.u_core.u_pp.wire_post_saturated[7:0]!==pw_post[value_index]) $fatal(1,"PW post mismatch index=%0d",value_index); pw_post_seen[value_index]=1'b1; end
				post_checks=post_checks+1;
			end
		end
	end

	// One reset case cancels four short generations, clears endpoint/TB ownership, then completes once.
	initial begin
		wait(started);
		if(case_id==3) begin
			while(reset_stage<4) begin
				case(reset_stage)
					0:wait(rstn && write_requests>=100);
					1:wait(rstn && phase==ST_TABLE && table_entries>=512);
					2:wait(rstn && phase==ST_READ_RESPONSE && read_requests>=1 && pending && !rsp_valid);
					3:wait(rstn && phase==ST_EXPORT_BYTE && dut.core_output_index>=128);
				endcase
				#1 rstn=1'b0;
				repeat(4) @(negedge clk);
				clear_generation;
				reset_stage=reset_stage+1;
				rstn=1'b1;
			end
			reset_done=1'b1;
		end
	end

	task check_success;
		begin
			if(writes!==32'd78336 || reads!==32'd97564 || output_bytes!==32'd221184 ||
			   write_requests!=78336 || write_responses!=78336 || read_requests!=97564 || read_responses!=97564)
				$fatal(1,"Endpoint conservation W=%0d/%0d/%0d R=%0d/%0d/%0d O=%0d",write_requests,write_responses,writes,read_requests,read_responses,reads,output_bytes);
			if(halo_checks!=STEM_HALO+DW_HALO || acc_checks!=STEM_VALUES+DW_VALUES+PW_VALUES ||
			   pre_checks!=STEM_VALUES+DW_VALUES+PW_VALUES || silu_checks!=STEM_VALUES+DW_VALUES+PW_VALUES || post_checks!=STEM_VALUES+DW_VALUES+PW_VALUES)
				$fatal(1,"Coverage halo=%0d acc/pre/silu/post=%0d/%0d/%0d/%0d",halo_checks,acc_checks,pre_checks,silu_checks,post_checks);
			if(table_entries!=1024 || dut.cnt_stem_tile!=2304 || dut.cnt_down_tile!=576 || dut.cnt_program!=10799)
				$fatal(1,"Program coverage table=%0d tiles=%0d/%0d final_zero_based_command=%0d",table_entries,dut.cnt_stem_tile,dut.cnt_down_tile,dut.cnt_program);
			for(i=0;i<INPUT_WORDS;i=i+1) if(!input_write_seen[i]) $fatal(1,"Input write hole %0d",i);
			for(i=0;i<STEM_WORDS;i=i+1) if(!stem_write_seen[i]) $fatal(1,"Stem write hole %0d",i);
			for(i=0;i<PW_WORDS;i=i+1) if(!pw_write_seen[i]) $fatal(1,"PW write hole %0d",i);
			sum_bins=0;
			for(i=0;i<10;i=i+1) sum_bins=sum_bins+cycle_bins[i*32+:32];
			if(sum_bins!==cycles) $fatal(1,"Cycle bins do not close sum=%0d cycles=%0d",sum_bins,cycles);
			if(case_id==2 && stall_count!=512) $fatal(1,"512-cycle request stall not covered: %0d",stall_count);
			if(case_id==3 && (!reset_done || reset_stage!=4)) $fatal(1,"Four reset cancellation points not covered stage=%0d",reset_stage);
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=0;
		if(!$value$plusargs("VECTORS=%s",vector_dir)) $fatal(1,"Missing VECTORS");
		if(!$value$plusargs("GENERATED=%s",generated_dir)) $fatal(1,"Missing GENERATED");
		if(case_id<0 || case_id>7) $fatal(1,"CASE must be 0..7");
		$sformat(path,"%0s/input_ddr_128.hex",vector_dir); $readmemh(path,input_golden);
		$sformat(path,"%0s/stem_ddr_128.hex",vector_dir); $readmemh(path,stem_golden);
		$sformat(path,"%0s/pw_ddr_128.hex",vector_dir); $readmemh(path,pw_golden);
		$sformat(path,"%0s/stem_acc_s32.hex",vector_dir); $readmemh(path,stem_acc);
		$sformat(path,"%0s/stem_pre_s16.hex",vector_dir); $readmemh(path,stem_pre);
		$sformat(path,"%0s/stem_silu_s16.hex",vector_dir); $readmemh(path,stem_silu);
		$sformat(path,"%0s/stem_post_s8.hex",vector_dir); $readmemh(path,stem_post);
		$sformat(path,"%0s/dw_acc_s32.hex",vector_dir); $readmemh(path,dw_acc);
		$sformat(path,"%0s/dw_pre_s16.hex",vector_dir); $readmemh(path,dw_pre);
		$sformat(path,"%0s/dw_silu_s16.hex",vector_dir); $readmemh(path,dw_silu);
		$sformat(path,"%0s/dw_post_s8.hex",vector_dir); $readmemh(path,dw_post);
		$sformat(path,"%0s/pw_acc_s32.hex",vector_dir); $readmemh(path,pw_acc);
		$sformat(path,"%0s/pw_pre_s16.hex",vector_dir); $readmemh(path,pw_pre);
		$sformat(path,"%0s/pw_silu_s16.hex",vector_dir); $readmemh(path,pw_silu);
		$sformat(path,"%0s/pw_post_s8.hex",vector_dir); $readmemh(path,pw_post);
		$sformat(path,"%0s/stem_halo_values.hex",generated_dir); $readmemh(path,stem_halo_value);
		$sformat(path,"%0s/stem_halo_addr.hex",generated_dir); $readmemh(path,stem_halo_addr);
		$sformat(path,"%0s/dw_halo_values.hex",generated_dir); $readmemh(path,dw_halo_value);
		$sformat(path,"%0s/dw_halo_addr.hex",generated_dir); $readmemh(path,dw_halo_addr);
		$sformat(path,"%0s/stem_read_trace.hex",generated_dir); $readmemh(path,stem_read_trace);
		$sformat(path,"%0s/dw_read_trace.hex",generated_dir); $readmemh(path,dw_read_trace);
		clear_generation;
		repeat(8) @(negedge clk);
		phy_ready=1'b1; rstn=1'b1; started=1'b1;
		while(status==0) begin
			@(posedge clk); ticks=ticks+1;
			if(ticks%1000000==0) $display("TB_PROGRESS cycles=%0d phase=%0d W=%0d R=%0d stem_tile=%0d down_tile=%0d",ticks,phase,writes,reads,dut.cnt_stem_tile,dut.cnt_down_tile);
			if(ticks>20000000) $fatal(1,"TB timeout phase=%0d W=%0d R=%0d",phase,writes,reads);
		end
		if(case_id==4 || case_id==5 || case_id==7) begin
			if(status!==2 || (case_id==4 && error_code!==7) || (case_id==5 && error_code!==9) || (case_id==7 && error_code!==4))
				$fatal(1,"Expected fault mismatch case=%0d status=%0d error=%0d injected_bad_data=%0d",case_id,status,error_code,injected_bad_data);
			$display("TB_PASS_EXPECTED_FAULT case=%0d status=%0d error=%0d cycles=%0d",case_id,status,error_code,cycles);
		end else begin
			if(status!==1) $fatal(1,"Unexpected DUT failure error=%0d phase=%0d addr=%h expected=%h actual=%h",error_code,phase,address_debug,expected_debug,actual_debug);
			check_success;
			if(case_id==6) begin
				@(negedge clk); ddr_fault=1'b1; wait(status==2); @(posedge clk);
				if(error_code!==1 || req_valid || rsp_ready) $fatal(1,"PASS fault did not revoke success error=%0d",error_code);
				$display("TB_PASS_EXPECTED_FAULT case=6 status=%0d error=%0d cycles=%0d",status,error_code,cycles);
			end else begin
				$display("BINS %0d %0d %0d %0d %0d %0d %0d %0d %0d %0d",cycle_bins[31:0],cycle_bins[63:32],cycle_bins[95:64],cycle_bins[127:96],cycle_bins[159:128],cycle_bins[191:160],cycle_bins[223:192],cycle_bins[255:224],cycle_bins[287:256],cycle_bins[319:288]);
				$display("TB_PASS_FRONTEND_DDR case=%0d cycles=%0d writes=%0d reads=%0d output=%0d halo=%0d stages=%0d/%0d/%0d/%0d",case_id,cycles,writes,reads,output_bytes,halo_checks,acc_checks,pre_checks,silu_checks,post_checks);
			end
		end
		$finish;
	end
endmodule
