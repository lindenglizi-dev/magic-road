`timescale 1ns / 1ps

// 固定CSP tile硬件调度、单事务operand provider和真实计算链自检。
module tb_csp_scheduled_chain(output reg o_test_done);
    localparam integer GROUPS = 320;
    localparam integer TASKS = 160;
    localparam integer OUTPUTS = 384;
    localparam [31:0] DW_BASE = 32'd56532992;
    localparam [31:0] RESIDUAL_BASE = 32'd56643584;

    reg clk;
    reg rstn;
    reg start;
    reg table_valid;
    reg [9:0] table_addr;
    reg signed [15:0] table_data;
    wire start_ready;
    wire table_ready;
    wire table_loaded;
    wire busy;
    wire done;
    wire fault;
    wire operand_request_valid;
    reg operand_request_ready;
    wire [24:0] operand_request_descriptor;
    reg operand_response_valid;
    wire operand_response_ready;
    reg [24:0] operand_response_descriptor;
    reg [63:0] operand_activation;
    reg [191:0] operand_weight;
    reg [95:0] operand_bias;
    reg [95:0] operand_pre_multipliers;
    reg [17:0] operand_pre_shifts;
    reg [31:0] operand_post_multiplier;
    reg [5:0] operand_post_shift;
    reg [23:0] operand_bypass;
    reg operand_fault;
    reg result_ready;
    wire result_valid;
    wire signed [7:0] result_data;
    wire [15:0] result_tag;
    wire [31:0] result_address;
    wire signed [8:0] result_sum;
    wire group_accept;
    wire task_commit;
    wire request_accept;
    wire cache_read_accept;
    wire cache_write_accept;
    wire [2:0] cycle_reason;

    reg [63:0] group_activation[0:GROUPS-1];
    reg [191:0] group_weight[0:GROUPS-1];
    reg [95:0] group_bias[0:GROUPS-1];
    reg [7:0] group_mask[0:GROUPS-1];
    reg [7:0] group_first[0:GROUPS-1];
    reg [7:0] group_last[0:GROUPS-1];
    reg [47:0] task_tags[0:TASKS-1];
    reg [95:0] task_addresses[0:TASKS-1];
    reg [95:0] task_pre_multiplier[0:TASKS-1];
    reg [23:0] task_pre_shift[0:TASKS-1];
    reg [31:0] task_post_multiplier[0:TASKS-1];
    reg [7:0] task_post_shift[0:TASKS-1];
    reg [7:0] task_mask[0:TASKS-1];
    reg [7:0] task_residual[0:TASKS-1];
    reg [47:0] task_bypass_indices[0:TASKS-1];
    reg [127:0] input_words[0:95];
    reg [31:0] input_native_addresses[0:95];
    reg [31:0] bypass_native_addresses[0:191];
    reg [7:0] bypass_byte_lanes[0:191];
    reg signed [7:0] golden_bypass[0:191];
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
    reg signed [15:0] silu_table[0:1023];
    reg [24:0] reference_descriptor[0:GROUPS-1];
    reg [47:0] reference_tags[0:TASKS-1];
    reg [95:0] reference_addresses[0:TASKS-1];

    reg signed [7:0] actual_dw[0:191];
    reg signed [7:0] actual_residual[0:191];
    reg seen_output[0:383];
    reg seen_acc[0:383];
    reg seen_pre[0:383];
    reg seen_silu[0:383];
    reg seen_post[0:383];
    reg seen_sum[0:383];
    reg [31:0] reason_count[0:7];
    reg [31:0] reason7_count[0:4];
    reg [31:0] pre_busy_count;
    reg [31:0] silu_busy_count;
    reg [31:0] post_busy_count;
    reg [31:0] table_accept_count;

    integer test_case;
    integer cycles;
    integer tile_number;
    integer request_count;
    integer response_count;
    integer group_count;
    integer commit_count;
    integer output_count;
    integer cache_write_count;
    integer cache_read_count;
    integer acc_count;
    integer pre_count;
    integer silu_count;
    integer post_count;
    integer sum_count;
    integer stall_count;
    integer busy_cycle_count;
    integer lane;
    integer metadata_lane;
    integer stage_tag;
    integer provider_delay;
    integer provider_group;
    integer provider_task;
    reg provider_pending;
    reg [24:0] provider_descriptor;
    reg random_mode;
    reg hold_request;
    reg [24:0] held_request_descriptor;
    reg hold_response;
    reg [24:0] held_response_descriptor;
    reg [63:0] held_response_activation;
    reg [191:0] held_response_weight;
    reg [95:0] held_response_bias;
    reg [95:0] held_response_pre_multipliers;
    reg [17:0] held_response_pre_shifts;
    reg [31:0] held_response_post_multiplier;
    reg [5:0] held_response_post_shift;
    reg [23:0] held_response_bypass;
    reg held_response_fault;
    reg hold_result;
    reg signed [7:0] held_result_data;
    reg [15:0] held_result_tag;
    reg [31:0] held_result_address;
    reg signed [8:0] held_result_sum;
    reg [31:0] lfsr;
    reg acc_moved;
    reg [8*1024-1:0] vector_root;
    reg [8*1024-1:0] reference_root;
    reg [8*1024-1:0] vector_file;

    road_csp_scheduled_chain u_dut(
        .i_clk(clk),.i_rstn(rstn),.i_start(start),
        .i_table_valid(table_valid),.i_table_addr(table_addr),.i_table_data(table_data),
        .o_start_ready(start_ready),.o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .o_busy(busy),.o_done(done),.o_fault(fault),
        .o_operand_request_valid(operand_request_valid),
        .i_operand_request_ready(operand_request_ready),
        .o_operand_request_descriptor(operand_request_descriptor),
        .i_operand_response_valid(operand_response_valid),
        .o_operand_response_ready(operand_response_ready),
        .i_operand_response_descriptor(operand_response_descriptor),
        .i_operand_activation(operand_activation),.i_operand_weight(operand_weight),
        .i_operand_bias(operand_bias),.i_operand_pre_multipliers(operand_pre_multipliers),
        .i_operand_pre_shifts(operand_pre_shifts),.i_operand_post_multiplier(operand_post_multiplier),
        .i_operand_post_shift(operand_post_shift),.i_operand_bypass(operand_bypass),
        .i_operand_fault(operand_fault),.i_result_ready(result_ready),
        .o_result_valid(result_valid),.o_result_data(result_data),.o_result_tag(result_tag),
        .o_result_address(result_address),.o_result_sum(result_sum),
        .o_group_accept(group_accept),.o_task_commit(task_commit),
        .o_request_accept(request_accept),.o_cache_read_accept(cache_read_accept),
        .o_cache_write_accept(cache_write_accept),.o_cycle_reason(cycle_reason)
    );

    always #5 clk = ~clk;

    function [7:0] read_input_byte;
        input [31:0] native_address;
        input [7:0] byte_lane;
        integer search_index;
        integer matches;
        begin
            read_input_byte = 8'hxx;
            matches = 0;
            if (byte_lane > 8'd15) $fatal(1,"scheduled CSP byte lane out of range lane=%0d",byte_lane);
            for (search_index=0;search_index<96;search_index=search_index+1) begin
                if (input_native_addresses[search_index] == native_address) begin
                    read_input_byte = input_words[search_index][byte_lane*8 +: 8];
                    matches = matches + 1;
                end
            end
            if (matches != 1) $fatal(1,"scheduled CSP input lookup address=%0d matches=%0d",native_address,matches);
        end
    endfunction

    task build_normal_bypass;
        input integer task_index;
        output [23:0] bypass_value;
        integer bypass_lane;
        integer source_index;
        reg [7:0] source_value;
        begin
            bypass_value = 24'd0;
            for (bypass_lane=0;bypass_lane<3;bypass_lane=bypass_lane+1) begin
                source_index = (task_bypass_indices[task_index] >> (bypass_lane*16)) & 16'hffff;
                source_value = 8'd0;
                if (source_index != 16'hffff) begin
                    if (source_index >= 192) $fatal(1,"scheduled CSP bypass index task=%0d index=%0d",task_index,source_index);
                    source_value = read_input_byte(bypass_native_addresses[source_index],bypass_byte_lanes[source_index]);
                    if (source_value !== golden_bypass[source_index])
                        $fatal(1,"scheduled CSP bypass reconstruction index=%0d",source_index);
                end
                bypass_value[bypass_lane*8 +: 8] = source_value;
            end
        end
    endtask

    task clear_scoreboard;
        integer clear_index;
        begin
            request_count=0; response_count=0; group_count=0; commit_count=0;
            output_count=0; cache_write_count=0; cache_read_count=0;
            acc_count=0; pre_count=0; silu_count=0; post_count=0; sum_count=0;
            stall_count=0; busy_cycle_count=0;
            pre_busy_count=32'd0; silu_busy_count=32'd0; post_busy_count=32'd0;
            acc_moved=1'b0;
            hold_request=1'b0; hold_response=1'b0; hold_result=1'b0;
            for(clear_index=0;clear_index<384;clear_index=clear_index+1)begin
                seen_output[clear_index]=1'b0; seen_acc[clear_index]=1'b0;
                seen_pre[clear_index]=1'b0; seen_silu[clear_index]=1'b0;
                seen_post[clear_index]=1'b0; seen_sum[clear_index]=1'b0;
            end
            for(clear_index=0;clear_index<192;clear_index=clear_index+1)begin
                actual_dw[clear_index]=8'sd0; actual_residual[clear_index]=8'sd0;
            end
            for(clear_index=0;clear_index<8;clear_index=clear_index+1)reason_count[clear_index]=32'd0;
            for(clear_index=0;clear_index<5;clear_index=clear_index+1)reason7_count[clear_index]=32'd0;
        end
    endtask

    task check_accumulator;
        input integer tag_value;
        input signed [31:0] actual_value;
        begin
            if(tag_value<0 || tag_value>=384 || seen_acc[tag_value])$fatal(1,"scheduled CSP ACC tag=%0d",tag_value);
            if(tag_value<192)begin
                if(actual_value!==golden_dw_acc[tag_value])$fatal(1,"scheduled CSP DW ACC tag=%0d got=%0d",tag_value,actual_value);
            end else if(actual_value!==golden_pw_acc[tag_value-192])
                $fatal(1,"scheduled CSP PW ACC tag=%0d got=%0d",tag_value,actual_value);
            seen_acc[tag_value]=1'b1; acc_count=acc_count+1;
        end
    endtask

    task check_pre;
        input integer tag_value;
        input signed [15:0] actual_value;
        begin
            if(tag_value<0 || tag_value>=384 || seen_pre[tag_value])$fatal(1,"scheduled CSP PRE tag=%0d",tag_value);
            if(tag_value<192)begin
                if(actual_value!==golden_dw_pre[tag_value])$fatal(1,"scheduled CSP DW PRE tag=%0d",tag_value);
            end else if(actual_value!==golden_pw_pre[tag_value-192])$fatal(1,"scheduled CSP PW PRE tag=%0d",tag_value);
            seen_pre[tag_value]=1'b1; pre_count=pre_count+1;
        end
    endtask

    task check_silu;
        input integer tag_value;
        input signed [15:0] actual_value;
        begin
            if(tag_value<0 || tag_value>=384 || seen_silu[tag_value])$fatal(1,"scheduled CSP SILU tag=%0d",tag_value);
            if(tag_value<192)begin
                if(actual_value!==golden_dw_silu[tag_value])$fatal(1,"scheduled CSP DW SILU tag=%0d",tag_value);
            end else if(actual_value!==golden_pw_silu[tag_value-192])$fatal(1,"scheduled CSP PW SILU tag=%0d",tag_value);
            seen_silu[tag_value]=1'b1; silu_count=silu_count+1;
        end
    endtask

    task check_post;
        input integer tag_value;
        input signed [15:0] actual_value;
        begin
            if(tag_value<0 || tag_value>=384 || seen_post[tag_value])$fatal(1,"scheduled CSP POST tag=%0d",tag_value);
            if(tag_value<192)begin
                if(actual_value!==$signed(golden_dw_post[tag_value]))$fatal(1,"scheduled CSP DW POST tag=%0d",tag_value);
            end else if(actual_value!==$signed(golden_pw_post[tag_value-192]))$fatal(1,"scheduled CSP PW POST tag=%0d",tag_value);
            seen_post[tag_value]=1'b1; post_count=post_count+1;
        end
    endtask

    // provider是唯一operand来源；PW activation故意投毒，迫使DUT使用真实DW缓存。
    always @(posedge clk or negedge rstn) begin
        if(!rstn)begin
            operand_request_ready <= 1'b0;
            operand_response_valid <= 1'b0;
            operand_response_descriptor <= 25'd0;
            operand_activation <= 64'd0;
            operand_weight <= 192'd0;
            operand_bias <= 96'd0;
            operand_pre_multipliers <= 96'd0;
            operand_pre_shifts <= 18'd0;
            operand_post_multiplier <= 32'd0;
            operand_post_shift <= 6'd0;
            operand_bypass <= 24'd0;
            operand_fault <= 1'b0;
            provider_pending <= 1'b0;
            provider_descriptor <= 25'd0;
            provider_delay <= 0;
        end else begin
            operand_request_ready <= random_mode ? (lfsr[0] || lfsr[3]) : 1'b1;
            if(operand_response_valid && operand_response_ready)begin
                operand_response_valid <= 1'b0;
                provider_pending <= 1'b0;
            end
            if(operand_request_valid && operand_request_ready)begin
                if(provider_pending || operand_response_valid)$fatal(1,"scheduled CSP provider accepted two requests");
                provider_descriptor <= operand_request_descriptor;
                provider_pending <= 1'b1;
                if(test_case==3 && tile_number==0)provider_delay <= 64;
                else if(random_mode)provider_delay <= lfsr[6:5];
                else provider_delay <= 0;
            end else if(provider_pending && !operand_response_valid)begin
                if(provider_delay!=0)provider_delay <= provider_delay-1;
                else begin
                    provider_task = provider_descriptor[24:17];
                    provider_group = provider_task*2+(provider_descriptor[6] ? 1 : 0);
                    if(provider_task<0 || provider_task>=TASKS || provider_group<0 || provider_group>=GROUPS)
                        $fatal(1,"scheduled CSP provider descriptor range descriptor=%h",provider_descriptor);
                    if(provider_descriptor!==reference_descriptor[provider_group])
                        $fatal(1,"scheduled CSP request order group=%0d got=%h expected=%h",
                               provider_group,provider_descriptor,reference_descriptor[provider_group]);
                    operand_response_descriptor <= (test_case==7 && provider_group==0) ?
                                                   (provider_descriptor^25'd1) : provider_descriptor;
                    operand_activation <= provider_descriptor[16] ? 64'ha55aa55aa55aa55a : group_activation[provider_group];
                    operand_weight <= group_weight[provider_group];
                    operand_bias <= group_bias[provider_group];
                    operand_pre_multipliers <= task_pre_multiplier[provider_task];
                    operand_pre_shifts <= (test_case==5 && provider_task==0) ?
                                          {task_pre_shift[provider_task][17:6],6'd63} :
                                          task_pre_shift[provider_task][17:0];
                    operand_post_multiplier <= task_post_multiplier[provider_task];
                    operand_post_shift <= task_post_shift[provider_task][5:0];
                    build_normal_bypass(provider_task,operand_bypass);
                    operand_fault <= test_case==6 && provider_task==159 && provider_descriptor[7];
                    operand_response_valid <= 1'b1;
                end
            end
        end
    end

    always @(posedge clk) begin
        cycles = cycles+1;
        if(cycles>1500000)$fatal(1,"scheduled CSP watchdog case=%0d",test_case);
        if(rstn)lfsr={lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
        if(rstn && random_mode)result_ready <= lfsr[2] || lfsr[7];

        if(rstn && start && start_ready)begin
            tile_number=tile_number+1;
            clear_scoreboard;
        end
        if(rstn && busy)begin
            if(^cycle_reason===1'bx)$fatal(1,"scheduled CSP cycle reason X");
            reason_count[cycle_reason]=reason_count[cycle_reason]+1'b1;
            busy_cycle_count=busy_cycle_count+1;
            if(cycle_reason==3'd7)begin
                if(u_dut.flag_start_pending)reason7_count[0]=reason7_count[0]+1'b1;
                else if(u_dut.u_compute.flag_acc_accept)reason7_count[1]=reason7_count[1]+1'b1;
                else if(u_dut.u_compute.flag_closed && !acc_moved)reason7_count[2]=reason7_count[2]+1'b1;
                else if(acc_moved && u_dut.u_compute.flag_owned)reason7_count[3]=reason7_count[3]+1'b1;
                else reason7_count[4]=reason7_count[4]+1'b1;
            end
            if(u_dut.u_compute.road_dynamic_postprocess_Inst_core.o_pre_busy)pre_busy_count=pre_busy_count+1'b1;
            if(u_dut.u_compute.road_dynamic_postprocess_Inst_core.o_silu_busy)silu_busy_count=silu_busy_count+1'b1;
            if(u_dut.u_compute.road_dynamic_postprocess_Inst_core.o_post_busy)post_busy_count=post_busy_count+1'b1;
        end
        if(!rstn)table_accept_count=32'd0;
        else if(table_valid && table_ready)table_accept_count=table_accept_count+1'b1;
        if(rstn && request_accept)request_count=request_count+1;
        if(rstn && operand_response_valid && operand_response_ready)response_count=response_count+1;
        if(rstn && group_accept)group_count=group_count+1;
        if(rstn && task_commit)commit_count=commit_count+1;
        if(rstn && cache_write_accept)cache_write_count=cache_write_count+1;
        if(rstn && cache_read_accept)cache_read_count=cache_read_count+1;

        // reason7按本沿之前的事务状态分类，随后才更新acc_moved观察状态。
        if(!rstn)acc_moved=1'b0;
        else begin
            if(group_accept && u_dut.reg_descriptor[7])acc_moved=1'b0;
            if(u_dut.u_compute.flag_acc_accept)acc_moved=1'b1;
        end

        if(rstn && hold_request && (!operand_request_valid || operand_request_descriptor!==held_request_descriptor))
            $fatal(1,"scheduled CSP request changed under backpressure");
        hold_request=rstn && operand_request_valid && !operand_request_ready;
        if(hold_request)held_request_descriptor=operand_request_descriptor;

        if(rstn && hold_response && (!operand_response_valid ||
           operand_response_descriptor!==held_response_descriptor || operand_activation!==held_response_activation ||
           operand_weight!==held_response_weight || operand_bias!==held_response_bias ||
           operand_pre_multipliers!==held_response_pre_multipliers ||
           operand_pre_shifts!==held_response_pre_shifts ||
           operand_post_multiplier!==held_response_post_multiplier ||
           operand_post_shift!==held_response_post_shift || operand_bypass!==held_response_bypass ||
           operand_fault!==held_response_fault))
            $fatal(1,"scheduled CSP provider payload changed under backpressure");
        hold_response=rstn && operand_response_valid && !operand_response_ready;
        if(hold_response)begin
            held_response_descriptor=operand_response_descriptor; held_response_activation=operand_activation;
            held_response_weight=operand_weight; held_response_bias=operand_bias;
            held_response_pre_multipliers=operand_pre_multipliers;
            held_response_pre_shifts=operand_pre_shifts;
            held_response_post_multiplier=operand_post_multiplier;
            held_response_post_shift=operand_post_shift;
            held_response_bypass=operand_bypass; held_response_fault=operand_fault;
        end

        if(rstn && hold_result && (!result_valid || result_data!==held_result_data || result_tag!==held_result_tag ||
           result_address!==held_result_address || result_sum!==held_result_sum))
            $fatal(1,"scheduled CSP result changed under backpressure");
        hold_result=rstn && result_valid && !result_ready;
        if(hold_result)begin
            held_result_data=result_data; held_result_tag=result_tag;
            held_result_address=result_address; held_result_sum=result_sum; stall_count=stall_count+1;
        end

        if(rstn && !fault && u_dut.u_compute.flag_acc_accept)begin
            for(lane=0;lane<3;lane=lane+1)if(u_dut.u_compute.reg_output_mask[lane])begin
                stage_tag=(u_dut.u_compute.reg_tags>>(lane*16))&16'hffff;
                check_accumulator(stage_tag,$signed(u_dut.u_compute.mac_data[lane*32 +: 32]));
            end
        end
        if(rstn && !fault && u_dut.u_compute.road_dynamic_postprocess_Inst_core.flag_silu_accept)begin
            stage_tag=(u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_retire_tags[
                      u_dut.u_compute.road_dynamic_postprocess_Inst_core.pre_result_tag[4:2]]>>
                      (u_dut.u_compute.road_dynamic_postprocess_Inst_core.pre_result_tag[1:0]*16))&16'hffff;
            check_pre(stage_tag,$signed(u_dut.u_compute.road_dynamic_postprocess_Inst_core.pre_result_data));
        end
        if(rstn && !fault && u_dut.u_compute.road_dynamic_postprocess_Inst_core.flag_post_accept)begin
            stage_tag=(u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_retire_tags[
                      u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_meta_tags[
                      u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_meta_read][4:2]]>>
                      (u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_meta_tags[
                      u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_meta_read][1:0]*16))&16'hffff;
            check_silu(stage_tag,$signed(u_dut.u_compute.road_dynamic_postprocess_Inst_core.silu_output_data));
        end
        if(rstn && !fault && u_dut.u_compute.road_dynamic_postprocess_Inst_core.flag_post_complete)begin
            stage_tag=(u_dut.u_compute.road_dynamic_postprocess_Inst_core.reg_retire_tags[
                      u_dut.u_compute.road_dynamic_postprocess_Inst_core.post_result_tag[4:2]]>>
                      (u_dut.u_compute.road_dynamic_postprocess_Inst_core.post_result_tag[1:0]*16))&16'hffff;
            check_post(stage_tag,$signed(u_dut.u_compute.road_dynamic_postprocess_Inst_core.wire_post_saturated));
        end
        if(rstn && !fault && u_dut.u_compute.flag_pp_accept && u_dut.u_compute.pp_tag>=16'd192)begin
            stage_tag=u_dut.u_compute.pp_tag;
            if(stage_tag>=384 || seen_sum[stage_tag] ||
               $signed(u_dut.u_compute.wire_sum)!==$signed(golden_residual_sum[stage_tag-192]) ||
               $signed(u_dut.u_compute.wire_saturated)!==$signed(golden_residual_post[stage_tag-192]))
                $fatal(1,"scheduled CSP residual sum tag=%0d",stage_tag);
            seen_sum[stage_tag]=1'b1; sum_count=sum_count+1;
        end

        if(rstn && result_valid && result_ready)begin
            if(result_tag>=384 || seen_output[result_tag])$fatal(1,"scheduled CSP output tag=%0d",result_tag);
            if(result_tag<192)begin
                if(result_address!==DW_BASE+result_tag || result_data!==golden_dw_post[result_tag] ||
                   $signed(result_sum)!==$signed(golden_dw_post[result_tag]))
                    $fatal(1,"scheduled CSP DW output tag=%0d",result_tag);
                actual_dw[result_tag]=result_data;
            end else begin
                if(result_address!==RESIDUAL_BASE+(result_tag-192) ||
                   result_data!==golden_residual_post[result_tag-192] ||
                   $signed({{7{result_sum[8]}},result_sum})!==$signed(golden_residual_sum[result_tag-192]))
                    $fatal(1,"scheduled CSP residual output tag=%0d",result_tag);
                actual_residual[result_tag-192]=result_data;
            end
            seen_output[result_tag]=1'b1; output_count=output_count+1;
        end
    end

    task read_vectors;
        begin
            $sformat(vector_file,"%0s/group_activation.hex",vector_root);$readmemh(vector_file,group_activation);
            $sformat(vector_file,"%0s/group_weight.hex",vector_root);$readmemh(vector_file,group_weight);
            $sformat(vector_file,"%0s/group_bias.hex",vector_root);$readmemh(vector_file,group_bias);
            $sformat(vector_file,"%0s/group_mask.hex",vector_root);$readmemh(vector_file,group_mask);
            $sformat(vector_file,"%0s/group_first.hex",vector_root);$readmemh(vector_file,group_first);
            $sformat(vector_file,"%0s/group_last.hex",vector_root);$readmemh(vector_file,group_last);
            $sformat(vector_file,"%0s/task_tags.hex",vector_root);$readmemh(vector_file,task_tags);
            $sformat(vector_file,"%0s/task_addresses.hex",vector_root);$readmemh(vector_file,task_addresses);
            $sformat(vector_file,"%0s/task_pre_multiplier.hex",vector_root);$readmemh(vector_file,task_pre_multiplier);
            $sformat(vector_file,"%0s/task_pre_shift.hex",vector_root);$readmemh(vector_file,task_pre_shift);
            $sformat(vector_file,"%0s/task_post_multiplier.hex",vector_root);$readmemh(vector_file,task_post_multiplier);
            $sformat(vector_file,"%0s/task_post_shift.hex",vector_root);$readmemh(vector_file,task_post_shift);
            $sformat(vector_file,"%0s/task_mask.hex",vector_root);$readmemh(vector_file,task_mask);
            $sformat(vector_file,"%0s/task_residual.hex",vector_root);$readmemh(vector_file,task_residual);
            $sformat(vector_file,"%0s/task_bypass_indices.hex",vector_root);$readmemh(vector_file,task_bypass_indices);
            $sformat(vector_file,"%0s/input_words.hex",vector_root);$readmemh(vector_file,input_words);
            $sformat(vector_file,"%0s/input_native_addresses.hex",vector_root);$readmemh(vector_file,input_native_addresses);
            $sformat(vector_file,"%0s/bypass_native_addresses.hex",vector_root);$readmemh(vector_file,bypass_native_addresses);
            $sformat(vector_file,"%0s/bypass_byte_lanes.hex",vector_root);$readmemh(vector_file,bypass_byte_lanes);
            $sformat(vector_file,"%0s/bypass.hex",vector_root);$readmemh(vector_file,golden_bypass);
            $sformat(vector_file,"%0s/dw_acc.hex",vector_root);$readmemh(vector_file,golden_dw_acc);
            $sformat(vector_file,"%0s/dw_pre.hex",vector_root);$readmemh(vector_file,golden_dw_pre);
            $sformat(vector_file,"%0s/dw_silu.hex",vector_root);$readmemh(vector_file,golden_dw_silu);
            $sformat(vector_file,"%0s/dw_post.hex",vector_root);$readmemh(vector_file,golden_dw_post);
            $sformat(vector_file,"%0s/pw_acc.hex",vector_root);$readmemh(vector_file,golden_pw_acc);
            $sformat(vector_file,"%0s/pw_pre.hex",vector_root);$readmemh(vector_file,golden_pw_pre);
            $sformat(vector_file,"%0s/pw_silu.hex",vector_root);$readmemh(vector_file,golden_pw_silu);
            $sformat(vector_file,"%0s/pw_post.hex",vector_root);$readmemh(vector_file,golden_pw_post);
            $sformat(vector_file,"%0s/residual_sum.hex",vector_root);$readmemh(vector_file,golden_residual_sum);
            $sformat(vector_file,"%0s/residual_post.hex",vector_root);$readmemh(vector_file,golden_residual_post);
            $sformat(vector_file,"%0s/dw_words.hex",vector_root);$readmemh(vector_file,golden_dw_words);
            $sformat(vector_file,"%0s/residual_words.hex",vector_root);$readmemh(vector_file,golden_residual_words);
            $sformat(vector_file,"%0s/silu.hex",vector_root);$readmemh(vector_file,silu_table);
            $sformat(vector_file,"%0s/descriptor.hex",reference_root);$readmemh(vector_file,reference_descriptor);
            $sformat(vector_file,"%0s/tags.hex",reference_root);$readmemh(vector_file,reference_tags);
            $sformat(vector_file,"%0s/address.hex",reference_root);$readmemh(vector_file,reference_addresses);
        end
    endtask

    task reset_common;
        begin
            @(negedge clk);rstn=1'b0;start=1'b0;table_valid=1'b0;result_ready=1'b0;random_mode=1'b0;
            repeat(3)@(negedge clk);rstn=1'b1;result_ready=1'b1;
            repeat(3)@(posedge clk);#1;
            if(fault || busy || done || result_valid || operand_request_valid)$fatal(1,"scheduled CSP reset release");
        end
    endtask

    task load_table;
        integer table_index;
        begin
            for(table_index=0;table_index<1024;table_index=table_index+1)begin
                @(negedge clk);table_valid=1'b1;table_addr=table_index;table_data=silu_table[table_index];#1;
                if(!table_ready || fault)$fatal(1,"scheduled CSP table address=%0d",table_index);
                @(posedge clk);
            end
            @(negedge clk);table_valid=1'b0;@(posedge clk);#1;
            if(!table_loaded || !start_ready)$fatal(1,"scheduled CSP table incomplete");
        end
    endtask

    task launch_tile;
        begin
            @(negedge clk);start=1'b1;
            while(!start_ready)@(negedge clk);
            @(posedge clk);@(negedge clk);start=1'b0;
        end
    endtask

    task check_complete_tile;
        integer check_index;
        integer word_index;
        integer word_lane;
        reg [127:0] packed_word;
        begin
            if(request_count!=320 || response_count!=320 || group_count!=320 || commit_count!=160 ||
               output_count!=384 || cache_write_count!=192 || cache_read_count!=128 ||
               acc_count!=384 || pre_count!=384 || silu_count!=384 || post_count!=384 || sum_count!=192)
                $fatal(1,"scheduled CSP endpoint req/resp/group/task/out/cachew/cacher=%0d/%0d/%0d/%0d/%0d/%0d/%0d stages=%0d/%0d/%0d/%0d sum=%0d",
                       request_count,response_count,group_count,commit_count,output_count,cache_write_count,cache_read_count,
                       acc_count,pre_count,silu_count,post_count,sum_count);
            if(busy_cycle_count !== reason_count[0]+reason_count[1]+reason_count[2]+reason_count[3]+
               reason_count[4]+reason_count[5]+reason_count[6]+reason_count[7])
                $fatal(1,"scheduled CSP cycle reason partition busy=%0d",busy_cycle_count);
            if(reason_count[7] !== reason7_count[0]+reason7_count[1]+reason7_count[2]+
               reason7_count[3]+reason7_count[4])
                $fatal(1,"scheduled CSP reason7 partition total=%0d",reason_count[7]);
            if(table_accept_count!==32'd1024)
                $fatal(1,"scheduled CSP table accept count=%0d",table_accept_count);
            for(check_index=0;check_index<384;check_index=check_index+1)
                if(!seen_output[check_index] || !seen_acc[check_index] || !seen_pre[check_index] ||
                   !seen_silu[check_index] || !seen_post[check_index])$fatal(1,"scheduled CSP coverage tag=%0d",check_index);
            for(check_index=192;check_index<384;check_index=check_index+1)
                if(!seen_sum[check_index])$fatal(1,"scheduled CSP sum coverage tag=%0d",check_index);
            for(word_index=0;word_index<12;word_index=word_index+1)begin
                packed_word=128'd0;
                for(word_lane=0;word_lane<16;word_lane=word_lane+1)
                    packed_word[word_lane*8 +: 8]=actual_dw[word_index*16+word_lane];
                if(packed_word!==golden_dw_words[word_index])$fatal(1,"scheduled CSP DW packing word=%0d",word_index);
                packed_word=128'd0;
                for(word_lane=0;word_lane<16;word_lane=word_lane+1)
                    packed_word[word_lane*8 +: 8]=actual_residual[word_index*16+word_lane];
                if(packed_word!==golden_residual_words[word_index])$fatal(1,"scheduled CSP residual packing word=%0d",word_index);
            end
        end
    endtask

    task report_tile_metrics;
        begin
            $display("CSP_SCHEDULED_TILE tile=%0d req=%0d mac=%0d commit=%0d output=%0d cache_write=%0d cache_read=%0d cycles=%0d reasons=%0d/%0d/%0d/%0d/%0d/%0d/%0d/%0d reason7=%0d/%0d/%0d/%0d/%0d pp_busy=%0d/%0d/%0d table_accept=%0d",
                     tile_number,request_count,group_count,commit_count,output_count,cache_write_count,cache_read_count,
                     busy_cycle_count,reason_count[0],reason_count[1],reason_count[2],reason_count[3],
                     reason_count[4],reason_count[5],reason_count[6],reason_count[7],
                     reason7_count[0],reason7_count[1],reason7_count[2],reason7_count[3],reason7_count[4],
                     pre_busy_count,silu_busy_count,post_busy_count,table_accept_count);
        end
    endtask

    task run_success_tile;
        begin
            launch_tile;
            wait(done);#1;
            check_complete_tile;
            if(fault)$fatal(1,"scheduled CSP success tile fault");
            report_tile_metrics;
            @(posedge clk);#1;
            if(done || busy)$fatal(1,"scheduled CSP done not pulse");
        end
    endtask

    task finish_expected_fault;
        input integer expected_outputs;
        begin
            wait(fault);repeat(4)@(posedge clk);#1;
            if(output_count!=expected_outputs || result_valid || done)
                $fatal(1,"scheduled CSP expected fault outputs=%0d expected=%0d",output_count,expected_outputs);
            o_test_done=1'b1;
            $display("CSP_SCHEDULED_EXPECTED_FAULT case=%0d request=%0d group=%0d commit=%0d output=%0d",
                     test_case,request_count,group_count,commit_count,output_count);
            $finish;
        end
    endtask

    initial begin
        clk=1'b0;rstn=1'b0;start=1'b0;table_valid=1'b0;table_addr=10'd0;table_data=16'sd0;
        operand_request_ready=1'b0;operand_response_valid=1'b0;operand_response_descriptor=25'd0;
        operand_activation=64'd0;operand_weight=192'd0;operand_bias=96'd0;
        operand_pre_multipliers=96'd0;operand_pre_shifts=18'd0;operand_post_multiplier=32'd0;
        operand_post_shift=6'd0;operand_bypass=24'd0;operand_fault=1'b0;result_ready=1'b0;
        o_test_done=1'b0;test_case=0;cycles=0;tile_number=-1;
        provider_pending=1'b0;provider_descriptor=25'd0;provider_delay=0;random_mode=1'b0;
        lfsr=32'h6d2b79f5;table_accept_count=32'd0;clear_scoreboard;
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("VECTORS=%s",vector_root))$fatal(1,"VECTORS missing");
        if(!$value$plusargs("REFERENCE=%s",reference_root))$fatal(1,"REFERENCE missing");
        if(test_case<0 || test_case>7)$fatal(1,"scheduled CSP unsupported CASE=%0d",test_case);
        read_vectors;
        for(lane=0;lane<TASKS;lane=lane+1)begin
            if(task_addresses[lane]!==reference_addresses[lane])
                $fatal(1,"scheduled CSP frozen address task=%0d",lane);
            for(metadata_lane=0;metadata_lane<3;metadata_lane=metadata_lane+1)begin
                if(task_mask[lane][metadata_lane])begin
                    if(task_tags[lane][metadata_lane*16 +: 16]!==
                       reference_tags[lane][metadata_lane*16 +: 16])
                        $fatal(1,"scheduled CSP valid tag task=%0d lane=%0d",lane,metadata_lane);
                end else if(task_tags[lane][metadata_lane*16 +: 16]!==16'hffff ||
                            reference_tags[lane][metadata_lane*16 +: 16]!==16'h0000)
                    $fatal(1,"scheduled CSP invalid tag normalization task=%0d lane=%0d",lane,metadata_lane);
            end
        end
        reset_common;
        load_table;
        case(test_case)
            0:begin
                run_success_tile;
                run_success_tile;
                o_test_done=1'b1;
                $display("CSP_SCHEDULED_PASS case=0 tiles=2 table_loads=1 outputs_per_tile=384");
                $finish;
            end
            1:begin
                random_mode=1'b1;run_success_tile;random_mode=1'b0;result_ready=1'b1;
                if(stall_count==0)$fatal(1,"scheduled CSP random result stall missing");
                o_test_done=1'b1;$display("CSP_SCHEDULED_PASS case=1 random_provider_and_result stalls=%0d",stall_count);$finish;
            end
            2:begin
                launch_tile;
                wait(result_valid);@(negedge clk);result_ready=1'b0;
                repeat(512)begin @(posedge clk);#1;if(!result_valid || fault)$fatal(1,"scheduled CSP long stall escaped");end
                @(negedge clk);result_ready=1'b1;wait(done);#1;check_complete_tile;
                if(stall_count<512)$fatal(1,"scheduled CSP long stall count=%0d",stall_count);
                report_tile_metrics;
                o_test_done=1'b1;$display("CSP_SCHEDULED_PASS case=2 long_result_stall=%0d",stall_count);$finish;
            end
            3:begin
                launch_tile;wait(request_accept);repeat(4)@(posedge clk);
                if(!provider_pending || operand_response_valid)$fatal(1,"scheduled CSP reset request window missing");
                reset_common;load_table;run_success_tile;
                o_test_done=1'b1;$display("CSP_SCHEDULED_PASS case=3 provider_cancel_rerun");$finish;
            end
            4:begin
                launch_tile;wait(group_accept && operand_request_descriptor[16]);
                reset_common;load_table;run_success_tile;
                o_test_done=1'b1;$display("CSP_SCHEDULED_PASS case=4 pw_reset_rerun");$finish;
            end
            5:begin launch_tile;finish_expected_fault(0);end
            6:begin launch_tile;finish_expected_fault(381);end
            7:begin launch_tile;finish_expected_fault(0);end
        endcase
    end
endmodule
