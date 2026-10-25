`timescale 1ns / 1ps

// 深通道PW固定形状自检；PROFILE仅允许96->24或192->12分片。
module tb_pw_deep #(parameter PROFILE=1)(output reg o_test_done);
    localparam integer CIN=(PROFILE==1)?96:192;
    localparam integer COUT=(PROFILE==1)?24:12;
    localparam integer GROUPS=CIN/8;
    localparam integer OUTPUT_GROUPS=COUT/3;
    localparam integer INPUT_WORDS=16*CIN;
    localparam integer OUTPUT_WORDS=16*COUT;
    localparam integer TASKS=16*OUTPUT_GROUPS;
    localparam integer SLABS=(PROFILE==1)?1:8;
    localparam [3:0] ST_IDLE=4'd0, ST_PREPARE=4'd1, ST_SEND=4'd2, ST_MAC_WAIT=4'd3;
    localparam [3:0] ST_DRAIN=4'd4, ST_ADVANCE=4'd5, ST_DONE=4'd6, ST_EXPORT=4'd7, ST_FAULT=4'd8;

    reg clk, rstn;
    reg table_valid, load_valid, start, commit_ready, export_start, output_ready;
    reg [9:0] table_addr;
    reg signed [15:0] table_data;
    reg [2:0] load_kind;
    reg [11:0] load_addr;
    reg signed [31:0] load_data;
    wire table_ready, table_loaded, load_ready, busy, done, fault;
    wire [31:0] core_cycles;
    wire mac_valid, mac_ready, mac_first, mac_last;
    wire [7:0] mac_mask;
    wire [63:0] mac_activation;
    wire [191:0] mac_weight;
    wire [95:0] mac_bias;
    wire mac_result_valid, mac_result_ready, mac_fault;
    wire [95:0] mac_result;
    wire pp_input_valid, pp_input_ready;
    wire [95:0] pp_acc, pp_multipliers;
    wire [17:0] pp_shifts;
    wire [31:0] pp_post_multiplier;
    wire [5:0] pp_post_shift;
    wire [2:0] pp_mask;
    wire [47:0] pp_tags;
    wire pp_output_valid, scheduler_pp_ready;
    wire signed [15:0] pp_data;
    wire [15:0] pp_tag;
    wire pp_int16, pp_fault;
    wire output_valid, export_done;
    wire signed [7:0] output_data;
    wire [9:0] output_index;

    reg signed [31:0] vector_input[0:3071];
    reg [7:0] vector_weight[0:2303];
    reg signed [31:0] vector_bias[0:23];
    reg [31:0] vector_multiplier[0:23];
    reg [7:0] vector_shift[0:23];
    reg [31:0] vector_post[0:1];
    reg signed [31:0] golden_acc[0:383];
    reg signed [15:0] golden_pre[0:383];
    reg signed [15:0] golden_silu[0:383];
    reg signed [7:0] golden_post[0:383];
    reg signed [15:0] silu_table[0:1023];
    reg signed [7:0] reconstructed[0:1535];
    reg signed [7:0] reconstructed_golden[0:1535];

    integer ticks, index, lane, output_lane, expected_index, global_index, slab_id;
    integer report_fd, mac_groups, mac_finals, pp_batches, pre_count, silu_count, post_count;
    integer commit_count, commit_stall_cycles, export_count, export_stall_cycles, observed_core_cycles;
    integer prepare_cycles, send_accept_cycles, send_stall_cycles;
    integer mac_wait_accept_cycles, mac_wait_cycles, drain_cycles, advance_cycles;
    integer raw_pre_busy_cycles, raw_silu_busy_cycles, raw_post_busy_cycles;
    integer load_window_start_tick, load_window_cycles, export_window_start_tick, export_window_cycles;
    integer stage_slot, stage_lane, stage_tag, state_hits, successful_cases;
    integer reset_cases, malformed_cases, reconstructed_count;
    reg track_numeric, track_export, random_commit, random_output, output_was_stalled;
    reg [9:0] held_output_index;
    reg signed [7:0] held_output_data;
    reg [31:0] lfsr;
    reg [8*1024-1:0] vector_root, vector_file, vector_prefix, report_path;

    road_pw_tile_scheduler #(.PROFILE(PROFILE)) dut(
        .i_clk(clk),.i_rstn(rstn),.i_table_loaded(table_loaded),
        .i_load_valid(load_valid),.i_load_kind(load_kind),.i_load_addr(load_addr),.i_load_data(load_data),.o_load_ready(load_ready),
        .i_start(start),.o_busy(busy),.o_done(done),.o_fault(fault),.o_core_cycles(core_cycles),
        .o_mac_valid(mac_valid),.i_mac_ready(mac_ready),.o_mac_first(mac_first),.o_mac_last(mac_last),
        .o_mac_mask(mac_mask),.o_mac_activation(mac_activation),.o_mac_weight(mac_weight),.o_mac_bias(mac_bias),
        .i_mac_result_valid(mac_result_valid),.o_mac_result_ready(mac_result_ready),.i_mac_result(mac_result),.i_mac_fault(mac_fault),
        .o_pp_valid(pp_input_valid),.i_pp_ready(pp_input_ready),.o_pp_acc(pp_acc),.o_pp_multipliers(pp_multipliers),
        .o_pp_shifts(pp_shifts),.o_pp_post_multiplier(pp_post_multiplier),.o_pp_post_shift(pp_post_shift),
        .o_pp_mask(pp_mask),.o_pp_tags(pp_tags),.i_pp_valid(pp_output_valid),.o_pp_ready(scheduler_pp_ready),
        .i_pp_data(pp_data),.i_pp_tag(pp_tag),.i_pp_int16(pp_int16),.i_pp_fault(pp_fault),
        .i_commit_ready(commit_ready),.i_export_start(export_start),.o_output_valid(output_valid),.i_output_ready(output_ready),
        .o_output_data(output_data),.o_output_index(output_index),.o_export_done(export_done)
    );

    road_mac_probe u_mac(
        .i_clk(clk),.i_rstn(rstn),.i_input_valid(mac_valid),.o_input_ready(mac_ready),
        .i_first(mac_first),.i_last(mac_last),.i_lane_mask(mac_mask),
        .i_activation_data(mac_activation),.i_weight_data(mac_weight),.i_bias_data(mac_bias),
        .i_result_ready(mac_result_ready),.o_result_valid(mac_result_valid),.o_result_data(mac_result),.o_fault(mac_fault)
    );

    road_dynamic_postprocess u_pp(
        .i_clk(clk),.i_rstn(rstn),.i_table_valid(table_valid),.i_table_addr(table_addr),.i_table_data(table_data),
        .o_table_ready(table_ready),.o_table_loaded(table_loaded),.i_input_valid(pp_input_valid),.o_input_ready(pp_input_ready),
        .i_accumulators(pp_acc),.i_pre_multipliers(pp_multipliers),.i_pre_shifts(pp_shifts),
        .i_post_multiplier(pp_post_multiplier),.i_post_shift(pp_post_shift),.i_activate(1'b1),
        .i_lane_mask(pp_mask),.i_tags(pp_tags),.i_input_fault(1'b0),.i_output_ready(scheduler_pp_ready),
        .o_output_valid(pp_output_valid),.o_output_data(pp_data),.o_output_tag(pp_tag),.o_output_int16(pp_int16),.o_fault(pp_fault),
        .o_queue_count(),.o_pending_count(),.o_meta_count(),.o_pre_busy(),.o_silu_busy(),.o_post_busy(),
        .o_pre_accept(),.o_silu_accept(),.o_post_accept()
    );

    always #5 clk=~clk;

    always @(posedge clk)begin
        ticks=ticks+1;
        if(ticks>800000)$fatal(1,"PW deep watchdog timeout profile=%0d",PROFILE);
        if(rstn)lfsr<={lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};

        if(rstn && busy)begin
            observed_core_cycles=observed_core_cycles+1;
            state_hits=0;
            case(dut.state_current)
                ST_PREPARE:begin prepare_cycles=prepare_cycles+1; state_hits=state_hits+1; end
                ST_SEND:begin
                    state_hits=state_hits+1;
                    if(mac_valid && mac_ready)send_accept_cycles=send_accept_cycles+1;
                    else send_stall_cycles=send_stall_cycles+1;
                end
                ST_MAC_WAIT:begin
                    state_hits=state_hits+1;
                    if(mac_result_valid && mac_result_ready)mac_wait_accept_cycles=mac_wait_accept_cycles+1;
                    else mac_wait_cycles=mac_wait_cycles+1;
                end
                ST_DRAIN:begin drain_cycles=drain_cycles+1; state_hits=state_hits+1; end
                ST_ADVANCE:begin advance_cycles=advance_cycles+1; state_hits=state_hits+1; end
                default:state_hits=0;
            endcase
            if(state_hits!=1)$fatal(1,"PW deep non-exclusive core cause state=%0d profile=%0d",dut.state_current,PROFILE);
        end

        if(rstn && track_numeric)begin
            if(u_pp.o_pre_busy)raw_pre_busy_cycles=raw_pre_busy_cycles+1;
            if(u_pp.o_silu_busy)raw_silu_busy_cycles=raw_silu_busy_cycles+1;
            if(u_pp.o_post_busy)raw_post_busy_cycles=raw_post_busy_cycles+1;
        end

        if(rstn && track_numeric && mac_valid && mac_ready)begin
            mac_groups=mac_groups+1;
            expected_index=dut.cnt_position*CIN+dut.cnt_group*8;
            if(mac_first !== (dut.cnt_group==0) || mac_last !== (dut.cnt_group==GROUPS-1) || mac_mask!==8'hff)
                $fatal(1,"PW deep MAC boundary p=%0d og=%0d g=%0d",dut.cnt_position,dut.cnt_output_group,dut.cnt_group);
            for(lane=0;lane<8;lane=lane+1)begin
                if($signed(mac_activation[lane*8+:8]) !== $signed(vector_input[expected_index+lane][7:0]))
                    $fatal(1,"PW deep input bank map p=%0d g=%0d lane=%0d",dut.cnt_position,dut.cnt_group,lane);
                for(output_lane=0;output_lane<3;output_lane=output_lane+1)
                    if(mac_weight[(output_lane*8+lane)*8+:8] !==
                       vector_weight[(dut.cnt_output_group*3+output_lane)*CIN+dut.cnt_group*8+lane])
                        $fatal(1,"PW deep weight bank map og=%0d g=%0d ol=%0d il=%0d",
                               dut.cnt_output_group,dut.cnt_group,output_lane,lane);
            end
            for(output_lane=0;output_lane<3;output_lane=output_lane+1)
                if($signed(mac_bias[output_lane*32+:32]) !== $signed(vector_bias[dut.cnt_output_group*3+output_lane]))
                    $fatal(1,"PW deep bias snapshot og=%0d lane=%0d",dut.cnt_output_group,output_lane);
        end

        if(rstn && track_numeric && mac_result_valid && mac_result_ready)begin
            mac_finals=mac_finals+1;
            expected_index=dut.cnt_position*COUT+dut.cnt_output_group*3;
            for(lane=0;lane<3;lane=lane+1)
                if($signed(mac_result[lane*32+:32]) !== $signed(golden_acc[expected_index+lane]))
                    $fatal(1,"PW deep accumulator tag=%0d got=%0d expected=%0d",expected_index+lane,
                           $signed(mac_result[lane*32+:32]),$signed(golden_acc[expected_index+lane]));
        end

        if(rstn && track_numeric && pp_input_valid && pp_input_ready)begin
            pp_batches=pp_batches+1;
            expected_index=dut.cnt_position*COUT+dut.cnt_output_group*3;
            for(lane=0;lane<3;lane=lane+1)begin
                if(pp_tags[lane*16+:16] !== expected_index+lane ||
                   pp_multipliers[lane*32+:32] !== vector_multiplier[dut.cnt_output_group*3+lane] ||
                   pp_shifts[lane*6+:6] !== vector_shift[dut.cnt_output_group*3+lane][5:0])
                    $fatal(1,"PW deep coefficient/tag snapshot tag=%0d lane=%0d",expected_index+lane,lane);
            end
            if(pp_post_multiplier!==vector_post[0] || pp_post_shift!==vector_post[1][5:0] || pp_mask!==3'b111)
                $fatal(1,"PW deep common post coefficient mismatch");
        end

        if(rstn && track_numeric && u_pp.flag_pre_complete)begin
            stage_slot=u_pp.pre_result_tag[4:2]; stage_lane=u_pp.pre_result_tag[1:0];
            stage_tag=(u_pp.reg_retire_tags[stage_slot]>>(stage_lane*16)) & 16'hffff;
            if(stage_tag<0 || stage_tag>=OUTPUT_WORDS || $signed(u_pp.pre_result_data)!==$signed(golden_pre[stage_tag]))
                $fatal(1,"PW deep pre stage tag=%0d got=%0d",stage_tag,$signed(u_pp.pre_result_data));
            pre_count=pre_count+1;
        end
        if(rstn && track_numeric && u_pp.flag_post_accept)begin
            stage_slot=u_pp.reg_meta_tags[u_pp.reg_meta_read][4:2];
            stage_lane=u_pp.reg_meta_tags[u_pp.reg_meta_read][1:0];
            stage_tag=(u_pp.reg_retire_tags[stage_slot]>>(stage_lane*16)) & 16'hffff;
            if(stage_tag<0 || stage_tag>=OUTPUT_WORDS || $signed(u_pp.silu_output_data)!==$signed(golden_silu[stage_tag]))
                $fatal(1,"PW deep SiLU stage tag=%0d got=%0d",stage_tag,$signed(u_pp.silu_output_data));
            silu_count=silu_count+1;
        end
        if(rstn && track_numeric && u_pp.flag_post_complete)begin
            stage_slot=u_pp.post_result_tag[4:2]; stage_lane=u_pp.post_result_tag[1:0];
            stage_tag=(u_pp.reg_retire_tags[stage_slot]>>(stage_lane*16)) & 16'hffff;
            if(stage_tag<0 || stage_tag>=OUTPUT_WORDS || $signed(u_pp.wire_post_saturated)!==$signed(golden_post[stage_tag]))
                $fatal(1,"PW deep post stage tag=%0d got=%0d",stage_tag,$signed(u_pp.wire_post_saturated));
            post_count=post_count+1;
        end

        if(rstn && track_numeric && pp_output_valid && scheduler_pp_ready)begin
            if(pp_tag!==commit_count || pp_int16 || $signed(pp_data)!==$signed(golden_post[commit_count]))
                $fatal(1,"PW deep commit tag=%0d expected=%0d data=%0d expected_data=%0d",
                       pp_tag,commit_count,$signed(pp_data),$signed(golden_post[commit_count]));
            if(PROFILE==2)begin
                global_index=(commit_count/COUT)*96+slab_id*COUT+(commit_count%COUT);
                reconstructed[global_index]=pp_data[7:0];
                reconstructed_golden[global_index]=golden_post[commit_count];
                reconstructed_count=reconstructed_count+1;
            end
            commit_count=commit_count+1;
        end else if(rstn && track_numeric && pp_output_valid)commit_stall_cycles=commit_stall_cycles+1;
        if(rstn && track_numeric && done && commit_count!=OUTPUT_WORDS)
            $fatal(1,"PW deep done before all commits count=%0d expected=%0d",commit_count,OUTPUT_WORDS);

        if(rstn && track_export && output_valid && output_ready)begin
            if(output_index!==export_count || $signed(output_data)!==$signed(golden_post[export_count]))
                $fatal(1,"PW deep export index=%0d expected=%0d data=%0d expected_data=%0d",
                       output_index,export_count,$signed(output_data),$signed(golden_post[export_count]));
            export_count=export_count+1;
        end else if(rstn && track_export && output_valid)export_stall_cycles=export_stall_cycles+1;
        if(rstn && output_was_stalled && (!output_valid || output_index!==held_output_index || output_data!==held_output_data))
            $fatal(1,"PW deep export payload changed under stall");
        output_was_stalled=rstn && output_valid && !output_ready;
        if(output_was_stalled)begin held_output_index=output_index; held_output_data=output_data; end
    end

    always @(negedge clk)begin
        if(random_commit)commit_ready=lfsr[0] || lfsr[3];
        if(random_output)output_ready=lfsr[1] || lfsr[5];
    end

    task read_slab;
        input integer selected_slab;
        begin
            if(PROFILE==1)$sformat(vector_prefix,"p96_squeeze");
            else $sformat(vector_prefix,"p192_slice%02d",selected_slab);
            $sformat(vector_file,"%0s/%0s_input.hex",vector_root,vector_prefix); $readmemh(vector_file,vector_input);
            $sformat(vector_file,"%0s/%0s_weights.hex",vector_root,vector_prefix); $readmemh(vector_file,vector_weight);
            $sformat(vector_file,"%0s/%0s_bias.hex",vector_root,vector_prefix); $readmemh(vector_file,vector_bias);
            $sformat(vector_file,"%0s/%0s_pre_multiplier.hex",vector_root,vector_prefix); $readmemh(vector_file,vector_multiplier);
            $sformat(vector_file,"%0s/%0s_pre_shift.hex",vector_root,vector_prefix); $readmemh(vector_file,vector_shift);
            $sformat(vector_file,"%0s/%0s_post_params.hex",vector_root,vector_prefix); $readmemh(vector_file,vector_post);
            $sformat(vector_file,"%0s/%0s_acc.hex",vector_root,vector_prefix); $readmemh(vector_file,golden_acc);
            $sformat(vector_file,"%0s/%0s_pre.hex",vector_root,vector_prefix); $readmemh(vector_file,golden_pre);
            $sformat(vector_file,"%0s/%0s_silu.hex",vector_root,vector_prefix); $readmemh(vector_file,golden_silu);
            $sformat(vector_file,"%0s/%0s_post.hex",vector_root,vector_prefix); $readmemh(vector_file,golden_post);
        end
    endtask

    task reset_dut;
        begin
            @(negedge clk); rstn=1'b0; table_valid=1'b0; load_valid=1'b0; start=1'b0; export_start=1'b0;
            random_commit=1'b0; random_output=1'b0; commit_ready=1'b1; output_ready=1'b1; track_numeric=1'b0; track_export=1'b0;
            #1;
            if(busy || done || fault || table_loaded || output_valid || export_done || dut.state_current!=ST_IDLE ||
               dut.reg_loaded!=0 || dut.cnt_written!=0 || dut.flag_tile_valid || dut.flag_load_pending ||
               u_pp.reg_ingress_count!=0 || u_pp.reg_retire_count!=0 || u_pp.reg_meta_count!=0)
                $fatal(1,"PW deep reset retained ownership profile=%0d",PROFILE);
            repeat(2)@(negedge clk); rstn=1'b1; repeat(2)@(posedge clk); #1;
            if(fault || busy || table_loaded || !load_ready)$fatal(1,"PW deep reset release invalid profile=%0d",PROFILE);
            reset_cases=reset_cases+1;
        end
    endtask

    task load_table_full;
        begin
            for(index=0;index<1024;index=index+1)begin
                @(negedge clk); table_valid=1'b1; table_addr=index; table_data=silu_table[index]; #1;
                if(!table_ready)$fatal(1,"PW deep table rejected address=%0d",index);
            end
            @(negedge clk); table_valid=1'b0; @(posedge clk); #1;
            if(!table_loaded || pp_fault)$fatal(1,"PW deep table failed to complete");
        end
    endtask

    task load_word;
        input [2:0] kind;
        input integer address;
        input [31:0] value;
        begin
            @(negedge clk); load_valid=1'b1; load_kind=kind; load_addr=address; load_data=value; #1;
            if(!load_ready)$fatal(1,"PW deep load rejected kind=%0d address=%0d",kind,address);
            @(posedge clk);
        end
    endtask

    task stop_load;
        begin @(negedge clk); load_valid=1'b0; end
    endtask

    task load_case_and_start;
        begin
            load_window_start_tick=ticks;
            for(index=0;index<INPUT_WORDS;index=index+1)load_word(3'd0,index,vector_input[index]);
            for(index=0;index<COUT;index=index+1)load_word(3'd3,index,vector_bias[index]);
            for(index=0;index<COUT;index=index+1)load_word(3'd4,index,vector_multiplier[index]);
            for(index=0;index<COUT;index=index+1)load_word(3'd5,index,{24'd0,vector_shift[index]});
            load_word(3'd6,0,vector_post[0]); load_word(3'd6,1,vector_post[1]);
            for(index=0;index<2304;index=index+1)load_word(3'd2,index,{{24{vector_weight[index][7]}},vector_weight[index]});
            @(negedge clk); load_valid=1'b0; start=1'b1; #1;
            if(!dut.flag_load_pending || dut.reg_pending_bank!=5'd23 || dut.reg_pending_address!=9'd95)
                $fatal(1,"PW deep final weight pending mismatch bank=%0d row=%0d",dut.reg_pending_bank,dut.reg_pending_address);
            @(posedge clk); #1;
            if(!busy || dut.weight_banks[23].reg_cache[95]!==vector_weight[2303])
                $fatal(1,"PW deep final weight commit/start overlap failed");
            load_window_cycles=ticks-load_window_start_tick;
            @(negedge clk); start=1'b0;
        end
    endtask

    task clear_case_counters;
        begin
            mac_groups=0; mac_finals=0; pp_batches=0; pre_count=0; silu_count=0; post_count=0;
            commit_count=0; commit_stall_cycles=0; export_count=0; export_stall_cycles=0; observed_core_cycles=0;
            prepare_cycles=0; send_accept_cycles=0; send_stall_cycles=0;
            mac_wait_accept_cycles=0; mac_wait_cycles=0; drain_cycles=0; advance_cycles=0;
            raw_pre_busy_cycles=0; raw_silu_busy_cycles=0; raw_post_busy_cycles=0;
            load_window_start_tick=0; load_window_cycles=0; export_window_start_tick=0; export_window_cycles=0;
        end
    endtask

    task export_case;
        input enable_random;
        begin
            track_export=1'b1; random_output=enable_random; output_ready=1'b1;
            wait(dut.state_current==ST_IDLE);
            export_window_start_tick=ticks;
            @(negedge clk); export_start=1'b1; @(negedge clk); export_start=1'b0;
            wait(export_done); @(negedge clk); random_output=1'b0; output_ready=1'b1; track_export=1'b0;
            export_window_cycles=ticks-export_window_start_tick;
            if(export_count!=OUTPUT_WORDS || dut.flag_tile_valid)
                $fatal(1,"PW deep export incomplete count=%0d expected=%0d",export_count,OUTPUT_WORDS);
            if(enable_random && export_stall_cycles==0)$fatal(1,"PW deep random export stall missing");
        end
    endtask

    task run_slab;
        input integer selected_slab;
        input integer stall_mode;
        begin
            slab_id=selected_slab; read_slab(selected_slab); clear_case_counters; track_numeric=1'b1;
            random_commit=(stall_mode==1); commit_ready=(stall_mode==2 || stall_mode==3)?1'b0:1'b1;
            load_case_and_start;
            if(stall_mode==2 || stall_mode==3)begin
                wait(u_pp.reg_retire_count==4'd8 && pp_output_valid);
                for(index=0;index<512;index=index+1)begin
                    @(posedge clk); #1;
                    if(u_pp.reg_retire_count!=4'd8 || scheduler_pp_ready || !busy || dut.cnt_written!=0)
                        $fatal(1,"PW deep 512-cycle queue-full escaped cycle=%0d",index);
                end
                @(negedge clk); commit_ready=1'b1; random_commit=(stall_mode==3);
            end
            wait(done); #1; random_commit=1'b0; commit_ready=1'b1;
            if(mac_groups!=TASKS*GROUPS || mac_finals!=TASKS || pp_batches!=TASKS ||
               pre_count!=OUTPUT_WORDS || silu_count!=OUTPUT_WORDS || post_count!=OUTPUT_WORDS ||
               commit_count!=OUTPUT_WORDS || dut.cnt_written!=OUTPUT_WORDS || !dut.flag_tile_valid)
                $fatal(1,"PW deep endpoint slab=%0d groups=%0d finals=%0d batches=%0d stages=%0d/%0d/%0d commits=%0d",
                       selected_slab,mac_groups,mac_finals,pp_batches,pre_count,silu_count,post_count,commit_count);
            if(core_cycles!=observed_core_cycles ||
               observed_core_cycles!=prepare_cycles+send_accept_cycles+send_stall_cycles+
               mac_wait_accept_cycles+mac_wait_cycles+drain_cycles+advance_cycles)
                $fatal(1,"PW deep core classification core=%0d observed=%0d sum=%0d",core_cycles,observed_core_cycles,
                       prepare_cycles+send_accept_cycles+send_stall_cycles+mac_wait_accept_cycles+mac_wait_cycles+drain_cycles+advance_cycles);
            if(send_accept_cycles!=TASKS*GROUPS || mac_wait_accept_cycles!=TASKS || advance_cycles!=TASKS)
                $fatal(1,"PW deep FSM endpoint send=%0d mac=%0d advance=%0d",send_accept_cycles,mac_wait_accept_cycles,advance_cycles);
            if((stall_mode==2 || stall_mode==3) && commit_stall_cycles<512)
                $fatal(1,"PW deep commit stall accounting=%0d",commit_stall_cycles);
            export_case(stall_mode==1 || stall_mode==3); track_numeric=1'b0; successful_cases=successful_cases+1;
            $fwrite(report_fd,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    PROFILE,selected_slab,stall_mode,load_window_cycles,core_cycles,export_window_cycles,
                    raw_pre_busy_cycles,raw_silu_busy_cycles,raw_post_busy_cycles,prepare_cycles,send_accept_cycles,
                    send_stall_cycles,mac_wait_accept_cycles,mac_wait_cycles,drain_cycles,advance_cycles,
                    commit_count,commit_stall_cycles,export_count,export_stall_cycles);
        end
    endtask

    task prepare_current_slab;
        begin load_table_full; clear_case_counters; track_numeric=1'b0; commit_ready=1'b1; load_case_and_start; end
    endtask

    initial begin
        clk=1'b0; rstn=1'b0; table_valid=1'b0; load_valid=1'b0; start=1'b0; commit_ready=1'b1;
        export_start=1'b0; output_ready=1'b1; table_addr=0; table_data=0; load_kind=0; load_addr=0; load_data=0;
        ticks=0; lfsr=32'h6d2b79f5; track_numeric=1'b0; track_export=1'b0; random_commit=1'b0; random_output=1'b0;
        output_was_stalled=1'b0; successful_cases=0; reset_cases=0; malformed_cases=0; reconstructed_count=0;
        slab_id=0; o_test_done=1'b0; clear_case_counters;
        if(PROFILE!=1 && PROFILE!=2)$fatal(1,"tb_pw_deep PROFILE must be 1 or 2");
        if(!$value$plusargs("VECTORS=%s",vector_root))vector_root=".";
        if(!$value$plusargs("REPORT=%s",report_path))report_path="tb_pw_deep_cycles.csv";
        report_fd=$fopen(report_path,"w");
        if(report_fd==0)$fatal(1,"PW deep cannot open REPORT=%0s",report_path);
        $fwrite(report_fd,"profile,slab,stall_mode,load_window_cycles,core_cycles,export_window_cycles,raw_pre_busy,raw_silu_busy,raw_post_busy,prepare,send_accept,send_stall,mac_wait_accept,mac_wait,drain,advance,commits,commit_stall,exports,export_stall\n");
        $sformat(vector_file,"%0s/silu_table.hex",vector_root); $readmemh(vector_file,silu_table);
        read_slab(0);

        repeat(3)@(negedge clk); rstn=1'b1; repeat(2)@(posedge clk);

        // 部分输入装载和部分SiLU表均由复位取消。
        load_word(3'd0,0,32'd7); load_word(3'd0,1,-32'sd8); stop_load; reset_dut;
        load_word(3'd0,INPUT_WORDS,32'd1); stop_load; repeat(2)@(posedge clk); #1;
        if(!fault || done || output_valid || dut.flag_tile_valid)$fatal(1,"PW deep malformed input boundary did not fail closed");
        malformed_cases=malformed_cases+1; reset_dut;
        for(index=0;index<37;index=index+1)begin
            @(negedge clk); table_valid=1'b1; table_addr=index; table_data=silu_table[index]; #1;
            if(!table_ready)$fatal(1,"PW deep partial table rejected address=%0d",index);
        end
        @(negedge clk); table_valid=1'b0; reset_dut; load_table_full;

        if(PROFILE==1)run_slab(0,3);
        else begin
            for(slab_id=0;slab_id<SLABS;slab_id=slab_id+1)begin
                if(slab_id==0)run_slab(slab_id,1);
                else if(slab_id==1)run_slab(slab_id,2);
                else run_slab(slab_id,0);
            end
            if(reconstructed_count!=1536)$fatal(1,"PW192 reconstruction count=%0d",reconstructed_count);
            for(index=0;index<1536;index=index+1)
                if($signed(reconstructed[index])!==$signed(reconstructed_golden[index]))
                    $fatal(1,"PW192 reconstructed output mismatch global=%0d",index);
        end

        // 最后任务末输入组接受后复位，不能遗留MAC或发布状态。
        slab_id=0; read_slab(0); reset_dut; prepare_current_slab;
        wait(dut.state_current==ST_SEND && dut.cnt_position==15 &&
             dut.cnt_output_group==OUTPUT_GROUPS-1 && dut.cnt_group==GROUPS-1 && mac_valid && mac_ready);
        reset_dut;

        // PP任一阶段活动时复位，所有队列和完整表状态取消。
        read_slab(0); prepare_current_slab;
        wait(u_pp.o_pre_busy || u_pp.o_silu_busy || u_pp.o_post_busy); reset_dut;

        // 最后MAC结果故障必须进入FAULT且禁止tile发布。
        read_slab(0); prepare_current_slab;
        wait(dut.state_current==ST_MAC_WAIT && dut.cnt_position==15 &&
             dut.cnt_output_group==OUTPUT_GROUPS-1 && mac_result_valid);
        force mac_fault=1'b1; @(posedge clk); #1; release mac_fault; repeat(2)@(posedge clk); #1;
        if(!fault || dut.state_current!=ST_FAULT || dut.flag_tile_valid || done || output_valid || export_done)
            $fatal(1,"PW deep final MAC fault published a tile");

        if(successful_cases!=SLABS || malformed_cases!=1 || reset_cases!=6)
            $fatal(1,"PW deep coverage cases=%0d/%0d malformed=%0d resets=%0d",successful_cases,SLABS,malformed_cases,reset_cases);
        $fclose(report_fd); o_test_done=1'b1;
        $display("TB_PASS_PW_DEEP profile=%0d slabs=%0d cin=%0d cout=%0d groups=%0d tasks=%0d output_words=%0d all_acc_pre_silu_post_commit_export=checked random_stalls=1 queue_full_stall=512 reconstruction=%0d malformed_boundary=1 reset_partial_load_table_last_group_pp=1 final_mac_fault=1",
                 PROFILE,SLABS,CIN,COUT,GROUPS,TASKS,OUTPUT_WORDS,(PROFILE==2));
        $finish;
    end
endmodule

module tb_pw_deep96;
    wire test_done;
    tb_pw_deep #(.PROFILE(1)) u_test(.o_test_done(test_done));
endmodule

module tb_pw_deep192;
    wire test_done;
    tb_pw_deep #(.PROFILE(2)) u_test(.o_test_done(test_done));
endmodule
