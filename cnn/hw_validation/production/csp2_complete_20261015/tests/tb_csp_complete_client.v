`timescale 1ns / 1ps
// 仅提供冻结参数和受控逻辑字节内存；任务、算术结果和完成均来自真实DUT闭包。
module tb_csp_complete_client(output o_test_complete);
    localparam [31:0]BASE_SOURCE = 32'h035b4000;
    localparam [31:0]BASE_STAGE0 = 32'h035ea000;
    localparam [31:0]BASE_STAGE1 = 32'h03605000;
    localparam [31:0]BASE_STAGE2 = 32'h03620000;
    localparam [31:0]BASE_STAGE3 = 32'h0363b000;
    localparam [31:0]BASE_STAGE4 = 32'h03656000;
    localparam integer SIZE12 = 110592;
    localparam integer SIZE24 = 221184;

    reg clk = 0;
    reg rstn = 0;
    reg start = 0;
    reg [6:0]tile_y = 0;
    reg [7:0]tile_x = 0;
    reg cancel = 0;
    wire start_ready;
    wire busy;
    wire done;
    wire fault;
    wire [2:0]layer;

    wire parameter_valid;
    wire [4:0]parameter_channel;
    wire [1:0]parameter_group;
    wire [2:0]parameter_window;
    reg parameter_ready = 1;
    reg parameter_response_valid = 0;
    reg [2:0]parameter_response_layer = 0;
    reg [4:0]parameter_response_channel = 0;
    reg [1:0]parameter_response_group = 0;
    reg [2:0]parameter_response_window = 0;
    reg [191:0]parameter_response_weight = 0;
    reg [247:0]parameter_response_data = 0;
    reg parameter_error = 0;
    wire parameter_response_ready;

    wire read_valid;
    wire [31:0]read_address;
    reg read_ready = 1;
    reg read_response_valid = 0;
    reg [31:0]read_response_address = 0;
    reg [7:0]read_response_data = 0;
    reg read_error = 0;
    wire read_response_ready;

    wire write_valid;
    wire [31:0]write_address;
    wire [7:0]write_data;
    wire signed [8:0]write_sum;
    reg write_ready = 1;
    wire barrier_valid;
    reg barrier_ready = 0;
    reg [2:0]barrier_layer = 0;

    wire core_valid;
    wire core_ready;
    wire owner_core_ready; // 原核真实ready与外围owner授予分别观察
    reg owner_admit = 1; // 仅TB模拟owner暂不授予，不改变原核II
    wire core_first;
    wire core_last;
    wire [7:0]core_input_mask;
    wire [63:0]core_activation;
    wire [191:0]core_weight;
    wire [95:0]core_bias;
    wire [2:0]core_output_mask;
    wire [47:0]core_tags;
    wire [95:0]core_addresses;
    wire [95:0]core_pre_multiplier;
    wire [17:0]core_pre_shift;
    wire [31:0]core_post_multiplier;
    wire [5:0]core_post_shift;
    wire core_residual;
    wire [23:0]core_bypass;
    wire core_output_valid;
    wire core_output_ready;
    wire signed [7:0]core_output_data;
    wire [15:0]core_output_tag;
    wire [31:0]core_output_address;
    wire signed [8:0]core_output_sum;
    wire core_fault;

    reg table_valid = 0;
    reg [9:0]table_address = 0;
    reg signed [15:0]table_data = 0;
    wire table_ready;
    wire table_loaded;
    reg signed [15:0]silu_table [0:1023];

    reg signed [7:0]source_hwc [0:SIZE24-1];
    reg signed [7:0]memory0 [0:SIZE12-1];
    reg signed [7:0]memory1 [0:SIZE12-1];
    reg signed [7:0]memory2 [0:SIZE12-1];
    reg signed [7:0]memory3 [0:SIZE12-1];
    reg signed [7:0]memory4 [0:SIZE24-1];
    reg [SIZE12-1:0]written0, written1, written2, written3;
    reg [SIZE24-1:0]written4;
    reg [SIZE12-1:0]visible0, visible1, visible2, visible3;
    reg [SIZE24-1:0]visible4;

    reg signed [7:0]weight0 [0:107];
    reg signed [7:0]weight1 [0:143];
    reg signed [7:0]weight2 [0:107];
    reg signed [7:0]weight3 [0:143];
    reg signed [7:0]weight4 [0:575];
    reg signed [31:0]bias0 [0:11];
    reg signed [31:0]bias1 [0:11];
    reg signed [31:0]bias2 [0:11];
    reg signed [31:0]bias3 [0:11];
    reg signed [31:0]bias4 [0:23];
    reg signed [31:0]premul0 [0:11];
    reg signed [31:0]premul1 [0:11];
    reg signed [31:0]premul2 [0:11];
    reg signed [31:0]premul3 [0:11];
    reg signed [31:0]premul4 [0:23];
    reg [7:0]preshift0 [0:11];
    reg [7:0]preshift1 [0:11];
    reg [7:0]preshift2 [0:11];
    reg [7:0]preshift3 [0:11];
    reg [7:0]preshift4 [0:23];
    reg signed [31:0]postmul0 [0:0], postmul1 [0:0], postmul2 [0:0], postmul3 [0:0], postmul4 [0:0];
    reg [7:0]postshift0 [0:0], postshift1 [0:0], postshift2 [0:0], postshift3 [0:0], postshift4 [0:0];

    reg signed [31:0]gold_acc0 [0:SIZE12-1], gold_acc1 [0:SIZE12-1];
    reg signed [31:0]gold_acc2 [0:SIZE12-1], gold_acc3 [0:SIZE12-1];
    reg signed [31:0]gold_acc4 [0:SIZE24-1];
    reg signed [15:0]gold_pre0 [0:SIZE12-1], gold_pre1 [0:SIZE12-1];
    reg signed [15:0]gold_pre2 [0:SIZE12-1], gold_pre3 [0:SIZE12-1];
    reg signed [15:0]gold_pre4 [0:SIZE24-1];
    reg signed [15:0]gold_silu0 [0:SIZE12-1], gold_silu1 [0:SIZE12-1];
    reg signed [15:0]gold_silu2 [0:SIZE12-1], gold_silu3 [0:SIZE12-1];
    reg signed [15:0]gold_silu4 [0:SIZE24-1];
    reg signed [7:0]gold_post0 [0:SIZE12-1], gold_post1 [0:SIZE12-1];
    reg signed [7:0]gold_post2 [0:SIZE12-1], gold_post3 [0:SIZE12-1];
    reg signed [7:0]gold_post4 [0:SIZE24-1];
    reg signed [15:0]gold_sum0 [0:SIZE12-1], gold_sum1 [0:SIZE12-1];
    reg signed [15:0]gold_sum2 [0:SIZE12-1], gold_sum3 [0:SIZE12-1];
    reg signed [15:0]gold_sum4 [0:SIZE24-1];
    reg signed [7:0]gold_output0 [0:SIZE12-1], gold_output1 [0:SIZE12-1];
    reg signed [7:0]gold_output2 [0:SIZE12-1], gold_output3 [0:SIZE12-1];
    reg signed [7:0]gold_output4 [0:SIZE24-1];

    reg [SIZE12-1:0]seen_acc0, seen_acc1, seen_acc2, seen_acc3;
    reg [SIZE24-1:0]seen_acc4;
    reg [SIZE12-1:0]seen_pre0, seen_pre1, seen_pre2, seen_pre3;
    reg [SIZE24-1:0]seen_pre4;
    reg [SIZE12-1:0]seen_silu0, seen_silu1, seen_silu2, seen_silu3;
    reg [SIZE24-1:0]seen_silu4;
    reg [SIZE12-1:0]seen_post0, seen_post1, seen_post2, seen_post3;
    reg [SIZE24-1:0]seen_post4;

    reg parameter_pending = 0;
    reg [7:0]parameter_delay = 0;
    reg [2:0]saved_parameter_layer;
    reg [4:0]saved_parameter_channel;
    reg [1:0]saved_parameter_group;
    reg [2:0]saved_parameter_window;
    reg read_pending = 0;
    reg [7:0]read_delay = 0;
    reg [31:0]saved_read_address;
    reg [31:0]lfsr = 32'h75bcd15a;
    reg complete = 0;
    reg active = 0;
    reg [4095:0]vector_path;
    reg [191:0]expected_weight;
    reg [247:0]expected_parameter;
    reg held_parameter_request, held_parameter_response, held_read_request, held_read_response;
    reg held_core, held_write, held_barrier;
    reg [12:0]held_parameter_request_payload;
    reg [453:0]held_parameter_response_payload;
    reg [31:0]held_read_request_payload;
    reg [40:0]held_read_response_payload;
    reg [685:0]held_core_payload;
    reg [48:0]held_write_payload;
    reg [2:0]held_barrier_payload;
    reg [31:0]first_write_address;
    integer test_case;
    integer fault_kind;
    integer reset_stage;
    integer negative_acc;
    integer cycles = 0;
    integer run_start = 0;
    integer final_cycles = 0;
    integer groups = 0;
    integer tasks = 0;
    integer outputs = 0;
    integer accumulators = 0;
    integer pres = 0;
    integer silus = 0;
    integer posts = 0;
    integer reads = 0;
    integer barriers = 0;
    integer runs = 0;
    integer table_loads = 0;
    integer parameter_stalls = 0;
    integer read_stalls = 0;
    integer write_stalls = 0;
    integer barrier_stalls = 0;
    integer core_stalls = 0;
    integer stage_cycles [0:4]; // 当前run互斥阶段周期
    integer stage_reads [0:4]; // 每层实际读请求
    integer stage_outputs [0:4]; // 每层真实外写
    integer stage_groups [0:4]; // 每层真正进入原核的组
    integer stage_tasks [0:4]; // 每层注册退休事件
    integer state_cycles [0:14]; // FSM状态互斥周期账本
    integer counter_index; // 当前run账本初始化和输出索引
    integer cycle_sum; // 状态周期合计核验
    integer held_cycles = 0;
    integer index;
    integer lane;
    integer score_index;
    integer score_tag;
    integer expected_outputs;
    integer expected_tasks;
    integer expected_groups;

    assign o_test_complete = complete;
    assign core_ready = owner_core_ready && owner_admit; // owner拒绝时双方均不提交该组
    always #5 clk = ~clk;

    function [31:0]stage_base;
        input [2:0]stage;
        begin
            case(stage)
                0:stage_base=BASE_STAGE0; 1:stage_base=BASE_STAGE1;
                2:stage_base=BASE_STAGE2; 3:stage_base=BASE_STAGE3;
                default:stage_base=BASE_STAGE4;
            endcase
        end
    endfunction

    function integer physical_to_hwc;
        input integer physical_index;
        input integer channels;
        integer pixel_index, intra_index, tile_index, y_value, x_value, channel_value;
        begin
            channel_value=physical_index%channels;
            pixel_index=physical_index/channels;
            intra_index=pixel_index%16;
            tile_index=pixel_index/16;
            y_value=(tile_index/32)*4+intra_index/4;
            x_value=(tile_index%32)*4+intra_index%4;
            physical_to_hwc=(y_value*128+x_value)*channels+channel_value;
        end
    endfunction

    function integer address_to_hwc;
        input [2:0]stage;
        input [31:0]address;
        integer offset, channels;
        begin
            channels=stage==4 ? 24 : 12;
            offset=address-stage_base(stage);
            if(offset<0 || offset>=(stage==4 ? SIZE24 : SIZE12))address_to_hwc=-1;
            else address_to_hwc=physical_to_hwc(offset,channels);
        end
    endfunction

    function [31:0]golden_acc;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:golden_acc=gold_acc0[position]; 1:golden_acc=gold_acc1[position];
            2:golden_acc=gold_acc2[position]; 3:golden_acc=gold_acc3[position];
            default:golden_acc=gold_acc4[position]; endcase
        end
    endfunction

    function [15:0]golden_pre;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:golden_pre=gold_pre0[position]; 1:golden_pre=gold_pre1[position];
            2:golden_pre=gold_pre2[position]; 3:golden_pre=gold_pre3[position];
            default:golden_pre=gold_pre4[position]; endcase
        end
    endfunction

    function [15:0]golden_silu;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:golden_silu=gold_silu0[position]; 1:golden_silu=gold_silu1[position];
            2:golden_silu=gold_silu2[position]; 3:golden_silu=gold_silu3[position];
            default:golden_silu=gold_silu4[position]; endcase
        end
    endfunction

    function [7:0]golden_post;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:golden_post=gold_post0[position]; 1:golden_post=gold_post1[position];
            2:golden_post=gold_post2[position]; 3:golden_post=gold_post3[position];
            default:golden_post=gold_post4[position]; endcase
        end
    endfunction

    function [15:0]golden_sum;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:golden_sum=gold_sum0[position]; 1:golden_sum=gold_sum1[position];
            2:golden_sum=gold_sum2[position]; 3:golden_sum=gold_sum3[position];
            default:golden_sum=gold_sum4[position]; endcase
        end
    endfunction

    function [7:0]golden_output;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:golden_output=gold_output0[position]; 1:golden_output=gold_output1[position];
            2:golden_output=gold_output2[position]; 3:golden_output=gold_output3[position];
            default:golden_output=gold_output4[position]; endcase
        end
    endfunction

    task build_parameter;
        input [2:0]stage;
        input [4:0]channel;
        input [1:0]group_number;
        input [2:0]window;
        output [191:0]packed_weight;
        output [247:0]packed_parameter;
        integer output_lane, input_lane, union_index, kernel_y, kernel_x;
        integer output_channel, input_channel, input_channels, weight_index;
        reg [7:0]weight_value;
        reg [31:0]bias_value, premul_value, postmul_value;
        reg [5:0]preshift_value, postshift_value;
        begin
            packed_weight=0; packed_parameter=0;
            input_channels=stage==4 ? 24 : 12;
            case(stage)
                0:begin postmul_value=postmul0[0]; postshift_value=postshift0[0][5:0]; end
                1:begin postmul_value=postmul1[0]; postshift_value=postshift1[0][5:0]; end
                2:begin postmul_value=postmul2[0]; postshift_value=postshift2[0][5:0]; end
                3:begin postmul_value=postmul3[0]; postshift_value=postshift3[0][5:0]; end
                default:begin postmul_value=postmul4[0]; postshift_value=postshift4[0][5:0]; end
            endcase
            for(output_lane=0;output_lane<3;output_lane=output_lane+1)begin
                output_channel=(stage==0 || stage==2) ? channel : channel+output_lane;
                case(stage)
                    0:begin bias_value=bias0[channel]; premul_value=premul0[channel]; preshift_value=preshift0[channel][5:0]; end
                    1:begin bias_value=bias1[output_channel]; premul_value=premul1[output_channel]; preshift_value=preshift1[output_channel][5:0]; end
                    2:begin bias_value=bias2[channel]; premul_value=premul2[channel]; preshift_value=preshift2[channel][5:0]; end
                    3:begin bias_value=bias3[output_channel]; premul_value=premul3[output_channel]; preshift_value=preshift3[output_channel][5:0]; end
                    default:begin bias_value=bias4[output_channel]; premul_value=premul4[output_channel]; preshift_value=preshift4[output_channel][5:0]; end
                endcase
                packed_parameter[output_lane*32 +: 32]=bias_value;
                packed_parameter[96+output_lane*32 +: 32]=premul_value;
                packed_parameter[192+output_lane*6 +: 6]=preshift_value;
                for(input_lane=0;input_lane<8;input_lane=input_lane+1)begin
                    weight_value=0;
                    if(stage==0 || stage==2)begin
                        union_index=group_number*8+input_lane;
                        kernel_y=union_index/window;
                        kernel_x=union_index%window-output_lane;
                        if(union_index<window*3 && kernel_y<3 && kernel_x>=0 && kernel_x<3)begin
                            weight_index=channel*9+kernel_y*3+kernel_x;
                            if(stage==0)weight_value=weight0[weight_index];
                            else weight_value=weight2[weight_index];
                        end
                    end else begin
                        input_channel=group_number*8+input_lane;
                        if(output_channel<(stage==4 ? 24 : 12) && input_channel<input_channels)begin
                            weight_index=output_channel*input_channels+input_channel;
                            case(stage)
                                1:weight_value=weight1[weight_index];
                                3:weight_value=weight3[weight_index];
                                default:weight_value=weight4[weight_index];
                            endcase
                        end
                    end
                    packed_weight[output_lane*64+input_lane*8 +: 8]=weight_value;
                end
            end
            packed_parameter[241:210]=postmul_value;
            packed_parameter[247:242]=postshift_value;
        end
    endtask

    task check_read_request;
        input [31:0]actual_address;
        integer calc_y, calc_x, calc_slot, calc_channel, calc_channels, calc_base;
        integer calc_padding;
        reg [31:0]expected_address;
        begin
            calc_y=client.reg_origin_y+client.reg_row-(layer<2 ? 1 : 0);
            calc_x=client.reg_origin_x+client.reg_column-(layer<2 ? 1 : 0);
            calc_slot=client.reg_group*8+client.reg_fetch_lane;
            calc_channel=calc_slot; calc_channels=12; calc_base=BASE_STAGE0;
            if(client.flag_bypass)begin
                calc_channel=client.reg_channel+client.reg_fetch_lane;
                if(layer==1)begin calc_base=BASE_SOURCE; calc_channels=24; calc_channel=calc_channel+12; end
                else calc_base=BASE_STAGE1;
            end else if(layer==0 || layer==2)begin
                calc_y=calc_y-1+calc_slot/client.wire_window;
                calc_x=calc_x-1+calc_slot%client.wire_window;
                calc_channel=client.reg_channel;
                if(layer==0)begin calc_base=BASE_SOURCE; calc_channels=24; calc_channel=calc_channel+12; end
                else calc_base=BASE_STAGE1;
            end else if(layer==3)calc_base=BASE_STAGE2;
            else if(layer==4)begin
                if(calc_slot<12)begin calc_base=BASE_SOURCE; calc_channels=24; end
                else begin calc_base=BASE_STAGE3; calc_channel=calc_slot-12; end
            end
            calc_padding=calc_y<0 || calc_y>=72 || calc_x<0 || calc_x>=128 ||
                (!client.flag_bypass && calc_slot>=client.wire_inputs) ||
                (client.flag_bypass && !client.reg_output_mask[client.reg_fetch_lane]);
            if(calc_padding)$fatal(1,"client issued a read for padding");
            expected_address=calc_base+(((calc_y/4)*32+calc_x/4)*16+(calc_y%4)*4+calc_x%4)*calc_channels+calc_channel;
            if(actual_address!==expected_address)$fatal(1,"read trajectory mismatch layer=%0d got=%h expected=%h",layer,actual_address,expected_address);
        end
    endtask

    task mark_seen_acc;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:begin if(seen_acc0[position])$fatal(1,"duplicate acc"); seen_acc0[position]=1; end
            1:begin if(seen_acc1[position])$fatal(1,"duplicate acc"); seen_acc1[position]=1; end
            2:begin if(seen_acc2[position])$fatal(1,"duplicate acc"); seen_acc2[position]=1; end
            3:begin if(seen_acc3[position])$fatal(1,"duplicate acc"); seen_acc3[position]=1; end
            default:begin if(seen_acc4[position])$fatal(1,"duplicate acc"); seen_acc4[position]=1; end
        endcase end
    endtask

    task mark_seen_pre;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:begin if(seen_pre0[position])$fatal(1,"duplicate pre"); seen_pre0[position]=1; end
            1:begin if(seen_pre1[position])$fatal(1,"duplicate pre"); seen_pre1[position]=1; end
            2:begin if(seen_pre2[position])$fatal(1,"duplicate pre"); seen_pre2[position]=1; end
            3:begin if(seen_pre3[position])$fatal(1,"duplicate pre"); seen_pre3[position]=1; end
            default:begin if(seen_pre4[position])$fatal(1,"duplicate pre"); seen_pre4[position]=1; end
        endcase end
    endtask

    task mark_seen_silu;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:begin if(seen_silu0[position])$fatal(1,"duplicate silu"); seen_silu0[position]=1; end
            1:begin if(seen_silu1[position])$fatal(1,"duplicate silu"); seen_silu1[position]=1; end
            2:begin if(seen_silu2[position])$fatal(1,"duplicate silu"); seen_silu2[position]=1; end
            3:begin if(seen_silu3[position])$fatal(1,"duplicate silu"); seen_silu3[position]=1; end
            default:begin if(seen_silu4[position])$fatal(1,"duplicate silu"); seen_silu4[position]=1; end
        endcase end
    endtask

    task mark_seen_post;
        input [2:0]stage; input integer position;
        begin case(stage)
            0:begin if(seen_post0[position])$fatal(1,"duplicate post"); seen_post0[position]=1; end
            1:begin if(seen_post1[position])$fatal(1,"duplicate post"); seen_post1[position]=1; end
            2:begin if(seen_post2[position])$fatal(1,"duplicate post"); seen_post2[position]=1; end
            3:begin if(seen_post3[position])$fatal(1,"duplicate post"); seen_post3[position]=1; end
            default:begin if(seen_post4[position])$fatal(1,"duplicate post"); seen_post4[position]=1; end
        endcase end
    endtask

    task clear_run_state;
        begin
            groups=0; tasks=0; outputs=0; accumulators=0; pres=0; silus=0; posts=0; reads=0; barriers=0;
            parameter_stalls=0; read_stalls=0; write_stalls=0; barrier_stalls=0; held_cycles=0;
            core_stalls=0;
            for(counter_index=0;counter_index<5;counter_index=counter_index+1)begin
                stage_cycles[counter_index]=0; stage_reads[counter_index]=0; stage_outputs[counter_index]=0;
                stage_groups[counter_index]=0; stage_tasks[counter_index]=0;
            end
            for(counter_index=0;counter_index<15;counter_index=counter_index+1)state_cycles[counter_index]=0;
            seen_acc0=0; seen_acc1=0; seen_acc2=0; seen_acc3=0; seen_acc4=0;
            seen_pre0=0; seen_pre1=0; seen_pre2=0; seen_pre3=0; seen_pre4=0;
            seen_silu0=0; seen_silu1=0; seen_silu2=0; seen_silu3=0; seen_silu4=0;
            seen_post0=0; seen_post1=0; seen_post2=0; seen_post3=0; seen_post4=0;
            held_parameter_request=0; held_parameter_response=0; held_read_request=0; held_read_response=0;
            held_core=0; held_write=0; held_barrier=0; first_write_address=0;
        end
    endtask

    task new_tile_memory;
        begin
            written0=0; written1=0; written2=0; written3=0; written4=0;
            visible0=0; visible1=0; visible2=0; visible3=0; visible4=0;
        end
    endtask

    task reset_and_load_table;
        begin
            active=0; start=0; cancel=0; table_valid=0;
            @(negedge clk); rstn=0;
            repeat(3)@(negedge clk);
            rstn=1;
            repeat(3)@(negedge clk);
            if(table_loaded || start_ready || done || fault)$fatal(1,"reset retained protocol state");
            for(index=0;index<1024;index=index+1)begin
                @(negedge clk); table_valid=1; table_address=index; table_data=silu_table[index];
                #1;if(!table_ready)$fatal(1,"LUT load blocked index=%0d",index);
            end
            @(negedge clk); table_valid=0;
            #1;if(!table_loaded || !start_ready)$fatal(1,"LUT did not become active");
            table_loads=table_loads+1;
        end
    endtask

    task launch_tile;
        input [6:0]launch_y; input [7:0]launch_x;
        begin
            tile_y=launch_y; tile_x=launch_x; clear_run_state; new_tile_memory;
            @(negedge clk); start=1;
            #1;if(!start_ready)$fatal(1,"tile start blocked y=%0d x=%0d",launch_y,launch_x);
            run_start=cycles; active=1;
            @(posedge clk); @(negedge clk); start=0;
        end
    endtask

    task set_expected_counts;
        input [6:0]launch_y; input [7:0]launch_x;
        integer valid_height, valid_width;
        begin
            valid_height=6-(launch_y==0)-(launch_y==68);
            valid_width=6-(launch_x==0)-(launch_x==124);
            expected_outputs=valid_height*valid_width*24+768;
            expected_tasks=valid_height*24+valid_height*valid_width*4+288;
            expected_groups=expected_tasks*2+128;
        end
    endtask

    task finish_run;
        input [6:0]launch_y; input [7:0]launch_x;
        begin
            set_expected_counts(launch_y,launch_x);
            wait(done); @(negedge clk); #1;
            if(fault || !busy || outputs!=expected_outputs || tasks!=expected_tasks || groups!=expected_groups ||
                accumulators!=expected_outputs || pres!=expected_outputs || silus!=expected_outputs || posts!=expected_outputs || barriers!=5)
                $fatal(1,"incomplete run outputs=%0d/%0d tasks=%0d/%0d groups=%0d/%0d acc=%0d pre=%0d silu=%0d post=%0d barriers=%0d",
                    outputs,expected_outputs,tasks,expected_tasks,groups,expected_groups,accumulators,pres,silus,posts,barriers);
            final_cycles=cycles-run_start; runs=runs+1; active=0;
            cycle_sum=0;
            for(counter_index=0;counter_index<15;counter_index=counter_index+1)begin
                cycle_sum=cycle_sum+state_cycles[counter_index];
                $display("CSP_COMPLETE_STATE case=%0d run=%0d state=%0d cycles=%0d",test_case,runs,counter_index,state_cycles[counter_index]);
            end
            if(cycle_sum!=final_cycles)$fatal(1,"state cycle ledger mismatch %0d/%0d",cycle_sum,final_cycles);
            for(counter_index=0;counter_index<5;counter_index=counter_index+1)begin
                $display("CSP_COMPLETE_STAGE case=%0d run=%0d stage=%0d cycles=%0d reads=%0d groups=%0d tasks=%0d outputs=%0d",
                    test_case,runs,counter_index,stage_cycles[counter_index],stage_reads[counter_index],stage_groups[counter_index],stage_tasks[counter_index],stage_outputs[counter_index]);
            end
            $display("CSP_COMPLETE_RUN case=%0d run=%0d y=%0d x=%0d cycles=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d reads=%0d barriers=%0d",
                test_case,runs,launch_y,launch_x,final_cycles,groups,tasks,outputs,accumulators,pres,silus,posts,reads,barriers);
            @(posedge clk); @(negedge clk); #1;
            if(done || busy || write_valid || fault || !start_ready)$fatal(1,"run did not retire to clean idle");
            repeat(3)@(negedge clk);
            if(done || busy || write_valid || fault || !start_ready)$fatal(1,"run emitted stale completion");
        end
    endtask

    road_csp_complete_client client(
        .i_clk(clk),.i_rstn(rstn),.i_start(start),.i_tile_y(tile_y),.i_tile_x(tile_x),.i_cancel(cancel),
        .i_table_loaded(table_loaded),.o_start_ready(start_ready),.o_busy(busy),.o_done(done),.o_fault(fault),.o_layer(layer),
        .o_parameter_valid(parameter_valid),.o_parameter_channel(parameter_channel),.o_parameter_group(parameter_group),
        .o_parameter_window(parameter_window),.i_parameter_ready(parameter_ready),
        .i_parameter_response_valid(parameter_response_valid),.o_parameter_response_ready(parameter_response_ready),
        .i_parameter_response_layer(parameter_response_layer),.i_parameter_response_channel(parameter_response_channel),
        .i_parameter_response_group(parameter_response_group),.i_parameter_response_window(parameter_response_window),
        .i_parameter_weight(parameter_response_weight),.i_parameter_data(parameter_response_data),.i_parameter_error(parameter_error),
        .o_read_valid(read_valid),.o_read_address(read_address),.i_read_ready(read_ready),
        .i_read_response_valid(read_response_valid),.o_read_response_ready(read_response_ready),
        .i_read_response_address(read_response_address),.i_read_response_data(read_response_data),.i_read_error(read_error),
        .o_write_valid(write_valid),.o_write_address(write_address),.o_write_data(write_data),.o_write_sum(write_sum),.i_write_ready(write_ready),
        .o_barrier_valid(barrier_valid),.i_barrier_ready(barrier_ready),.i_barrier_layer(barrier_layer),
        .o_core_valid(core_valid),.i_core_ready(core_ready),.o_core_first(core_first),.o_core_last(core_last),
        .o_core_input_mask(core_input_mask),.o_core_activation(core_activation),.o_core_weight(core_weight),.o_core_bias(core_bias),
        .o_core_output_mask(core_output_mask),.o_core_tags(core_tags),.o_core_addresses(core_addresses),
        .o_core_pre_multiplier(core_pre_multiplier),.o_core_pre_shift(core_pre_shift),
        .o_core_post_multiplier(core_post_multiplier),.o_core_post_shift(core_post_shift),
        .o_core_residual(core_residual),.o_core_bypass(core_bypass),
        .i_core_output_valid(core_output_valid),.o_core_output_ready(core_output_ready),
        .i_core_output_tag(core_output_tag),.i_core_output_address(core_output_address),
        .i_core_output_data(core_output_data),.i_core_output_sum(core_output_sum),.i_core_fault(core_fault)
    );

    road_csp_first_probe arithmetic_Inst(
        .i_clk(clk),.i_rstn(rstn),.i_table_valid(table_valid),.i_table_addr(table_address),.i_table_data(table_data),
        .i_input_valid(core_valid && owner_admit),.i_first(core_first),.i_last(core_last),.i_lane_mask(core_input_mask),
        .i_activation_data(core_activation),.i_weight_data(core_weight),.i_bias_data(core_bias),
        .i_output_mask(core_output_mask),.i_tags(core_tags),.i_addresses(core_addresses),
        .i_pre_multipliers(core_pre_multiplier),.i_pre_shifts(core_pre_shift),
        .i_post_multiplier(core_post_multiplier),.i_post_shift(core_post_shift),
        .i_residual(core_residual),.i_bypass_data(core_bypass),.i_input_fault(1'b0),
        .i_output_ready(core_output_ready),.o_table_ready(table_ready),.o_table_loaded(table_loaded),
        .o_input_ready(owner_core_ready),.o_output_valid(core_output_valid),.o_output_data(core_output_data),
        .o_output_tag(core_output_tag),.o_output_address(core_output_address),.o_output_sum(core_output_sum),.o_fault(core_fault)
    );

    // 真实请求服务：响应保持到ready，且中间层只允许读取已通过对应屏障的实际写。
    always @(posedge clk or negedge rstn)begin
        if(!rstn)begin
            parameter_pending<=0; parameter_response_valid<=0; parameter_error<=0;
            read_pending<=0; read_response_valid<=0; read_error<=0;
            written0<=0; written1<=0; written2<=0; written3<=0; written4<=0;
            visible0<=0; visible1<=0; visible2<=0; visible3<=0; visible4<=0;
        end else begin
            if(parameter_response_valid && parameter_response_ready)begin parameter_response_valid<=0; parameter_error<=0; end
            if(parameter_valid && parameter_ready)begin
                if(parameter_pending || parameter_response_valid)$fatal(1,"multiple parameter requests");
                saved_parameter_layer<=layer; saved_parameter_channel<=parameter_channel;
                saved_parameter_group<=parameter_group; saved_parameter_window<=parameter_window;
                parameter_delay<=test_case==9 ? lfsr[7:5] : 2; parameter_pending<=1;
            end
            if(parameter_pending)begin
                if(parameter_delay!=0)parameter_delay<=parameter_delay-1'b1;
                else if(!parameter_response_valid)begin
                    parameter_response_layer<=saved_parameter_layer;
                    parameter_response_channel<=saved_parameter_channel;
                    parameter_response_group<=saved_parameter_group;
                    parameter_response_window<=saved_parameter_window;
                    build_parameter(saved_parameter_layer,saved_parameter_channel,saved_parameter_group,saved_parameter_window,
                        parameter_response_weight,parameter_response_data);
                    if(test_case==15 && fault_kind==2 && saved_parameter_group==1 && outputs==0)
                        parameter_response_data[0]=!parameter_response_data[0]; // 后组字段漂移必须拒绝
                    parameter_error<=test_case==15 && fault_kind==1 && outputs==0;
                    if(test_case==15 && fault_kind==0 && outputs==0)parameter_response_layer<=saved_parameter_layer+1'b1;
                    parameter_response_valid<=1; parameter_pending<=0;
                end
            end
            if(read_response_valid && read_response_ready)begin read_response_valid<=0; read_error<=0; end
            if(read_valid && read_ready)begin
                if(read_pending || read_response_valid)$fatal(1,"multiple read requests");
                check_read_request(read_address);
                saved_read_address<=read_address; read_delay<=test_case==9 ? lfsr[11:9] : 2; read_pending<=1; reads=reads+1;
                stage_reads[layer]=stage_reads[layer]+1;
            end
            if(read_pending)begin
                if(read_delay!=0)read_delay<=read_delay-1'b1;
                else if(!read_response_valid)begin
                    read_response_address<=saved_read_address;
                    read_error<=test_case==14 && fault_kind==1 && outputs==0;
                    if(test_case==14 && fault_kind==0 && outputs==0)read_response_address<=saved_read_address+1'b1;
                    if(saved_read_address>=BASE_SOURCE && saved_read_address<BASE_SOURCE+SIZE24)
                        read_response_data<=source_hwc[physical_to_hwc(saved_read_address-BASE_SOURCE,24)];
                    else if(saved_read_address>=BASE_STAGE0 && saved_read_address<BASE_STAGE0+SIZE12)begin
                        index=saved_read_address-BASE_STAGE0; if(!visible0[index])$fatal(1,"unwritten stage0 read"); read_response_data<=memory0[index];
                    end else if(saved_read_address>=BASE_STAGE1 && saved_read_address<BASE_STAGE1+SIZE12)begin
                        index=saved_read_address-BASE_STAGE1; if(!visible1[index])$fatal(1,"unwritten stage1 read"); read_response_data<=memory1[index];
                    end else if(saved_read_address>=BASE_STAGE2 && saved_read_address<BASE_STAGE2+SIZE12)begin
                        index=saved_read_address-BASE_STAGE2; if(!visible2[index])$fatal(1,"unwritten stage2 read"); read_response_data<=memory2[index];
                    end else if(saved_read_address>=BASE_STAGE3 && saved_read_address<BASE_STAGE3+SIZE12)begin
                        index=saved_read_address-BASE_STAGE3; if(!visible3[index])$fatal(1,"unwritten stage3 read"); read_response_data<=memory3[index];
                    end else $fatal(1,"illegal logical read address %h",saved_read_address);
                    read_response_valid<=1; read_pending<=0;
                end
            end
            if(write_valid && write_ready)begin
                score_index=address_to_hwc(layer,write_address);
                if(score_index<0)$fatal(1,"write address outside layer=%0d address=%h",layer,write_address);
                if(write_data!==golden_output(layer,score_index) || $signed(write_sum)!=$signed(golden_sum(layer,score_index)))
                    $fatal(1,"write mismatch layer=%0d index=%0d data=%h sum=%0d",layer,score_index,write_data,$signed(write_sum));
                index=write_address-stage_base(layer);
                case(layer)
                    0:begin if(written0[index])$fatal(1,"duplicate stage0 write"); written0[index]=1; memory0[index]=write_data; end
                    1:begin if(written1[index])$fatal(1,"duplicate stage1 write"); written1[index]=1; memory1[index]=write_data; end
                    2:begin if(written2[index])$fatal(1,"duplicate stage2 write"); written2[index]=1; memory2[index]=write_data; end
                    3:begin if(written3[index])$fatal(1,"duplicate stage3 write"); written3[index]=1; memory3[index]=write_data; end
                    default:begin if(written4[index])$fatal(1,"duplicate stage4 write"); written4[index]=1; memory4[index]=write_data; end
                endcase
                if(outputs==0)first_write_address=write_address;
                outputs=outputs+1;
                stage_outputs[layer]=stage_outputs[layer]+1;
            end
            if(barrier_valid && barrier_ready && barrier_layer==layer)begin
                case(layer)
                    0:visible0<=written0; 1:visible1<=written1; 2:visible2<=written2;
                    3:visible3<=written3; default:visible4<=written4;
                endcase
                barriers=barriers+1;
            end
        end
    end

    // 反压只改变ready；valid及完整载荷稳定性由下面的逐拍检查器验证。
    always @(negedge clk)begin
        if(!rstn)begin parameter_ready=0; read_ready=0; write_ready=0; barrier_ready=0; barrier_layer=0; owner_admit=0; end
        else begin
            parameter_ready=1; read_ready=1; write_ready=1; barrier_ready=barrier_valid; barrier_layer=layer; owner_admit=1;
            if(test_case==9)begin
                parameter_ready=lfsr[0]||lfsr[3]; read_ready=lfsr[1]||lfsr[5]; write_ready=lfsr[2]||lfsr[7];
                owner_admit=lfsr[4]||lfsr[6];
            end
            if(test_case==10)begin
                if(parameter_valid && parameter_stalls<64)begin parameter_ready=0; parameter_stalls=parameter_stalls+1; end
                if(read_valid && read_stalls<128)begin read_ready=0; read_stalls=read_stalls+1; end
                if(write_valid && write_stalls<512)begin write_ready=0; write_stalls=write_stalls+1; end
                if(core_valid && core_stalls<64)begin owner_admit=0; core_stalls=core_stalls+1; end
            end
            if(test_case==17 && barrier_valid && barrier_stalls<320)begin barrier_ready=0; barrier_stalls=barrier_stalls+1; end
            if(test_case==18 && barrier_valid && barriers==0)begin barrier_ready=1; barrier_layer=layer+1'b1; end
        end
    end

    // 数值、唯一性、组参数和所有ready/valid保持合同均只观察真实握手。
    always @(posedge clk)begin
        cycles=cycles+1;
        if(active && cycles-run_start>3000000)$fatal(1,"CSP complete watchdog case=%0d",test_case);
        if(active && rstn)begin
            state_cycles[client.state_current]=state_cycles[client.state_current]+1;
            stage_cycles[layer]=stage_cycles[layer]+1;
        end
        if(rstn)lfsr<={lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
        if(active && fault && test_case<13)$fatal(1,"unexpected fault case=%0d",test_case);
        if(done && barriers!=5)$fatal(1,"done before five visible barriers");
        if(client.flag_task_done)begin tasks=tasks+1; stage_tasks[layer]=stage_tasks[layer]+1; end
        if(core_valid && core_ready)begin
            build_parameter(layer,parameter_channel,parameter_group,parameter_window,expected_weight,expected_parameter);
            for(lane=0;lane<3;lane=lane+1)begin
                if(core_output_mask[lane])begin
                    if(core_weight[lane*64 +: 64]!==expected_weight[lane*64 +: 64] ||
                        core_bias[lane*32 +: 32]!==expected_parameter[lane*32 +: 32] ||
                        core_pre_multiplier[lane*32 +: 32]!==expected_parameter[96+lane*32 +: 32] ||
                        core_pre_shift[lane*6 +: 6]!==expected_parameter[192+lane*6 +: 6])$fatal(1,"core parameter mapping mismatch");
                end else if(core_weight[lane*64 +: 64]!==0 || core_bias[lane*32 +: 32]!==0 ||
                    core_pre_multiplier[lane*32 +: 32]!==0 || core_pre_shift[lane*6 +: 6]!==0)$fatal(1,"masked output lane not zero");
            end
            if(core_post_multiplier!==expected_parameter[241:210] || core_post_shift!==expected_parameter[247:242] ||
                core_tags!==48'h000200010000)$fatal(1,"core shared metadata mismatch");
            for(lane=0;lane<8;lane=lane+1)if(!core_input_mask[lane] && core_activation[lane*8 +: 8]!==0)$fatal(1,"tail input lane not zero");
            groups=groups+1;
            stage_groups[layer]=stage_groups[layer]+1;
        end
        if(arithmetic_Inst.flag_acc_accept)begin
            for(lane=0;lane<3;lane=lane+1)if(arithmetic_Inst.reg_output_mask[lane])begin
                score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(lane*32))&32'hffffffff);
                if(score_index<0)$fatal(1,"acc address decode failed");
                mark_seen_acc(layer,score_index);
                if(negative_acc!=0 && accumulators==0)begin
                    if(arithmetic_Inst.mac_data[lane*32 +: 32]!==
                        (golden_acc(layer,score_index)^32'd1))$fatal(1,"NEGATIVE_ACC injected acc mismatch");
                end else if(arithmetic_Inst.mac_data[lane*32 +: 32]!==golden_acc(layer,score_index))$fatal(1,"acc mismatch layer=%0d index=%0d",layer,score_index);
                accumulators=accumulators+1;
            end
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_silu_accept)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[1:0]*16))&65535;
            if(score_tag>2)$fatal(1,"pre tag invalid");
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            mark_seen_pre(layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_data!==golden_pre(layer,score_index))$fatal(1,"pre mismatch");
            pres=pres+1;
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_accept)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][1:0]*16))&65535;
            if(score_tag>2)$fatal(1,"silu tag invalid");
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            mark_seen_silu(layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.silu_output_data!==golden_silu(layer,score_index))$fatal(1,"silu mismatch");
            silus=silus+1;
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_complete)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[1:0]*16))&65535;
            if(score_tag>2)$fatal(1,"post tag invalid");
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            mark_seen_post(layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.wire_post_saturated!==$signed(golden_post(layer,score_index)))$fatal(1,"post mismatch");
            posts=posts+1;
        end
        if(held_parameter_request && {layer,parameter_channel,parameter_group,parameter_window}!==held_parameter_request_payload)$fatal(1,"parameter request changed under backpressure");
        held_parameter_request=parameter_valid&&!parameter_ready; held_parameter_request_payload={layer,parameter_channel,parameter_group,parameter_window};
        if(held_parameter_response && {parameter_error,parameter_response_layer,parameter_response_channel,parameter_response_group,parameter_response_window,parameter_response_weight,parameter_response_data}!==held_parameter_response_payload)$fatal(1,"parameter response changed under backpressure");
        held_parameter_response=parameter_response_valid&&!parameter_response_ready;
        held_parameter_response_payload={parameter_error,parameter_response_layer,parameter_response_channel,parameter_response_group,parameter_response_window,parameter_response_weight,parameter_response_data};
        if(held_read_request && read_address!==held_read_request_payload)$fatal(1,"read request changed under backpressure");
        held_read_request=read_valid&&!read_ready; held_read_request_payload=read_address;
        if(held_read_response && {read_error,read_response_address,read_response_data}!==held_read_response_payload)$fatal(1,"read response changed under backpressure");
        held_read_response=read_response_valid&&!read_response_ready; held_read_response_payload={read_error,read_response_address,read_response_data};
        if(held_core && {core_first,core_last,core_input_mask,core_activation,core_weight,core_bias,core_output_mask,core_tags,core_addresses,core_pre_multiplier,core_pre_shift,core_post_multiplier,core_post_shift,core_residual,core_bypass}!==held_core_payload)$fatal(1,"core group changed under backpressure");
        held_core=core_valid&&!core_ready; held_core_payload={core_first,core_last,core_input_mask,core_activation,core_weight,core_bias,core_output_mask,core_tags,core_addresses,core_pre_multiplier,core_pre_shift,core_post_multiplier,core_post_shift,core_residual,core_bypass};
        if(held_write && {write_sum,write_address,write_data}!==held_write_payload)$fatal(1,"write changed under backpressure");
        held_write=write_valid&&!write_ready; held_write_payload={write_sum,write_address,write_data}; if(held_write)held_cycles=held_cycles+1;
        if(held_barrier && layer!==held_barrier_payload)$fatal(1,"barrier layer changed under backpressure");
        held_barrier=barrier_valid&&!barrier_ready; held_barrier_payload=layer;
    end

    task load_reference;
        begin
            $readmemh({vector_path,"/parameters/silu.hex"},silu_table);
            $readmemh({vector_path,"/vectors/source.hex"},source_hwc);
            $readmemh({vector_path,"/parameters/stage0_weights.hex"},weight0); $readmemh({vector_path,"/parameters/stage1_weights.hex"},weight1);
            $readmemh({vector_path,"/parameters/stage2_weights.hex"},weight2); $readmemh({vector_path,"/parameters/stage3_weights.hex"},weight3); $readmemh({vector_path,"/parameters/stage4_weights.hex"},weight4);
            $readmemh({vector_path,"/parameters/stage0_bias.hex"},bias0); $readmemh({vector_path,"/parameters/stage1_bias.hex"},bias1); $readmemh({vector_path,"/parameters/stage2_bias.hex"},bias2); $readmemh({vector_path,"/parameters/stage3_bias.hex"},bias3); $readmemh({vector_path,"/parameters/stage4_bias.hex"},bias4);
            $readmemh({vector_path,"/parameters/stage0_pre_multiplier.hex"},premul0); $readmemh({vector_path,"/parameters/stage1_pre_multiplier.hex"},premul1); $readmemh({vector_path,"/parameters/stage2_pre_multiplier.hex"},premul2); $readmemh({vector_path,"/parameters/stage3_pre_multiplier.hex"},premul3); $readmemh({vector_path,"/parameters/stage4_pre_multiplier.hex"},premul4);
            $readmemh({vector_path,"/parameters/stage0_pre_shift.hex"},preshift0); $readmemh({vector_path,"/parameters/stage1_pre_shift.hex"},preshift1); $readmemh({vector_path,"/parameters/stage2_pre_shift.hex"},preshift2); $readmemh({vector_path,"/parameters/stage3_pre_shift.hex"},preshift3); $readmemh({vector_path,"/parameters/stage4_pre_shift.hex"},preshift4);
            $readmemh({vector_path,"/parameters/stage0_post_multiplier.hex"},postmul0); $readmemh({vector_path,"/parameters/stage1_post_multiplier.hex"},postmul1); $readmemh({vector_path,"/parameters/stage2_post_multiplier.hex"},postmul2); $readmemh({vector_path,"/parameters/stage3_post_multiplier.hex"},postmul3); $readmemh({vector_path,"/parameters/stage4_post_multiplier.hex"},postmul4);
            $readmemh({vector_path,"/parameters/stage0_post_shift.hex"},postshift0); $readmemh({vector_path,"/parameters/stage1_post_shift.hex"},postshift1); $readmemh({vector_path,"/parameters/stage2_post_shift.hex"},postshift2); $readmemh({vector_path,"/parameters/stage3_post_shift.hex"},postshift3); $readmemh({vector_path,"/parameters/stage4_post_shift.hex"},postshift4);
            $readmemh({vector_path,"/vectors/stage0_acc.hex"},gold_acc0); $readmemh({vector_path,"/vectors/stage1_acc.hex"},gold_acc1); $readmemh({vector_path,"/vectors/stage2_acc.hex"},gold_acc2); $readmemh({vector_path,"/vectors/stage3_acc.hex"},gold_acc3); $readmemh({vector_path,"/vectors/stage4_acc.hex"},gold_acc4);
            $readmemh({vector_path,"/vectors/stage0_pre.hex"},gold_pre0); $readmemh({vector_path,"/vectors/stage1_pre.hex"},gold_pre1); $readmemh({vector_path,"/vectors/stage2_pre.hex"},gold_pre2); $readmemh({vector_path,"/vectors/stage3_pre.hex"},gold_pre3); $readmemh({vector_path,"/vectors/stage4_pre.hex"},gold_pre4);
            $readmemh({vector_path,"/vectors/stage0_silu.hex"},gold_silu0); $readmemh({vector_path,"/vectors/stage1_silu.hex"},gold_silu1); $readmemh({vector_path,"/vectors/stage2_silu.hex"},gold_silu2); $readmemh({vector_path,"/vectors/stage3_silu.hex"},gold_silu3); $readmemh({vector_path,"/vectors/stage4_silu.hex"},gold_silu4);
            $readmemh({vector_path,"/vectors/stage0_post.hex"},gold_post0); $readmemh({vector_path,"/vectors/stage1_post.hex"},gold_post1); $readmemh({vector_path,"/vectors/stage2_post.hex"},gold_post2); $readmemh({vector_path,"/vectors/stage3_post.hex"},gold_post3); $readmemh({vector_path,"/vectors/stage4_post.hex"},gold_post4);
            $readmemh({vector_path,"/vectors/stage0_sum.hex"},gold_sum0); $readmemh({vector_path,"/vectors/stage1_sum.hex"},gold_sum1); $readmemh({vector_path,"/vectors/stage2_sum.hex"},gold_sum2); $readmemh({vector_path,"/vectors/stage3_sum.hex"},gold_sum3); $readmemh({vector_path,"/vectors/stage4_sum.hex"},gold_sum4);
            $readmemh({vector_path,"/vectors/stage0_output.hex"},gold_output0); $readmemh({vector_path,"/vectors/stage1_output.hex"},gold_output1); $readmemh({vector_path,"/vectors/stage2_output.hex"},gold_output2); $readmemh({vector_path,"/vectors/stage3_output.hex"},gold_output3); $readmemh({vector_path,"/vectors/stage4_output.hex"},gold_output4);
        end
    endtask

    initial begin
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("FAULT_KIND=%d",fault_kind))fault_kind=0;
        if(!$value$plusargs("RESET_STAGE=%d",reset_stage))reset_stage=0;
        if(!$value$plusargs("NEGATIVE_ACC=%d",negative_acc))negative_acc=0;
        if(!$value$plusargs("VECTORS=%s",vector_path))$fatal(1,"VECTORS reference root missing");
        load_reference;
        case(test_case)
            0:begin tile_y=0; tile_x=0; end
            1:begin tile_y=0; tile_x=60; end
            2:begin tile_y=0; tile_x=124; end
            3:begin tile_y=32; tile_x=0; end
            4:begin tile_y=32; tile_x=60; end
            5:begin tile_y=32; tile_x=124; end
            6:begin tile_y=68; tile_x=0; end
            7:begin tile_y=68; tile_x=60; end
            8:begin tile_y=68; tile_x=124; end
            11:begin tile_y=0; tile_x=0; end
            default:begin tile_y=32; tile_x=60; end
        endcase
        reset_and_load_table;
        launch_tile(tile_y,tile_x);
        if(test_case==12)begin
            wait(layer==reset_stage && busy);
            repeat(12)@(posedge clk);
            reset_and_load_table;
            launch_tile(32,60);
            finish_run(32,60);
            $display("CSP_COMPLETE_PASS case=%0d runs=%0d cycles=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d reads=%0d barriers=%0d",
                test_case,runs,final_cycles,groups,tasks,outputs,accumulators,pres,silus,posts,reads,barriers);
        end else if(test_case==13)begin
            wait(outputs==20); @(negedge clk); cancel=1; @(posedge clk); @(negedge clk); cancel=0; active=0;
            repeat(8)@(negedge clk);
            if(!fault || done || write_valid || start_ready || outputs!=20)$fatal(1,"cancel fault contract failed");
            $display("CSP_COMPLETE_EXPECTED_FAULT case=%0d outputs=%0d kind=%0d",test_case,outputs,fault_kind);
        end else if(test_case==14 || test_case==15 || test_case==18)begin
            wait(fault); active=0; repeat(8)@(negedge clk);
            if(done || write_valid || start_ready)$fatal(1,"service fault leaked completion/write");
            if((test_case==14 || test_case==15) && outputs!=0)$fatal(1,"early service fault wrote data");
            if(test_case==18 && outputs!=432)$fatal(1,"wrong barrier layer output boundary mismatch");
            $display("CSP_COMPLETE_EXPECTED_FAULT case=%0d outputs=%0d kind=%0d",test_case,outputs,fault_kind);
        end else if(test_case==16)begin
            if(fault_kind==0)begin
                wait(core_output_valid); @(negedge clk); force core_output_tag=16'd3;
            end else if(fault_kind==2)begin
                wait(core_output_valid); @(negedge clk); force core_output_address=32'hffffffff;
            end else begin
                wait(outputs==1); wait(core_output_valid); @(negedge clk);
                force core_output_tag=16'd0; force core_output_address=first_write_address;
            end
            @(posedge clk); @(negedge clk); active=0;
            repeat(8)@(negedge clk);
            if(!fault || done || write_valid || start_ready || outputs!=(fault_kind==1 ? 1 : 0))$fatal(1,"illegal/duplicate result not rejected");
            release core_output_tag; release core_output_address;
            $display("CSP_COMPLETE_EXPECTED_FAULT case=%0d outputs=%0d kind=%0d",test_case,outputs,fault_kind);
        end else begin
            finish_run(tile_y,tile_x);
            if(test_case==11)begin
                if(table_loads!=1)$fatal(1,"table unexpectedly reloaded");
                launch_tile(68,124); finish_run(68,124);
                if(table_loads!=1 || runs!=2)$fatal(1,"two-tile reuse contract failed");
            end
            $display("CSP_COMPLETE_PASS case=%0d runs=%0d cycles=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d reads=%0d barriers=%0d",
                test_case,runs,final_cycles,groups,tasks,outputs,accumulators,pres,silus,posts,reads,barriers);
        end
        complete=1; $finish;
    end
endmodule
