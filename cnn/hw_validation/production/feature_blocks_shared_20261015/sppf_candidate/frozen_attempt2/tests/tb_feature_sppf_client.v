`timescale 1ns / 1ps
// CSP4真实输出驱动SPPF；池化、concat与共享算术核按同一实例检查。
module tb_feature_sppf_client(output o_test_complete);
    // 形状仅由测试期望块选择，DUT只接收4位固定块ID。
    integer selected_block = 4;
    integer HEIGHT, WIDTH, HALF_CHANNELS, FULL_CHANNELS;
    integer TILE_COLUMNS, TILE_ROWS, TILE_COUNT, STAGE_COUNT;
    integer HALF_LOGICAL, FULL_LOGICAL, HALF_PHYSICAL, FULL_PHYSICAL;
    integer TOTAL_OUTPUTS, TOTAL_TASKS, TOTAL_GROUPS, TOTAL_NUMERIC;
    localparam integer MAX_LOGICAL = 55296;
    localparam integer MAX_PHYSICAL = 61440;
    localparam [31:0] BASE_MEMORY = 32'h0372c000;
    localparam integer MEMORY_BYTES = 446464;
    localparam integer STATE_COUNT = 20;
    localparam integer MAX_WEIGHT = 9216;
    localparam integer MAX_CHANNEL = 96;
    localparam integer WATCHDOG_CYCLES = 130000000;
    reg [31:0] BASE_SOURCE;
    reg [31:0] stage_bases [0:6];
    reg [3:0] input_block_id = 0;
    wire [3:0] block_id;
    reg [3:0] parameter_response_block_id = 0;
    reg [3:0] saved_parameter_block_id = 0;
    reg [3:0] barrier_block_id = 0;
    reg [4095:0] vectors_root;
    integer sequence_start = 0;
    integer clean_cycles = 0;
    integer clean_accounted = 0;
    integer clean_outputs = 0;
    integer clean_acc = 0;
    integer clean_pre = 0;
    integer clean_silu = 0;
    integer clean_post = 0;
    integer clean_groups = 0;
    integer clean_tasks = 0;
    integer clean_reads = 0;
    integer clean_parameters = 0;
    integer clean_barriers = 0;
    integer aborted_cycles = 0;
    integer aborted_outputs = 0;
    integer aborted_runs = 0;
    integer sequence_block;
    integer load_stage;
    integer vector_handle;
    reg [4095:0] stage_path;

    reg clk = 0;
    reg rstn = 0;
    reg start = 0;
    reg cancel = 0;
    wire start_ready;
    wire busy;
    wire done;
    wire fault;
    wire [2:0] layer;
    wire [6:0] tile_y;
    wire [7:0] tile_x;

    wire parameter_valid;
    wire [6:0] parameter_channel;
    wire [4:0] parameter_group;
    wire [2:0] parameter_window;
    reg parameter_ready = 0;
    reg parameter_response_valid = 0;
    reg [2:0] parameter_response_layer = 0;
    reg [6:0] parameter_response_channel = 0;
    reg [4:0] parameter_response_group = 0;
    reg [2:0] parameter_response_window = 0;
    reg [191:0] parameter_response_weight = 0;
    reg [247:0] parameter_response_data = 0;
    reg parameter_error = 0;
    wire parameter_response_ready;

    wire read_valid;
    wire [31:0] read_address;
    reg read_ready = 0;
    reg read_response_valid = 0;
    reg [31:0] read_response_address = 0;
    reg [127:0] read_response_data = 0;
    reg read_error = 0;
    wire read_response_ready;

    wire write_valid;
    wire [31:0] write_address;
    wire [7:0] write_data;
    wire signed [8:0] write_sum;
    reg write_ready = 0;
    wire barrier_valid;
    reg barrier_ready = 0;
    reg [2:0] barrier_layer = 0;

    wire core_valid;
    wire core_ready;
    wire owner_core_ready;
    reg owner_admit = 0;
    wire core_first;
    wire core_last;
    wire [7:0] core_input_mask;
    wire [63:0] core_activation;
    wire [191:0] core_weight;
    wire [95:0] core_bias;
    wire [2:0] core_output_mask;
    wire [47:0] core_tags;
    wire [95:0] core_addresses;
    wire [95:0] core_pre_multiplier;
    wire [17:0] core_pre_shift;
    wire [31:0] core_post_multiplier;
    wire [5:0] core_post_shift;
    wire core_residual;
    wire [23:0] core_bypass;
    wire core_output_valid;
    wire core_output_ready;
    wire signed [7:0] core_output_data;
    wire [15:0] core_output_tag;
    wire [31:0] core_output_address;
    wire signed [8:0] core_output_sum;
    wire core_fault;

    reg table_valid = 0;
    reg [9:0] table_address = 0;
    reg signed [15:0] table_data = 0;
    wire table_ready;
    wire table_loaded;
    reg signed [15:0] silu_table [0:1023];

    // 扁平数组避免为七阶段复制访问逻辑；每阶段仍有独立固定槽位。
    reg signed [7:0] source_hwc [0:MAX_LOGICAL-1];
    reg signed [7:0] live_memory [0:MEMORY_BYTES-1];
    reg [MEMORY_BYTES-1:0] written;
    reg [MEMORY_BYTES-1:0] visible;
    reg signed [7:0] weights [0:7*MAX_WEIGHT-1];
    reg signed [31:0] biases [0:7*MAX_CHANNEL-1];
    reg signed [31:0] premuls [0:7*MAX_CHANNEL-1];
    reg [7:0] preshifts [0:7*MAX_CHANNEL-1];
    reg signed [31:0] postmuls [0:6];
    reg [7:0] postshifts [0:6];
    reg signed [31:0] gold_acc [0:7*MAX_LOGICAL-1];
    reg signed [15:0] gold_pre [0:7*MAX_LOGICAL-1];
    reg signed [15:0] gold_silu [0:7*MAX_LOGICAL-1];
    reg signed [7:0] gold_post [0:7*MAX_LOGICAL-1];
    reg signed [15:0] gold_sum [0:7*MAX_LOGICAL-1];
    reg signed [7:0] gold_output [0:7*MAX_LOGICAL-1];
    reg [7*MAX_LOGICAL-1:0] seen_acc;
    reg [7*MAX_LOGICAL-1:0] seen_pre;
    reg [7*MAX_LOGICAL-1:0] seen_silu;
    reg [7*MAX_LOGICAL-1:0] seen_post;
    reg [7*576-1:0] tile_seen;

    reg parameter_pending = 0;
    reg [7:0] parameter_delay = 0;
    reg [2:0] saved_parameter_layer = 0;
    reg [6:0] saved_parameter_channel = 0;
    reg [4:0] saved_parameter_group = 0;
    reg [2:0] saved_parameter_window = 0;
    reg read_pending = 0;
    reg [7:0] read_delay = 0;
    reg [31:0] saved_read_address = 0;
    reg [127:0] generated_read_data = 0;
    reg [31:0] lfsr = 32'h75bcd15a;
    reg complete = 0;
    reg active = 0;
    reg random_mode = 0;
    reg [4095:0] vector_path;
    reg [191:0] expected_weight;
    reg [247:0] expected_parameter;

    reg held_parameter_request, held_parameter_response, held_read_request, held_read_response;
    reg held_core, held_core_output, held_write, held_barrier;
    reg [21:0] held_parameter_request_payload;
    reg [462:0] held_parameter_response_payload;
    reg [31:0] held_read_request_payload;
    reg [160:0] held_read_response_payload;
    reg [685:0] held_core_payload;
    reg [65:0] held_core_output_payload;
    reg [48:0] held_write_payload;
    reg [6:0] held_barrier_payload;

    integer test_case;
            integer negative_acc;
    reg prefix_mode = 0;
    integer prefix_outputs = 0;
    integer negative_pool;
    integer pools = 0;
    integer clean_pools = 0;
    integer long_pool_stalls = 0;
    integer pool_stall_bursts = 0;
    integer concat_values = 0;
    integer clean_concat_values = 0;
    integer busy_id_perturb_cycles = 0;
    integer busy_start_cycles = 0;
    integer clean_busy_id_perturb_cycles = 0;
    integer clean_busy_start_cycles = 0;
    integer negative_pool_outputs = 0;
    integer clean_negative_pool_outputs = 0;
    integer golden_index;
    integer reference_stage;
    reg [4095:0] node_name;
    reg signed [7:0] gold_concat [0:55295];
    integer cycles = 0;
    integer run_start = 0;
    integer final_cycles = 0;
    integer groups = 0;
    integer tasks = 0;
    integer retires = 0;
    integer outputs = 0;
    integer accumulators = 0;
    integer pres = 0;
    integer silus = 0;
    integer posts = 0;
    integer reads = 0;
    integer parameters = 0;
    integer barriers = 0;
    integer runs = 0;
    integer table_loads = 0;
    integer accounted_cycles = 0;
    integer stage_cycles [0:6];
    integer stage_reads [0:6];
    integer stage_parameters [0:6];
    integer stage_outputs [0:6];
    integer stage_groups [0:6];
    integer stage_tasks [0:6];
    integer stage_barriers [0:6];
    integer state_cycles [0:STATE_COUNT-1];
    integer counter_index;
    integer cycle_sum;
    integer memory_index;
    integer poison_index;
    integer lane;
    integer score_index;
    integer score_tag;
    integer tile_index;
    integer core_group_index = 0;
    integer core_channel;
    integer core_window;
    integer core_position;
    integer core_expected_groups;
    integer core_expected_inputs;
    integer core_seen_inputs;
    integer physical_index;

    assign o_test_complete = complete;
    assign core_ready = owner_core_ready && owner_admit;
    always #5 clk = ~clk;

    function integer flag_dw_stage;
        input integer stage;
        begin flag_dw_stage = selected_block==4 && stage < STAGE_COUNT-1 && (stage == 0 || stage == 2 || stage == 4); end
    endfunction

    // SPPF三层池化不经过算术owner。
    function integer flag_pool_stage;
        input integer stage;
        begin flag_pool_stage=selected_block==5 && stage>=1 && stage<=3; end
    endfunction

    function integer stage_input_channels;
        input integer stage;
        begin stage_input_channels=selected_block==5 || stage==STAGE_COUNT-1 ? FULL_CHANNELS : HALF_CHANNELS; end
    endfunction

    function integer stage_channels;
        input integer stage;
        begin stage_channels = stage == STAGE_COUNT-1 ? FULL_CHANNELS : HALF_CHANNELS; end
    endfunction

    function integer stage_logical_size;
        input integer stage;
        begin stage_logical_size = stage == STAGE_COUNT-1 ? FULL_LOGICAL : HALF_LOGICAL; end
    endfunction

    function integer stage_physical_size;
        input integer stage;
        begin stage_physical_size = stage == STAGE_COUNT-1 ? FULL_PHYSICAL : HALF_PHYSICAL; end
    endfunction

    function [31:0] stage_base;
        input integer stage;
        begin
            stage_base=stage_bases[stage];
        end
    endfunction

    function integer physical_to_hwc;
        input integer index;
        input integer channels;
        integer pixel_index, intra_index, physical_tile, y_value, x_value, channel_value;
        begin
            channel_value=index%channels;
            pixel_index=index/channels;
            intra_index=pixel_index%16;
            physical_tile=pixel_index/16;
            y_value=(physical_tile/TILE_COLUMNS)*4+intra_index/4;
            x_value=(physical_tile%TILE_COLUMNS)*4+intra_index%4;
            if(y_value>=HEIGHT) physical_to_hwc=-2;
            else physical_to_hwc=(y_value*WIDTH+x_value)*channels+channel_value;
        end
    endfunction

    function integer hwc_to_physical;
        input integer index;
        input integer channels;
        integer pixel_index, y_value, x_value, channel_value;
        begin
            channel_value=index%channels;
            pixel_index=index/channels;
            y_value=pixel_index/WIDTH;
            x_value=pixel_index%WIDTH;
            hwc_to_physical=(((y_value/4)*TILE_COLUMNS+x_value/4)*16+(y_value%4)*4+x_value%4)*channels+channel_value;
        end
    endfunction

    function integer address_to_hwc;
        input integer stage;
        input [31:0] address;
        integer offset;
        begin
            offset=address-stage_base(stage);
            if(offset<0 || offset>=stage_physical_size(stage)) address_to_hwc=-1;
            else address_to_hwc=physical_to_hwc(offset,stage_channels(stage));
        end
    endfunction

    function integer expected_stage_tasks;
        input integer stage;
        integer pixels, output_groups;
        begin
            pixels=HEIGHT*WIDTH;
            if(flag_pool_stage(stage)) expected_stage_tasks=0;
            else if(flag_dw_stage(stage)) expected_stage_tasks=HEIGHT*TILE_COLUMNS*2*HALF_CHANNELS;
            else begin
                output_groups=stage_channels(stage)/3;
                expected_stage_tasks=pixels*output_groups;
            end
        end
    endfunction

    function integer expected_stage_groups;
        input integer stage;
        integer input_groups;
        begin
            if(flag_dw_stage(stage)) expected_stage_groups=expected_stage_tasks(stage)*2;
            else begin
                input_groups=(stage_input_channels(stage)+7)/8;
                expected_stage_groups=expected_stage_tasks(stage)*input_groups;
            end
        end
    endfunction

    function integer expected_stage_parameters;
        input integer stage;
        begin
            if(flag_pool_stage(stage)) expected_stage_parameters=0;
            else if(flag_dw_stage(stage)) expected_stage_parameters=TILE_COUNT*HALF_CHANNELS*4;
            else expected_stage_parameters=TILE_COUNT*(stage_channels(stage)/3)*((stage_input_channels(stage)+7)/8);
        end
    endfunction

    function integer expected_stage_reads;
        input integer stage;
        begin
            if(selected_block==5)begin
                case(stage)
                    0:expected_stage_reads=3456;
                    1,2,3:expected_stage_reads=3060;
                    default:expected_stage_reads=4608;
                endcase
            end else if(selected_block==2)begin
                case(stage)
                    0:expected_stage_reads=30210; 1:expected_stage_reads=20736; 2:expected_stage_reads=16748;
                    3:expected_stage_reads=13824; default:expected_stage_reads=27648;
                endcase
            end else if(selected_block==3)begin
                case(stage)
                    0:expected_stage_reads=9776; 1:expected_stage_reads=8064; 2:expected_stage_reads=8112;
                    3:expected_stage_reads=6912; 4:expected_stage_reads=8112; 5:expected_stage_reads=6912;
                    default:expected_stage_reads=9216;
                endcase
            end else begin
                case(stage)
                    0:expected_stage_reads=3588; 1:expected_stage_reads=3456; 2:expected_stage_reads=3588;
                    3:expected_stage_reads=3456; 4:expected_stage_reads=3588; 5:expected_stage_reads=3456;
                    default:expected_stage_reads=3456;
                endcase
            end
        end
    endfunction

    function integer count_mask_bits;
        input [7:0] mask;
        integer bit_index;
        begin
            count_mask_bits=0;
            for(bit_index=0;bit_index<8;bit_index=bit_index+1)count_mask_bits=count_mask_bits+mask[bit_index];
        end
    endfunction

    // 参数服务按冻结包原布局打包，不计算任何golden算术结果。
    task build_parameter;
        input [2:0] stage;
        input [6:0] channel;
        input [4:0] group_number;
        input [2:0] window;
        output [191:0] packed_weight;
        output [247:0] packed_parameter;
        integer output_lane, input_lane, union_index, kernel_y, kernel_x;
        integer output_channel, input_channel, input_channels, weight_index, parameter_index;
        reg [7:0] weight_value;
        begin
            packed_weight=0;
            packed_parameter=0;
            input_channels=stage_input_channels(stage);
            for(output_lane=0;output_lane<3;output_lane=output_lane+1)begin
                output_channel=flag_dw_stage(stage) ? channel : channel+output_lane;
                parameter_index=stage*MAX_CHANNEL+output_channel;
                packed_parameter[output_lane*32 +: 32]=biases[parameter_index];
                packed_parameter[96+output_lane*32 +: 32]=premuls[parameter_index];
                packed_parameter[192+output_lane*6 +: 6]=preshifts[parameter_index][5:0];
                for(input_lane=0;input_lane<8;input_lane=input_lane+1)begin
                    weight_value=0;
                    if(flag_dw_stage(stage))begin
                        union_index=group_number*8+input_lane;
                        kernel_y=union_index/window;
                        kernel_x=union_index%window-output_lane;
                        if(union_index<window*3 && kernel_y<3 && kernel_x>=0 && kernel_x<3)begin
                            weight_index=stage*MAX_WEIGHT+channel*9+kernel_y*3+kernel_x;
                            weight_value=weights[weight_index];
                        end
                    end else begin
                        input_channel=group_number*8+input_lane;
                        if(output_channel<stage_channels(stage) && input_channel<input_channels)begin
                            weight_index=stage*MAX_WEIGHT+output_channel*input_channels+input_channel;
                            weight_value=weights[weight_index];
                        end
                    end
                    packed_weight[output_lane*64+input_lane*8 +: 8]=weight_value;
                end
            end
            packed_parameter[241:210]=postmuls[stage];
            packed_parameter[247:242]=postshifts[stage][5:0];
        end
    endtask

    // 128位行服务只暴露源或已过屏障的真实写回；物理尾行字节返回零。
    task build_read_line;
        input [31:0] line_address;
        output [127:0] line_data;
        integer byte_lane, byte_offset, hwc_index, region, found, channels;
        reg [31:0] byte_address, region_base;
        begin
            line_data=0;
            if(line_address[3:0]!=0)$fatal(1,"read address unaligned block=%0d",selected_block);
            for(byte_lane=0;byte_lane<16;byte_lane=byte_lane+1)begin
                byte_address=line_address+byte_lane; found=0;
                // 只有CSP4最初source允许CPU提供；SPPF输入必须命中真实已可见写回。
                if(byte_address>=32'h0372c000 && byte_address<32'h0373b000)begin
                    byte_offset=byte_address-32'h0372c000;
                    hwc_index=physical_to_hwc(byte_offset,96);
                    line_data[byte_lane*8 +: 8]=hwc_index<0 ? 0 : source_hwc[hwc_index];
                    found=1;
                end
                for(region=0;region<12;region=region+1)begin
                    case(region)
                        0:begin region_base=32'h0373b000; channels=48; end
                        1:begin region_base=32'h03743000; channels=48; end
                        2:begin region_base=32'h0374b000; channels=48; end
                        3:begin region_base=32'h03753000; channels=48; end
                        4:begin region_base=32'h0375b000; channels=48; end
                        5:begin region_base=32'h03763000; channels=48; end
                        6:begin region_base=32'h0376b000; channels=96; end
                        7:begin region_base=32'h0377a000; channels=24; end
                        8:begin region_base=32'h0377e000; channels=24; end
                        9:begin region_base=32'h03782000; channels=24; end
                        10:begin region_base=32'h03786000; channels=24; end
                        default:begin region_base=32'h0378a000; channels=96; end
                    endcase
                    if(byte_address>=region_base && byte_address<region_base+TILE_COUNT*16*channels)begin
                        byte_offset=byte_address-region_base;
                        hwc_index=physical_to_hwc(byte_offset,channels);
                        if(hwc_index>=0 && !visible[byte_address-BASE_MEMORY])
                            $fatal(1,"read before real write/barrier block=%0d address=%h",selected_block,byte_address);
                        line_data[byte_lane*8 +: 8]=hwc_index<0 ? 0 : live_memory[byte_address-BASE_MEMORY];
                        found=1;
                    end
                end
                if(!found)$fatal(1,"read outside CSP4/SPPF regions block=%0d address=%h",selected_block,byte_address);
            end
        end
    endtask

    task mark_seen;
        input integer kind;
        input integer stage;
        input integer position;
        integer slot;
        begin
            slot=stage*MAX_LOGICAL+position;
            case(kind)
                0:begin if(seen_acc[slot])$fatal(1,"duplicate acc"); seen_acc[slot]=1; end
                1:begin if(seen_pre[slot])$fatal(1,"duplicate pre"); seen_pre[slot]=1; end
                2:begin if(seen_silu[slot])$fatal(1,"duplicate silu"); seen_silu[slot]=1; end
                default:begin if(seen_post[slot])$fatal(1,"duplicate post"); seen_post[slot]=1; end
            endcase
        end
    endtask

    task clear_scoreboard;
        begin
            groups=0; tasks=0; retires=0; outputs=0; accumulators=0; pres=0; silus=0; posts=0;
            reads=0; parameters=0; barriers=0; pools=0; concat_values=0; accounted_cycles=0; core_group_index=0; core_seen_inputs=0;
            busy_id_perturb_cycles=0; busy_start_cycles=0; negative_pool_outputs=0;
            for(counter_index=0;counter_index<7;counter_index=counter_index+1)begin
                stage_cycles[counter_index]=0; stage_reads[counter_index]=0; stage_parameters[counter_index]=0;
                stage_outputs[counter_index]=0; stage_groups[counter_index]=0; stage_tasks[counter_index]=0;
                stage_barriers[counter_index]=0;
            end
            for(counter_index=0;counter_index<STATE_COUNT;counter_index=counter_index+1)state_cycles[counter_index]=0;
            seen_acc=0; seen_pre=0; seen_silu=0; seen_post=0; tile_seen=0;
            held_parameter_request=0; held_parameter_response=0; held_read_request=0; held_read_response=0;
            held_core=0; held_core_output=0; held_write=0; held_barrier=0;
        end
    endtask

    task reset_and_load_table;
        begin
            active=0; start=0; cancel=0; table_valid=0;
            @(negedge clk); rstn=0;
            repeat(3)@(negedge clk);
            rstn=1;
            repeat(3)@(negedge clk);
            if(block_id!==0)$fatal(1,"common reset retained block identity");
            if(table_loaded || start_ready || done || fault)$fatal(1,"reset retained protocol state block=%0d",selected_block);
            for(memory_index=0;memory_index<1024;memory_index=memory_index+1)begin
                @(negedge clk); table_valid=1; table_address=memory_index; table_data=silu_table[memory_index];
                #1; if(!table_ready)$fatal(1,"LUT load blocked block=%0d index=%0d",selected_block,memory_index);
            end
            @(negedge clk); table_valid=0;
            #1; if(!table_loaded || !start_ready)$fatal(1,"LUT did not become active block=%0d",selected_block);
            table_loads=table_loads+1;
        end
    endtask

    task launch_frame;
        begin
            clear_scoreboard;
            @(negedge clk); input_block_id=selected_block; start=1;
            #1; if(!start_ready)$fatal(1,"full-frame start blocked block=%0d",selected_block);
            run_start=cycles; active=1;
            if(sequence_start==0)sequence_start=cycles;
            @(posedge clk); @(negedge clk); start=0;
        end
    endtask

    task finish_frame;
        integer stage_number, logical, physical, slot;
        begin
            wait(done); @(negedge clk); #1;
            final_cycles=cycles-run_start;
            if(final_cycles!=accounted_cycles)$fatal(1,"cycle endpoint mismatch block=%0d endpoint=%0d accounted=%0d",selected_block,final_cycles,accounted_cycles);
            if(fault || !busy || outputs!=TOTAL_OUTPUTS || tasks!=TOTAL_TASKS || retires!=TOTAL_TASKS ||
                groups!=TOTAL_GROUPS || accumulators!=TOTAL_NUMERIC || pres!=TOTAL_NUMERIC ||
                silus!=TOTAL_NUMERIC || posts!=TOTAL_NUMERIC || barriers!=STAGE_COUNT)
                $fatal(1,"incomplete block=%0d groups=%0d tasks=%0d retires=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d barriers=%0d",
                    selected_block,groups,tasks,retires,outputs,accumulators,pres,silus,posts,barriers);
            if(selected_block==5 && (pools!=41472 || concat_values!=1769472 || negative_pool_outputs!=1628))$fatal(1,"SPPF pool/concat coverage incomplete");
            for(stage_number=0;stage_number<STAGE_COUNT;stage_number=stage_number+1)begin
                for(logical=0;logical<stage_logical_size(stage_number);logical=logical+1)begin
                    slot=stage_number*MAX_LOGICAL+logical;
                    physical=stage_base(stage_number)-BASE_MEMORY+hwc_to_physical(logical,stage_channels(stage_number));
                    if(!written[physical] || (!flag_pool_stage(stage_number) && (!seen_acc[slot] || !seen_pre[slot] || !seen_silu[slot] || !seen_post[slot])))
                        $fatal(1,"logical coverage incomplete block=%0d stage=%0d index=%0d",selected_block,stage_number,logical);
                end
                for(physical=0;physical<stage_physical_size(stage_number);physical=physical+1)
                    if(physical_to_hwc(physical,stage_channels(stage_number))<0 && written[stage_base(stage_number)-BASE_MEMORY+physical])
                        $fatal(1,"padding row was written block=%0d stage=%0d physical=%0d",selected_block,stage_number,physical);
                for(tile_index=0;tile_index<TILE_COUNT;tile_index=tile_index+1)
                    if(!tile_seen[stage_number*576+tile_index])$fatal(1,"tile coverage incomplete block=%0d stage=%0d tile=%0d",selected_block,stage_number,tile_index);
            end
            cycle_sum=0;
            for(counter_index=0;counter_index<STATE_COUNT;counter_index=counter_index+1)begin
                cycle_sum=cycle_sum+state_cycles[counter_index];
                if(!prefix_mode)$display("FEAT_SPPF_STATE block=%0d case=%0d run=%0d state=%0d cycles=%0d",selected_block,test_case,runs+1,counter_index,state_cycles[counter_index]);
            end
            if(cycle_sum!=accounted_cycles)$fatal(1,"raw state ledger mismatch block=%0d sum=%0d accounted=%0d",selected_block,cycle_sum,accounted_cycles);
            cycle_sum=0;
            for(counter_index=0;counter_index<STAGE_COUNT;counter_index=counter_index+1)begin
                cycle_sum=cycle_sum+stage_cycles[counter_index];
                if(stage_outputs[counter_index]!=stage_logical_size(counter_index) ||
                    stage_tasks[counter_index]!=expected_stage_tasks(counter_index) ||
                    stage_groups[counter_index]!=expected_stage_groups(counter_index) ||
                    stage_reads[counter_index]!=expected_stage_reads(counter_index) ||
                    stage_parameters[counter_index]!=expected_stage_parameters(counter_index) ||
                    stage_barriers[counter_index]!=1)$fatal(1,"stage ledger mismatch block=%0d stage=%0d",selected_block,counter_index);
                if(!prefix_mode)$display("FEAT_SPPF_STAGE block=%0d case=%0d run=%0d stage=%0d cycles=%0d reads=%0d parameters=%0d groups=%0d tasks=%0d outputs=%0d barriers=%0d",
                    selected_block,test_case,runs+1,counter_index,stage_cycles[counter_index],stage_reads[counter_index],stage_parameters[counter_index],
                    stage_groups[counter_index],stage_tasks[counter_index],stage_outputs[counter_index],stage_barriers[counter_index]);
            end
            if(cycle_sum!=accounted_cycles)$fatal(1,"stage cycle ledger mismatch block=%0d",selected_block);
            active=0;
            if(prefix_mode)prefix_outputs=prefix_outputs+outputs;
            else begin
            runs=runs+1;
            clean_cycles=clean_cycles+final_cycles; clean_accounted=clean_accounted+accounted_cycles;
            clean_outputs=clean_outputs+outputs; clean_acc=clean_acc+accumulators;
            clean_pre=clean_pre+pres; clean_silu=clean_silu+silus; clean_post=clean_post+posts;
            clean_groups=clean_groups+groups; clean_tasks=clean_tasks+tasks;
            clean_reads=clean_reads+reads; clean_parameters=clean_parameters+parameters;
            clean_barriers=clean_barriers+barriers; clean_pools=clean_pools+pools;
            clean_concat_values=clean_concat_values+concat_values;
            clean_busy_id_perturb_cycles=clean_busy_id_perturb_cycles+busy_id_perturb_cycles;
            clean_busy_start_cycles=clean_busy_start_cycles+busy_start_cycles;
            clean_negative_pool_outputs=clean_negative_pool_outputs+negative_pool_outputs;
            end
            if(!prefix_mode)$display("FEAT_SPPF_RUN block=%0d case=%0d run=%0d cycles=%0d accounted=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d reads=%0d parameters=%0d barriers=%0d pools=%0d concat_values=%0d",
                selected_block,test_case,runs,final_cycles,accounted_cycles,groups,tasks,outputs,accumulators,pres,silus,posts,reads,parameters,barriers,pools,concat_values);
            @(posedge clk); @(negedge clk); start=0; #1;
            if(done || busy || write_valid || fault || !start_ready)$fatal(1,"frame did not retire to clean idle block=%0d",selected_block);
            repeat(3)@(negedge clk);
            if(done || busy || write_valid || fault || !start_ready)$fatal(1,"frame emitted stale completion block=%0d",selected_block);
        end
    endtask

    road_feature_blocks_client client(
        .i_clk(clk),.i_rstn(rstn),.i_start(start),.i_block_id(input_block_id),.o_block_id(block_id),.i_cancel(cancel),.i_table_loaded(table_loaded),
        .o_start_ready(start_ready),.o_busy(busy),.o_done(done),.o_fault(fault),.o_layer(layer),
        .o_tile_y(tile_y),.o_tile_x(tile_x),
        .o_parameter_valid(parameter_valid),.o_parameter_channel(parameter_channel),.o_parameter_group(parameter_group),
        .o_parameter_window(parameter_window),.i_parameter_ready(parameter_ready),
        .i_parameter_response_valid(parameter_response_valid),.o_parameter_response_ready(parameter_response_ready),
        .i_parameter_response_block_id(parameter_response_block_id),.i_parameter_response_layer(parameter_response_layer),.i_parameter_response_channel(parameter_response_channel),
        .i_parameter_response_group(parameter_response_group),.i_parameter_response_window(parameter_response_window),
        .i_parameter_weight(parameter_response_weight),.i_parameter_data(parameter_response_data),.i_parameter_error(parameter_error),
        .o_read_valid(read_valid),.o_read_address(read_address),.i_read_ready(read_ready),
        .i_read_response_valid(read_response_valid),.o_read_response_ready(read_response_ready),
        .i_read_response_address(read_response_address),.i_read_response_data(read_response_data),.i_read_error(read_error),
        .o_write_valid(write_valid),.o_write_address(write_address),.o_write_data(write_data),.o_write_sum(write_sum),.i_write_ready(write_ready),
        .o_barrier_valid(barrier_valid),.i_barrier_ready(barrier_ready),.i_barrier_block_id(barrier_block_id),.i_barrier_layer(barrier_layer),
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

    // 单在途参数/读服务以及写回可见性屏障。
    always @(posedge clk or negedge rstn)begin
        if(!rstn)begin
            parameter_pending<=0; parameter_response_valid<=0; parameter_error<=0;
            read_pending<=0; read_response_valid<=0; read_error<=0; written<=0; visible<=0;
        end else begin
            if(parameter_response_valid && parameter_response_ready)begin parameter_response_valid<=0; parameter_error<=0; end
            if(parameter_valid && parameter_ready)begin
                if(parameter_pending || parameter_response_valid)$fatal(1,"multiple parameter requests block=%0d",selected_block);
                parameters=parameters+1; stage_parameters[layer]=stage_parameters[layer]+1;
                saved_parameter_block_id<=block_id; saved_parameter_layer<=layer; saved_parameter_channel<=parameter_channel;
                saved_parameter_group<=parameter_group; saved_parameter_window<=parameter_window;
                parameter_delay<=random_mode ? lfsr[7:5] : 2; parameter_pending<=1;
            end
            if(parameter_pending)begin
                if(parameter_delay!=0)parameter_delay<=parameter_delay-1'b1;
                else if(!parameter_response_valid)begin
                    parameter_response_block_id<=saved_parameter_block_id; parameter_response_layer<=saved_parameter_layer; parameter_response_channel<=saved_parameter_channel;
                    parameter_response_group<=saved_parameter_group; parameter_response_window<=saved_parameter_window;
                    build_parameter(saved_parameter_layer,saved_parameter_channel,saved_parameter_group,saved_parameter_window,
                        parameter_response_weight,parameter_response_data);
                    parameter_error<=0;
                    parameter_response_valid<=1; parameter_pending<=0;
                end
            end
            if(read_response_valid && read_response_ready)begin read_response_valid<=0; read_error<=0; end
            if(read_valid && read_ready)begin
                if(read_pending || read_response_valid)$fatal(1,"multiple read requests block=%0d",selected_block);
                if(read_address[3:0]!=0)$fatal(1,"unaligned block read block=%0d address=%h",selected_block,read_address);
                saved_read_address<=read_address; read_delay<=random_mode ? lfsr[11:9] : 2; read_pending<=1;
                reads=reads+1; stage_reads[layer]=stage_reads[layer]+1;
            end
            if(read_pending)begin
                if(read_delay!=0)read_delay<=read_delay-1'b1;
                else if(!read_response_valid)begin
                    build_read_line(saved_read_address,generated_read_data);
                    read_response_address<=saved_read_address; read_response_data<=generated_read_data; read_error<=0;
                    
                    read_response_valid<=1; read_pending<=0;
                end
            end
            if(write_valid && write_ready)begin
                if(flag_pool_stage(layer))begin
                    if(negative_pool!=0 && pools==0 && write_data!==(gold_output[layer*MAX_LOGICAL+address_to_hwc(layer,write_address)]^8'd1))
                        $fatal(1,"NEGATIVE_POOL injected pool mismatch block=%0d stage=%0d",selected_block,layer);
                    pools=pools+1;
                    if($signed(write_data)<0)negative_pool_outputs=negative_pool_outputs+1;
                end
                score_index=address_to_hwc(layer,write_address);
                if(score_index<0)$fatal(1,"write address outside logical image block=%0d stage=%0d address=%h",selected_block,layer,write_address);
                if(write_data!==gold_output[layer*MAX_LOGICAL+score_index] ||
                    $signed(write_sum)!=$signed(gold_sum[layer*MAX_LOGICAL+score_index]))
                    $fatal(1,"write mismatch block=%0d stage=%0d index=%0d data=%h sum=%0d",selected_block,layer,score_index,write_data,$signed(write_sum));
                memory_index=write_address-stage_base(layer);
                physical_index=write_address-BASE_MEMORY;
                if(written[physical_index])$fatal(1,"duplicate write block=%0d stage=%0d index=%0d",selected_block,layer,memory_index);
                written[physical_index]=1; live_memory[physical_index]=write_data;
                outputs=outputs+1; stage_outputs[layer]=stage_outputs[layer]+1;
            end
            if(barrier_valid && barrier_ready && barrier_layer==layer && barrier_block_id==block_id)begin
                if(stage_outputs[layer]!=stage_logical_size(layer) || stage_tasks[layer]!=expected_stage_tasks(layer) ||
                    stage_groups[layer]!=expected_stage_groups(layer) || stage_reads[layer]!=expected_stage_reads(layer) ||
                    stage_parameters[layer]!=expected_stage_parameters(layer))
                    $fatal(1,"barrier before exact stage completion block=%0d stage=%0d",selected_block,layer);
                for(memory_index=0;memory_index<stage_physical_size(layer);memory_index=memory_index+1)
                    visible[stage_base(layer)-BASE_MEMORY+memory_index]<=written[stage_base(layer)-BASE_MEMORY+memory_index];
                barriers=barriers+1; stage_barriers[layer]=stage_barriers[layer]+1;
                $display("FEAT_SPPF_PROGRESS block=%0d case=%0d run=%0d stage=%0d cycles=%0d reads=%0d parameters=%0d groups=%0d tasks=%0d outputs=%0d",
                    selected_block,test_case,runs+1,layer,cycles-run_start,stage_reads[layer],stage_parameters[layer],stage_groups[layer],stage_tasks[layer],stage_outputs[layer]);
            end
        end
    end

    // CASE1从启动起采用确定性停顿，其他正例使用最短服务延迟。
    always @(negedge clk)begin
        if(!rstn)begin
            parameter_ready=0; read_ready=0; write_ready=0; barrier_ready=0; barrier_layer=0; barrier_block_id=0; owner_admit=0;
        end else begin
            parameter_ready=1; read_ready=1; write_ready=1; owner_admit=1;
            barrier_ready=barrier_valid; barrier_layer=layer; barrier_block_id=block_id;
            if(active && busy)begin
                // 忙时交错合法/非法ID和start脉冲，DONE周期也保持start。
                input_block_id=lfsr[19:16]; start=done ? 1 : lfsr[12];
            end
            if(test_case==3 && selected_block==5 && layer==1 && write_valid && long_pool_stalls<64)begin
                write_ready=0;
                if(long_pool_stalls==0)pool_stall_bursts=pool_stall_bursts+1;
                long_pool_stalls=long_pool_stalls+1;
            end
            if(random_mode)begin
                barrier_ready=barrier_valid && (lfsr[8]||lfsr[10]);
                parameter_ready=lfsr[0]||lfsr[3]; read_ready=lfsr[1]||lfsr[5];
                write_ready=lfsr[2]||lfsr[7]; owner_admit=lfsr[4]||lfsr[6];
            end

        end
    end

    // 全部计数只观察真实握手；accepted group序号由TB独立维护。
    always @(posedge clk)begin
        cycles=cycles+1;
        if(rstn)lfsr<={lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
        if(cycles>WATCHDOG_CYCLES)$fatal(1,"sequence watchdog block=%0d case=%0d",selected_block,test_case);
        if(active && rstn)begin
            if(client.state_current>=STATE_COUNT)$fatal(1,"unknown raw state block=%0d state=%0d",selected_block,client.state_current);
            state_cycles[client.state_current]=state_cycles[client.state_current]+1;
            if(start && start_ready)stage_cycles[0]=stage_cycles[0]+1;
            else stage_cycles[layer]=stage_cycles[layer]+1;
            accounted_cycles=accounted_cycles+1;
            if(busy && block_id!==selected_block[3:0])$fatal(1,"busy owner switched expected=%0d actual=%0d",selected_block,block_id);
            if(busy && start_ready)$fatal(1,"busy admitted another start");
            if(busy && input_block_id!==block_id)busy_id_perturb_cycles=busy_id_perturb_cycles+1;
            if(busy && start)busy_start_cycles=busy_start_cycles+1;
            if(busy && selected_block!=15 && layer>=STAGE_COUNT)$fatal(1,"active layer outside fixed block shape");
            if(busy && selected_block!=15 && (tile_y>=HEIGHT || tile_x>=WIDTH || tile_y[1:0]!=0 || tile_x[1:0]!=0))
                $fatal(1,"invalid tile block=%0d stage=%0d y=%0d x=%0d",selected_block,layer,tile_y,tile_x);
            if(busy && selected_block!=15)begin
                tile_index=(tile_y/4)*TILE_COLUMNS+tile_x/4;
                tile_seen[layer*576+tile_index]=1;
            end
        end
        if(active && fault)$fatal(1,"unexpected fault block=%0d case=%0d",selected_block,test_case);
        if(done && barriers!=STAGE_COUNT)$fatal(1,"done before seven accepted barriers block=%0d",selected_block);
        if(client.flag_task_done)retires=retires+1;
        if(core_valid && core_ready)begin
            core_position=address_to_hwc(layer,core_addresses[31:0]);
            if(flag_pool_stage(layer))$fatal(1,"pool emitted core traffic");
            if(core_position<0)$fatal(1,"core address decode failed block=%0d stage=%0d address=%h",selected_block,layer,core_addresses[31:0]);
            core_channel=core_position%stage_channels(layer);
            if(flag_dw_stage(layer))begin
                if(core_output_mask==3'b111)begin core_window=5; core_expected_inputs=15; end
                else if(core_output_mask==3'b001)begin core_window=3; core_expected_inputs=9; end
                else $fatal(1,"illegal DW output mask block=%0d mask=%b",selected_block,core_output_mask);
                core_expected_groups=(core_expected_inputs+7)/8;
                if(core_input_mask!==(core_group_index==0 ? 8'hff : (core_window==5 ? 8'h7f : 8'h01)))
                    $fatal(1,"DW mask mismatch block=%0d stage=%0d group=%0d mask=%h",selected_block,layer,core_group_index,core_input_mask);
            end else begin
                core_window=0;
                core_expected_inputs=stage_input_channels(layer);
                core_expected_groups=(core_expected_inputs+7)/8;
                if(core_output_mask!=3'b111 || core_input_mask!==
                    (core_group_index==core_expected_groups-1 && core_expected_inputs%8!=0 ? 8'h0f : 8'hff))
                    $fatal(1,"PW mask mismatch block=%0d stage=%0d group=%0d mask=%h",selected_block,layer,core_group_index,core_input_mask);
            end
            if(core_first)begin
                if(core_group_index!=0)$fatal(1,"core first mid-task block=%0d group=%0d",selected_block,core_group_index);
                core_seen_inputs=0;
            end else if(core_group_index==0)$fatal(1,"core task omitted first block=%0d",selected_block);
            if(core_last!=(core_group_index==core_expected_groups-1))
                $fatal(1,"core last/group mismatch block=%0d stage=%0d group=%0d expected=%0d",selected_block,layer,core_group_index,core_expected_groups);
            core_seen_inputs=core_seen_inputs+count_mask_bits(core_input_mask);
            build_parameter(layer,core_channel,core_group_index,core_window,expected_weight,expected_parameter);
            for(lane=0;lane<3;lane=lane+1)begin
                if(core_output_mask[lane])begin
                    if(core_weight[lane*64 +: 64]!==expected_weight[lane*64 +: 64] ||
                        core_bias[lane*32 +: 32]!==expected_parameter[lane*32 +: 32] ||
                        core_pre_multiplier[lane*32 +: 32]!==expected_parameter[96+lane*32 +: 32] ||
                        core_pre_shift[lane*6 +: 6]!==expected_parameter[192+lane*6 +: 6])
                        $fatal(1,"core parameter mapping mismatch block=%0d stage=%0d",selected_block,layer);
                end else if(core_weight[lane*64 +: 64]!==0 || core_bias[lane*32 +: 32]!==0 ||
                    core_pre_multiplier[lane*32 +: 32]!==0 || core_pre_shift[lane*6 +: 6]!==0)
                    $fatal(1,"masked output lane not zero block=%0d stage=%0d",selected_block,layer);
            end
            if(core_post_multiplier!==expected_parameter[241:210] || core_post_shift!==expected_parameter[247:242] ||
                core_tags!==48'h000200010000 || core_residual!==(selected_block==4 && layer<STAGE_COUNT-1 && (layer==1 || layer==3 || layer==5)))
                $fatal(1,"core shared metadata mismatch block=%0d stage=%0d",selected_block,layer);
            for(lane=0;lane<8;lane=lane+1)
                if(!core_input_mask[lane] && core_activation[lane*8 +: 8]!==0)$fatal(1,"tail input lane not zero block=%0d",selected_block);
            if(selected_block==5 && layer==4)begin
                for(lane=0;lane<8;lane=lane+1)begin
                    golden_index=(core_position/stage_channels(layer))*96+core_group_index*8+lane;
                    if(core_activation[lane*8 +: 8]!==gold_concat[golden_index])
                        $fatal(1,"concat input mismatch pixel=%0d channel=%0d",core_position/stage_channels(layer),core_group_index*8+lane);
                    concat_values=concat_values+1;
                end
            end
            groups=groups+1; stage_groups[layer]=stage_groups[layer]+1;
            if(core_last)begin
                if(core_seen_inputs!=core_expected_inputs)$fatal(1,"accepted input count mismatch block=%0d stage=%0d seen=%0d expected=%0d",selected_block,layer,core_seen_inputs,core_expected_inputs);
                tasks=tasks+1; stage_tasks[layer]=stage_tasks[layer]+1; core_group_index=0;
            end else core_group_index=core_group_index+1;
        end
        if(arithmetic_Inst.flag_acc_accept)begin
            for(lane=0;lane<3;lane=lane+1)if(arithmetic_Inst.reg_output_mask[lane])begin
                score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(lane*32))&32'hffffffff);
                if(score_index<0)$fatal(1,"acc address decode failed block=%0d",selected_block);
                mark_seen(0,layer,score_index);
                if(negative_acc!=0 && accumulators==0)begin
                    if(arithmetic_Inst.mac_data[lane*32 +: 32]!== (gold_acc[layer*MAX_LOGICAL+score_index]^32'd1))
                        $fatal(1,"NEGATIVE_ACC injected acc mismatch block=%0d stage=%0d index=%0d",selected_block,layer,score_index);
                end else if(arithmetic_Inst.mac_data[lane*32 +: 32]!==gold_acc[layer*MAX_LOGICAL+score_index])
                    $fatal(1,"acc mismatch block=%0d stage=%0d index=%0d",selected_block,layer,score_index);
                accumulators=accumulators+1;
            end
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_silu_accept)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[1:0]*16))&65535;
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            if(score_tag>2 || score_index<0)$fatal(1,"pre tag/address invalid block=%0d",selected_block);
            mark_seen(1,layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_data!==gold_pre[layer*MAX_LOGICAL+score_index])
                $fatal(1,"pre mismatch block=%0d stage=%0d index=%0d",selected_block,layer,score_index);
            pres=pres+1;
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_accept)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][1:0]*16))&65535;
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            if(score_tag>2 || score_index<0)$fatal(1,"silu tag/address invalid block=%0d",selected_block);
            mark_seen(2,layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.silu_output_data!==gold_silu[layer*MAX_LOGICAL+score_index])
                $fatal(1,"silu mismatch block=%0d stage=%0d index=%0d",selected_block,layer,score_index);
            silus=silus+1;
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_complete)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[1:0]*16))&65535;
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            if(score_tag>2 || score_index<0)$fatal(1,"post tag/address invalid block=%0d",selected_block);
            mark_seen(3,layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.wire_post_saturated!==$signed(gold_post[layer*MAX_LOGICAL+score_index]))
                $fatal(1,"post mismatch block=%0d stage=%0d index=%0d",selected_block,layer,score_index);
            posts=posts+1;
        end
        if(!rstn)begin
            held_parameter_request=0; held_parameter_response=0; held_read_request=0; held_read_response=0;
            held_core=0; held_core_output=0; held_write=0; held_barrier=0;
        end else begin
            if(held_parameter_request && {block_id,layer,parameter_channel,parameter_group,parameter_window}!==held_parameter_request_payload)
                $fatal(1,"parameter request changed under backpressure block=%0d",selected_block);
            held_parameter_request=parameter_valid&&!parameter_ready;
            held_parameter_request_payload={block_id,layer,parameter_channel,parameter_group,parameter_window};
            if(held_parameter_response && {parameter_error,parameter_response_block_id,parameter_response_layer,parameter_response_channel,parameter_response_group,
                parameter_response_window,parameter_response_weight,parameter_response_data}!==held_parameter_response_payload)
                $fatal(1,"parameter response changed under backpressure block=%0d",selected_block);
            held_parameter_response=parameter_response_valid&&!parameter_response_ready;
            held_parameter_response_payload={parameter_error,parameter_response_block_id,parameter_response_layer,parameter_response_channel,parameter_response_group,
                parameter_response_window,parameter_response_weight,parameter_response_data};
            if(held_read_request && read_address!==held_read_request_payload)$fatal(1,"read request changed under backpressure block=%0d",selected_block);
            held_read_request=read_valid&&!read_ready; held_read_request_payload=read_address;
            if(held_read_response && {read_error,read_response_address,read_response_data}!==held_read_response_payload)
                $fatal(1,"read response changed under backpressure block=%0d",selected_block);
            held_read_response=read_response_valid&&!read_response_ready;
            held_read_response_payload={read_error,read_response_address,read_response_data};
            if(held_core && {core_first,core_last,core_input_mask,core_activation,core_weight,core_bias,core_output_mask,core_tags,
                core_addresses,core_pre_multiplier,core_pre_shift,core_post_multiplier,core_post_shift,core_residual,core_bypass}!==held_core_payload)
                $fatal(1,"core group changed under backpressure block=%0d",selected_block);
            held_core=core_valid&&!core_ready;
            held_core_payload={core_first,core_last,core_input_mask,core_activation,core_weight,core_bias,core_output_mask,core_tags,
                core_addresses,core_pre_multiplier,core_pre_shift,core_post_multiplier,core_post_shift,core_residual,core_bypass};
            if(held_core_output && {core_fault,core_output_tag,core_output_address,core_output_data,core_output_sum}!==held_core_output_payload)
                $fatal(1,"core output changed under backpressure block=%0d",selected_block);
            held_core_output=core_output_valid&&!core_output_ready;
            held_core_output_payload={core_fault,core_output_tag,core_output_address,core_output_data,core_output_sum};
            if(held_write && {write_sum,write_address,write_data}!==held_write_payload)$fatal(1,"write changed under backpressure block=%0d",selected_block);
            held_write=write_valid&&!write_ready; held_write_payload={write_sum,write_address,write_data};
            if(held_barrier && {block_id,layer}!==held_barrier_payload)$fatal(1,"barrier layer changed under backpressure block=%0d",selected_block);
            held_barrier=barrier_valid&&!barrier_ready; held_barrier_payload={block_id,layer};
        end
    end

    // 每块源由独立CPU夹具生成；下采样尚未接成RTL依赖链。
    // CSP4 source是唯一CPU可读入口；block5只换golden和参数，保留真实live memory。
    task load_reference;
        input integer requested_block;
        begin
            selected_block=requested_block;
            HEIGHT=18; WIDTH=32; FULL_CHANNELS=96;
            HALF_CHANNELS=requested_block==4 ? 48 : 24;
            STAGE_COUNT=requested_block==4 ? 7 : 5;
            TILE_COLUMNS=8; TILE_ROWS=5; TILE_COUNT=40;
            HALF_LOGICAL=HEIGHT*WIDTH*HALF_CHANNELS; FULL_LOGICAL=55296;
            HALF_PHYSICAL=TILE_COUNT*16*HALF_CHANNELS; FULL_PHYSICAL=61440;
            TOTAL_OUTPUTS=requested_block==4 ? 221184 : 110592;
            TOTAL_NUMERIC=requested_block==4 ? 221184 : 69120;
            TOTAL_TASKS=requested_block==4 ? 87552 : 23040;
            TOTAL_GROUPS=requested_block==4 ? 470016 : 276480;
            if(requested_block==4)begin
                vector_path={vectors_root,"/csp4"};
                BASE_SOURCE=32'h0372c000;
                stage_bases[0]=32'h0373b000; stage_bases[1]=32'h03743000;
                stage_bases[2]=32'h0374b000; stage_bases[3]=32'h03753000;
                stage_bases[4]=32'h0375b000; stage_bases[5]=32'h03763000; stage_bases[6]=32'h0376b000;
                $readmemh({vector_path,"/parameters/silu.hex"},silu_table);
                $readmemh({vector_path,"/vectors/source.hex"},source_hwc,0,FULL_LOGICAL-1);
                for(load_stage=0;load_stage<STAGE_COUNT;load_stage=load_stage+1)begin
                    $sformat(stage_path,"%0s/parameters/stage%0d",vector_path,load_stage);
                    $readmemh({stage_path,"_weights.hex"},weights,load_stage*MAX_WEIGHT,
                        load_stage*MAX_WEIGHT+(flag_dw_stage(load_stage) ? HALF_CHANNELS*9 :
                        stage_channels(load_stage)*stage_input_channels(load_stage))-1);
                    $readmemh({stage_path,"_bias.hex"},biases,load_stage*MAX_CHANNEL,load_stage*MAX_CHANNEL+stage_channels(load_stage)-1);
                    $readmemh({stage_path,"_pre_multiplier.hex"},premuls,load_stage*MAX_CHANNEL,load_stage*MAX_CHANNEL+stage_channels(load_stage)-1);
                    $readmemh({stage_path,"_pre_shift.hex"},preshifts,load_stage*MAX_CHANNEL,load_stage*MAX_CHANNEL+stage_channels(load_stage)-1);
                    $readmemh({stage_path,"_post_multiplier.hex"},postmuls,load_stage,load_stage);
                    $readmemh({stage_path,"_post_shift.hex"},postshifts,load_stage,load_stage);
                    $sformat(stage_path,"%0s/vectors/stage%0d",vector_path,load_stage);
                    $readmemh({stage_path,"_acc.hex"},gold_acc,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                    $readmemh({stage_path,"_pre.hex"},gold_pre,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                    $readmemh({stage_path,"_silu.hex"},gold_silu,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                    $readmemh({stage_path,"_post.hex"},gold_post,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                    $readmemh({stage_path,"_sum.hex"},gold_sum,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                    $readmemh({stage_path,"_output.hex"},gold_output,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                end
            end else begin
                vector_path={vectors_root,"/sppf"};
                BASE_SOURCE=32'h0376b000;
                stage_bases[0]=32'h0377a000; stage_bases[1]=32'h0377e000;
                stage_bases[2]=32'h03782000; stage_bases[3]=32'h03786000; stage_bases[4]=32'h0378a000;
                $readmemh({vector_path,"/concat.03.hex"},gold_concat,0,55295);
                for(load_stage=0;load_stage<5;load_stage=load_stage+1)begin
                    if(flag_pool_stage(load_stage))begin
                        case(load_stage)
                            1:stage_path={vector_path,"/pool.00.hex"};
                            2:stage_path={vector_path,"/pool.01.hex"};
                            default:stage_path={vector_path,"/pool.02.hex"};
                        endcase
                        vector_handle=$fopen(stage_path,"r");
                        if(vector_handle==0)$fatal(1,"VECTOR_FILE_OPEN_REJECTED %0s",stage_path);
                        $fclose(vector_handle);
                        $readmemh(stage_path,gold_output,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+HALF_LOGICAL-1);
                    end else begin
                        node_name=load_stage==0 ? "sppf.squeeze.conv" : "sppf.out.conv";
                        $sformat(stage_path,"%0s/parameters/%0s",vector_path,node_name);
                        $readmemh({stage_path,".weights.hex"},weights,load_stage*MAX_WEIGHT,
                            load_stage*MAX_WEIGHT+stage_channels(load_stage)*96-1);
                        $readmemh({stage_path,".bias.hex"},biases,load_stage*MAX_CHANNEL,load_stage*MAX_CHANNEL+stage_channels(load_stage)-1);
                        $readmemh({stage_path,".pre_multiplier.hex"},premuls,load_stage*MAX_CHANNEL,load_stage*MAX_CHANNEL+stage_channels(load_stage)-1);
                        $readmemh({stage_path,".pre_shift.hex"},preshifts,load_stage*MAX_CHANNEL,load_stage*MAX_CHANNEL+stage_channels(load_stage)-1);
                        $readmemh({stage_path,".post_multiplier.hex"},postmuls,load_stage,load_stage);
                        $readmemh({stage_path,".post_shift.hex"},postshifts,load_stage,load_stage);
                        $sformat(stage_path,"%0s/%0s",vector_path,node_name);
                        $readmemh({stage_path,".acc.hex"},gold_acc,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                        $readmemh({stage_path,".pre.hex"},gold_pre,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                        $readmemh({stage_path,".silu.hex"},gold_silu,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                        $readmemh({stage_path,".post.hex"},gold_post,load_stage*MAX_LOGICAL,load_stage*MAX_LOGICAL+stage_logical_size(load_stage)-1);
                        for(golden_index=0;golden_index<stage_logical_size(load_stage);golden_index=golden_index+1)
                            gold_output[load_stage*MAX_LOGICAL+golden_index]=gold_post[load_stage*MAX_LOGICAL+golden_index];
                    end
                    for(golden_index=0;golden_index<stage_logical_size(load_stage);golden_index=golden_index+1)
                        gold_sum[load_stage*MAX_LOGICAL+golden_index]=$signed(gold_output[load_stage*MAX_LOGICAL+golden_index]);
                end
            end
        end
    endtask

    // pool中断片段包含前置CSP4，但不发出完整RUN账本；clean只计重跑的两块。
    initial begin
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("NEGATIVE_POOL=%d",negative_pool))negative_pool=0;
        negative_acc=0;
        if(!$value$plusargs("VECTORS_ROOT=%s",vectors_root))$fatal(1,"VECTORS_ROOT missing");
        if(test_case<0 || test_case>3)$fatal(1,"unsupported CASE=%0d",test_case);
        for(poison_index=0;poison_index<MEMORY_BYTES;poison_index=poison_index+1)
            live_memory[poison_index]=8'ha5^(poison_index&8'hff);
        load_reference(4); reset_and_load_table;
        if(test_case==1)random_mode=1;
        if(test_case==2)begin
            prefix_mode=1;
            launch_frame; finish_frame;
            load_reference(5); launch_frame;
            wait(layer==2 && busy && stage_outputs[2]>=128);
            @(negedge clk);
            aborted_cycles=cycles-sequence_start; aborted_outputs=prefix_outputs+outputs; aborted_runs=1;
            rstn=0;
            $display("FEAT_SPPF_ABORT block=5 case=2 cycles=%0d outputs=%0d",aborted_cycles,aborted_outputs);
            load_reference(4); reset_and_load_table;
            prefix_mode=0;
        end
        for(sequence_block=4;sequence_block<=5;sequence_block=sequence_block+1)begin
            load_reference(sequence_block); launch_frame; finish_frame;
        end
        if(runs!=2 || clean_outputs!=331776 || clean_acc!=290304 || clean_pre!=290304 ||
            clean_silu!=290304 || clean_post!=290304 || clean_groups!=746496 ||
            clean_tasks!=110592 || clean_reads!=41832 || clean_parameters!=69120 || clean_barriers!=12 ||
            clean_pools!=41472 || clean_concat_values!=1769472)$fatal(1,"chain exact count mismatch");
        if(test_case==3 && (long_pool_stalls!=64 || pool_stall_bursts!=1))$fatal(1,"long pool write stall not covered");
        if(clean_busy_id_perturb_cycles==0 || clean_busy_start_cycles==0 || clean_negative_pool_outputs!=1628)$fatal(1,"busy/pool signed coverage absent");
        if(clean_cycles!=clean_accounted || clean_cycles>=100000000)$fatal(1,"clean chain cycle/ledger mismatch");
        if(table_loads!=(test_case==2 ? 2 : 1))$fatal(1,"common reset LUT reload count mismatch");
        $display("FEATURE_SPPF_PASS case=%0d blocks=2 runs=%0d cycles=%0d accounted=%0d sequence_cycles=%0d overhead_cycles=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d groups=%0d tasks=%0d reads=%0d parameters=%0d barriers=%0d pools=%0d concat_values=%0d long_pool_stalls=%0d table_loads=%0d aborted_runs=%0d aborted_cycles=%0d aborted_outputs=%0d busy_id_perturb_cycles=%0d busy_start_cycles=%0d negative_pool_outputs=%0d",
            test_case,runs,clean_cycles,clean_accounted,cycles-sequence_start,cycles-sequence_start-clean_cycles-aborted_cycles,
            clean_outputs,clean_acc,clean_pre,clean_silu,clean_post,clean_groups,clean_tasks,clean_reads,clean_parameters,
            clean_barriers,clean_pools,clean_concat_values,long_pool_stalls,table_loads,aborted_runs,aborted_cycles,aborted_outputs,
            clean_busy_id_perturb_cycles,clean_busy_start_cycles,clean_negative_pool_outputs);
        complete=1;
        $finish;
    end
endmodule
