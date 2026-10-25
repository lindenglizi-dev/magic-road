`timescale 1ns / 1ps

// PW48调度、真实MAC/PP及冻结向量的自检；从报告目录运行以读取同级hex文件。
module tb_pw_tile(output reg o_test_done);
    localparam [3:0] ST_IDLE=4'd0, ST_PREPARE=4'd1, ST_SEND=4'd2, ST_MAC_WAIT=4'd3;
    localparam [3:0] ST_DRAIN=4'd4, ST_ADVANCE=4'd5, ST_DONE=4'd6, ST_EXPORT=4'd7, ST_FAULT=4'd8;

    reg clk, rstn;
    reg table_valid, load_valid, start, commit_ready, export_start, output_ready;
    reg [9:0] table_addr;
    reg signed [15:0] table_data;
    reg [2:0] load_kind;
    reg [11:0] load_addr;
    reg signed [31:0] load_data;
    wire table_ready, table_loaded;
    wire load_ready, busy, done, fault;
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
    wire output_valid;
    wire signed [7:0] output_data;
    wire [9:0] output_index;
    wire export_done;

    reg signed [31:0] vector_input[0:767];
    reg [7:0] vector_weight[0:2303];
    reg signed [31:0] vector_bias[0:47];
    reg [31:0] vector_multiplier[0:47];
    reg [7:0] vector_shift[0:47];
    reg [31:0] vector_post[0:1];
    reg signed [31:0] golden_acc[0:767];
    reg signed [15:0] golden_pre[0:767];
    reg signed [15:0] golden_silu[0:767];
    reg signed [7:0] golden_post[0:767];
    reg signed [15:0] silu_table[0:1023];

    integer ticks, index, lane, output_lane, expected_index;
    integer report_fd;
    integer mac_groups, mac_finals, pp_batches, pre_count, silu_count, post_count;
    integer commit_count, commit_stall_cycles, export_count, export_stall_cycles, observed_core_cycles;
    integer prepare_cycles, send_accept_cycles, send_stall_cycles;
    integer mac_wait_accept_cycles, mac_wait_stall_cycles, drain_cycles, advance_cycles;
    integer raw_pre_busy_cycles, raw_silu_busy_cycles, raw_post_busy_cycles;
    integer load_window_start_tick, load_window_cycles, export_window_start_tick, export_window_cycles;
    integer table_entries;
    integer stage_slot, stage_lane, stage_tag, state_hits;
    integer successful_cases, reset_cases, malformed_cases;
    reg track_numeric, track_export, random_commit, random_output;
    reg output_was_stalled;
    reg [9:0] held_output_index;
    reg signed [7:0] held_output_data;
    reg [31:0] lfsr;
    reg [8*1024-1:0] vector_root, vector_file, report_path;

    road_pw_tile_scheduler dut(
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

    always @(posedge clk) begin
        ticks=ticks+1;
        if(ticks>500000)$fatal(1,"PW48 watchdog timeout");
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
                    else mac_wait_stall_cycles=mac_wait_stall_cycles+1;
                end
                ST_DRAIN:begin drain_cycles=drain_cycles+1; state_hits=state_hits+1; end
                ST_ADVANCE:begin advance_cycles=advance_cycles+1; state_hits=state_hits+1; end
                default:state_hits=0;
            endcase
            if(state_hits!=1)$fatal(1,"PW48 busy cycle has non-exclusive FSM cause state=%0d",dut.state_current);
        end

        // 原始PP活动周期可重叠，只作被动观测，不并入上面的互斥调度状态总和。
        if(rstn && track_numeric)begin
            if(u_pp.o_pre_busy)raw_pre_busy_cycles=raw_pre_busy_cycles+1;
            if(u_pp.o_silu_busy)raw_silu_busy_cycles=raw_silu_busy_cycles+1;
            if(u_pp.o_post_busy)raw_post_busy_cycles=raw_post_busy_cycles+1;
        end

        if(rstn && track_numeric && mac_valid && mac_ready)begin
            mac_groups=mac_groups+1;
            expected_index=dut.cnt_position*48+dut.cnt_group*8;
            if(mac_first !== (dut.cnt_group==0) || mac_last !== (dut.cnt_group==5) || mac_mask!==8'hff)
                $fatal(1,"PW48 MAC attributes p=%0d og=%0d g=%0d",dut.cnt_position,dut.cnt_output_group,dut.cnt_group);
            for(lane=0;lane<8;lane=lane+1)begin
                if($signed(mac_activation[lane*8+:8]) !== $signed(vector_input[expected_index+lane][7:0]))
                    $fatal(1,"PW48 activation bank map p=%0d g=%0d lane=%0d",dut.cnt_position,dut.cnt_group,lane);
                for(output_lane=0;output_lane<3;output_lane=output_lane+1)
                    if(mac_weight[(output_lane*8+lane)*8+:8] !==
                       vector_weight[(dut.cnt_output_group*3+output_lane)*48+dut.cnt_group*8+lane])
                        $fatal(1,"PW48 weight bank map og=%0d g=%0d ol=%0d il=%0d",
                               dut.cnt_output_group,dut.cnt_group,output_lane,lane);
            end
            for(output_lane=0;output_lane<3;output_lane=output_lane+1)
                if($signed(mac_bias[output_lane*32+:32]) !== $signed(vector_bias[dut.cnt_output_group*3+output_lane]))
                    $fatal(1,"PW48 bias snapshot og=%0d lane=%0d",dut.cnt_output_group,output_lane);
        end

        if(rstn && track_numeric && mac_result_valid && mac_result_ready)begin
            mac_finals=mac_finals+1;
            expected_index=dut.cnt_position*48+dut.cnt_output_group*3;
            for(lane=0;lane<3;lane=lane+1)
                if($signed(mac_result[lane*32+:32]) !== $signed(golden_acc[expected_index+lane]))
                    $fatal(1,"PW48 MAC final tag=%0d got=%0d expected=%0d",expected_index+lane,
                           $signed(mac_result[lane*32+:32]),$signed(golden_acc[expected_index+lane]));
        end

        if(rstn && track_numeric && pp_input_valid && pp_input_ready)begin
            pp_batches=pp_batches+1;
            expected_index=dut.cnt_position*48+dut.cnt_output_group*3;
            for(lane=0;lane<3;lane=lane+1)begin
                if(pp_tags[lane*16+:16] !== expected_index+lane ||
                   pp_multipliers[lane*32+:32] !== vector_multiplier[dut.cnt_output_group*3+lane] ||
                   pp_shifts[lane*6+:6] !== vector_shift[dut.cnt_output_group*3+lane][5:0])
                    $fatal(1,"PW48 PP snapshot tag=%0d lane=%0d",expected_index+lane,lane);
            end
            if(pp_post_multiplier!==vector_post[0] || pp_post_shift!==vector_post[1][5:0] || pp_mask!==3'b111)
                $fatal(1,"PW48 shared PP parameter snapshot mismatch");
        end

        if(rstn && track_numeric && u_pp.flag_pre_complete)begin
            stage_slot=u_pp.pre_result_tag[4:2]; stage_lane=u_pp.pre_result_tag[1:0];
            stage_tag=(u_pp.reg_retire_tags[stage_slot]>>(stage_lane*16)) & 16'hffff;
            if(stage_tag<0 || stage_tag>=768 || $signed(u_pp.pre_result_data)!==$signed(golden_pre[stage_tag]))
                $fatal(1,"PW48 pre stage tag=%0d got=%0d",stage_tag,$signed(u_pp.pre_result_data));
            pre_count=pre_count+1;
        end
        if(rstn && track_numeric && u_pp.flag_post_accept)begin
            stage_slot=u_pp.reg_meta_tags[u_pp.reg_meta_read][4:2];
            stage_lane=u_pp.reg_meta_tags[u_pp.reg_meta_read][1:0];
            stage_tag=(u_pp.reg_retire_tags[stage_slot]>>(stage_lane*16)) & 16'hffff;
            if(stage_tag<0 || stage_tag>=768 || $signed(u_pp.silu_output_data)!==$signed(golden_silu[stage_tag]))
                $fatal(1,"PW48 SiLU stage tag=%0d got=%0d",stage_tag,$signed(u_pp.silu_output_data));
            silu_count=silu_count+1;
        end
        if(rstn && track_numeric && u_pp.flag_post_complete)begin
            stage_slot=u_pp.post_result_tag[4:2]; stage_lane=u_pp.post_result_tag[1:0];
            stage_tag=(u_pp.reg_retire_tags[stage_slot]>>(stage_lane*16)) & 16'hffff;
            if(stage_tag<0 || stage_tag>=768 || $signed(u_pp.wire_post_saturated)!==$signed(golden_post[stage_tag]))
                $fatal(1,"PW48 post stage tag=%0d got=%0d",stage_tag,$signed(u_pp.wire_post_saturated));
            post_count=post_count+1;
        end

        if(rstn && track_numeric && pp_output_valid && scheduler_pp_ready)begin
            if(pp_tag!==commit_count || pp_int16 || $signed(pp_data)!==$signed(golden_post[commit_count]))
                $fatal(1,"PW48 commit tag=%0d expected=%0d data=%0d expected_data=%0d",
                       pp_tag,commit_count,$signed(pp_data),$signed(golden_post[commit_count]));
            commit_count=commit_count+1;
        end else if(rstn && track_numeric && pp_output_valid)commit_stall_cycles=commit_stall_cycles+1;
        if(rstn && track_numeric && done && commit_count!=768)
            $fatal(1,"PW48 done before 768 commits count=%0d",commit_count);

        if(rstn && track_export && output_valid && output_ready)begin
            if(output_index!==export_count || $signed(output_data)!==$signed(golden_post[export_count]))
                $fatal(1,"PW48 export index=%0d expected=%0d data=%0d expected_data=%0d",
                       output_index,export_count,$signed(output_data),$signed(golden_post[export_count]));
            export_count=export_count+1;
        end else if(rstn && track_export && output_valid)export_stall_cycles=export_stall_cycles+1;
        if(rstn && output_was_stalled && (!output_valid || output_index!==held_output_index || output_data!==held_output_data))
            $fatal(1,"PW48 export payload changed under stall");
        output_was_stalled=rstn && output_valid && !output_ready;
        if(output_was_stalled)begin held_output_index=output_index; held_output_data=output_data; end
    end

    always @(negedge clk)begin
        if(random_commit)commit_ready=lfsr[0] || lfsr[3];
        if(random_output)output_ready=lfsr[1] || lfsr[5];
    end

    task read_case;
        input integer case_id;
        begin
            case(case_id)
                0:begin
                    $sformat(vector_file,"%0s/cls_package_input.hex",vector_root); $readmemh(vector_file,vector_input);
                    $sformat(vector_file,"%0s/cls_package_weights.hex",vector_root); $readmemh(vector_file,vector_weight);
                    $sformat(vector_file,"%0s/cls_package_bias.hex",vector_root); $readmemh(vector_file,vector_bias);
                    $sformat(vector_file,"%0s/cls_package_pre_multiplier.hex",vector_root); $readmemh(vector_file,vector_multiplier);
                    $sformat(vector_file,"%0s/cls_package_pre_shift.hex",vector_root); $readmemh(vector_file,vector_shift);
                    $sformat(vector_file,"%0s/cls_package_post_params.hex",vector_root); $readmemh(vector_file,vector_post);
                    $sformat(vector_file,"%0s/cls_package_acc.hex",vector_root); $readmemh(vector_file,golden_acc);
                    $sformat(vector_file,"%0s/cls_package_pre.hex",vector_root); $readmemh(vector_file,golden_pre);
                    $sformat(vector_file,"%0s/cls_package_silu.hex",vector_root); $readmemh(vector_file,golden_silu);
                    $sformat(vector_file,"%0s/cls_package_post.hex",vector_root); $readmemh(vector_file,golden_post);
                end
                1:begin
                    $sformat(vector_file,"%0s/reg_package_input.hex",vector_root); $readmemh(vector_file,vector_input);
                    $sformat(vector_file,"%0s/reg_package_weights.hex",vector_root); $readmemh(vector_file,vector_weight);
                    $sformat(vector_file,"%0s/reg_package_bias.hex",vector_root); $readmemh(vector_file,vector_bias);
                    $sformat(vector_file,"%0s/reg_package_pre_multiplier.hex",vector_root); $readmemh(vector_file,vector_multiplier);
                    $sformat(vector_file,"%0s/reg_package_pre_shift.hex",vector_root); $readmemh(vector_file,vector_shift);
                    $sformat(vector_file,"%0s/reg_package_post_params.hex",vector_root); $readmemh(vector_file,vector_post);
                    $sformat(vector_file,"%0s/reg_package_acc.hex",vector_root); $readmemh(vector_file,golden_acc);
                    $sformat(vector_file,"%0s/reg_package_pre.hex",vector_root); $readmemh(vector_file,golden_pre);
                    $sformat(vector_file,"%0s/reg_package_silu.hex",vector_root); $readmemh(vector_file,golden_silu);
                    $sformat(vector_file,"%0s/reg_package_post.hex",vector_root); $readmemh(vector_file,golden_post);
                end
                2:begin
                    $sformat(vector_file,"%0s/extrema_channel_scale_input.hex",vector_root); $readmemh(vector_file,vector_input);
                    $sformat(vector_file,"%0s/extrema_channel_scale_weights.hex",vector_root); $readmemh(vector_file,vector_weight);
                    $sformat(vector_file,"%0s/extrema_channel_scale_bias.hex",vector_root); $readmemh(vector_file,vector_bias);
                    $sformat(vector_file,"%0s/extrema_channel_scale_pre_multiplier.hex",vector_root); $readmemh(vector_file,vector_multiplier);
                    $sformat(vector_file,"%0s/extrema_channel_scale_pre_shift.hex",vector_root); $readmemh(vector_file,vector_shift);
                    $sformat(vector_file,"%0s/extrema_channel_scale_post_params.hex",vector_root); $readmemh(vector_file,vector_post);
                    $sformat(vector_file,"%0s/extrema_channel_scale_acc.hex",vector_root); $readmemh(vector_file,golden_acc);
                    $sformat(vector_file,"%0s/extrema_channel_scale_pre.hex",vector_root); $readmemh(vector_file,golden_pre);
                    $sformat(vector_file,"%0s/extrema_channel_scale_silu.hex",vector_root); $readmemh(vector_file,golden_silu);
                    $sformat(vector_file,"%0s/extrema_channel_scale_post.hex",vector_root); $readmemh(vector_file,golden_post);
                end
                default:begin
                    $sformat(vector_file,"%0s/zero_bias_limits_input.hex",vector_root); $readmemh(vector_file,vector_input);
                    $sformat(vector_file,"%0s/zero_bias_limits_weights.hex",vector_root); $readmemh(vector_file,vector_weight);
                    $sformat(vector_file,"%0s/zero_bias_limits_bias.hex",vector_root); $readmemh(vector_file,vector_bias);
                    $sformat(vector_file,"%0s/zero_bias_limits_pre_multiplier.hex",vector_root); $readmemh(vector_file,vector_multiplier);
                    $sformat(vector_file,"%0s/zero_bias_limits_pre_shift.hex",vector_root); $readmemh(vector_file,vector_shift);
                    $sformat(vector_file,"%0s/zero_bias_limits_post_params.hex",vector_root); $readmemh(vector_file,vector_post);
                    $sformat(vector_file,"%0s/zero_bias_limits_acc.hex",vector_root); $readmemh(vector_file,golden_acc);
                    $sformat(vector_file,"%0s/zero_bias_limits_pre.hex",vector_root); $readmemh(vector_file,golden_pre);
                    $sformat(vector_file,"%0s/zero_bias_limits_silu.hex",vector_root); $readmemh(vector_file,golden_silu);
                    $sformat(vector_file,"%0s/zero_bias_limits_post.hex",vector_root); $readmemh(vector_file,golden_post);
                end
            endcase
        end
    endtask

    task reset_dut;
        begin
            @(negedge clk); rstn=1'b0; table_valid=1'b0; load_valid=1'b0; start=1'b0; export_start=1'b0;
            random_commit=1'b0; random_output=1'b0; commit_ready=1'b1; output_ready=1'b1;
            #1;
            if(busy || done || fault || table_loaded || output_valid || export_done || dut.state_current!=ST_IDLE ||
               dut.reg_loaded!=0 || dut.cnt_written!=0 || dut.flag_tile_valid || dut.flag_load_pending ||
               u_pp.reg_ingress_count!=0 || u_pp.reg_retire_count!=0 || u_pp.reg_meta_count!=0)
                $fatal(1,"PW48 reset did not cancel all ownership");
            repeat(2)@(negedge clk); rstn=1'b1; repeat(2)@(posedge clk); #1;
            if(fault || busy || table_loaded || !load_ready)$fatal(1,"PW48 reset release invalid");
            reset_cases=reset_cases+1;
        end
    endtask

    task load_table_full;
        begin
            for(index=0;index<1024;index=index+1)begin
                @(negedge clk); table_valid=1'b1; table_addr=index; table_data=silu_table[index]; #1;
                if(!table_ready)$fatal(1,"PW48 table rejected address=%0d",index);
                table_entries=table_entries+1;
            end
            @(negedge clk); table_valid=1'b0; @(posedge clk); #1;
            if(!table_loaded || pp_fault)$fatal(1,"PW48 table failed to complete");
        end
    endtask

    task load_word;
        input [2:0] kind;
        input integer address;
        input [31:0] value;
        begin
            @(negedge clk); load_valid=1'b1; load_kind=kind; load_addr=address; load_data=value; #1;
            if(!load_ready)$fatal(1,"PW48 load rejected kind=%0d address=%0d",kind,address);
            @(posedge clk);
        end
    endtask

    task stop_load;
        begin @(negedge clk); load_valid=1'b0; end
    endtask

    task check_parameter_word;
        input [2:0] kind;
        input integer address;
        input [31:0] expected;
        integer bank;
        integer row;
        begin
            bank=address%3; row=address/3;
            case(kind)
                3'd3:case(bank)
                    0:if(dut.param_banks[0].reg_bias[row]!==expected)
                        $fatal(1,"PW48 bias bank map address=%0d bank=0 row=%0d",address,row);
                    1:if(dut.param_banks[1].reg_bias[row]!==expected)
                        $fatal(1,"PW48 bias bank map address=%0d bank=1 row=%0d",address,row);
                    default:if(dut.param_banks[2].reg_bias[row]!==expected)
                        $fatal(1,"PW48 bias bank map address=%0d bank=2 row=%0d",address,row);
                endcase
                3'd4:case(bank)
                    0:if(dut.param_banks[0].reg_multiplier[row]!==expected)
                        $fatal(1,"PW48 multiplier bank map address=%0d bank=0 row=%0d",address,row);
                    1:if(dut.param_banks[1].reg_multiplier[row]!==expected)
                        $fatal(1,"PW48 multiplier bank map address=%0d bank=1 row=%0d",address,row);
                    default:if(dut.param_banks[2].reg_multiplier[row]!==expected)
                        $fatal(1,"PW48 multiplier bank map address=%0d bank=2 row=%0d",address,row);
                endcase
                default:$fatal(1,"PW48 unsupported parameter check kind=%0d",kind);
            endcase
        end
    endtask

    task verify_parameter_banks;
        begin
            reset_dut;

            // 两类游标交错前进，地址映射固定为bank=address%3、row=address/3。
            for(index=0;index<48;index=index+1)begin
                load_word(3'd3,index,32'h81000000+index);
                load_word(3'd4,index,32'h01000000+index);
            end
            stop_load; #1;
            if(dut.reg_loaded[3:2]!==2'b11 || dut.cnt_bias_address!=0 || dut.cnt_multiplier_address!=0 ||
               dut.cnt_bias_lane!=0 || dut.cnt_multiplier_lane!=0 || dut.cnt_bias_row!=0 || dut.cnt_multiplier_row!=0)
                $fatal(1,"PW48 parameter boundary47 did not complete/reset both cursors");
            for(index=0;index<48;index=index+1)begin
                check_parameter_word(3'd3,index,32'h81000000+index);
                check_parameter_word(3'd4,index,32'h01000000+index);
            end
            check_parameter_word(3'd3,47,32'h8100002f);
            check_parameter_word(3'd4,47,32'h0100002f);

            // 部分重装后地址0必须覆盖bank0/row0，并把两类独立游标各自重启到地址1。
            load_word(3'd3,0,32'ha5000000); load_word(3'd4,0,32'h05000000);
            load_word(3'd3,1,32'ha5000001); load_word(3'd4,1,32'h05000001);
            load_word(3'd3,2,32'ha5000002); load_word(3'd4,2,32'h05000002);
            load_word(3'd3,3,32'ha5000003); load_word(3'd4,3,32'h05000003);
            load_word(3'd3,0,32'hb5000000); load_word(3'd4,0,32'h06000000);
            stop_load; #1;
            check_parameter_word(3'd3,0,32'hb5000000);
            check_parameter_word(3'd4,0,32'h06000000);
            if(dut.reg_loaded[3:2]!==2'b00 || dut.cnt_bias_address!=1 || dut.cnt_multiplier_address!=1 ||
               dut.cnt_bias_lane!=1 || dut.cnt_multiplier_lane!=1 || dut.cnt_bias_row!=0 || dut.cnt_multiplier_row!=0)
                $fatal(1,"PW48 address-zero parameter restart cursor mismatch");
            load_word(3'd3,1,32'hb5000001); load_word(3'd4,1,32'h06000001); stop_load; #1;
            check_parameter_word(3'd3,1,32'hb5000001);
            check_parameter_word(3'd4,1,32'h06000001);

            // 非期望bias地址置故障，但bias与premul游标及目标bank均不得前进/改写。
            load_word(3'd3,3,32'hdead0003); stop_load; #1;
            if(!fault || dut.cnt_bias_address!=2 || dut.cnt_bias_lane!=2 || dut.cnt_bias_row!=0 ||
               dut.cnt_multiplier_address!=2 || dut.cnt_multiplier_lane!=2 || dut.cnt_multiplier_row!=0)
                $fatal(1,"PW48 invalid bias record advanced a parameter cursor");
            check_parameter_word(3'd3,2,32'ha5000002);
            reset_dut;

            // premul非法记录单独覆盖，证明其故障不借用bias游标。
            load_word(3'd4,0,32'h07000000); load_word(3'd4,1,32'h07000001);
            load_word(3'd4,3,32'h0bad0004); stop_load; #1;
            if(!fault || dut.cnt_bias_address!=0 || dut.cnt_bias_lane!=0 || dut.cnt_bias_row!=0 ||
               dut.cnt_multiplier_address!=2 || dut.cnt_multiplier_lane!=2 || dut.cnt_multiplier_row!=0)
                $fatal(1,"PW48 invalid multiplier record advanced a parameter cursor");
            check_parameter_word(3'd4,2,32'h05000002);
            reset_dut;

            // 参数装载中复位只取消完整性与游标；RAM内容不依赖复位值。
            load_word(3'd3,0,32'hc5000000); load_word(3'd4,0,32'h08000000);
            load_word(3'd3,1,32'hc5000001); load_word(3'd4,1,32'h08000001); stop_load; #1;
            if(dut.cnt_bias_address!=2 || dut.cnt_multiplier_address!=2)
                $fatal(1,"PW48 partial parameter load did not reach reset checkpoint");
            reset_dut;
            if(dut.reg_loaded[3:2]!==2'b00 || dut.cnt_bias_address!=0 || dut.cnt_multiplier_address!=0 ||
               dut.cnt_bias_lane!=0 || dut.cnt_multiplier_lane!=0 || dut.cnt_bias_row!=0 || dut.cnt_multiplier_row!=0)
                $fatal(1,"PW48 reset during parameter load retained cursor/completeness");
        end
    endtask

    task rejected_start;
        begin
            @(negedge clk); start=1'b1; @(posedge clk); #1;
            if(busy || done || fault)$fatal(1,"PW48 incomplete parameters started or faulted");
            @(negedge clk); start=1'b0;
        end
    endtask

    task load_case_and_start;
        input integer check_reload;
        begin
            // 装载窗口从进入task、等待首个load沿之前开始，到末权重提交与start同沿完成为止。
            load_window_start_tick=ticks;
            load_word(3'd0,0,vector_input[0]); stop_load;
            if(check_reload)begin
                #1; if(dut.reg_loaded[0])$fatal(1,"PW48 address-zero reload did not invalidate input class");
                rejected_start;
            end
            for(index=1;index<768;index=index+1)load_word(3'd0,index,vector_input[index]);
            for(index=0;index<48;index=index+1)load_word(3'd3,index,vector_bias[index]);
            for(index=0;index<48;index=index+1)load_word(3'd4,index,vector_multiplier[index]);
            for(index=0;index<48;index=index+1)load_word(3'd5,index,{24'd0,vector_shift[index]});
            load_word(3'd6,0,vector_post[0]); load_word(3'd6,1,vector_post[1]);
            for(index=0;index<2304;index=index+1)load_word(3'd2,index,{{24{vector_weight[index][7]}},vector_weight[index]});
            @(negedge clk); load_valid=1'b0; start=1'b1; #1;
            if(!dut.flag_load_pending || dut.reg_pending_bank!=5'd23 || dut.reg_pending_address!=7'd95)
                $fatal(1,"PW48 final weight was not pending at start boundary");
            @(posedge clk); #1;
            if(!busy || dut.weight_banks[23].reg_cache[95]!==vector_weight[2303])
                $fatal(1,"PW48 final weight commit/start overlap failed");
            load_window_cycles=ticks-load_window_start_tick;
            @(negedge clk); start=1'b0;
        end
    endtask

    task clear_case_counters;
        begin
            mac_groups=0; mac_finals=0; pp_batches=0; pre_count=0; silu_count=0; post_count=0;
            commit_count=0; commit_stall_cycles=0; export_count=0; export_stall_cycles=0; observed_core_cycles=0;
            prepare_cycles=0; send_accept_cycles=0; send_stall_cycles=0;
            mac_wait_accept_cycles=0; mac_wait_stall_cycles=0; drain_cycles=0; advance_cycles=0;
            raw_pre_busy_cycles=0; raw_silu_busy_cycles=0; raw_post_busy_cycles=0;
            load_window_start_tick=0; load_window_cycles=0; export_window_start_tick=0; export_window_cycles=0;
        end
    endtask

    task export_case;
        input enable_random;
        begin
            track_export=1'b1; random_output=enable_random; output_ready=1'b1;
            wait(dut.state_current==ST_IDLE);
            // 导出窗口从发出export命令前的时钟计数快照，到第768项真实握手产生export_done为止。
            export_window_start_tick=ticks;
            @(negedge clk); export_start=1'b1; @(negedge clk); export_start=1'b0;
            wait(export_done); @(negedge clk); random_output=1'b0; output_ready=1'b1; track_export=1'b0;
            export_window_cycles=ticks-export_window_start_tick;
            if(export_count!=768 || dut.flag_tile_valid)$fatal(1,"PW48 export incomplete count=%0d",export_count);
            if(enable_random && export_stall_cycles==0)$fatal(1,"PW48 random export stall coverage missing");
        end
    endtask

    task run_numeric_case;
        input integer case_id;
        input integer stall_mode;
        begin
            read_case(case_id); clear_case_counters; track_numeric=1'b1;
            random_commit=(stall_mode==1); commit_ready=(stall_mode==2)?1'b0:1'b1;
            load_case_and_start(case_id!=0);
            if(stall_mode==2)begin
                wait(u_pp.reg_retire_count==4'd8 && pp_output_valid);
                for(index=0;index<512;index=index+1)begin
                    @(posedge clk); #1;
                    if(u_pp.reg_retire_count!=4'd8 || scheduler_pp_ready || !busy || dut.cnt_written!=0)
                        $fatal(1,"PW48 512-cycle queue-full stall escaped cycle=%0d",index);
                end
                @(negedge clk); commit_ready=1'b1;
            end
            wait(done); #1; random_commit=1'b0; commit_ready=1'b1;
            if(mac_groups!=1536 || mac_finals!=256 || pp_batches!=256 || pre_count!=768 ||
               silu_count!=768 || post_count!=768 || commit_count!=768 || dut.cnt_written!=768 || !dut.flag_tile_valid)
                $fatal(1,"PW48 case=%0d endpoint groups=%0d finals=%0d batches=%0d stages=%0d/%0d/%0d commits=%0d",
                       case_id,mac_groups,mac_finals,pp_batches,pre_count,silu_count,post_count,commit_count);
            if(core_cycles!=observed_core_cycles ||
               observed_core_cycles!=prepare_cycles+send_accept_cycles+send_stall_cycles+
               mac_wait_accept_cycles+mac_wait_stall_cycles+drain_cycles+advance_cycles)
                $fatal(1,"PW48 core counter/classification mismatch core=%0d observed=%0d",core_cycles,observed_core_cycles);
            if(send_accept_cycles!=1536 || mac_wait_accept_cycles!=256 || advance_cycles!=256)
                $fatal(1,"PW48 FSM endpoint send=%0d mac=%0d advance=%0d",send_accept_cycles,mac_wait_accept_cycles,advance_cycles);
            if(stall_mode==2 && commit_stall_cycles<512)$fatal(1,"PW48 commit stall accounting=%0d",commit_stall_cycles);
            export_case(stall_mode==1); track_numeric=1'b0; successful_cases=successful_cases+1;
            $fwrite(report_fd,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                    case_id,stall_mode,table_entries,load_window_cycles,core_cycles,export_window_cycles,
                    raw_pre_busy_cycles,raw_silu_busy_cycles,raw_post_busy_cycles,
                    prepare_cycles,send_accept_cycles,send_stall_cycles,mac_wait_accept_cycles,
                    mac_wait_stall_cycles,drain_cycles,advance_cycles,commit_count,commit_stall_cycles,export_stall_cycles);
        end
    endtask

    task prepare_case_zero;
        begin read_case(0); load_table_full; clear_case_counters; track_numeric=1'b0; commit_ready=1'b1; load_case_and_start(0); end
    endtask

    initial begin
        clk=1'b0; rstn=1'b0; table_valid=1'b0; load_valid=1'b0; start=1'b0; commit_ready=1'b1;
        export_start=1'b0; output_ready=1'b1; table_addr=0; table_data=0; load_kind=0; load_addr=0; load_data=0;
        ticks=0; lfsr=32'h6d2b79f5; track_numeric=1'b0; track_export=1'b0; random_commit=1'b0; random_output=1'b0;
        output_was_stalled=1'b0; successful_cases=0; reset_cases=0; malformed_cases=0; table_entries=0; o_test_done=1'b0; clear_case_counters;
        if(!$value$plusargs("VECTORS=%s",vector_root))vector_root=".";
        if(!$value$plusargs("REPORT=%s",report_path))report_path="tb_pw_tile_cycles.csv";
        report_fd=$fopen(report_path,"w");
        if(report_fd==0)$fatal(1,"PW48 cannot open REPORT=%0s",report_path);
        $fwrite(report_fd,"case_id,stall_mode,table_entries,load_window_cycles,core_cycles,export_window_cycles,raw_pre_busy,raw_silu_busy,raw_post_busy,prepare,send_accept,send_stall,mac_wait_accept,mac_wait_stall,drain,advance,commits,commit_stall,export_stall\n");
        $sformat(vector_file,"%0s/silu_table.hex",vector_root); $readmemh(vector_file,silu_table);

        repeat(3)@(negedge clk); rstn=1'b1; repeat(2)@(posedge clk);

        // 部分动态装载复位，pending写不得越过复位。
        load_word(3'd0,0,32'd7); reset_dut;

        // 不完整参数start无效；不连续/非法kind记录置粘滞故障且不可发布。
        load_word(3'd0,0,32'd1); stop_load; rejected_start;
        load_word(3'd0,2,32'd1); stop_load; repeat(2)@(posedge clk); #1;
        if(!fault || done || output_valid || dut.flag_tile_valid)$fatal(1,"PW48 malformed address did not fail closed");
        malformed_cases=malformed_cases+1; reset_dut;
        load_word(3'd1,0,32'd0); stop_load; repeat(2)@(posedge clk); #1;
        if(!fault || done || output_valid)$fatal(1,"PW48 illegal kind did not fail closed");
        malformed_cases=malformed_cases+1; reset_dut;

        // SiLU表中途复位，完整性必须清零；随后仅装一次完整公共表。
        for(index=0;index<37;index=index+1)begin
            @(negedge clk); table_valid=1'b1; table_addr=index; table_data=silu_table[index]; #1;
            if(!table_ready)$fatal(1,"PW48 partial table rejected address=%0d",index);
        end
        @(negedge clk); table_valid=1'b0; reset_dut; table_entries=0; load_table_full;
        if(table_entries!=1024)$fatal(1,"PW48 successful table entry count=%0d",table_entries);

        // 五次窗口：reg_package保留随机反压，并增加同向量无反压基线。
        run_numeric_case(0,0);
        run_numeric_case(1,0);
        run_numeric_case(1,1);
        run_numeric_case(2,2);
        run_numeric_case(3,0);

        // MAC活动点异步复位。
        reset_dut; prepare_case_zero;
        wait(mac_valid && mac_ready && dut.state_current==ST_SEND); reset_dut;

        // PP pre/SiLU/post活动点复位，所有在途slot和表完整性取消。
        prepare_case_zero;
        wait(u_pp.o_pre_busy || u_pp.o_silu_busy || u_pp.o_post_busy); reset_dut;

        // 最后一任务真实MAC终态注入故障；即使此前已有提交，也不得发布tile。
        prepare_case_zero;
        wait(dut.state_current==ST_MAC_WAIT && dut.cnt_position==15 && dut.cnt_output_group==15 && mac_result_valid);
        force mac_fault=1'b1; @(posedge clk); #1; release mac_fault; repeat(2)@(posedge clk); #1;
        if(!fault || dut.state_current!=ST_FAULT || dut.flag_tile_valid || done || output_valid || export_done)
            $fatal(1,"PW48 final MAC fault published a tile");

        if(successful_cases!=5 || malformed_cases!=2 || reset_cases!=7)
            $fatal(1,"PW48 coverage counters cases=%0d malformed=%0d resets=%0d",successful_cases,malformed_cases,reset_cases);
        verify_parameter_banks;
        $fclose(report_fd);
        o_test_done=1'b1;
        $display("TB_PASS_PW_TILE cases=5 mac_groups_per_case=1536 mac_finals=256 pp_stages=768 commits=768 exports=768 random_stalls=1 queue_full_stall=512 continuous_reload=4 table_entries=1024 raw_pp_busy=reported load_core_export_windows=reported malformed=2 reset_partial_load_table_mac_pp=1_each final_mac_fault=1");
        $display("TB_PASS_PARAMETER_BANKS interleaved_bias_multiplier=48 boundary47=1 address0_restart=2 invalid_no_advance=2 reset_during_load=1");
        $finish;
    end
endmodule
