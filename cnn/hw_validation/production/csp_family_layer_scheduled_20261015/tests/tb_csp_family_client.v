`timescale 1ns / 1ps
// CSP3/CSP4七阶段全幅自检；真实中间存储只接收DUT写回并在匹配屏障后可见。
module tb_csp_family_client #(
    parameter integer C_FAMILY = 3
)(output o_test_complete);
    localparam integer HEIGHT = C_FAMILY == 3 ? 36 : 18;
    localparam integer WIDTH = C_FAMILY == 3 ? 64 : 32;
    localparam integer HALF_CHANNELS = C_FAMILY == 3 ? 24 : 48;
    localparam integer FULL_CHANNELS = C_FAMILY == 3 ? 48 : 96;
    localparam integer TILE_COLUMNS = WIDTH / 4;
    localparam integer TILE_ROWS = (HEIGHT + 3) / 4;
    localparam integer TILE_COUNT = TILE_COLUMNS * TILE_ROWS;
    localparam integer HALF_LOGICAL = HEIGHT * WIDTH * HALF_CHANNELS;
    localparam integer FULL_LOGICAL = HEIGHT * WIDTH * FULL_CHANNELS;
    localparam integer HALF_PHYSICAL = TILE_COUNT * 16 * HALF_CHANNELS;
    localparam integer FULL_PHYSICAL = TILE_COUNT * 16 * FULL_CHANNELS;
    localparam integer MAX_LOGICAL = 110592;
    localparam integer MAX_PHYSICAL = 110592;
    localparam integer MAX_WEIGHT = 9216;
    localparam integer MAX_CHANNEL = 96;
    localparam integer TOTAL_OUTPUTS = C_FAMILY == 3 ? 442368 : 221184;
    localparam integer TOTAL_TASKS = C_FAMILY == 3 ? 175104 : 87552;
    localparam integer TOTAL_GROUPS = C_FAMILY == 3 ? 552960 : 470016;
    localparam integer WATCHDOG_CYCLES = 100000000;
    localparam [31:0] BASE_SOURCE = C_FAMILY == 3 ? 32'h0369a000 : 32'h0372c000;
    localparam [31:0] BASE_STAGE0 = C_FAMILY == 3 ? 32'h036b5000 : 32'h0373b000;
    localparam [31:0] BASE_STAGE1 = C_FAMILY == 3 ? 32'h036c3000 : 32'h03743000;
    localparam [31:0] BASE_STAGE2 = C_FAMILY == 3 ? 32'h036d1000 : 32'h0374b000;
    localparam [31:0] BASE_STAGE3 = C_FAMILY == 3 ? 32'h036df000 : 32'h03753000;
    localparam [31:0] BASE_STAGE4 = C_FAMILY == 3 ? 32'h036ed000 : 32'h0375b000;
    localparam [31:0] BASE_STAGE5 = C_FAMILY == 3 ? 32'h036fb000 : 32'h03763000;
    localparam [31:0] BASE_STAGE6 = C_FAMILY == 3 ? 32'h03709000 : 32'h0376b000;

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
    wire [3:0] parameter_group;
    wire [2:0] parameter_window;
    reg parameter_ready = 0;
    reg parameter_response_valid = 0;
    reg [2:0] parameter_response_layer = 0;
    reg [6:0] parameter_response_channel = 0;
    reg [3:0] parameter_response_group = 0;
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
    reg signed [7:0] live_memory [0:7*MAX_PHYSICAL-1];
    reg [7*MAX_PHYSICAL-1:0] written;
    reg [7*MAX_PHYSICAL-1:0] visible;
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
    reg [7*144-1:0] tile_seen;

    reg parameter_pending = 0;
    reg [7:0] parameter_delay = 0;
    reg [2:0] saved_parameter_layer = 0;
    reg [6:0] saved_parameter_channel = 0;
    reg [3:0] saved_parameter_group = 0;
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
    reg [16:0] held_parameter_request_payload;
    reg [457:0] held_parameter_response_payload;
    reg [31:0] held_read_request_payload;
    reg [160:0] held_read_response_payload;
    reg [685:0] held_core_payload;
    reg [65:0] held_core_output_payload;
    reg [48:0] held_write_payload;
    reg [2:0] held_barrier_payload;

    integer test_case;
    integer fault_kind;
    integer reset_stage;
    integer negative_acc;
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
    integer state_cycles [0:16];
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
        begin flag_dw_stage = stage == 0 || stage == 2 || stage == 4; end
    endfunction

    function integer stage_channels;
        input integer stage;
        begin stage_channels = stage == 6 ? FULL_CHANNELS : HALF_CHANNELS; end
    endfunction

    function integer stage_logical_size;
        input integer stage;
        begin stage_logical_size = stage == 6 ? FULL_LOGICAL : HALF_LOGICAL; end
    endfunction

    function integer stage_physical_size;
        input integer stage;
        begin stage_physical_size = stage == 6 ? FULL_PHYSICAL : HALF_PHYSICAL; end
    endfunction

    function [31:0] stage_base;
        input integer stage;
        begin
            case(stage)
                0: stage_base=BASE_STAGE0;
                1: stage_base=BASE_STAGE1;
                2: stage_base=BASE_STAGE2;
                3: stage_base=BASE_STAGE3;
                4: stage_base=BASE_STAGE4;
                5: stage_base=BASE_STAGE5;
                default: stage_base=BASE_STAGE6;
            endcase
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
            if(flag_dw_stage(stage)) expected_stage_tasks=HEIGHT*TILE_COLUMNS*2*HALF_CHANNELS;
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
                input_groups=(stage==6 ? FULL_CHANNELS : HALF_CHANNELS)/8;
                expected_stage_groups=expected_stage_tasks(stage)*input_groups;
            end
        end
    endfunction

    function integer expected_stage_parameters;
        input integer stage;
        begin
            if(flag_dw_stage(stage)) expected_stage_parameters=TILE_COUNT*HALF_CHANNELS*4;
            else expected_stage_parameters=TILE_COUNT*(stage_channels(stage)/3)*((stage==6 ? FULL_CHANNELS : HALF_CHANNELS)/8);
        end
    endfunction

    function integer expected_stage_reads;
        input integer stage;
        begin
            if(C_FAMILY==3)begin
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
        input [3:0] group_number;
        input [2:0] window;
        output [191:0] packed_weight;
        output [247:0] packed_parameter;
        integer output_lane, input_lane, union_index, kernel_y, kernel_x;
        integer output_channel, input_channel, input_channels, weight_index, parameter_index;
        reg [7:0] weight_value;
        begin
            packed_weight=0;
            packed_parameter=0;
            input_channels=stage==6 ? FULL_CHANNELS : HALF_CHANNELS;
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
        integer byte_lane, byte_offset, hwc_index, region, found;
        reg [31:0] byte_address;
        begin
            line_data=0;
            if(line_address[3:0]!=0) $fatal(1,"read address is not 16-byte aligned family=%0d address=%h",C_FAMILY,line_address);
            for(byte_lane=0;byte_lane<16;byte_lane=byte_lane+1)begin
                byte_address=line_address+byte_lane;
                found=0;
                if(byte_address>=BASE_SOURCE && byte_address<BASE_SOURCE+FULL_PHYSICAL)begin
                    byte_offset=byte_address-BASE_SOURCE;
                    hwc_index=physical_to_hwc(byte_offset,FULL_CHANNELS);
                    line_data[byte_lane*8 +: 8]=hwc_index<0 ? 0 : source_hwc[hwc_index];
                    found=1;
                end
                for(region=0;region<6;region=region+1)begin
                    if(byte_address>=stage_base(region) && byte_address<stage_base(region)+stage_physical_size(region))begin
                        byte_offset=byte_address-stage_base(region);
                        hwc_index=physical_to_hwc(byte_offset,stage_channels(region));
                        if(hwc_index>=0 && !visible[region*MAX_PHYSICAL+byte_offset])
                            $fatal(1,"read byte not visible family=%0d stage=%0d address=%h",C_FAMILY,region,byte_address);
                        line_data[byte_lane*8 +: 8]=hwc_index<0 ? 0 : live_memory[region*MAX_PHYSICAL+byte_offset];
                        found=1;
                    end
                end
                if(!found) $fatal(1,"read byte outside legal regions family=%0d address=%h",C_FAMILY,byte_address);
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
            reads=0; parameters=0; barriers=0; accounted_cycles=0; core_group_index=0; core_seen_inputs=0;
            for(counter_index=0;counter_index<7;counter_index=counter_index+1)begin
                stage_cycles[counter_index]=0; stage_reads[counter_index]=0; stage_parameters[counter_index]=0;
                stage_outputs[counter_index]=0; stage_groups[counter_index]=0; stage_tasks[counter_index]=0;
                stage_barriers[counter_index]=0;
            end
            for(counter_index=0;counter_index<17;counter_index=counter_index+1)state_cycles[counter_index]=0;
            written=0; visible=0; seen_acc=0; seen_pre=0; seen_silu=0; seen_post=0; tile_seen=0;
            held_parameter_request=0; held_parameter_response=0; held_read_request=0; held_read_response=0;
            held_core=0; held_core_output=0; held_write=0; held_barrier=0;
            for(poison_index=0;poison_index<7*MAX_PHYSICAL;poison_index=poison_index+1)
                live_memory[poison_index]=8'ha5^(poison_index&8'hff);
        end
    endtask

    task reset_and_load_table;
        begin
            active=0; start=0; cancel=0; table_valid=0;
            @(negedge clk); rstn=0;
            repeat(3)@(negedge clk);
            rstn=1;
            repeat(3)@(negedge clk);
            if(table_loaded || start_ready || done || fault)$fatal(1,"reset retained protocol state family=%0d",C_FAMILY);
            for(memory_index=0;memory_index<1024;memory_index=memory_index+1)begin
                @(negedge clk); table_valid=1; table_address=memory_index; table_data=silu_table[memory_index];
                #1; if(!table_ready)$fatal(1,"LUT load blocked family=%0d index=%0d",C_FAMILY,memory_index);
            end
            @(negedge clk); table_valid=0;
            #1; if(!table_loaded || !start_ready)$fatal(1,"LUT did not become active family=%0d",C_FAMILY);
            table_loads=table_loads+1;
        end
    endtask

    task launch_frame;
        begin
            clear_scoreboard;
            @(negedge clk); start=1;
            #1; if(!start_ready)$fatal(1,"full-frame start blocked family=%0d",C_FAMILY);
            run_start=cycles; active=1;
            @(posedge clk); @(negedge clk); start=0;
        end
    endtask

    task finish_frame;
        integer stage_number, logical, physical, slot;
        begin
            wait(done); @(negedge clk); #1;
            final_cycles=cycles-run_start;
            if(final_cycles!=accounted_cycles)$fatal(1,"cycle endpoint mismatch family=%0d endpoint=%0d accounted=%0d",C_FAMILY,final_cycles,accounted_cycles);
            if(fault || !busy || outputs!=TOTAL_OUTPUTS || tasks!=TOTAL_TASKS || retires!=TOTAL_TASKS ||
                groups!=TOTAL_GROUPS || accumulators!=TOTAL_OUTPUTS || pres!=TOTAL_OUTPUTS ||
                silus!=TOTAL_OUTPUTS || posts!=TOTAL_OUTPUTS || barriers!=7)
                $fatal(1,"incomplete family=%0d groups=%0d tasks=%0d retires=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d barriers=%0d",
                    C_FAMILY,groups,tasks,retires,outputs,accumulators,pres,silus,posts,barriers);
            for(stage_number=0;stage_number<7;stage_number=stage_number+1)begin
                for(logical=0;logical<stage_logical_size(stage_number);logical=logical+1)begin
                    slot=stage_number*MAX_LOGICAL+logical;
                    physical=stage_number*MAX_PHYSICAL+hwc_to_physical(logical,stage_channels(stage_number));
                    if(!written[physical] || !seen_acc[slot] || !seen_pre[slot] || !seen_silu[slot] || !seen_post[slot])
                        $fatal(1,"logical coverage incomplete family=%0d stage=%0d index=%0d",C_FAMILY,stage_number,logical);
                end
                for(physical=0;physical<stage_physical_size(stage_number);physical=physical+1)
                    if(physical_to_hwc(physical,stage_channels(stage_number))<0 && written[stage_number*MAX_PHYSICAL+physical])
                        $fatal(1,"padding row was written family=%0d stage=%0d physical=%0d",C_FAMILY,stage_number,physical);
                for(tile_index=0;tile_index<TILE_COUNT;tile_index=tile_index+1)
                    if(!tile_seen[stage_number*144+tile_index])$fatal(1,"tile coverage incomplete family=%0d stage=%0d tile=%0d",C_FAMILY,stage_number,tile_index);
            end
            cycle_sum=0;
            for(counter_index=0;counter_index<17;counter_index=counter_index+1)begin
                cycle_sum=cycle_sum+state_cycles[counter_index];
                $display("CSP_FAMILY_STATE family=%0d case=%0d run=%0d state=%0d cycles=%0d",C_FAMILY,test_case,runs+1,counter_index,state_cycles[counter_index]);
            end
            if(cycle_sum!=accounted_cycles)$fatal(1,"raw state ledger mismatch family=%0d sum=%0d accounted=%0d",C_FAMILY,cycle_sum,accounted_cycles);
            for(counter_index=0;counter_index<7;counter_index=counter_index+1)begin
                if(stage_outputs[counter_index]!=stage_logical_size(counter_index) ||
                    stage_tasks[counter_index]!=expected_stage_tasks(counter_index) ||
                    stage_groups[counter_index]!=expected_stage_groups(counter_index) ||
                    stage_reads[counter_index]!=expected_stage_reads(counter_index) ||
                    stage_parameters[counter_index]!=expected_stage_parameters(counter_index) ||
                    stage_barriers[counter_index]!=1)$fatal(1,"stage ledger mismatch family=%0d stage=%0d",C_FAMILY,counter_index);
                $display("CSP_FAMILY_STAGE family=%0d case=%0d run=%0d stage=%0d cycles=%0d reads=%0d parameters=%0d groups=%0d tasks=%0d outputs=%0d barriers=%0d",
                    C_FAMILY,test_case,runs+1,counter_index,stage_cycles[counter_index],stage_reads[counter_index],stage_parameters[counter_index],
                    stage_groups[counter_index],stage_tasks[counter_index],stage_outputs[counter_index],stage_barriers[counter_index]);
            end
            runs=runs+1; active=0;
            $display("CSP_FAMILY_RUN family=%0d case=%0d run=%0d cycles=%0d accounted=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d reads=%0d parameters=%0d barriers=%0d",
                C_FAMILY,test_case,runs,final_cycles,accounted_cycles,groups,tasks,outputs,accumulators,pres,silus,posts,reads,parameters,barriers);
            @(posedge clk); @(negedge clk); #1;
            if(done || busy || write_valid || fault || !start_ready)$fatal(1,"frame did not retire to clean idle family=%0d",C_FAMILY);
            repeat(3)@(negedge clk);
            if(done || busy || write_valid || fault || !start_ready)$fatal(1,"frame emitted stale completion family=%0d",C_FAMILY);
        end
    endtask

    road_csp_family_client #(.C_FAMILY(C_FAMILY)) client(
        .i_clk(clk),.i_rstn(rstn),.i_start(start),.i_cancel(cancel),.i_table_loaded(table_loaded),
        .o_start_ready(start_ready),.o_busy(busy),.o_done(done),.o_fault(fault),.o_layer(layer),
        .o_tile_y(tile_y),.o_tile_x(tile_x),
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

    // 单在途参数/读服务以及写回可见性屏障。
    always @(posedge clk or negedge rstn)begin
        if(!rstn)begin
            parameter_pending<=0; parameter_response_valid<=0; parameter_error<=0;
            read_pending<=0; read_response_valid<=0; read_error<=0; written<=0; visible<=0;
        end else begin
            if(parameter_response_valid && parameter_response_ready)begin parameter_response_valid<=0; parameter_error<=0; end
            if(parameter_valid && parameter_ready)begin
                if(parameter_pending || parameter_response_valid)$fatal(1,"multiple parameter requests family=%0d",C_FAMILY);
                parameters=parameters+1; stage_parameters[layer]=stage_parameters[layer]+1;
                saved_parameter_layer<=layer; saved_parameter_channel<=parameter_channel;
                saved_parameter_group<=parameter_group; saved_parameter_window<=parameter_window;
                parameter_delay<=random_mode ? lfsr[7:5] : 2; parameter_pending<=1;
            end
            if(parameter_pending)begin
                if(parameter_delay!=0)parameter_delay<=parameter_delay-1'b1;
                else if(!parameter_response_valid)begin
                    parameter_response_layer<=saved_parameter_layer; parameter_response_channel<=saved_parameter_channel;
                    parameter_response_group<=saved_parameter_group; parameter_response_window<=saved_parameter_window;
                    build_parameter(saved_parameter_layer,saved_parameter_channel,saved_parameter_group,saved_parameter_window,
                        parameter_response_weight,parameter_response_data);
                    parameter_error<=0;
                    if(test_case==4 && outputs==0)parameter_response_layer<=saved_parameter_layer+1'b1;
                    parameter_response_valid<=1; parameter_pending<=0;
                end
            end
            if(read_response_valid && read_response_ready)begin read_response_valid<=0; read_error<=0; end
            if(read_valid && read_ready)begin
                if(read_pending || read_response_valid)$fatal(1,"multiple read requests family=%0d",C_FAMILY);
                if(read_address[3:0]!=0)$fatal(1,"unaligned block read family=%0d address=%h",C_FAMILY,read_address);
                saved_read_address<=read_address; read_delay<=random_mode ? lfsr[11:9] : 2; read_pending<=1;
                reads=reads+1; stage_reads[layer]=stage_reads[layer]+1;
            end
            if(read_pending)begin
                if(read_delay!=0)read_delay<=read_delay-1'b1;
                else if(!read_response_valid)begin
                    build_read_line(saved_read_address,generated_read_data);
                    read_response_address<=saved_read_address; read_response_data<=generated_read_data; read_error<=0;
                    if(test_case==3 && outputs==0)read_response_address<=saved_read_address+16;
                    read_response_valid<=1; read_pending<=0;
                end
            end
            if(write_valid && write_ready)begin
                score_index=address_to_hwc(layer,write_address);
                if(score_index<0)$fatal(1,"write address outside logical image family=%0d stage=%0d address=%h",C_FAMILY,layer,write_address);
                if(write_data!==gold_output[layer*MAX_LOGICAL+score_index] ||
                    $signed(write_sum)!=$signed(gold_sum[layer*MAX_LOGICAL+score_index]))
                    $fatal(1,"write mismatch family=%0d stage=%0d index=%0d data=%h sum=%0d",C_FAMILY,layer,score_index,write_data,$signed(write_sum));
                memory_index=write_address-stage_base(layer);
                physical_index=layer*MAX_PHYSICAL+memory_index;
                if(written[physical_index])$fatal(1,"duplicate write family=%0d stage=%0d index=%0d",C_FAMILY,layer,memory_index);
                written[physical_index]=1; live_memory[physical_index]=write_data;
                outputs=outputs+1; stage_outputs[layer]=stage_outputs[layer]+1;
            end
            if(barrier_valid && barrier_ready && barrier_layer==layer)begin
                if(stage_outputs[layer]!=stage_logical_size(layer) || stage_tasks[layer]!=expected_stage_tasks(layer) ||
                    stage_groups[layer]!=expected_stage_groups(layer) || stage_reads[layer]!=expected_stage_reads(layer) ||
                    stage_parameters[layer]!=expected_stage_parameters(layer))
                    $fatal(1,"barrier before exact stage completion family=%0d stage=%0d",C_FAMILY,layer);
                for(memory_index=0;memory_index<stage_physical_size(layer);memory_index=memory_index+1)
                    visible[layer*MAX_PHYSICAL+memory_index]<=written[layer*MAX_PHYSICAL+memory_index];
                barriers=barriers+1; stage_barriers[layer]=stage_barriers[layer]+1;
                $display("CSP_FAMILY_PROGRESS family=%0d case=%0d run=%0d stage=%0d cycles=%0d reads=%0d parameters=%0d groups=%0d tasks=%0d outputs=%0d",
                    C_FAMILY,test_case,runs+1,layer,cycles-run_start,stage_reads[layer],stage_parameters[layer],stage_groups[layer],stage_tasks[layer],stage_outputs[layer]);
            end
        end
    end

    // CASE1从启动起采用确定性停顿，其他正例使用最短服务延迟。
    always @(negedge clk)begin
        if(!rstn)begin
            parameter_ready=0; read_ready=0; write_ready=0; barrier_ready=0; barrier_layer=0; owner_admit=0;
        end else begin
            parameter_ready=1; read_ready=1; write_ready=1; owner_admit=1;
            barrier_ready=barrier_valid; barrier_layer=layer;
            if(random_mode)begin
                parameter_ready=lfsr[0]||lfsr[3]; read_ready=lfsr[1]||lfsr[5];
                write_ready=lfsr[2]||lfsr[7]; owner_admit=lfsr[4]||lfsr[6];
            end
            if(test_case==5 && fault_kind==1 && barrier_valid && barriers==0)begin
                barrier_ready=1; barrier_layer=layer+1'b1;
            end
        end
    end

    // 全部计数只观察真实握手；accepted group序号由TB独立维护。
    always @(posedge clk)begin
        cycles=cycles+1;
        if(rstn)lfsr<={lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
        if(active && cycles-run_start>WATCHDOG_CYCLES)$fatal(1,"watchdog family=%0d case=%0d",C_FAMILY,test_case);
        if(active && rstn)begin
            if(client.state_current>16)$fatal(1,"unknown raw state family=%0d state=%0d",C_FAMILY,client.state_current);
            state_cycles[client.state_current]=state_cycles[client.state_current]+1;
            stage_cycles[layer]=stage_cycles[layer]+1; accounted_cycles=accounted_cycles+1;
            if(tile_y>=HEIGHT || tile_x>=WIDTH || tile_y[1:0]!=0 || tile_x[1:0]!=0)
                $fatal(1,"invalid tile family=%0d stage=%0d y=%0d x=%0d",C_FAMILY,layer,tile_y,tile_x);
            tile_index=(tile_y/4)*TILE_COLUMNS+tile_x/4;
            tile_seen[layer*144+tile_index]=1;
        end
        if(active && fault && test_case<=2)$fatal(1,"unexpected fault family=%0d case=%0d",C_FAMILY,test_case);
        if(done && barriers!=7)$fatal(1,"done before seven accepted barriers family=%0d",C_FAMILY);
        if(client.flag_task_done)retires=retires+1;
        if(core_valid && core_ready)begin
            core_position=address_to_hwc(layer,core_addresses[31:0]);
            if(core_position<0)$fatal(1,"core address decode failed family=%0d stage=%0d address=%h",C_FAMILY,layer,core_addresses[31:0]);
            core_channel=core_position%stage_channels(layer);
            if(flag_dw_stage(layer))begin
                if(core_output_mask==3'b111)begin core_window=5; core_expected_inputs=15; end
                else if(core_output_mask==3'b001)begin core_window=3; core_expected_inputs=9; end
                else $fatal(1,"illegal DW output mask family=%0d mask=%b",C_FAMILY,core_output_mask);
                core_expected_groups=(core_expected_inputs+7)/8;
                if(core_input_mask!==(core_group_index==0 ? 8'hff : (core_window==5 ? 8'h7f : 8'h01)))
                    $fatal(1,"DW mask mismatch family=%0d stage=%0d group=%0d mask=%h",C_FAMILY,layer,core_group_index,core_input_mask);
            end else begin
                core_window=0;
                if(core_output_mask!=3'b111 || core_input_mask!=8'hff)$fatal(1,"PW mask mismatch family=%0d stage=%0d",C_FAMILY,layer);
                core_expected_groups=(layer==6 ? FULL_CHANNELS : HALF_CHANNELS)/8;
                core_expected_inputs=core_expected_groups*8;
            end
            if(core_first)begin
                if(core_group_index!=0)$fatal(1,"core first mid-task family=%0d group=%0d",C_FAMILY,core_group_index);
                core_seen_inputs=0;
            end else if(core_group_index==0)$fatal(1,"core task omitted first family=%0d",C_FAMILY);
            if(core_last!=(core_group_index==core_expected_groups-1))
                $fatal(1,"core last/group mismatch family=%0d stage=%0d group=%0d expected=%0d",C_FAMILY,layer,core_group_index,core_expected_groups);
            core_seen_inputs=core_seen_inputs+count_mask_bits(core_input_mask);
            build_parameter(layer,core_channel,core_group_index,core_window,expected_weight,expected_parameter);
            for(lane=0;lane<3;lane=lane+1)begin
                if(core_output_mask[lane])begin
                    if(core_weight[lane*64 +: 64]!==expected_weight[lane*64 +: 64] ||
                        core_bias[lane*32 +: 32]!==expected_parameter[lane*32 +: 32] ||
                        core_pre_multiplier[lane*32 +: 32]!==expected_parameter[96+lane*32 +: 32] ||
                        core_pre_shift[lane*6 +: 6]!==expected_parameter[192+lane*6 +: 6])
                        $fatal(1,"core parameter mapping mismatch family=%0d stage=%0d",C_FAMILY,layer);
                end else if(core_weight[lane*64 +: 64]!==0 || core_bias[lane*32 +: 32]!==0 ||
                    core_pre_multiplier[lane*32 +: 32]!==0 || core_pre_shift[lane*6 +: 6]!==0)
                    $fatal(1,"masked output lane not zero family=%0d stage=%0d",C_FAMILY,layer);
            end
            if(core_post_multiplier!==expected_parameter[241:210] || core_post_shift!==expected_parameter[247:242] ||
                core_tags!==48'h000200010000 || core_residual!==(layer==1 || layer==3 || layer==5))
                $fatal(1,"core shared metadata mismatch family=%0d stage=%0d",C_FAMILY,layer);
            for(lane=0;lane<8;lane=lane+1)
                if(!core_input_mask[lane] && core_activation[lane*8 +: 8]!==0)$fatal(1,"tail input lane not zero family=%0d",C_FAMILY);
            groups=groups+1; stage_groups[layer]=stage_groups[layer]+1;
            if(core_last)begin
                if(core_seen_inputs!=core_expected_inputs)$fatal(1,"accepted input count mismatch family=%0d stage=%0d seen=%0d expected=%0d",C_FAMILY,layer,core_seen_inputs,core_expected_inputs);
                tasks=tasks+1; stage_tasks[layer]=stage_tasks[layer]+1; core_group_index=0;
            end else core_group_index=core_group_index+1;
        end
        if(arithmetic_Inst.flag_acc_accept)begin
            for(lane=0;lane<3;lane=lane+1)if(arithmetic_Inst.reg_output_mask[lane])begin
                score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(lane*32))&32'hffffffff);
                if(score_index<0)$fatal(1,"acc address decode failed family=%0d",C_FAMILY);
                mark_seen(0,layer,score_index);
                if(negative_acc!=0 && accumulators==0)begin
                    if(arithmetic_Inst.mac_data[lane*32 +: 32]!== (gold_acc[layer*MAX_LOGICAL+score_index]^32'd1))
                        $fatal(1,"NEGATIVE_ACC injected acc mismatch family=%0d stage=%0d index=%0d",C_FAMILY,layer,score_index);
                end else if(arithmetic_Inst.mac_data[lane*32 +: 32]!==gold_acc[layer*MAX_LOGICAL+score_index])
                    $fatal(1,"acc mismatch family=%0d stage=%0d index=%0d",C_FAMILY,layer,score_index);
                accumulators=accumulators+1;
            end
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_silu_accept)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_tag[1:0]*16))&65535;
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            if(score_tag>2 || score_index<0)$fatal(1,"pre tag/address invalid family=%0d",C_FAMILY);
            mark_seen(1,layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.pre_result_data!==gold_pre[layer*MAX_LOGICAL+score_index])
                $fatal(1,"pre mismatch family=%0d stage=%0d index=%0d",C_FAMILY,layer,score_index);
            pres=pres+1;
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_accept)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_meta_read][1:0]*16))&65535;
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            if(score_tag>2 || score_index<0)$fatal(1,"silu tag/address invalid family=%0d",C_FAMILY);
            mark_seen(2,layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.silu_output_data!==gold_silu[layer*MAX_LOGICAL+score_index])
                $fatal(1,"silu mismatch family=%0d stage=%0d index=%0d",C_FAMILY,layer,score_index);
            silus=silus+1;
        end
        if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.flag_post_complete)begin
            score_tag=(arithmetic_Inst.road_dynamic_postprocess_Inst_core.reg_retire_tags[arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[4:2]] >>
                (arithmetic_Inst.road_dynamic_postprocess_Inst_core.post_result_tag[1:0]*16))&65535;
            score_index=address_to_hwc(layer,(arithmetic_Inst.reg_addresses>>(score_tag*32))&32'hffffffff);
            if(score_tag>2 || score_index<0)$fatal(1,"post tag/address invalid family=%0d",C_FAMILY);
            mark_seen(3,layer,score_index);
            if(arithmetic_Inst.road_dynamic_postprocess_Inst_core.wire_post_saturated!==$signed(gold_post[layer*MAX_LOGICAL+score_index]))
                $fatal(1,"post mismatch family=%0d stage=%0d index=%0d",C_FAMILY,layer,score_index);
            posts=posts+1;
        end
        if(!rstn)begin
            held_parameter_request=0; held_parameter_response=0; held_read_request=0; held_read_response=0;
            held_core=0; held_core_output=0; held_write=0; held_barrier=0;
        end else begin
            if(held_parameter_request && {layer,parameter_channel,parameter_group,parameter_window}!==held_parameter_request_payload)
                $fatal(1,"parameter request changed under backpressure family=%0d",C_FAMILY);
            held_parameter_request=parameter_valid&&!parameter_ready;
            held_parameter_request_payload={layer,parameter_channel,parameter_group,parameter_window};
            if(held_parameter_response && {parameter_error,parameter_response_layer,parameter_response_channel,parameter_response_group,
                parameter_response_window,parameter_response_weight,parameter_response_data}!==held_parameter_response_payload)
                $fatal(1,"parameter response changed under backpressure family=%0d",C_FAMILY);
            held_parameter_response=parameter_response_valid&&!parameter_response_ready;
            held_parameter_response_payload={parameter_error,parameter_response_layer,parameter_response_channel,parameter_response_group,
                parameter_response_window,parameter_response_weight,parameter_response_data};
            if(held_read_request && read_address!==held_read_request_payload)$fatal(1,"read request changed under backpressure family=%0d",C_FAMILY);
            held_read_request=read_valid&&!read_ready; held_read_request_payload=read_address;
            if(held_read_response && {read_error,read_response_address,read_response_data}!==held_read_response_payload)
                $fatal(1,"read response changed under backpressure family=%0d",C_FAMILY);
            held_read_response=read_response_valid&&!read_response_ready;
            held_read_response_payload={read_error,read_response_address,read_response_data};
            if(held_core && {core_first,core_last,core_input_mask,core_activation,core_weight,core_bias,core_output_mask,core_tags,
                core_addresses,core_pre_multiplier,core_pre_shift,core_post_multiplier,core_post_shift,core_residual,core_bypass}!==held_core_payload)
                $fatal(1,"core group changed under backpressure family=%0d",C_FAMILY);
            held_core=core_valid&&!core_ready;
            held_core_payload={core_first,core_last,core_input_mask,core_activation,core_weight,core_bias,core_output_mask,core_tags,
                core_addresses,core_pre_multiplier,core_pre_shift,core_post_multiplier,core_post_shift,core_residual,core_bypass};
            if(held_core_output && {core_fault,core_output_tag,core_output_address,core_output_data,core_output_sum}!==held_core_output_payload)
                $fatal(1,"core output changed under backpressure family=%0d",C_FAMILY);
            held_core_output=core_output_valid&&!core_output_ready;
            held_core_output_payload={core_fault,core_output_tag,core_output_address,core_output_data,core_output_sum};
            if(held_write && {write_sum,write_address,write_data}!==held_write_payload)$fatal(1,"write changed under backpressure family=%0d",C_FAMILY);
            held_write=write_valid&&!write_ready; held_write_payload={write_sum,write_address,write_data};
            if(held_barrier && layer!==held_barrier_payload)$fatal(1,"barrier layer changed under backpressure family=%0d",C_FAMILY);
            held_barrier=barrier_valid&&!barrier_ready; held_barrier_payload=layer;
        end
    end

    task load_reference;
        begin
            $readmemh({vector_path,"/parameters/silu.hex"},silu_table);
            $readmemh({vector_path,"/vectors/source.hex"},source_hwc,0,FULL_LOGICAL-1);
            $readmemh({vector_path,"/parameters/stage0_weights.hex"},weights,0*MAX_WEIGHT,0*MAX_WEIGHT+HALF_CHANNELS*9-1);
            $readmemh({vector_path,"/parameters/stage1_weights.hex"},weights,1*MAX_WEIGHT,1*MAX_WEIGHT+HALF_CHANNELS*HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage2_weights.hex"},weights,2*MAX_WEIGHT,2*MAX_WEIGHT+HALF_CHANNELS*9-1);
            $readmemh({vector_path,"/parameters/stage3_weights.hex"},weights,3*MAX_WEIGHT,3*MAX_WEIGHT+HALF_CHANNELS*HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage4_weights.hex"},weights,4*MAX_WEIGHT,4*MAX_WEIGHT+HALF_CHANNELS*9-1);
            $readmemh({vector_path,"/parameters/stage5_weights.hex"},weights,5*MAX_WEIGHT,5*MAX_WEIGHT+HALF_CHANNELS*HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage6_weights.hex"},weights,6*MAX_WEIGHT,6*MAX_WEIGHT+FULL_CHANNELS*FULL_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage0_bias.hex"},biases,0*MAX_CHANNEL,0*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage1_bias.hex"},biases,1*MAX_CHANNEL,1*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage2_bias.hex"},biases,2*MAX_CHANNEL,2*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage3_bias.hex"},biases,3*MAX_CHANNEL,3*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage4_bias.hex"},biases,4*MAX_CHANNEL,4*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage5_bias.hex"},biases,5*MAX_CHANNEL,5*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage6_bias.hex"},biases,6*MAX_CHANNEL,6*MAX_CHANNEL+FULL_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage0_pre_multiplier.hex"},premuls,0*MAX_CHANNEL,0*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage1_pre_multiplier.hex"},premuls,1*MAX_CHANNEL,1*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage2_pre_multiplier.hex"},premuls,2*MAX_CHANNEL,2*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage3_pre_multiplier.hex"},premuls,3*MAX_CHANNEL,3*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage4_pre_multiplier.hex"},premuls,4*MAX_CHANNEL,4*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage5_pre_multiplier.hex"},premuls,5*MAX_CHANNEL,5*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage6_pre_multiplier.hex"},premuls,6*MAX_CHANNEL,6*MAX_CHANNEL+FULL_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage0_pre_shift.hex"},preshifts,0*MAX_CHANNEL,0*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage1_pre_shift.hex"},preshifts,1*MAX_CHANNEL,1*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage2_pre_shift.hex"},preshifts,2*MAX_CHANNEL,2*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage3_pre_shift.hex"},preshifts,3*MAX_CHANNEL,3*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage4_pre_shift.hex"},preshifts,4*MAX_CHANNEL,4*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage5_pre_shift.hex"},preshifts,5*MAX_CHANNEL,5*MAX_CHANNEL+HALF_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage6_pre_shift.hex"},preshifts,6*MAX_CHANNEL,6*MAX_CHANNEL+FULL_CHANNELS-1);
            $readmemh({vector_path,"/parameters/stage0_post_multiplier.hex"},postmuls,0,0);
            $readmemh({vector_path,"/parameters/stage1_post_multiplier.hex"},postmuls,1,1);
            $readmemh({vector_path,"/parameters/stage2_post_multiplier.hex"},postmuls,2,2);
            $readmemh({vector_path,"/parameters/stage3_post_multiplier.hex"},postmuls,3,3);
            $readmemh({vector_path,"/parameters/stage4_post_multiplier.hex"},postmuls,4,4);
            $readmemh({vector_path,"/parameters/stage5_post_multiplier.hex"},postmuls,5,5);
            $readmemh({vector_path,"/parameters/stage6_post_multiplier.hex"},postmuls,6,6);
            $readmemh({vector_path,"/parameters/stage0_post_shift.hex"},postshifts,0,0);
            $readmemh({vector_path,"/parameters/stage1_post_shift.hex"},postshifts,1,1);
            $readmemh({vector_path,"/parameters/stage2_post_shift.hex"},postshifts,2,2);
            $readmemh({vector_path,"/parameters/stage3_post_shift.hex"},postshifts,3,3);
            $readmemh({vector_path,"/parameters/stage4_post_shift.hex"},postshifts,4,4);
            $readmemh({vector_path,"/parameters/stage5_post_shift.hex"},postshifts,5,5);
            $readmemh({vector_path,"/parameters/stage6_post_shift.hex"},postshifts,6,6);
            $readmemh({vector_path,"/vectors/stage0_acc.hex"},gold_acc,0*MAX_LOGICAL,0*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage1_acc.hex"},gold_acc,1*MAX_LOGICAL,1*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage2_acc.hex"},gold_acc,2*MAX_LOGICAL,2*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage3_acc.hex"},gold_acc,3*MAX_LOGICAL,3*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage4_acc.hex"},gold_acc,4*MAX_LOGICAL,4*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage5_acc.hex"},gold_acc,5*MAX_LOGICAL,5*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage6_acc.hex"},gold_acc,6*MAX_LOGICAL,6*MAX_LOGICAL+FULL_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage0_pre.hex"},gold_pre,0*MAX_LOGICAL,0*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage1_pre.hex"},gold_pre,1*MAX_LOGICAL,1*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage2_pre.hex"},gold_pre,2*MAX_LOGICAL,2*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage3_pre.hex"},gold_pre,3*MAX_LOGICAL,3*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage4_pre.hex"},gold_pre,4*MAX_LOGICAL,4*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage5_pre.hex"},gold_pre,5*MAX_LOGICAL,5*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage6_pre.hex"},gold_pre,6*MAX_LOGICAL,6*MAX_LOGICAL+FULL_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage0_silu.hex"},gold_silu,0*MAX_LOGICAL,0*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage1_silu.hex"},gold_silu,1*MAX_LOGICAL,1*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage2_silu.hex"},gold_silu,2*MAX_LOGICAL,2*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage3_silu.hex"},gold_silu,3*MAX_LOGICAL,3*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage4_silu.hex"},gold_silu,4*MAX_LOGICAL,4*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage5_silu.hex"},gold_silu,5*MAX_LOGICAL,5*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage6_silu.hex"},gold_silu,6*MAX_LOGICAL,6*MAX_LOGICAL+FULL_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage0_post.hex"},gold_post,0*MAX_LOGICAL,0*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage1_post.hex"},gold_post,1*MAX_LOGICAL,1*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage2_post.hex"},gold_post,2*MAX_LOGICAL,2*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage3_post.hex"},gold_post,3*MAX_LOGICAL,3*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage4_post.hex"},gold_post,4*MAX_LOGICAL,4*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage5_post.hex"},gold_post,5*MAX_LOGICAL,5*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage6_post.hex"},gold_post,6*MAX_LOGICAL,6*MAX_LOGICAL+FULL_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage0_sum.hex"},gold_sum,0*MAX_LOGICAL,0*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage1_sum.hex"},gold_sum,1*MAX_LOGICAL,1*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage2_sum.hex"},gold_sum,2*MAX_LOGICAL,2*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage3_sum.hex"},gold_sum,3*MAX_LOGICAL,3*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage4_sum.hex"},gold_sum,4*MAX_LOGICAL,4*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage5_sum.hex"},gold_sum,5*MAX_LOGICAL,5*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage6_sum.hex"},gold_sum,6*MAX_LOGICAL,6*MAX_LOGICAL+FULL_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage0_output.hex"},gold_output,0*MAX_LOGICAL,0*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage1_output.hex"},gold_output,1*MAX_LOGICAL,1*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage2_output.hex"},gold_output,2*MAX_LOGICAL,2*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage3_output.hex"},gold_output,3*MAX_LOGICAL,3*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage4_output.hex"},gold_output,4*MAX_LOGICAL,4*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage5_output.hex"},gold_output,5*MAX_LOGICAL,5*MAX_LOGICAL+HALF_LOGICAL-1);
            $readmemh({vector_path,"/vectors/stage6_output.hex"},gold_output,6*MAX_LOGICAL,6*MAX_LOGICAL+FULL_LOGICAL-1);
        end
    endtask

    initial begin
        if(C_FAMILY!=3 && C_FAMILY!=4)$fatal(1,"unsupported C_FAMILY=%0d",C_FAMILY);
        if(!$value$plusargs("CASE=%d",test_case))test_case=0;
        if(!$value$plusargs("FAULT_KIND=%d",fault_kind))fault_kind=0;
        if(!$value$plusargs("RESET_STAGE=%d",reset_stage))reset_stage=2;
        if(!$value$plusargs("NEGATIVE_ACC=%d",negative_acc))negative_acc=0;
        if(!$value$plusargs("VECTORS=%s",vector_path))$fatal(1,"VECTORS reference root missing family=%0d",C_FAMILY);
        if(test_case<0 || test_case>5)$fatal(1,"unsupported CASE=%0d",test_case);
        if(reset_stage<0 || reset_stage>6)$fatal(1,"unsupported RESET_STAGE=%0d",reset_stage);
        if(test_case==5 && fault_kind!=0 && fault_kind!=1)$fatal(1,"unsupported FAULT_KIND=%0d",fault_kind);
        load_reference;
        reset_and_load_table;
        if(test_case==1)random_mode=1;
        launch_frame;
        if(test_case==0 || test_case==1)begin
            finish_frame;
            $display("CSP_FAMILY_PASS family=%0d case=%0d runs=%0d cycles=%0d accounted=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d groups=%0d tasks=%0d reads=%0d parameters=%0d barriers=%0d",
                C_FAMILY,test_case,runs,final_cycles,accounted_cycles,outputs,accumulators,pres,silus,posts,groups,tasks,reads,parameters,barriers);
        end else if(test_case==2)begin
            wait(layer==reset_stage && busy && stage_outputs[reset_stage]>=128);
            reset_and_load_table;
            random_mode=0; launch_frame; finish_frame;
            if(table_loads!=2)$fatal(1,"reset case did not reload LUT family=%0d",C_FAMILY);
            $display("CSP_FAMILY_PASS family=%0d case=%0d runs=%0d cycles=%0d accounted=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d groups=%0d tasks=%0d reads=%0d parameters=%0d barriers=%0d",
                C_FAMILY,test_case,runs,final_cycles,accounted_cycles,outputs,accumulators,pres,silus,posts,groups,tasks,reads,parameters,barriers);
        end else if(test_case==5 && fault_kind==0)begin
            wait(core_output_valid); @(negedge clk); force core_output_address=32'hffffffff;
            @(posedge clk); @(negedge clk); wait(fault); active=0; repeat(8)@(negedge clk);
            if(done || write_valid || start_ready)$fatal(1,"wrong output address leaked completion family=%0d",C_FAMILY);
            $display("CSP_FAMILY_EXPECTED_FAULT family=%0d case=%0d kind=%0d runs=%0d cycles=%0d accounted=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d groups=%0d tasks=%0d reads=%0d parameters=%0d barriers=%0d",
                C_FAMILY,test_case,fault_kind,runs,cycles-run_start,accounted_cycles,outputs,accumulators,pres,silus,posts,groups,tasks,reads,parameters,barriers);
            release core_output_address;
        end else begin
            wait(fault); active=0; repeat(8)@(negedge clk);
            if(done || write_valid || start_ready)$fatal(1,"service/barrier fault leaked completion family=%0d",C_FAMILY);
            if((test_case==3 || test_case==4) && outputs!=0)$fatal(1,"early service fault wrote data family=%0d",C_FAMILY);
            if(test_case==5 && fault_kind==1 && outputs!=HALF_LOGICAL)$fatal(1,"barrier fault boundary mismatch family=%0d outputs=%0d",C_FAMILY,outputs);
            $display("CSP_FAMILY_EXPECTED_FAULT family=%0d case=%0d kind=%0d runs=%0d cycles=%0d accounted=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d groups=%0d tasks=%0d reads=%0d parameters=%0d barriers=%0d",
                C_FAMILY,test_case,fault_kind,runs,cycles-run_start,accounted_cycles,outputs,accumulators,pres,silus,posts,groups,tasks,reads,parameters,barriers);
        end
        complete=1;
        $finish;
    end
endmodule
