`timescale 1ns / 1ps

// CSP2首个残差单元的真实QAT因果链及独立饱和向量自检。
module tb_csp_first_probe(output reg o_test_complete);
    localparam integer NORMAL_GROUPS = 320;
    localparam integer NORMAL_TASKS = 160;
    localparam integer NORMAL_OUTPUTS = 384;
    localparam integer SAT_GROUPS = 12;
    localparam integer SAT_TASKS = 6;
    localparam integer SAT_OUTPUTS = 16;
    localparam [31:0] DW_BASE = 32'd56532992;
    localparam [31:0] RESIDUAL_BASE = 32'd56643584;

    reg clk;
    reg rstn;
    reg table_valid;
    reg [9:0] table_addr;
    reg signed [15:0] table_data;
    wire table_ready;
    wire table_loaded;
    reg input_valid;
    reg input_first;
    reg input_last;
    reg [7:0] input_mask;
    reg [63:0] input_activation;
    reg [191:0] input_weight;
    reg [95:0] input_bias;
    wire input_ready;
    reg [2:0] output_mask;
    reg [47:0] input_tags;
    reg [95:0] input_addresses;
    reg [95:0] input_pre_multipliers;
    reg [17:0] input_pre_shifts;
    reg [31:0] input_post_multiplier;
    reg [5:0] input_post_shift;
    reg input_residual;
    reg [23:0] input_bypass;
    reg input_fault;
    reg output_ready;
    wire output_valid;
    wire signed [7:0] output_data;
    wire [15:0] output_tag;
    wire [31:0] output_address;
    wire signed [8:0] output_sum;
    wire fault;

    reg [63:0] group_activation[0:NORMAL_GROUPS-1];
    reg [191:0] group_weight[0:NORMAL_GROUPS-1];
    reg [95:0] group_bias[0:NORMAL_GROUPS-1];
    reg [7:0] group_mask[0:NORMAL_GROUPS-1];
    reg [7:0] group_first[0:NORMAL_GROUPS-1];
    reg [7:0] group_last[0:NORMAL_GROUPS-1];
    reg [127:0] group_halo_indices[0:NORMAL_GROUPS-1];
    reg [47:0] task_tags[0:NORMAL_TASKS-1];
    reg [95:0] task_addresses[0:NORMAL_TASKS-1];
    reg [95:0] task_pre_multiplier[0:NORMAL_TASKS-1];
    reg [23:0] task_pre_shift[0:NORMAL_TASKS-1];
    reg [31:0] task_post_multiplier[0:NORMAL_TASKS-1];
    reg [7:0] task_post_shift[0:NORMAL_TASKS-1];
    reg [7:0] task_mask[0:NORMAL_TASKS-1];
    reg [7:0] task_residual[0:NORMAL_TASKS-1];
    reg [47:0] task_bypass_indices[0:NORMAL_TASKS-1];
    reg [127:0] input_words[0:95];
    reg [31:0] input_native_addresses[0:95];
    reg [31:0] halo_native_addresses[0:431];
    reg [7:0] halo_byte_lanes[0:431];
    reg [31:0] bypass_native_addresses[0:191];
    reg [7:0] bypass_byte_lanes[0:191];

    reg signed [31:0] golden_dw_acc[0:191];
    reg signed [15:0] golden_dw_pre[0:191];
    reg signed [15:0] golden_dw_silu[0:191];
    reg signed [7:0] golden_dw_post[0:191];
    reg signed [31:0] golden_pw_acc[0:191];
    reg signed [15:0] golden_pw_pre[0:191];
    reg signed [15:0] golden_pw_silu[0:191];
    reg signed [7:0] golden_pw_post[0:191];
    reg signed [15:0] golden_residual_sum[0:191];
    reg signed [7:0] golden_residual_post[0:191];
    reg [127:0] golden_dw_words[0:11];
    reg [127:0] golden_residual_words[0:11];
    reg signed [7:0] golden_halo[0:431];
    reg signed [7:0] golden_bypass[0:191];
    reg signed [15:0] silu_table[0:1023];

    reg [63:0] sat_group_activation[0:SAT_GROUPS-1];
    reg [191:0] sat_group_weight[0:SAT_GROUPS-1];
    reg [95:0] sat_group_bias[0:SAT_GROUPS-1];
    reg [7:0] sat_group_mask[0:SAT_GROUPS-1];
    reg [7:0] sat_group_first[0:SAT_GROUPS-1];
    reg [7:0] sat_group_last[0:SAT_GROUPS-1];
    reg [47:0] sat_task_tags[0:SAT_TASKS-1];
    reg [95:0] sat_task_addresses[0:SAT_TASKS-1];
    reg [95:0] sat_task_pre_multiplier[0:SAT_TASKS-1];
    reg [23:0] sat_task_pre_shift[0:SAT_TASKS-1];
    reg [31:0] sat_task_post_multiplier[0:SAT_TASKS-1];
    reg [7:0] sat_task_post_shift[0:SAT_TASKS-1];
    reg [7:0] sat_task_mask[0:SAT_TASKS-1];
    reg [7:0] sat_task_residual[0:SAT_TASKS-1];
    reg [23:0] sat_task_bypass[0:SAT_TASKS-1];
    reg signed [31:0] sat_acc[0:SAT_OUTPUTS-1];
    reg signed [15:0] sat_pre[0:SAT_OUTPUTS-1];
    reg signed [15:0] sat_silu[0:SAT_OUTPUTS-1];
    reg signed [7:0] sat_post[0:SAT_OUTPUTS-1];
    reg signed [15:0] sat_sum[0:SAT_OUTPUTS-1];
    reg signed [7:0] sat_output[0:SAT_OUTPUTS-1];
    reg [127:0] sat_word[0:0];

    reg signed [7:0] actual_dw[0:191];
    reg signed [7:0] actual_residual[0:191];
    reg signed [7:0] actual_sat[0:15];
    reg seen_dw[0:191];
    reg seen_residual[0:191];
    reg seen_sat[0:15];
    reg seen_acc[0:399];
    reg seen_pre[0:399];
    reg seen_silu[0:399];
    reg seen_post[0:399];
    reg seen_sum[0:399];

    integer test_case;
    integer generation;
    integer cycles;
    integer run_start_cycle;
    integer group_count;
    integer task_count;
    integer context_count;
    integer output_count;
    integer acc_count;
    integer pre_count;
    integer silu_count;
    integer post_count;
    integer sum_count;
    integer input_bubble_count;
    integer output_stall_count;
    integer metadata_poison_count;
    integer admission_block_count;
    integer partial_table_count;
    integer lane;
    integer case_task_index;
    integer stage_tag;
    reg track_numeric;
    reg expect_fault;
    reg random_output;
    reg output_was_stalled;
    reg signed [7:0] held_output_data;
    reg [15:0] held_output_tag;
    reg [31:0] held_output_address;
    reg signed [8:0] held_output_sum;
    reg [31:0] lfsr;
    reg [8*1024-1:0] vector_root;
    reg [8*1024-1:0] vector_file;

    road_csp_first_probe dut(
        .i_clk(clk),.i_rstn(rstn),
        .i_table_valid(table_valid),.i_table_addr(table_addr),.i_table_data(table_data),
        .o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .i_input_valid(input_valid),.i_first(input_first),.i_last(input_last),
        .i_lane_mask(input_mask),.i_activation_data(input_activation),.i_weight_data(input_weight),
        .i_bias_data(input_bias),.o_input_ready(input_ready),.i_output_mask(output_mask),
        .i_tags(input_tags),.i_addresses(input_addresses),.i_pre_multipliers(input_pre_multipliers),
        .i_pre_shifts(input_pre_shifts),.i_post_multiplier(input_post_multiplier),
        .i_post_shift(input_post_shift),.i_residual(input_residual),.i_bypass_data(input_bypass),
        .i_input_fault(input_fault),.i_output_ready(output_ready),.o_output_valid(output_valid),
        .o_output_data(output_data),.o_output_tag(output_tag),.o_output_address(output_address),
        .o_output_sum(output_sum),.o_fault(fault)
    );

    initial begin
        forever #5 clk = ~clk;
    end

    function [7:0] read_input_byte;
        input [31:0] native_address;
        input [7:0] byte_lane;
        integer search_index;
        integer matches;
        begin
            read_input_byte = 8'hxx;
            matches = 0;
            if (byte_lane > 8'd15) $fatal(1,"CSP input byte lane out of range lane=%0d",byte_lane);
            for (search_index=0;search_index<96;search_index=search_index+1) begin
                if (input_native_addresses[search_index] == native_address) begin
                    read_input_byte = input_words[search_index][byte_lane*8 +: 8];
                    matches = matches + 1;
                end
            end
            if (matches != 1)
                $fatal(1,"CSP native address lookup address=%0d matches=%0d",native_address,matches);
        end
    endfunction

    task check_accumulator;
        input integer tag_value;
        input signed [31:0] actual_value;
        begin
            if (tag_value < 0 || tag_value > 399 || seen_acc[tag_value])
                $fatal(1,"CSP accumulator tag duplicate/range tag=%0d",tag_value);
            if (test_case == 9 || test_case == 15) begin
                if (tag_value < 384 || tag_value > 399 || actual_value !== sat_acc[tag_value-384])
                    $fatal(1,"CSP SAT accumulator tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 192) begin
                if (actual_value !== golden_dw_acc[tag_value])
                    $fatal(1,"CSP DW accumulator tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 384) begin
                if (actual_value !== golden_pw_acc[tag_value-192])
                    $fatal(1,"CSP PW accumulator tag=%0d got=%0d",tag_value,actual_value);
            end else $fatal(1,"CSP normal accumulator tag out of range tag=%0d",tag_value);
            seen_acc[tag_value] = 1'b1;
            acc_count = acc_count + 1;
        end
    endtask

    task check_pre;
        input integer tag_value;
        input signed [15:0] actual_value;
        begin
            if (tag_value < 0 || tag_value > 399 || seen_pre[tag_value])
                $fatal(1,"CSP PRE tag duplicate/range tag=%0d",tag_value);
            if (test_case == 9 || test_case == 15) begin
                if (tag_value < 384 || tag_value > 399 || actual_value !== sat_pre[tag_value-384])
                    $fatal(1,"CSP SAT PRE tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 192) begin
                if (actual_value !== golden_dw_pre[tag_value])
                    $fatal(1,"CSP DW PRE tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 384) begin
                if (actual_value !== golden_pw_pre[tag_value-192])
                    $fatal(1,"CSP PW PRE tag=%0d got=%0d",tag_value,actual_value);
            end else $fatal(1,"CSP normal PRE tag out of range tag=%0d",tag_value);
            seen_pre[tag_value] = 1'b1;
            pre_count = pre_count + 1;
        end
    endtask

    task check_silu;
        input integer tag_value;
        input signed [15:0] actual_value;
        begin
            if (tag_value < 0 || tag_value > 399 || seen_silu[tag_value])
                $fatal(1,"CSP SiLU tag duplicate/range tag=%0d",tag_value);
            if (test_case == 9 || test_case == 15) begin
                if (tag_value < 384 || tag_value > 399 || actual_value !== sat_silu[tag_value-384])
                    $fatal(1,"CSP SAT SiLU tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 192) begin
                if (actual_value !== golden_dw_silu[tag_value])
                    $fatal(1,"CSP DW SiLU tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 384) begin
                if (actual_value !== golden_pw_silu[tag_value-192])
                    $fatal(1,"CSP PW SiLU tag=%0d got=%0d",tag_value,actual_value);
            end else $fatal(1,"CSP normal SiLU tag out of range tag=%0d",tag_value);
            seen_silu[tag_value] = 1'b1;
            silu_count = silu_count + 1;
        end
    endtask

    task check_post;
        input integer tag_value;
        input signed [15:0] actual_value;
        begin
            if (tag_value < 0 || tag_value > 399 || seen_post[tag_value])
                $fatal(1,"CSP POST tag duplicate/range tag=%0d",tag_value);
            if (test_case == 9 || test_case == 15) begin
                if (tag_value < 384 || tag_value > 399 || actual_value !== $signed(sat_post[tag_value-384]))
                    $fatal(1,"CSP SAT POST tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 192) begin
                if (actual_value !== $signed(golden_dw_post[tag_value]))
                    $fatal(1,"CSP DW POST tag=%0d got=%0d",tag_value,actual_value);
            end else if (tag_value < 384) begin
                if (actual_value !== $signed(golden_pw_post[tag_value-192]))
                    $fatal(1,"CSP PW POST tag=%0d got=%0d",tag_value,actual_value);
            end else $fatal(1,"CSP normal POST tag out of range tag=%0d",tag_value);
            seen_post[tag_value] = 1'b1;
            post_count = post_count + 1;
        end
    endtask

    always @(posedge clk) begin
        cycles = cycles + 1;
        if (cycles > 500000) $fatal(1,"CSP watchdog timeout case=%0d",test_case);
        if (rstn) lfsr = {lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};

        if (rstn && track_numeric && input_valid && input_ready) begin
            group_count = group_count + 1;
            if (input_last) task_count = task_count + 1;
        end

        if (rstn && track_numeric && dut.flag_acc_accept) begin
            context_count = context_count + 1;
            for (lane=0;lane<3;lane=lane+1) begin
                if (dut.reg_output_mask[lane]) begin
                    stage_tag = (dut.reg_tags >> (lane*16)) & 16'hffff;
                    check_accumulator(stage_tag,$signed(dut.mac_data[lane*32 +: 32]));
                end
            end
        end

        if (rstn && track_numeric && dut.u_pp.flag_silu_accept) begin
            stage_tag = (dut.u_pp.reg_retire_tags[dut.u_pp.pre_result_tag[4:2]] >>
                         (dut.u_pp.pre_result_tag[1:0]*16)) & 16'hffff;
            check_pre(stage_tag,$signed(dut.u_pp.pre_result_data));
        end

        if (rstn && track_numeric && dut.u_pp.flag_post_accept) begin
            stage_tag = (dut.u_pp.reg_retire_tags[dut.u_pp.reg_meta_tags[dut.u_pp.reg_meta_read][4:2]] >>
                         (dut.u_pp.reg_meta_tags[dut.u_pp.reg_meta_read][1:0]*16)) & 16'hffff;
            check_silu(stage_tag,$signed(dut.u_pp.silu_output_data));
        end

        if (rstn && track_numeric && dut.u_pp.flag_post_complete) begin
            stage_tag = (dut.u_pp.reg_retire_tags[dut.u_pp.post_result_tag[4:2]] >>
                         (dut.u_pp.post_result_tag[1:0]*16)) & 16'hffff;
            check_post(stage_tag,$signed(dut.u_pp.wire_post_saturated));
        end

        if (rstn && track_numeric && dut.flag_pp_accept && dut.pp_tag >= 16'd192) begin
            stage_tag = dut.pp_tag;
            if (stage_tag > 399 || seen_sum[stage_tag])
                $fatal(1,"CSP residual sum duplicate/range tag=%0d",stage_tag);
            if (test_case == 9 || test_case == 15) begin
                if (stage_tag < 384 || $signed(dut.wire_sum) !== $signed(sat_sum[stage_tag-384]) ||
                    $signed(dut.wire_saturated) !== $signed(sat_output[stage_tag-384]))
                    $fatal(1,"CSP SAT fused result tag=%0d sum=%0d output=%0d",
                           stage_tag,$signed(dut.wire_sum),$signed(dut.wire_saturated));
            end else begin
                if (stage_tag >= 384 || $signed(dut.wire_sum) !== $signed(golden_residual_sum[stage_tag-192]) ||
                    $signed(dut.wire_saturated) !== $signed(golden_residual_post[stage_tag-192]))
                    $fatal(1,"CSP residual result tag=%0d sum=%0d output=%0d",
                           stage_tag,$signed(dut.wire_sum),$signed(dut.wire_saturated));
            end
            seen_sum[stage_tag] = 1'b1;
            sum_count = sum_count + 1;
        end

        if (rstn && expect_fault && output_valid)
            $fatal(1,"CSP expected-fault case published output tag=%0d",output_tag);

        if (rstn && track_numeric && output_valid && output_ready) begin
            if (test_case == 9 || test_case == 15) begin
                if (output_tag < 384 || output_tag > 399 || seen_sat[output_tag-384])
                    $fatal(1,"CSP SAT output duplicate/range tag=%0d",output_tag);
                if (output_address !== RESIDUAL_BASE+(output_tag-384) ||
                    output_data !== sat_output[output_tag-384] ||
                    $signed({{7{output_sum[8]}},output_sum}) !== $signed(sat_sum[output_tag-384]))
                    $fatal(1,"CSP SAT output mismatch tag=%0d",output_tag);
                actual_sat[output_tag-384] = output_data;
                seen_sat[output_tag-384] = 1'b1;
            end else if (output_tag < 192) begin
                if (seen_dw[output_tag] || output_address !== DW_BASE+output_tag ||
                    output_data !== golden_dw_post[output_tag] ||
                    $signed(output_sum) !== $signed(golden_dw_post[output_tag]))
                    $fatal(1,"CSP DW output mismatch tag=%0d address=%0d data=%0d",
                           output_tag,output_address,$signed(output_data));
                actual_dw[output_tag] = output_data;
                seen_dw[output_tag] = 1'b1;
            end else if (output_tag < 384) begin
                if (seen_residual[output_tag-192] || output_address !== RESIDUAL_BASE+(output_tag-192) ||
                    output_data !== golden_residual_post[output_tag-192] ||
                    $signed({{7{output_sum[8]}},output_sum}) !== $signed(golden_residual_sum[output_tag-192]))
                    $fatal(1,"CSP residual output mismatch tag=%0d address=%0d data=%0d",
                           output_tag,output_address,$signed(output_data));
                actual_residual[output_tag-192] = output_data;
                seen_residual[output_tag-192] = 1'b1;
            end else $fatal(1,"CSP normal output tag out of range tag=%0d",output_tag);
            output_count = output_count + 1;
        end else if (rstn && track_numeric && output_valid) output_stall_count = output_stall_count + 1;

        if (rstn && output_was_stalled &&
            (!output_valid || output_data !== held_output_data || output_tag !== held_output_tag ||
             output_address !== held_output_address || output_sum !== held_output_sum))
            $fatal(1,"CSP output payload changed under backpressure");
        output_was_stalled = rstn && output_valid && !output_ready;
        if (output_was_stalled) begin
            held_output_data = output_data;
            held_output_tag = output_tag;
            held_output_address = output_address;
            held_output_sum = output_sum;
        end
    end

    always @(negedge clk) begin
        if (random_output && rstn) output_ready = lfsr[0] || lfsr[3];
    end

    task read_normal_vectors;
        begin
            $sformat(vector_file,"%0s/group_activation.hex",vector_root); $readmemh(vector_file,group_activation);
            $sformat(vector_file,"%0s/group_weight.hex",vector_root); $readmemh(vector_file,group_weight);
            $sformat(vector_file,"%0s/group_bias.hex",vector_root); $readmemh(vector_file,group_bias);
            $sformat(vector_file,"%0s/group_mask.hex",vector_root); $readmemh(vector_file,group_mask);
            $sformat(vector_file,"%0s/group_first.hex",vector_root); $readmemh(vector_file,group_first);
            $sformat(vector_file,"%0s/group_last.hex",vector_root); $readmemh(vector_file,group_last);
            $sformat(vector_file,"%0s/group_halo_indices.hex",vector_root); $readmemh(vector_file,group_halo_indices);
            $sformat(vector_file,"%0s/task_tags.hex",vector_root); $readmemh(vector_file,task_tags);
            $sformat(vector_file,"%0s/task_addresses.hex",vector_root); $readmemh(vector_file,task_addresses);
            $sformat(vector_file,"%0s/task_pre_multiplier.hex",vector_root); $readmemh(vector_file,task_pre_multiplier);
            $sformat(vector_file,"%0s/task_pre_shift.hex",vector_root); $readmemh(vector_file,task_pre_shift);
            $sformat(vector_file,"%0s/task_post_multiplier.hex",vector_root); $readmemh(vector_file,task_post_multiplier);
            $sformat(vector_file,"%0s/task_post_shift.hex",vector_root); $readmemh(vector_file,task_post_shift);
            $sformat(vector_file,"%0s/task_mask.hex",vector_root); $readmemh(vector_file,task_mask);
            $sformat(vector_file,"%0s/task_residual.hex",vector_root); $readmemh(vector_file,task_residual);
            $sformat(vector_file,"%0s/task_bypass_indices.hex",vector_root); $readmemh(vector_file,task_bypass_indices);
            $sformat(vector_file,"%0s/input_words.hex",vector_root); $readmemh(vector_file,input_words);
            $sformat(vector_file,"%0s/input_native_addresses.hex",vector_root); $readmemh(vector_file,input_native_addresses);
            $sformat(vector_file,"%0s/halo_native_addresses.hex",vector_root); $readmemh(vector_file,halo_native_addresses);
            $sformat(vector_file,"%0s/halo_byte_lanes.hex",vector_root); $readmemh(vector_file,halo_byte_lanes);
            $sformat(vector_file,"%0s/bypass_native_addresses.hex",vector_root); $readmemh(vector_file,bypass_native_addresses);
            $sformat(vector_file,"%0s/bypass_byte_lanes.hex",vector_root); $readmemh(vector_file,bypass_byte_lanes);
            $sformat(vector_file,"%0s/dw_acc.hex",vector_root); $readmemh(vector_file,golden_dw_acc);
            $sformat(vector_file,"%0s/dw_pre.hex",vector_root); $readmemh(vector_file,golden_dw_pre);
            $sformat(vector_file,"%0s/dw_silu.hex",vector_root); $readmemh(vector_file,golden_dw_silu);
            $sformat(vector_file,"%0s/dw_post.hex",vector_root); $readmemh(vector_file,golden_dw_post);
            $sformat(vector_file,"%0s/pw_acc.hex",vector_root); $readmemh(vector_file,golden_pw_acc);
            $sformat(vector_file,"%0s/pw_pre.hex",vector_root); $readmemh(vector_file,golden_pw_pre);
            $sformat(vector_file,"%0s/pw_silu.hex",vector_root); $readmemh(vector_file,golden_pw_silu);
            $sformat(vector_file,"%0s/pw_post.hex",vector_root); $readmemh(vector_file,golden_pw_post);
            $sformat(vector_file,"%0s/residual_sum.hex",vector_root); $readmemh(vector_file,golden_residual_sum);
            $sformat(vector_file,"%0s/residual_post.hex",vector_root); $readmemh(vector_file,golden_residual_post);
            $sformat(vector_file,"%0s/dw_words.hex",vector_root); $readmemh(vector_file,golden_dw_words);
            $sformat(vector_file,"%0s/residual_words.hex",vector_root); $readmemh(vector_file,golden_residual_words);
            $sformat(vector_file,"%0s/halo.hex",vector_root); $readmemh(vector_file,golden_halo);
            $sformat(vector_file,"%0s/bypass.hex",vector_root); $readmemh(vector_file,golden_bypass);
            $sformat(vector_file,"%0s/silu.hex",vector_root); $readmemh(vector_file,silu_table);
        end
    endtask

    task read_sat_vectors;
        begin
            $sformat(vector_file,"%0s/sat_group_activation.hex",vector_root); $readmemh(vector_file,sat_group_activation);
            $sformat(vector_file,"%0s/sat_group_weight.hex",vector_root); $readmemh(vector_file,sat_group_weight);
            $sformat(vector_file,"%0s/sat_group_bias.hex",vector_root); $readmemh(vector_file,sat_group_bias);
            $sformat(vector_file,"%0s/sat_group_mask.hex",vector_root); $readmemh(vector_file,sat_group_mask);
            $sformat(vector_file,"%0s/sat_group_first.hex",vector_root); $readmemh(vector_file,sat_group_first);
            $sformat(vector_file,"%0s/sat_group_last.hex",vector_root); $readmemh(vector_file,sat_group_last);
            $sformat(vector_file,"%0s/sat_task_tags.hex",vector_root); $readmemh(vector_file,sat_task_tags);
            $sformat(vector_file,"%0s/sat_task_addresses.hex",vector_root); $readmemh(vector_file,sat_task_addresses);
            $sformat(vector_file,"%0s/sat_task_pre_multiplier.hex",vector_root); $readmemh(vector_file,sat_task_pre_multiplier);
            $sformat(vector_file,"%0s/sat_task_pre_shift.hex",vector_root); $readmemh(vector_file,sat_task_pre_shift);
            $sformat(vector_file,"%0s/sat_task_post_multiplier.hex",vector_root); $readmemh(vector_file,sat_task_post_multiplier);
            $sformat(vector_file,"%0s/sat_task_post_shift.hex",vector_root); $readmemh(vector_file,sat_task_post_shift);
            $sformat(vector_file,"%0s/sat_task_mask.hex",vector_root); $readmemh(vector_file,sat_task_mask);
            $sformat(vector_file,"%0s/sat_task_residual.hex",vector_root); $readmemh(vector_file,sat_task_residual);
            $sformat(vector_file,"%0s/sat_task_bypass.hex",vector_root); $readmemh(vector_file,sat_task_bypass);
            $sformat(vector_file,"%0s/sat_acc.hex",vector_root); $readmemh(vector_file,sat_acc);
            $sformat(vector_file,"%0s/sat_pre.hex",vector_root); $readmemh(vector_file,sat_pre);
            $sformat(vector_file,"%0s/sat_silu.hex",vector_root); $readmemh(vector_file,sat_silu);
            $sformat(vector_file,"%0s/sat_post.hex",vector_root); $readmemh(vector_file,sat_post);
            $sformat(vector_file,"%0s/sat_sum.hex",vector_root); $readmemh(vector_file,sat_sum);
            $sformat(vector_file,"%0s/sat_output.hex",vector_root); $readmemh(vector_file,sat_output);
            $sformat(vector_file,"%0s/sat_word.hex",vector_root); $readmemh(vector_file,sat_word);
        end
    endtask

    task clear_scoreboard;
        integer clear_index;
        begin
            group_count=0; task_count=0; context_count=0; output_count=0;
            acc_count=0; pre_count=0; silu_count=0; post_count=0; sum_count=0;
            input_bubble_count=0; output_stall_count=0; output_was_stalled=1'b0;
            for(clear_index=0;clear_index<400;clear_index=clear_index+1)begin
                seen_acc[clear_index]=1'b0; seen_pre[clear_index]=1'b0;
                seen_silu[clear_index]=1'b0; seen_post[clear_index]=1'b0; seen_sum[clear_index]=1'b0;
            end
            for(clear_index=0;clear_index<192;clear_index=clear_index+1)begin
                seen_dw[clear_index]=1'b0; seen_residual[clear_index]=1'b0;
                actual_dw[clear_index]=8'sd0; actual_residual[clear_index]=8'sd0;
            end
            for(clear_index=0;clear_index<16;clear_index=clear_index+1)begin
                seen_sat[clear_index]=1'b0; actual_sat[clear_index]=8'sd0;
            end
        end
    endtask

    task reset_dut;
        begin
            @(negedge clk); rstn=1'b0; table_valid=1'b0; input_valid=1'b0;
            input_fault=1'b0; random_output=1'b0; output_ready=1'b0; #1;
            if(output_valid || fault || table_loaded || dut.flag_owned || dut.flag_closed || dut.flag_valid_o ||
               dut.u_mac.o_result_valid || dut.u_mac.o_fault || dut.u_pp.o_pre_busy || dut.u_pp.o_silu_busy ||
               dut.u_pp.o_post_busy || dut.u_pp.reg_ingress_count!=0 || dut.u_pp.reg_retire_count!=0 ||
               dut.u_pp.reg_meta_count!=0)
                $fatal(1,"CSP reset did not clear ownership and arithmetic queues");
            repeat(2)@(negedge clk); rstn=1'b1; output_ready=1'b1;
            repeat(2)@(posedge clk); #1;
            if(output_valid || fault || table_loaded || !table_ready || input_ready || dut.flag_owned)
                $fatal(1,"CSP reset release invalid");
            generation=generation+1;
        end
    endtask

    task load_silu_table;
        integer table_index;
        begin
            for(table_index=0;table_index<1024;table_index=table_index+1)begin
                @(negedge clk); table_valid=1'b1; table_addr=table_index; table_data=silu_table[table_index]; #1;
                if(!table_ready || output_valid || fault)
                    $fatal(1,"CSP SiLU table reload invalid address=%0d",table_index);
                @(posedge clk);
            end
            @(negedge clk); table_valid=1'b0; @(posedge clk); #1;
            if(!table_loaded || fault)$fatal(1,"CSP SiLU table reload failed generation=%0d",generation);
        end
    endtask

    task load_partial_silu_table;
        input integer entry_count;
        integer table_index;
        begin
            for(table_index=0;table_index<entry_count;table_index=table_index+1)begin
                @(negedge clk); table_valid=1'b1; table_addr=table_index; table_data=silu_table[table_index]; #1;
                if(!table_ready || table_loaded || input_ready || output_valid || fault)
                    $fatal(1,"CSP partial SiLU load invalid address=%0d",table_index);
                @(posedge clk);
                partial_table_count=partial_table_count+1;
            end
            @(negedge clk); table_valid=1'b0; #1;
            if(table_loaded || !table_ready || input_ready || output_valid || fault)
                $fatal(1,"CSP partial SiLU load unexpectedly completed entries=%0d",entry_count);
        end
    endtask

    task reset_reload_clear;
        begin
            track_numeric=1'b0; reset_dut; clear_scoreboard; load_silu_table;
            run_start_cycle=cycles; track_numeric=1'b1;
        end
    endtask

    task build_normal_activation;
        input integer task_index;
        input integer group_index;
        output [63:0] activation_value;
        integer activation_lane;
        integer source_index;
        reg [7:0] source_value;
        begin
            activation_value=64'd0;
            for(activation_lane=0;activation_lane<8;activation_lane=activation_lane+1)begin
                source_index=(group_halo_indices[group_index]>>(activation_lane*16))&16'hffff;
                source_value=8'd0;
                if(source_index!=16'hffff)begin
                    if(task_index<96)begin
                        if(source_index>=432)$fatal(1,"CSP halo index out of range group=%0d index=%0d",group_index,source_index);
                        if(halo_native_addresses[source_index]!=32'hffffffff)
                            source_value=read_input_byte(halo_native_addresses[source_index],halo_byte_lanes[source_index]);
                        if(source_value!==golden_halo[source_index])
                            $fatal(1,"CSP halo reconstruction mismatch index=%0d",source_index);
                    end else begin
                        if(source_index>=192 || !seen_dw[source_index])
                            $fatal(1,"CSP PW used uncommitted DW output group=%0d index=%0d",group_index,source_index);
                        source_value=actual_dw[source_index];
                    end
                end
                activation_value[activation_lane*8 +: 8]=source_value;
            end
            if(activation_value!==group_activation[group_index])
                $fatal(1,"CSP packed activation check failed group=%0d causal=%h packed=%h",
                       group_index,activation_value,group_activation[group_index]);
        end
    endtask

    task build_normal_bypass;
        input integer task_index;
        output [23:0] bypass_value;
        integer bypass_lane;
        integer source_index;
        reg [7:0] source_value;
        begin
            bypass_value=24'd0;
            for(bypass_lane=0;bypass_lane<3;bypass_lane=bypass_lane+1)begin
                source_index=(task_bypass_indices[task_index]>>(bypass_lane*16))&16'hffff;
                source_value=8'd0;
                if(source_index!=16'hffff)begin
                    if(source_index>=192)$fatal(1,"CSP bypass index out of range task=%0d index=%0d",task_index,source_index);
                    source_value=read_input_byte(bypass_native_addresses[source_index],bypass_byte_lanes[source_index]);
                    if(source_value!==golden_bypass[source_index])
                        $fatal(1,"CSP bypass reconstruction mismatch index=%0d",source_index);
                end
                bypass_value[bypass_lane*8 +: 8]=source_value;
            end
        end
    endtask

    task apply_normal_group_payload;
        input integer task_index;
        input integer group_in_task;
        integer group_index;
        reg [63:0] causal_activation;
        reg [23:0] causal_bypass;
        begin
            group_index=task_index*2+group_in_task;
            build_normal_activation(task_index,group_index,causal_activation);
            build_normal_bypass(task_index,causal_bypass);
            if(group_first[group_index][0] !== (group_in_task==0) || group_last[group_index][0] !== (group_in_task==1))
                $fatal(1,"CSP first/last vector mismatch group=%0d",group_index);
            input_valid=1'b1; input_first=group_first[group_index][0]; input_last=group_last[group_index][0];
            input_mask=group_mask[group_index]; input_activation=causal_activation;
            input_weight=group_weight[group_index]; input_bias=group_bias[group_index];
            output_mask=task_mask[task_index][2:0]; input_tags=task_tags[task_index];
            input_addresses=task_addresses[task_index]; input_pre_multipliers=task_pre_multiplier[task_index];
            input_pre_shifts=task_pre_shift[task_index][17:0]; input_post_multiplier=task_post_multiplier[task_index];
            input_post_shift=task_post_shift[task_index][5:0]; input_residual=task_residual[task_index][0];
            input_bypass=causal_bypass; input_fault=1'b0;
        end
    endtask

    task poison_normal_metadata;
        input integer task_index;
        input [23:0] causal_bypass;
        begin
            output_mask=~task_mask[task_index][2:0]; input_tags=~task_tags[task_index];
            input_addresses=~task_addresses[task_index]; input_pre_multipliers=~task_pre_multiplier[task_index];
            input_pre_shifts=~task_pre_shift[task_index][17:0];
            input_post_multiplier=~task_post_multiplier[task_index];
            input_post_shift=~task_post_shift[task_index][5:0];
            input_residual=~task_residual[task_index][0]; input_bypass=~causal_bypass; input_fault=1'b1;
        end
    endtask

    task check_latched_normal_metadata;
        input integer task_index;
        reg [23:0] causal_bypass;
        begin
            build_normal_bypass(task_index,causal_bypass);
            if(dut.reg_output_mask !== task_mask[task_index][2:0] || dut.reg_tags !== task_tags[task_index] ||
               dut.reg_addresses !== task_addresses[task_index] ||
               dut.reg_pre_multipliers !== task_pre_multiplier[task_index] ||
               dut.reg_pre_shifts !== task_pre_shift[task_index][17:0] ||
               dut.reg_post_multiplier !== task_post_multiplier[task_index] ||
               dut.reg_post_shift !== task_post_shift[task_index][5:0] ||
               dut.flag_residual !== task_residual[task_index][0] || dut.reg_bypass !== causal_bypass ||
               dut.flag_input_fault !== 1'b0)
                $fatal(1,"CSP first-group metadata changed task=%0d",task_index);
        end
    endtask

    task drive_normal_group;
        input integer task_index;
        input integer group_in_task;
        input integer fault_mode;
        integer bubble_cycles;
        reg [23:0] causal_bypass;
        begin
            build_normal_bypass(task_index,causal_bypass);
            bubble_cycles=0;
            if(test_case==1)bubble_cycles=lfsr[2:1];
            repeat(bubble_cycles)begin @(negedge clk); input_valid=1'b0; input_bubble_count=input_bubble_count+1; end
            @(negedge clk);
            apply_normal_group_payload(task_index,group_in_task);
            input_fault=(fault_mode==6 && group_in_task==0);
            if(test_case==10 && group_in_task==1)poison_normal_metadata(task_index,causal_bypass);
            if(fault_mode==7)begin
                input_mask=8'hff; input_activation=64'h7f7f7f7f7f7f7f7f;
                input_weight={128'd0,64'h7f7f7f7f7f7f7f7f}; input_bias={64'd0,32'h7fffffff};
            end
            if(fault_mode==8)input_pre_shifts[5:0]=6'd63;
            if(fault_mode==12)output_mask=3'd0;
            if(fault_mode==13)begin
                output_mask=3'b011; input_tags={task_tags[task_index][47:32],
                                               task_tags[task_index][15:0],task_tags[task_index][15:0]};
            end
            @(posedge clk); while(!input_ready)@(posedge clk);
            @(negedge clk); input_valid=1'b0; #1;
            if(test_case==10 && group_in_task==1)begin
                check_latched_normal_metadata(task_index);
                metadata_poison_count=metadata_poison_count+1;
            end else input_fault=1'b0;
        end
    endtask

    task drive_normal_task;
        input integer task_index;
        input integer fault_mode;
        begin
            drive_normal_group(task_index,0,fault_mode);
            drive_normal_group(task_index,1,fault_mode);
            if(fault_mode==0)begin
                if(test_case==10)begin
                    output_ready=1'b0; #1;
                    if(input_ready || fault)$fatal(1,"CSP poisoned closed task admitted input task=%0d",task_index);
                    wait(output_valid); @(negedge clk); #1;
                    check_latched_normal_metadata(task_index);
                    if(!output_valid || input_ready || fault)
                        $fatal(1,"CSP poisoned metadata output stall missing task=%0d",task_index);
                    metadata_poison_count=metadata_poison_count+1;
                    repeat(2)begin
                        @(negedge clk); #1;
                        check_latched_normal_metadata(task_index);
                        if(!output_valid || input_ready || fault)
                            $fatal(1,"CSP poisoned metadata escaped stall task=%0d",task_index);
                    end
                    output_ready=1'b1;
                end
                wait(!dut.flag_owned); @(negedge clk);
            end
        end
    endtask

    task drive_all_normal;
        integer task_index;
        begin
            for(task_index=0;task_index<NORMAL_TASKS;task_index=task_index+1)
                drive_normal_task(task_index,0);
        end
    endtask

    task run_admission_negative_checks;
        begin
            @(negedge clk); apply_normal_group_payload(0,0); #1;
            if(input_ready || dut.flag_owned || dut.flag_closed || table_loaded || output_valid || fault || !table_ready)
                $fatal(1,"CSP unloaded table admitted first group");
            @(posedge clk); @(negedge clk); #1;
            if(input_ready || dut.flag_owned || dut.flag_closed || table_loaded || output_valid || fault)
                $fatal(1,"CSP unloaded first attempt changed state");
            input_valid=1'b0; admission_block_count=admission_block_count+1;

            load_silu_table;
            @(negedge clk); apply_normal_group_payload(0,1); input_last=1'b0; #1;
            if(input_ready || dut.flag_owned || dut.flag_closed || !table_loaded || output_valid || fault || !table_ready)
                $fatal(1,"CSP idle non-first group was not blocked");
            @(posedge clk); @(negedge clk); #1;
            if(input_ready || dut.flag_owned || dut.flag_closed || !table_loaded || output_valid || fault)
                $fatal(1,"CSP idle non-first attempt changed state");
            input_valid=1'b0; admission_block_count=admission_block_count+1;

            drive_normal_group(0,0,0);
            check_latched_normal_metadata(0);
            @(negedge clk); apply_normal_group_payload(1,0);
            table_valid=1'b1; table_addr=10'd0; table_data=~silu_table[0]; #1;
            if(input_ready || table_ready || !dut.flag_owned || dut.flag_closed || !table_loaded || output_valid || fault)
                $fatal(1,"CSP owned-open admission gate failed");
            if(dut.u_pp.i_table_valid !== 1'b0)
                $fatal(1,"CSP owned-open table request reached arithmetic core");
            @(posedge clk); @(negedge clk); #1;
            check_latched_normal_metadata(0);
            if(input_ready || table_ready || !dut.flag_owned || dut.flag_closed || !table_loaded || output_valid || fault)
                $fatal(1,"CSP owned-open blocked attempt changed state");
            input_valid=1'b0; table_valid=1'b0; admission_block_count=admission_block_count+1;

            output_ready=1'b0;
            drive_normal_group(0,1,0);
            wait(output_valid); @(negedge clk); apply_normal_group_payload(1,0);
            table_valid=1'b1; table_addr=10'd0; table_data=~silu_table[0]; #1;
            check_latched_normal_metadata(0);
            if(input_ready || table_ready || !dut.flag_owned || !dut.flag_closed || !table_loaded || !output_valid || fault)
                $fatal(1,"CSP closed output-stall admission gate failed");
            if(dut.u_pp.i_table_valid !== 1'b0)
                $fatal(1,"CSP closed table request reached arithmetic core");
            @(posedge clk); @(negedge clk); #1;
            check_latched_normal_metadata(0);
            if(input_ready || table_ready || !dut.flag_owned || !dut.flag_closed || !table_loaded || !output_valid || fault)
                $fatal(1,"CSP closed blocked attempt changed state");
            input_valid=1'b0; table_valid=1'b0; admission_block_count=admission_block_count+1;
        end
    endtask

    task run_partial_table_reset_checks;
        begin
            load_partial_silu_table(257);
            @(negedge clk); apply_normal_group_payload(0,0); #1;
            if(input_ready || dut.flag_owned || dut.flag_closed || table_loaded || output_valid || fault || !table_ready)
                $fatal(1,"CSP partial table admitted work");
            repeat(3)begin
                @(posedge clk); @(negedge clk); #1;
                if(input_ready || dut.flag_owned || dut.flag_closed || table_loaded || output_valid || fault || !table_ready)
                    $fatal(1,"CSP partial table state escaped block");
            end
            input_valid=1'b0; admission_block_count=admission_block_count+1;
        end
    endtask

    task drive_sat_group;
        input integer task_index;
        input integer group_in_task;
        integer group_index;
        begin
            group_index=task_index*2+group_in_task;
            if(sat_group_first[group_index][0] !== (group_in_task==0) || sat_group_last[group_index][0] !== (group_in_task==1))
                $fatal(1,"CSP SAT first/last vector mismatch group=%0d",group_index);
            if(sat_task_mask[task_index][2:0] !== (task_index==5 ? 3'b001 : 3'b111))
                $fatal(1,"CSP SAT output mask mismatch task=%0d",task_index);
            @(negedge clk); input_valid=1'b1; input_first=sat_group_first[group_index][0];
            input_last=sat_group_last[group_index][0]; input_mask=sat_group_mask[group_index];
            input_activation=sat_group_activation[group_index]; input_weight=sat_group_weight[group_index];
            input_bias=sat_group_bias[group_index]; output_mask=sat_task_mask[task_index][2:0];
            input_tags=sat_task_tags[task_index]; input_addresses=sat_task_addresses[task_index];
            input_pre_multipliers=sat_task_pre_multiplier[task_index];
            input_pre_shifts=sat_task_pre_shift[task_index][17:0];
            input_post_multiplier=sat_task_post_multiplier[task_index];
            input_post_shift=sat_task_post_shift[task_index][5:0];
            input_residual=sat_task_residual[task_index][0]; input_bypass=sat_task_bypass[task_index]; input_fault=1'b0;
            @(posedge clk); while(!input_ready)@(posedge clk);
            @(negedge clk); input_valid=1'b0;
        end
    endtask

    task drive_all_sat;
        integer task_index;
        begin
            for(task_index=0;task_index<SAT_TASKS;task_index=task_index+1)begin
                drive_sat_group(task_index,0); drive_sat_group(task_index,1);
                wait(!dut.flag_owned); @(negedge clk);
            end
        end
    endtask

    task check_normal_completion;
        integer check_index;
        integer word_index;
        integer word_lane;
        reg [127:0] packed_word;
        begin
            if(group_count!=NORMAL_GROUPS || task_count!=NORMAL_TASKS || context_count!=NORMAL_TASKS ||
               output_count!=NORMAL_OUTPUTS || acc_count!=NORMAL_OUTPUTS || pre_count!=NORMAL_OUTPUTS ||
               silu_count!=NORMAL_OUTPUTS || post_count!=NORMAL_OUTPUTS || sum_count!=192)
                $fatal(1,"CSP endpoint groups=%0d tasks=%0d contexts=%0d outputs=%0d stages=%0d/%0d/%0d/%0d sums=%0d",
                       group_count,task_count,context_count,output_count,acc_count,pre_count,silu_count,post_count,sum_count);
            for(check_index=0;check_index<384;check_index=check_index+1)
                if(!seen_acc[check_index] || !seen_pre[check_index] || !seen_silu[check_index] || !seen_post[check_index])
                    $fatal(1,"CSP stage coverage hole tag=%0d",check_index);
            for(check_index=0;check_index<192;check_index=check_index+1)
                if(!seen_dw[check_index] || !seen_residual[check_index] || !seen_sum[check_index+192])
                    $fatal(1,"CSP output coverage hole index=%0d",check_index);
            for(word_index=0;word_index<12;word_index=word_index+1)begin
                packed_word=128'd0;
                for(word_lane=0;word_lane<16;word_lane=word_lane+1)
                    packed_word[word_lane*8 +: 8]=actual_dw[word_index*16+word_lane];
                if(packed_word!==golden_dw_words[word_index])
                    $fatal(1,"CSP DW word packing mismatch word=%0d",word_index);
                packed_word=128'd0;
                for(word_lane=0;word_lane<16;word_lane=word_lane+1)
                    packed_word[word_lane*8 +: 8]=actual_residual[word_index*16+word_lane];
                if(packed_word!==golden_residual_words[word_index])
                    $fatal(1,"CSP residual word packing mismatch word=%0d",word_index);
            end
            if(test_case==1 && (input_bubble_count==0 || output_stall_count==0))
                $fatal(1,"CSP random bubble/stall coverage missing input=%0d output=%0d",input_bubble_count,output_stall_count);
            if(test_case==2 && output_stall_count<512)
                $fatal(1,"CSP long output stall coverage=%0d",output_stall_count);
        end
    endtask

    task check_sat_completion;
        integer check_index;
        integer saw_pos_127;
        integer saw_pos_128;
        integer saw_neg_129;
        integer saw_neg_128;
        integer saw_pos_254;
        integer saw_neg_256;
        reg [127:0] packed_word;
        begin
            if(group_count!=SAT_GROUPS || task_count!=SAT_TASKS || context_count!=SAT_TASKS ||
               output_count!=SAT_OUTPUTS || acc_count!=SAT_OUTPUTS || pre_count!=SAT_OUTPUTS ||
               silu_count!=SAT_OUTPUTS || post_count!=SAT_OUTPUTS || sum_count!=SAT_OUTPUTS)
                $fatal(1,"CSP SAT endpoint groups=%0d tasks=%0d contexts=%0d outputs=%0d stages=%0d/%0d/%0d/%0d sums=%0d",
                       group_count,task_count,context_count,output_count,acc_count,pre_count,silu_count,post_count,sum_count);
            packed_word=128'd0;
            saw_pos_127=0; saw_pos_128=0; saw_neg_129=0;
            saw_neg_128=0; saw_pos_254=0; saw_neg_256=0;
            for(check_index=0;check_index<16;check_index=check_index+1)begin
                if(!seen_acc[check_index+384] || !seen_pre[check_index+384] || !seen_silu[check_index+384] ||
                   !seen_post[check_index+384] || !seen_sum[check_index+384] || !seen_sat[check_index])
                    $fatal(1,"CSP SAT coverage hole tag=%0d",check_index+384);
                packed_word[check_index*8 +: 8]=actual_sat[check_index];
                if($signed(sat_sum[check_index])==16'sd127)saw_pos_127=1;
                if($signed(sat_sum[check_index])==16'sd128)saw_pos_128=1;
                if($signed(sat_sum[check_index])==-16'sd129)saw_neg_129=1;
                if($signed(sat_sum[check_index])==-16'sd128)saw_neg_128=1;
                if($signed(sat_sum[check_index])==16'sd254)saw_pos_254=1;
                if($signed(sat_sum[check_index])==-16'sd256)saw_neg_256=1;
            end
            if(packed_word!==sat_word[0])$fatal(1,"CSP SAT beat packing mismatch");
            if(test_case==15 && !(saw_pos_127 && saw_pos_128 && saw_neg_129 &&
                                 saw_neg_128 && saw_pos_254 && saw_neg_256))
                $fatal(1,"CSP SAT boundary vector coverage incomplete");
        end
    endtask

    task finish_normal_pass;
        begin
            check_normal_completion;
            if(test_case==10 && metadata_poison_count!=NORMAL_TASKS*2)
                $fatal(1,"CSP metadata poison coverage=%0d",metadata_poison_count);
            if(test_case==11 && (generation!=2 || admission_block_count!=4))
                $fatal(1,"CSP admission coverage generation=%0d blocks=%0d",generation,admission_block_count);
            if(test_case==14 && (generation!=2 || admission_block_count!=1 || partial_table_count!=257))
                $fatal(1,"CSP partial-table coverage generation=%0d blocks=%0d entries=%0d",
                       generation,admission_block_count,partial_table_count);
            track_numeric=1'b0; o_test_complete=1'b1;
            if(test_case==10 || test_case==11 || test_case==14)
                $display("CSP_FIRST_COVERAGE case=%0d metadata_poison=%0d admission_blocks=%0d partial_entries=%0d",
                         test_case,metadata_poison_count,admission_block_count,partial_table_count);
            $display("CSP_FIRST_PASS case=%0d generation=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d sums=%0d cycles=%0d",
                     test_case,generation,group_count,task_count,output_count,acc_count,pre_count,silu_count,post_count,sum_count,cycles-run_start_cycle);
            $finish;
        end
    endtask

    task finish_expected_fault;
        begin
            if(!fault || output_count!=0 || output_valid)
                $fatal(1,"CSP expected fault missing/leaked case=%0d fault=%0d outputs=%0d valid=%0d",
                       test_case,fault,output_count,output_valid);
            o_test_complete=1'b1;
            $display("CSP_FIRST_EXPECTED_FAULT case=%0d outputs=0",test_case);
            $finish;
        end
    endtask

    initial begin
        clk=1'b0; rstn=1'b0; table_valid=1'b0; table_addr=10'd0; table_data=16'sd0;
        input_valid=1'b0; input_first=1'b0; input_last=1'b0; input_mask=8'd0;
        input_activation=64'd0; input_weight=192'd0; input_bias=96'd0; output_mask=3'd0;
        input_tags=48'd0; input_addresses=96'd0; input_pre_multipliers=96'd0; input_pre_shifts=18'd0;
        input_post_multiplier=32'd0; input_post_shift=6'd0; input_residual=1'b0; input_bypass=24'd0;
        input_fault=1'b0; output_ready=1'b0; o_test_complete=1'b0;
        test_case=0; generation=0; cycles=0; run_start_cycle=0; track_numeric=1'b0; expect_fault=1'b0;
        random_output=1'b0; output_was_stalled=1'b0; lfsr=32'h6d2b79f5; clear_scoreboard;
        metadata_poison_count=0; admission_block_count=0; partial_table_count=0;
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("VECTORS=%s",vector_root))vector_root=".";
        if(test_case<0 || test_case>15)$fatal(1,"CSP unsupported CASE=%0d",test_case);
        read_normal_vectors;
        if(test_case==9 || test_case==15)read_sat_vectors;
        if(test_case==11 || test_case==14)begin
            reset_dut; clear_scoreboard; run_start_cycle=cycles; track_numeric=1'b0;
        end else reset_reload_clear;

        case(test_case)
            0:begin drive_all_normal; finish_normal_pass; end
            1:begin
                random_output=1'b1; drive_all_normal; random_output=1'b0; output_ready=1'b1;
                finish_normal_pass;
            end
            2:begin
                output_ready=1'b0;
                fork
                    begin drive_all_normal; end
                    begin
                        wait(output_valid);
                        repeat(512)begin
                            @(posedge clk); #1;
                            if(!output_valid || !dut.flag_owned || fault)
                                $fatal(1,"CSP long output stall escaped");
                        end
                        @(negedge clk); output_ready=1'b1;
                    end
                join
                finish_normal_pass;
            end
            3:begin
                drive_normal_group(0,0,0);
                if(!dut.flag_owned || dut.flag_closed)$fatal(1,"CSP reset case did not stop after first MAC group");
                reset_reload_clear; drive_all_normal; finish_normal_pass;
            end
            4:begin
                drive_normal_group(0,0,0); drive_normal_group(0,1,0);
                wait(dut.u_pp.flag_silu_accept || dut.u_pp.flag_post_accept || dut.u_pp.flag_post_complete);
                reset_reload_clear; drive_all_normal; finish_normal_pass;
            end
            5:begin
                for(case_task_index=0;case_task_index<159;case_task_index=case_task_index+1)
                    drive_normal_task(case_task_index,0);
                output_ready=1'b0; drive_normal_group(159,0,0); drive_normal_group(159,1,0);
                wait(output_valid); repeat(32)@(posedge clk);
                if(output_tag<16'd192 || !dut.flag_owned)$fatal(1,"CSP late-PW reset point not reached");
                reset_reload_clear; drive_all_normal; finish_normal_pass;
            end
            6:begin
                track_numeric=1'b0; expect_fault=1'b1; drive_normal_task(0,6); wait(fault); repeat(4)@(posedge clk);
                finish_expected_fault;
            end
            7:begin
                track_numeric=1'b0; expect_fault=1'b1; drive_normal_task(0,7); wait(fault); repeat(4)@(posedge clk);
                finish_expected_fault;
            end
            8:begin
                track_numeric=1'b0; expect_fault=1'b1; drive_normal_task(0,8); wait(fault); repeat(4)@(posedge clk);
                finish_expected_fault;
            end
            9:begin
                drive_all_sat; check_sat_completion; track_numeric=1'b0; o_test_complete=1'b1;
                $display("CSP_FIRST_PASS case=%0d generation=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d sums=%0d cycles=%0d",
                         test_case,generation,group_count,task_count,output_count,acc_count,pre_count,silu_count,post_count,sum_count,cycles-run_start_cycle);
                $finish;
            end
            10:begin drive_all_normal; finish_normal_pass; end
            11:begin
                run_admission_negative_checks;
                reset_reload_clear; drive_all_normal; finish_normal_pass;
            end
            12:begin
                track_numeric=1'b0; expect_fault=1'b1; drive_normal_group(0,0,12);
                wait(fault); repeat(4)@(posedge clk); finish_expected_fault;
            end
            13:begin
                track_numeric=1'b0; expect_fault=1'b1; drive_normal_group(0,0,13);
                wait(fault); repeat(4)@(posedge clk); finish_expected_fault;
            end
            14:begin
                run_partial_table_reset_checks;
                reset_reload_clear; drive_all_normal; finish_normal_pass;
            end
            15:begin
                drive_all_sat; check_sat_completion; track_numeric=1'b0; o_test_complete=1'b1;
                $display("CSP_FIRST_PASS case=%0d generation=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d sums=%0d cycles=%0d",
                         test_case,generation,group_count,task_count,output_count,acc_count,pre_count,silu_count,post_count,sum_count,cycles-run_start_cycle);
                $finish;
            end
        endcase
    end
endmodule
