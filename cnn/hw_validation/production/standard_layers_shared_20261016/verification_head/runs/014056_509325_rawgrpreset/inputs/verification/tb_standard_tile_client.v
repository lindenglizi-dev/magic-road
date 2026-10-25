`timescale 1ns / 1ps
// 固定四层独立自检；数组仅为行为服务，不代表物理4ERAM。
module tb_standard_tile_client(output o_test_complete);
    reg i_clk = 0;
    reg i_rstn = 0;
    reg i_cancel = 0;
    reg i_start_valid = 0;
    reg [6:0] i_layer_id = 0;
    reg [6:0] i_tile_y = 0;
    reg [6:0] i_tile_x = 0;
    wire i_table_loaded;
    reg i_parameter_ready = 0;
    reg i_parameter_rsp_valid = 0;
    reg [6:0] i_parameter_rsp_layer = 0;
    reg [6:0] i_parameter_rsp_channel = 0;
    reg [2:0] i_parameter_rsp_window = 0;
    reg [4:0] i_parameter_rsp_group = 0;
    reg [191:0] i_parameter_weight = 0;
    reg [247:0] i_parameter_quant = 0;
    reg i_parameter_error = 0;
    reg i_read_ready = 0;
    reg i_read_rsp_valid = 0;
    reg [31:0] i_read_rsp_address = 0;
    reg [127:0] i_read_rsp_data = 0;
    reg i_read_error = 0;
    reg i_write_ready = 0;
    reg i_barrier_ready = 0;
    wire [6:0] i_barrier_layer;
    wire [6:0] i_barrier_tile_y;
    wire [6:0] i_barrier_tile_x;
    wire i_byte_req_ready;
    wire i_byte_rsp_valid;
    wire [7:0] i_byte_rsp_data;
    wire i_byte_rsp_error;
    wire i_weight_req_ready;
    wire i_weight_rsp_valid;
    wire [191:0] i_weight_rsp_data;
    wire i_weight_rsp_error;
    wire i_work_fault;
    wire i_core_ready;
    wire i_core_output_valid;
    wire [15:0] i_core_output_tag;
    wire [31:0] i_core_output_address;
    wire [15:0] i_core_output_data;
    wire i_core_output_int16;
    wire i_core_fault;
    wire o_start_ready;
    wire o_busy;
    wire o_done;
    wire o_fault;
    wire [6:0] o_layer_id;
    wire [6:0] o_tile_y;
    wire [6:0] o_tile_x;
    wire o_parameter_valid;
    wire [6:0] o_parameter_channel;
    wire [2:0] o_parameter_window;
    wire [4:0] o_parameter_group;
    wire o_parameter_rsp_ready;
    wire o_read_valid;
    wire [31:0] o_read_address;
    wire o_read_rsp_ready;
    wire o_write_valid;
    wire [31:0] o_write_address;
    wire [15:0] o_write_data;
    wire o_write_int16;
    wire o_core_activate;
    wire o_barrier_valid;
    wire o_byte_req_valid;
    wire o_byte_req_write;
    wire [11:0] o_byte_req_addr;
    wire [7:0] o_byte_req_data;
    wire o_byte_rsp_ready;
    wire o_weight_req_valid;
    wire o_weight_req_write;
    wire [4:0] o_weight_req_group;
    wire [191:0] o_weight_req_data;
    wire o_weight_rsp_ready;
    wire o_core_valid;
    wire o_core_first;
    wire o_core_last;
    wire [7:0] o_core_input_mask;
    wire [63:0] o_core_activation;
    wire [191:0] o_core_weight;
    wire [95:0] o_core_bias;
    wire [2:0] o_core_output_mask;
    wire [47:0] o_core_tags;
    wire [95:0] o_core_addresses;
    wire [95:0] o_core_pre_multiplier;
    wire [17:0] o_core_pre_shift;
    wire [31:0] o_core_post_multiplier;
    wire [5:0] o_core_post_shift;
    wire o_core_output_ready;
    road_standard_tile_client dut(
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .i_cancel(i_cancel),
        .i_start_valid(i_start_valid),
        .i_layer_id(i_layer_id),
        .i_tile_y(i_tile_y),
        .i_tile_x(i_tile_x),
        .i_table_loaded(i_table_loaded),
        .i_parameter_ready(i_parameter_ready),
        .i_parameter_rsp_valid(i_parameter_rsp_valid),
        .i_parameter_rsp_layer(i_parameter_rsp_layer),
        .i_parameter_rsp_channel(i_parameter_rsp_channel),
        .i_parameter_rsp_window(i_parameter_rsp_window),
        .i_parameter_rsp_group(i_parameter_rsp_group),
        .i_parameter_weight(i_parameter_weight),
        .i_parameter_quant(i_parameter_quant),
        .i_parameter_error(i_parameter_error),
        .i_read_ready(i_read_ready),
        .i_read_rsp_valid(i_read_rsp_valid),
        .i_read_rsp_address(i_read_rsp_address),
        .i_read_rsp_data(i_read_rsp_data),
        .i_read_error(i_read_error),
        .i_write_ready(i_write_ready),
        .i_barrier_ready(i_barrier_ready),
        .i_barrier_layer(i_barrier_layer),
        .i_barrier_tile_y(i_barrier_tile_y),
        .i_barrier_tile_x(i_barrier_tile_x),
        .i_byte_req_ready(i_byte_req_ready),
        .i_byte_rsp_valid(i_byte_rsp_valid),
        .i_byte_rsp_data(i_byte_rsp_data),
        .i_byte_rsp_error(i_byte_rsp_error),
        .i_weight_req_ready(i_weight_req_ready),
        .i_weight_rsp_valid(i_weight_rsp_valid),
        .i_weight_rsp_data(i_weight_rsp_data),
        .i_weight_rsp_error(i_weight_rsp_error),
        .i_work_fault(i_work_fault),
        .i_core_ready(i_core_ready),
        .i_core_output_valid(i_core_output_valid),
        .i_core_output_tag(i_core_output_tag),
        .i_core_output_address(i_core_output_address),
        .i_core_output_data(i_core_output_data),
        .i_core_output_int16(i_core_output_int16),
        .i_core_fault(i_core_fault),
        .o_start_ready(o_start_ready),
        .o_busy(o_busy),
        .o_done(o_done),
        .o_fault(o_fault),
        .o_layer_id(o_layer_id),
        .o_tile_y(o_tile_y),
        .o_tile_x(o_tile_x),
        .o_parameter_valid(o_parameter_valid),
        .o_parameter_channel(o_parameter_channel),
        .o_parameter_window(o_parameter_window),
        .o_parameter_group(o_parameter_group),
        .o_parameter_rsp_ready(o_parameter_rsp_ready),
        .o_read_valid(o_read_valid),
        .o_read_address(o_read_address),
        .o_read_rsp_ready(o_read_rsp_ready),
        .o_write_valid(o_write_valid),
        .o_write_address(o_write_address),
        .o_write_data(o_write_data),
        .o_write_int16(o_write_int16),
        .o_core_activate(o_core_activate),
        .o_barrier_valid(o_barrier_valid),
        .o_byte_req_valid(o_byte_req_valid),
        .o_byte_req_write(o_byte_req_write),
        .o_byte_req_addr(o_byte_req_addr),
        .o_byte_req_data(o_byte_req_data),
        .o_byte_rsp_ready(o_byte_rsp_ready),
        .o_weight_req_valid(o_weight_req_valid),
        .o_weight_req_write(o_weight_req_write),
        .o_weight_req_group(o_weight_req_group),
        .o_weight_req_data(o_weight_req_data),
        .o_weight_rsp_ready(o_weight_rsp_ready),
        .o_core_valid(o_core_valid),
        .o_core_first(o_core_first),
        .o_core_last(o_core_last),
        .o_core_input_mask(o_core_input_mask),
        .o_core_activation(o_core_activation),
        .o_core_weight(o_core_weight),
        .o_core_bias(o_core_bias),
        .o_core_output_mask(o_core_output_mask),
        .o_core_tags(o_core_tags),
        .o_core_addresses(o_core_addresses),
        .o_core_pre_multiplier(o_core_pre_multiplier),
        .o_core_pre_shift(o_core_pre_shift),
        .o_core_post_multiplier(o_core_post_multiplier),
        .o_core_post_shift(o_core_post_shift),
        .o_core_output_ready(o_core_output_ready)
    );

    reg table_valid = 0;
    reg [9:0] table_addr = 0;
    reg [15:0] table_data = 0;
    wire table_ready, owner_ready;
    wire owner_busy;
    reg owner_admit = 0;
    reg complete = 0;
    assign o_test_complete = complete;
    assign i_core_ready = owner_ready && owner_admit;
    assign i_barrier_layer = o_layer_id;
    assign i_barrier_tile_y = o_tile_y;
    assign i_barrier_tile_x = o_tile_x;
    road_standard_arithmetic_owner arithmetic_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_table_valid(table_valid),.i_table_addr(table_addr),.i_table_data(table_data),
        .i_input_valid(o_core_valid && owner_admit),.i_first(o_core_first),.i_last(o_core_last),
        .i_lane_mask(o_core_input_mask),.i_activation_data(o_core_activation),.i_weight_data(o_core_weight),
        .i_bias_data(o_core_bias),.i_output_mask(o_core_output_mask),.i_tags(o_core_tags),.i_addresses(o_core_addresses),
        .i_pre_multipliers(o_core_pre_multiplier),.i_pre_shifts(o_core_pre_shift),
        .i_post_multiplier(o_core_post_multiplier),.i_post_shift(o_core_post_shift),
        .i_activate(o_core_activate),.i_input_fault(1'b0),
        .i_output_ready(o_core_output_ready),.o_table_ready(table_ready),.o_table_loaded(i_table_loaded),
        .o_input_ready(owner_ready),.o_output_valid(i_core_output_valid),.o_output_data(i_core_output_data),
        .o_output_tag(i_core_output_tag),.o_output_address(i_core_output_address),
        .o_output_int16(i_core_output_int16),.o_busy(owner_busy),.o_fault(i_core_fault)
    );
    // 端点按WIF1单未退休事务执行；存储内容不复位，每次使用前覆盖。
    reg [7:0] byte_memory [0:3071];
    reg [191:0] weight_memory [0:23];
    reg byte_written [0:3071];
    reg weight_written [0:23];
    reg [127:0] source_lines [0:262143];
    reg source_line_present [0:262143];
    reg [31:0] source_read_trace [0:32767];
    reg [15:0] silu_table [0:1023];
    reg [31:0] cfg [0:15];
    reg [21:0] parameter_ids [0:4095];
    reg [191:0] parameter_weights [0:4095];
    reg [247:0] parameter_quants [0:4095];
    reg [63:0] gold_activation [0:4095];
    reg [191:0] gold_weight [0:4095];
    reg [7:0] gold_mask [0:4095];
    reg gold_first [0:4095];
    reg gold_last [0:4095];
    reg [98:0] gold_partial [0:4095];
    reg [95:0] gold_acc [0:1023];
    reg [47:0] gold_pre [0:1023];
    reg [47:0] gold_silu [0:1023];
    reg [47:0] gold_post [0:1023];
    reg gold_output_int16 [0:1023];
    reg [95:0] gold_addresses [0:1023];
    reg [2:0] gold_output_mask [0:1023];
    reg [247:0] gold_quant [0:1023];
    reg [28:0] byte_trace [0:65535];
    reg [389:0] weight_trace [0:8191];
    reg [47:0] output_trace [0:2047];
    reg [4095:0] vector_root, layer_root, case_root, table_path, trace_path;
    integer mode = 0, negative = 0, random_mode = 1;
    integer groups = 0, tasks = 0, outputs = 0, accs = 0, pres = 0, silus = 0, posts = 0;
    integer partials = 0, byte_count = 0, weight_count = 0, parameters = 0, reads = 0, barriers = 0;
    integer raw_outputs = 0, raw_wide_outputs = 0;
    integer cycles = 0, run_start = 0, trace_fd;
    integer state_cycles [0:23];
    integer index, lane, hit, offset, tile_index, pixel_index, sy, sx, sc, logical_index;
    integer byte_delay = 0, weight_delay = 0, parameter_delay = 0, read_delay = 0;
    reg byte_pending = 0, weight_pending = 0, parameter_pending = 0, read_pending = 0;
    reg [7:0] saved_byte_data;
    reg [191:0] saved_weight_data;
    reg [21:0] saved_parameter_id;
    reg [191:0] saved_parameter_weight;
    reg [247:0] saved_parameter_quant;
    reg [31:0] saved_read_address;
    reg [127:0] saved_read_data;
    reg [127:0] generated_line;
    reg [31:0] rng = 32'h2b6df82a;
    reg active = 0, allow_ready = 1;
    reg [12:0] stalled = 0;
    reg [799:0] held [0:12];
    task stable;
        input integer slot;
        input valid_bit;
        input ready_bit;
        input [799:0] payload;
        begin
            if(stalled[slot] && (!valid_bit || held[slot] !== payload))
                $fatal(1,"STALLED_PAYLOAD slot=%0d",slot);
            stalled[slot] = valid_bit && !ready_bit;
            held[slot] = payload;
        end
    endtask
    // 真实C4 WIF1端点；原行为数组只作为独立期望记分板，不驱动客户端。
    road_feature_workstore physical_workstore_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),
        .i_byte_req_valid(o_byte_req_valid),.i_byte_req_write(o_byte_req_write),
        .i_byte_req_addr(o_byte_req_addr),.i_byte_req_data(o_byte_req_data),.i_byte_rsp_ready(o_byte_rsp_ready),
        .i_weight_req_valid(o_weight_req_valid),.i_weight_req_write(o_weight_req_write),
        .i_weight_req_group(o_weight_req_group),.i_weight_req_data(o_weight_req_data),.i_weight_rsp_ready(o_weight_rsp_ready),
        .o_byte_req_ready(i_byte_req_ready),.o_byte_rsp_valid(i_byte_rsp_valid),
        .o_byte_rsp_data(i_byte_rsp_data),.o_byte_rsp_error(i_byte_rsp_error),
        .o_weight_req_ready(i_weight_req_ready),.o_weight_rsp_valid(i_weight_rsp_valid),
        .o_weight_rsp_data(i_weight_rsp_data),.o_weight_rsp_error(i_weight_rsp_error),.o_fault(i_work_fault)
    );
    always #5 i_clk = !i_clk;
    always @(negedge i_clk) begin
        rng <= {rng[30:0],rng[31]^rng[21]^rng[1]^rng[0]};
        i_parameter_ready <= allow_ready && !parameter_pending && !i_parameter_rsp_valid && (!random_mode || rng[0]);
        i_read_ready <= allow_ready && !read_pending && !i_read_rsp_valid && (!random_mode || rng[1]);
        i_write_ready <= allow_ready && (!random_mode || rng[4:3] != 0);
        i_barrier_ready <= allow_ready && (!random_mode || rng[6:5] == 0);
        owner_admit <= allow_ready && (!random_mode || rng[8:7] != 0);
    end
    // 外部服务只在本通道握手后创建响应；随机延迟不依赖DUT内部状态。
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) begin
            byte_pending <= 0; weight_pending <= 0; parameter_pending <= 0; read_pending <= 0;
            i_parameter_rsp_valid <= 0; i_read_rsp_valid <= 0;
        end else begin
            if(i_byte_rsp_valid && o_byte_rsp_ready) begin
                if(!byte_pending || i_byte_rsp_error || i_byte_rsp_data !== saved_byte_data)
                    $fatal(1,"PHYSICAL_BYTE_RESPONSE");
                byte_pending <= 0;
            end
            if(i_weight_rsp_valid && o_weight_rsp_ready) begin
                if(!weight_pending || i_weight_rsp_error || i_weight_rsp_data !== saved_weight_data)
                    $fatal(1,"PHYSICAL_WEIGHT_RESPONSE");
                weight_pending <= 0;
            end
            if(i_parameter_rsp_valid && o_parameter_rsp_ready) i_parameter_rsp_valid <= 0;
            if(i_read_rsp_valid && o_read_rsp_ready) i_read_rsp_valid <= 0;
            if(o_byte_req_valid && i_byte_req_ready) begin
                if(byte_pending || i_byte_rsp_valid || o_byte_req_addr >= 3072) $fatal(1,"BYTE_OUTSTANDING_OR_RANGE");
                if(byte_count >= cfg[11] || {o_byte_req_write,o_byte_req_addr} !== byte_trace[byte_count][28:16])
                    $fatal(1,"BYTE_TRACE_ADDRESS index=%0d write=%0d addr=%0d expected=%h",byte_count,o_byte_req_write,o_byte_req_addr,byte_trace[byte_count]);
                if(o_byte_req_write) begin
                    if(o_byte_req_data !== byte_trace[byte_count][15:8]) $fatal(1,"BYTE_TRACE_WRITE index=%0d got=%h expected=%h",byte_count,o_byte_req_data,byte_trace[byte_count]);
                    byte_memory[o_byte_req_addr] = o_byte_req_data; byte_written[o_byte_req_addr] = 1;
                    saved_byte_data <= 0;
                end else begin
                    if(!byte_written[o_byte_req_addr]) $fatal(1,"BYTE_READ_BEFORE_WRITE");
                    if(byte_memory[o_byte_req_addr] !== byte_trace[byte_count][7:0]) $fatal(1,"BYTE_TRACE_READ index=%0d",byte_count);
                    saved_byte_data <= byte_memory[o_byte_req_addr];
                end
                $fdisplay(trace_fd,"byte,%0d,%0d,%0d,%h",cycles,o_byte_req_write,o_byte_req_addr,o_byte_req_data);
                byte_count = byte_count + 1; byte_pending <= 1; byte_delay <= random_mode ? rng[11:9] : 1;
            end
            if(o_weight_req_valid && i_weight_req_ready) begin
                if(weight_pending || i_weight_rsp_valid || o_weight_req_group >= 24) $fatal(1,"WEIGHT_OUTSTANDING_OR_RANGE");
                if(weight_count >= cfg[12] || {o_weight_req_write,o_weight_req_group} !== weight_trace[weight_count][389:384])
                    $fatal(1,"WEIGHT_TRACE_ADDRESS index=%0d",weight_count);
                if(o_weight_req_write) begin
                    if(o_weight_req_data !== weight_trace[weight_count][383:192]) $fatal(1,"WEIGHT_TRACE_WRITE index=%0d",weight_count);
                    weight_memory[o_weight_req_group] = o_weight_req_data; weight_written[o_weight_req_group] = 1;
                    saved_weight_data <= 0;
                end else begin
                    if(!weight_written[o_weight_req_group]) $fatal(1,"WEIGHT_READ_BEFORE_WRITE");
                    if(weight_memory[o_weight_req_group] !== weight_trace[weight_count][191:0]) $fatal(1,"WEIGHT_TRACE_READ index=%0d",weight_count);
                    saved_weight_data <= weight_memory[o_weight_req_group];
                end
                $fdisplay(trace_fd,"weight,%0d,%0d,%0d,%h",cycles,o_weight_req_write,o_weight_req_group,o_weight_req_data);
                weight_count = weight_count + 1; weight_pending <= 1; weight_delay <= random_mode ? rng[14:12] : 1;
            end
            if(o_parameter_valid && i_parameter_ready) begin
                if(parameter_pending || i_parameter_rsp_valid) $fatal(1,"PARAMETER_OUTSTANDING");
                hit = -1;
                for(index=0;index<cfg[10];index=index+1)
                    if(parameter_ids[index] === {o_layer_id,o_parameter_channel,o_parameter_window,o_parameter_group}) hit = index;
                if(hit < 0) $fatal(1,"PARAMETER_UNKNOWN_ID");
                saved_parameter_id <= parameter_ids[hit]; saved_parameter_weight <= parameter_weights[hit]; saved_parameter_quant <= parameter_quants[hit];
                parameters = parameters + 1; parameter_pending <= 1; parameter_delay <= random_mode ? rng[17:15] : 2;
            end
            if(parameter_pending) begin
                if(parameter_delay != 0) parameter_delay <= parameter_delay - 1;
                else begin
                    i_parameter_rsp_valid <= 1; parameter_pending <= 0;
                    {i_parameter_rsp_layer,i_parameter_rsp_channel,i_parameter_rsp_window,i_parameter_rsp_group} <= saved_parameter_id ^ (mode == 3 ? 22'h008000 : 0);
                    i_parameter_weight <= saved_parameter_weight; i_parameter_quant <= saved_parameter_quant;
                end
            end
            if(o_read_valid && i_read_ready) begin
                if(read_pending || i_read_rsp_valid || o_read_address[3:0] != 0) $fatal(1,"READ_OUTSTANDING_OR_ALIGNMENT");
                if(reads >= cfg[14] || o_read_address !== source_read_trace[reads])
                    $fatal(1,"READ_ADDRESS_TRACE index=%0d got=%h expected=%h",reads,o_read_address,source_read_trace[reads]);
                offset = (o_read_address - cfg[6]) / 16;
                if(o_read_address < cfg[6] || offset >= 262144 || source_line_present[offset] !== 1'b1)
                    $fatal(1,"READ_SOURCE_RANGE addr=%h",o_read_address);
                generated_line = source_lines[offset];
                $fdisplay(trace_fd,"source,%0d,0,%h,%h",cycles,o_read_address,generated_line);
                saved_read_address <= o_read_address; saved_read_data <= generated_line;
                reads = reads + 1; read_pending <= 1; read_delay <= random_mode ? rng[20:18] : 2;
            end
            if(read_pending) begin
                if(read_delay != 0) read_delay <= read_delay - 1;
                else begin i_read_rsp_valid <= 1; i_read_rsp_address <= saved_read_address; i_read_rsp_data <= saved_read_data; read_pending <= 0; end
            end
        end
    end
    // 每个实接收组与独立任务参考逐项比较，含首末组及仅一次偏置。
    always @(posedge i_clk) begin
        cycles = cycles + 1;
        if(cycles > 2000000) $fatal(1,"WATCHDOG");
        if(!i_rstn) stalled = 0;
        else if(active && !o_fault) begin
            state_cycles[dut.state_current] = state_cycles[dut.state_current] + 1;
            stable(0,o_parameter_valid,i_parameter_ready,{o_layer_id,o_parameter_channel,o_parameter_window,o_parameter_group});
            stable(1,i_parameter_rsp_valid,o_parameter_rsp_ready,{i_parameter_rsp_layer,i_parameter_rsp_channel,i_parameter_rsp_window,i_parameter_rsp_group,i_parameter_weight,i_parameter_quant,i_parameter_error});
            stable(2,o_read_valid,i_read_ready,o_read_address);
            stable(3,i_read_rsp_valid,o_read_rsp_ready,{i_read_rsp_address,i_read_rsp_data,i_read_error});
            stable(4,o_byte_req_valid,i_byte_req_ready,{o_byte_req_write,o_byte_req_addr,o_byte_req_data});
            stable(5,i_byte_rsp_valid,o_byte_rsp_ready,{i_byte_rsp_data,i_byte_rsp_error});
            stable(6,o_weight_req_valid,i_weight_req_ready,{o_weight_req_write,o_weight_req_group,o_weight_req_data});
            stable(7,i_weight_rsp_valid,o_weight_rsp_ready,{i_weight_rsp_data,i_weight_rsp_error});
            stable(8,o_core_valid,i_core_ready,{o_core_first,o_core_last,o_core_input_mask,o_core_activation,o_core_weight,o_core_bias,o_core_output_mask,o_core_tags,o_core_addresses,o_core_pre_multiplier,o_core_pre_shift,o_core_post_multiplier,o_core_post_shift,o_core_activate});
            stable(9,i_core_output_valid,o_core_output_ready,{i_core_output_tag,i_core_output_address,i_core_output_data,i_core_output_int16});
            stable(10,o_write_valid,i_write_ready,{o_write_address,o_write_data,o_write_int16});
            stable(11,o_barrier_valid,i_barrier_ready,{o_layer_id,o_tile_y,o_tile_x});
            if(o_core_valid && i_core_ready) begin
                if(byte_pending || weight_pending || parameter_pending || read_pending || i_byte_rsp_valid || i_weight_rsp_valid || i_parameter_rsp_valid || i_read_rsp_valid)
                    $fatal(1,"CORE_WITH_UNRETIRED_RESPONSE");
                if(groups >= cfg[7] || o_core_activation !== gold_activation[groups] || o_core_weight !== gold_weight[groups] ||
                    o_core_input_mask !== gold_mask[groups] || o_core_first !== gold_first[groups] || o_core_last !== gold_last[groups])
                    $fatal(1,"GROUP_MISMATCH index=%0d activation=%h expected=%h mask=%h first=%b last=%b",groups,o_core_activation,gold_activation[groups],o_core_input_mask,o_core_first,o_core_last);
                if(o_core_output_mask !== gold_output_mask[tasks] || o_core_tags !== 48'h000200010000) $fatal(1,"TASK_MASK_TAG");
                if(o_core_activate !== !gold_output_int16[tasks]) $fatal(1,"TASK_ACTIVATE_MODE");
                for(lane=0;lane<3;lane=lane+1) begin
                    if(gold_output_mask[tasks][lane]) begin
                        if(o_core_addresses[lane*32 +: 32] !== gold_addresses[tasks][lane*32 +: 32] ||
                            o_core_bias[lane*32 +: 32] !== gold_quant[tasks][lane*32 +: 32] ||
                            o_core_pre_multiplier[lane*32 +: 32] !== gold_quant[tasks][96+lane*32 +: 32] ||
                            o_core_pre_shift[lane*6 +: 6] !== gold_quant[tasks][192+lane*6 +: 6]) $fatal(1,"TASK_METADATA task=%0d lane=%0d",tasks,lane);
                    end else if(o_core_bias[lane*32 +: 32] !== 0 || o_core_pre_multiplier[lane*32 +: 32] !== 0 || o_core_pre_shift[lane*6 +: 6] !== 0) $fatal(1,"INVALID_LANE_QUANT");
                end
                if(o_core_post_multiplier !== gold_quant[tasks][241:210] || o_core_post_shift !== gold_quant[tasks][247:242]) $fatal(1,"TASK_POST_QUANT");
                groups = groups + 1;
                if(o_core_last) tasks = tasks + 1;
            end
            if(arithmetic_Inst.road_mac_probe_Inst.flag_dot_valid) begin
                if({arithmetic_Inst.road_mac_probe_Inst.candidate_gamma_sum[32:0],arithmetic_Inst.road_mac_probe_Inst.candidate_beta_sum[32:0],arithmetic_Inst.road_mac_probe_Inst.candidate_alpha_sum[32:0]} !== gold_partial[partials])
                    $fatal(1,"PARTIAL_ACC index=%0d",partials);
                partials = partials + 1;
            end
            if(arithmetic_Inst.flag_acc_accept) begin
                if(arithmetic_Inst.wire_mac_data !== (gold_acc[accs] ^ (negative != 0 && accs == 0 ? 96'd1 : 96'd0))) $fatal(1,"ACC_MISMATCH task=%0d negative=%0d",accs,negative);
                accs = accs + 1;
            end
            if(arithmetic_Inst.road_dynamic_postprocess_Inst.flag_pre_complete && !arithmetic_Inst.road_dynamic_postprocess_Inst.flag_pre_drop) begin
                lane = arithmetic_Inst.road_dynamic_postprocess_Inst.pre_result_tag[1:0];
                if(arithmetic_Inst.road_dynamic_postprocess_Inst.pre_result_data !== gold_pre[accs-1][lane*16 +: 16]) $fatal(1,"PRE_MISMATCH task=%0d lane=%0d",accs-1,lane);
                pres = pres + 1;
            end
            if(arithmetic_Inst.road_dynamic_postprocess_Inst.flag_post_accept) begin
                if(gold_output_int16[accs-1]) $fatal(1,"RAW16_UNEXPECTED_SILU_POST_TRANSACTION");
                lane = arithmetic_Inst.road_dynamic_postprocess_Inst.reg_meta_tags[arithmetic_Inst.road_dynamic_postprocess_Inst.reg_meta_read][1:0];
                if(arithmetic_Inst.road_dynamic_postprocess_Inst.silu_output_data !== gold_silu[accs-1][lane*16 +: 16]) $fatal(1,"SILU_MISMATCH");
                silus = silus + 1;
            end
            if(arithmetic_Inst.road_dynamic_postprocess_Inst.flag_post_complete) begin
                if(gold_output_int16[accs-1]) $fatal(1,"RAW16_UNEXPECTED_POST_COMPLETE");
                lane = arithmetic_Inst.road_dynamic_postprocess_Inst.post_result_tag[1:0];
                if(arithmetic_Inst.road_dynamic_postprocess_Inst.wire_post_saturated !== $signed(gold_post[accs-1][lane*8 +: 8])) $fatal(1,"POST_MISMATCH");
                posts = posts + 1;
            end
            if(arithmetic_Inst.road_dynamic_postprocess_Inst.flag_silu_accept && gold_output_int16[accs-1])
                $fatal(1,"RAW16_UNEXPECTED_SILU_ACCEPT");
            if(o_write_valid && i_write_ready) begin
                if(outputs >= cfg[9] || o_write_address !== output_trace[outputs][47:16] ||
                    o_write_int16 !== gold_output_int16[tasks-1] || i_core_output_int16 !== o_write_int16)
                    $fatal(1,"WRITE_ADDRESS_TYPE index=%0d address=%h",outputs,o_write_address);
                if(o_write_int16) begin
                    if(o_write_address[0] || o_write_data !== output_trace[outputs][15:0]) $fatal(1,"RAW16_WRITE_MISMATCH index=%0d data=%h",outputs,o_write_data);
                    raw_outputs = raw_outputs + 1;
                    if(o_write_data[15:8] !== {8{o_write_data[7]}}) raw_wide_outputs = raw_wide_outputs + 1;
                end else if(o_write_data[7:0] !== output_trace[outputs][7:0] || o_write_data[15:8] !== {8{o_write_data[7]}})
                    $fatal(1,"INT8_WRITE_MISMATCH index=%0d data=%h",outputs,o_write_data);
                outputs = outputs + 1;
            end
            if(o_barrier_valid && i_barrier_ready) begin
                if(byte_pending || weight_pending || parameter_pending || read_pending || i_byte_rsp_valid || i_weight_rsp_valid || i_parameter_rsp_valid || i_read_rsp_valid || outputs != cfg[9])
                    $fatal(1,"BARRIER_BEFORE_RETIREMENT");
                barriers = barriers + 1;
            end
        end
    end
    task reset_and_load;
        begin
            @(negedge i_clk); i_rstn = 0; i_start_valid = 0; i_cancel = 0; active = 0;
            repeat(4) @(negedge i_clk);
            if(o_done || o_busy || o_fault || owner_busy || i_table_loaded || i_byte_rsp_valid || i_weight_rsp_valid || i_read_rsp_valid || i_parameter_rsp_valid) $fatal(1,"COMMON_RESET_STATE");
            for(index=0;index<3072;index=index+1) byte_written[index] = 0;
            for(index=0;index<24;index=index+1) weight_written[index] = 0;
            i_rstn = 1;
            repeat(3) @(negedge i_clk);
            for(index=0;index<1024;index=index+1) begin
                table_valid = 1; table_addr = index; table_data = silu_table[index];
                @(negedge i_clk);
                if(!table_ready && index < 1023) $fatal(1,"TABLE_NOT_READY");
            end
            table_valid = 0;
            repeat(3) @(negedge i_clk);
            if(!o_start_ready || !i_table_loaded) $fatal(1,"RESET_RELOAD");
        end
    endtask
    initial begin
        if(!$value$plusargs("VECTOR_ROOT=%s",vector_root) || !$value$plusargs("LAYER_ROOT=%s",layer_root) ||
           !$value$plusargs("CASE_ROOT=%s",case_root) || !$value$plusargs("TABLE=%s",table_path) ||
           !$value$plusargs("TRACE=%s",trace_path)) $fatal(1,"MISSING_PATH");
        if(!$value$plusargs("MODE=%d",mode)) mode = 0;
        if(!$value$plusargs("NEGATIVE=%d",negative)) negative = 0;
        if(!$value$plusargs("RANDOM=%d",random_mode)) random_mode = 1;
        trace_fd = $fopen(trace_path,"w");
        $readmemh({case_root,"/cfg.hex"},cfg,0,15);
        $readmemh(table_path,silu_table,0,1023);
        $readmemh({layer_root,"/line_image128.hex"},source_lines);
        $readmemh({layer_root,"/line_present1.hex"},source_line_present);
        $readmemh({case_root,"/source_read_addresses32.hex"},source_read_trace,0,cfg[14]-1);
        $readmemh({vector_root,"/parameter_requests22.hex"},parameter_ids,0,cfg[10]-1);
        $readmemh({vector_root,"/parameter_weight192.hex"},parameter_weights,0,cfg[10]-1);
        $readmemh({vector_root,"/parameter_quant248.hex"},parameter_quants,0,cfg[10]-1);
        $readmemh({case_root,"/group_activation64.hex"},gold_activation,0,cfg[7]-1);
        $readmemh({case_root,"/group_weight192.hex"},gold_weight,0,cfg[7]-1);
        $readmemh({case_root,"/group_mask.hex"},gold_mask,0,cfg[7]-1);
        $readmemh({case_root,"/group_first.hex"},gold_first,0,cfg[7]-1);
        $readmemh({case_root,"/group_last.hex"},gold_last,0,cfg[7]-1);
        $readmemh({case_root,"/group_acc99.hex"},gold_partial,0,cfg[7]-1);
        $readmemh({case_root,"/task_acc.hex"},gold_acc,0,cfg[8]-1);
        $readmemh({case_root,"/task_pre.hex"},gold_pre,0,cfg[8]-1);
        $readmemh({case_root,"/task_silu.hex"},gold_silu,0,cfg[8]-1);
        $readmemh({case_root,"/task_post.hex"},gold_post,0,cfg[8]-1);
        $readmemh({case_root,"/task_addresses.hex"},gold_addresses,0,cfg[8]-1);
        $readmemh({case_root,"/task_mask.hex"},gold_output_mask,0,cfg[8]-1);
        $readmemh({case_root,"/task_output_int16.hex"},gold_output_int16,0,cfg[8]-1);
        $readmemh({case_root,"/task_quant248.hex"},gold_quant,0,cfg[8]-1);
        $readmemh({case_root,"/byte_trace29.hex"},byte_trace,0,cfg[11]-1);
        $readmemh({case_root,"/weight_trace390.hex"},weight_trace,0,cfg[12]-1);
        $readmemh({case_root,"/output_writes48.hex"},output_trace,0,cfg[9]-1);
        for(index=0;index<24;index=index+1) state_cycles[index] = 0;
        reset_and_load();
        i_layer_id = mode == 1 ? 7'd11 : cfg[0];
        i_tile_y = mode == 2 ? 7'd1 : cfg[1]; i_tile_x = cfg[2];
        active = 1; run_start = cycles; i_start_valid = 1;
        @(negedge i_clk); i_start_valid = 0;
        if(mode == 4) begin
            wait(read_pending); @(negedge i_clk); i_cancel = 1;
        end
        if(mode == 13) begin
            @(posedge i_clk);
            while(!(o_core_valid && i_core_ready)) @(posedge i_clk);
            @(negedge i_clk); i_cancel = 1;
        end
        if(mode >= 5 && mode <= 15 && mode != 13) begin
            if(mode == 5) begin wait(o_read_valid); @(negedge i_clk); end
            if(mode == 6) begin wait(i_read_rsp_valid); @(negedge i_clk); end
            if(mode == 7) begin wait(byte_pending); @(negedge i_clk); end
            if(mode == 8) begin wait(i_byte_rsp_valid); @(negedge i_clk); end
            if(mode == 9) begin wait(weight_pending); @(negedge i_clk); end
            if(mode == 10) begin wait(i_weight_rsp_valid); @(negedge i_clk); end
            if(mode == 11) begin wait(parameter_pending); @(negedge i_clk); end
            if(mode == 12) begin wait(i_parameter_rsp_valid); @(negedge i_clk); end
            if(mode == 14) begin wait(i_core_output_valid); @(negedge i_clk); end
            if(mode == 15) begin
                @(posedge i_clk);
                while(!(o_core_valid && i_core_ready)) @(posedge i_clk);
                @(negedge i_clk);
            end
            reset_and_load();
            $display("STANDARD_TILE_PROTOCOL_PASS mode=%0d reset=1",mode);
            complete = 1; $finish;
        end else if(mode != 0) begin
            wait(o_fault);
            repeat(8) @(negedge i_clk);
            if(!o_busy || o_done || o_start_ready || o_byte_req_valid || o_weight_req_valid || o_core_valid || o_write_valid) $fatal(1,"FAULT_OWNER_RELEASED");
            i_cancel = 0;
            repeat(8) @(negedge i_clk);
            if(!o_fault || !o_busy) $fatal(1,"FAULT_NOT_STICKY");
            reset_and_load();
            $display("STANDARD_TILE_PROTOCOL_PASS mode=%0d reset=1",mode);
            complete = 1; $finish;
        end else begin
            wait(o_done); @(negedge i_clk);
            if(o_fault || groups != cfg[7] || tasks != cfg[8] || outputs != cfg[9] || accs != cfg[8] ||
               partials != cfg[7] || pres != cfg[9] || silus != cfg[15] || posts != cfg[15] ||
               byte_count != cfg[11] || weight_count != cfg[12] || reads != cfg[14] || barriers != 1) $fatal(1,"INCOMPLETE_COUNTS groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d",groups,tasks,outputs,accs,pres,silus,posts);
            if(raw_outputs != cfg[9]-cfg[15] || (raw_outputs != 0 && raw_wide_outputs == 0)) $fatal(1,"RAW16_WIDTH_NOT_EXERCISED");
            $display("STANDARD_TILE_PASS layer=%0d y=%0d x=%0d cycles=%0d groups=%0d tasks=%0d outputs=%0d acc=%0d pre=%0d silu=%0d post=%0d byte=%0d weight=%0d reads=%0d parameters=%0d",cfg[0],cfg[1],cfg[2],cycles-run_start,groups,tasks,outputs,accs,pres,silus,posts,byte_count,weight_count,reads,parameters);
            $display("STANDARD_TILE_RAW outputs=%0d wide_outputs=%0d",raw_outputs,raw_wide_outputs);
            for(index=0;index<24;index=index+1) $display("STANDARD_TILE_STATE state=%0d cycles=%0d",index,state_cycles[index]);
            complete = 1; $fclose(trace_fd); $finish;
        end
    end
endmodule

