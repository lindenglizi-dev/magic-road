`timescale 1ns / 1ps

module tb_road_dispatch_publish;

    localparam [31:0] MODEL_ID = 32'hB35D4A66;
    localparam [2:0] PHASE_FREE = 3'd0;
    localparam [2:0] PHASE_SCAN = 3'd1;
    localparam [2:0] PHASE_SORT = 3'd2;
    localparam [2:0] PHASE_DECODE = 3'd3;
    localparam [2:0] PHASE_NMS = 3'd4;

    reg i_clk;
    reg i_rstn;
    reg common_cancel;
    wire start_valid;
    wire dispatch_job_valid;
    wire [224:0] dispatch_job_descriptor;
    wire dispatch_timestamp_mismatch;
    wire dispatch_busy;
    wire dispatch_error;
    wire [1:0] dispatch_free;
    wire [1:0] dispatch_reading;
    reg dispatch_job_enable=0;
    reg [224:0] accepted_dispatch_context;
    reg [31:0] start_frame_token;
    reg [31:0] start_model_id;
    reg cell_valid;
    reg [111:0] cell_data;
    reg [13:0] cell_id;
    reg [31:0] cell_frame_token;
    wire lut_rsp_valid;
    wire lut_rsp_kind;
    wire [9:0] lut_rsp_address;
    wire [15:0] lut_rsp_tag;
    wire [31:0] lut_rsp_frame_token;
    wire [31:0] lut_rsp_model_id;
    wire [15:0] lut_rsp_data;
    wire lut_rsp_error;
    reg entry_ready;

    wire start_ready;
    wire c2_start_ready;
    wire publisher_start_ready;
    wire publisher_busy;
    wire publisher_fault;
    wire pipeline_start_valid;
    wire [31:0] pipeline_frame_token;
    wire [31:0] pipeline_model_id;
    wire pipeline_cancel;
    wire publisher_entry_ready;
    wire publisher_entry_valid;
    wire [96:0] publisher_entry;
    wire publisher_meta_valid;
    wire [264:0] publisher_metadata;
    wire publisher_abort;
    wire table_entry_ready;
    wire table_meta_ready;
    wire table_copy_ack;
    wire table_busy;
    wire table_error;
    reg dst_clk = 1'b0;
    reg dst_copy_enable = 1'b1;
    reg meta_enable = 1'b1;
    reg [5:0] dst_read_index = 6'd0;
    wire [96:0] dst_entry;
    wire [264:0] dst_metadata;
    wire dst_active_valid;
    wire dst_draw_valid;
    wire dst_pending_valid;
    wire dst_copy_busy;
    wire dst_update;
    wire [63:0] dst_age_upper_ms;
    wire dst_error;
    wire [63:0] real_src_now_ms;
    wire [63:0] real_dst_now_ms;
    wire [31:0] real_dst_epoch;
    wire real_dst_time_valid;
    reg controlled_time = 1'b0;
    reg [63:0] controlled_src_now = 64'd1000;
    reg [63:0] controlled_dst_now = 64'd1000;
    reg controlled_time_valid = 1'b1;
    reg time_clock_enable = 1'b1;
    wire [63:0] source_now_ms;
    wire [63:0] destination_now_ms;
    wire [31:0] destination_epoch;
    wire destination_time_valid;
    reg [31:0] context_epoch = 32'h10203040;
    reg [31:0] context_task = 32'd0;
    reg [31:0] context_source_frame = 32'd0;
    reg [63:0] context_capture_ms = 64'd0;
    reg [264:0] expected_metadata;
    reg [63:0] expected_capture_ms;
    reg [31:0] expected_source_frame;
    reg [31:0] expected_task;
    integer meta_accept_cycle;
    integer copy_ack_cycle;
    realtime start_accept_time;
    realtime meta_accept_time;
    realtime copy_ack_time;
    realtime active_time;
    integer entry_wait_cycles;
    integer metadata_wait_cycles;
    integer copy_wait_dst_cycles;
    integer table_meta_seen = 0;
    integer table_ack_seen = 0;
    integer active_seen = 0;
    integer source_identity_results = 0;
    integer accepted_cells = 0;
    integer previous_publisher_state = -1;
    reg [31:0] last_counted_source = 32'hffffffff;
    reg held_metadata_valid = 1'b0;
    reg [264:0] held_metadata;
    reg [264:0] previous_active_metadata = 265'd0;
    reg [264:0] first_pending_expected_metadata;
    reg expect_first_pending_active = 1'b0;
    reg check_pending_source_hold = 1'b0;
    realtime first_pending_ack_time;
    realtime first_pending_active_time;
    reg dst_sof = 1'b0;
    integer dst_pixel_count = 0;
    integer sof_period_cycles = 1237500;
    wire cell_ready;
    wire lut_req_valid;
    wire lut_req_kind;
    wire [9:0] lut_req_address;
    wire [15:0] lut_req_tag;
    wire [31:0] lut_req_frame_token;
    wire [31:0] lut_req_model_id;
    wire lut_req_ready;
    wire lut_rsp_ready;
    wire lut_cancel;
    wire sealed_valid;
    wire [31:0] sealed_frame_token;
    wire [7:0] count_person;
    wire [7:0] count_vehicle;
    wire read_req_ready;
    wire read_rsp_valid;
    wire read_rsp_class;
    wire [6:0] read_rsp_index;
    wire [159:0] read_rsp_data;
    wire read_rsp_error;
    wire finish_ready;
    wire c2_fault;
    wire [3:0] c2_error_code;
    wire [2:0] c2_phase;
    wire [31:0] c2_scan_cycles;
    wire [31:0] c2_sort_cycles;
    wire [31:0] c2_decode_cycles;
    wire [31:0] c2_input_wait_cycles;
    wire [31:0] c2_lut_wait_cycles;
    wire [31:0] c2_ram_wait_cycles;
    wire [31:0] c2_ram_read_words;
    wire [31:0] c2_ram_write_words;

    wire nms_sealed_ready;
    wire nms_read_valid;
    wire nms_read_class;
    wire [6:0] nms_read_index;
    wire nms_response_ready;
    wire nms_entry_valid;
    wire [96:0] nms_entry_data;
    wire [31:0] nms_frame_token;
    wire [6:0] nms_output_count;
    wire nms_done;
    wire nms_fault;
    wire injected_response_error;

    // Simulation-only image: the controlled endpoint models one outstanding 160-bit read.
`ifndef USE_VENDOR_ROM
    reg [159:0] physical_words [0:7167];
`endif
    reg [4095:0] physical_path;
    wire rom_request_valid;
    wire [12:0] rom_request_addr;
    wire rom_request_ready;
`ifdef USE_VENDOR_ROM
    wire rom_response_valid;
    wire [159:0] rom_response_data;
    wire reader_request_ready;
    wire reader_response_valid;
    wire [159:0] reader_response_data;
    wire reader_request_enable;
    wire reader_response_enable;
`else
    reg rom_response_valid;
    reg [159:0] rom_response_data;
`endif
    wire vendor_rom_fault;
    wire rom_response_ready;
    wire service_fault;
    reg rom_fault;
    reg rom_pending;
    reg [12:0] rom_pending_address;
    integer rom_delay;
    reg hold_rom_response;
    reg hold_rom_request;
    reg [12:0] held_rom_address;
    reg hold_rom_word;
    reg [159:0] held_rom_word;
    integer rom_words_accepted;
    integer rom_words_consumed;
    integer frame_drain_words;
    integer rom_request_wait;
    integer rom_response_wait;
    integer adapter_queries;
    integer adapter_latency_total;
    integer adapter_latency_max;
    integer adapter_accept_cycle;
    integer drain_words;
    integer budget_fail_count;
    reg [96:0] expected_words [0:63];
    reg [111:0] streamed_head;
    reg [4095:0] head_path;
    reg [4095:0] expected_path;
    reg [4095:0] head2_path;
    reg [4095:0] expected2_path;

    integer mode;
    integer stall_mode;
    integer expect_person;
    integer expect_vehicle;
    integer expect_outputs;
    integer expect2_person;
    integer expect2_vehicle;
    integer expect2_outputs;
    integer max_cycles;
    integer cycle_count;
    integer fail_count;
    integer head_handle;
    integer scan_result;
    integer output_seen;
    integer done_seen;
    integer start_accept_cycle;
    integer seal_accept_cycle;
    integer seal_ram_write_words;
    integer last_output_cycle;
    integer done_cycle;
    integer frame_number;
    integer recovery_runs;

    integer nms_cycle_total;
    integer nms_request_phase;
    integer nms_response_phase;
    integer nms_output_phase;
    integer nms_multiply_phase;
    integer nms_other_phase;
    integer nms_request_stall;
    integer nms_response_stall;
    integer nms_output_stall;

    reg frame_monitor;
    reg nms_cycle_enable;
    reg force_output_stall;
    reg late_error_arm;
    reg late_error_used;
    reg [31:0] lfsr;

    reg hold_lut_request;
    reg hold_lut_kind;
    reg [9:0] hold_lut_address;
    reg [15:0] hold_lut_tag;
    reg [31:0] hold_lut_frame;
    reg [31:0] hold_lut_model;
    reg hold_seal;
    reg [31:0] hold_seal_token;
    reg [7:0] hold_seal_person;
    reg [7:0] hold_seal_vehicle;
    reg hold_entry;
    reg [96:0] hold_entry_data;
    reg [31:0] hold_entry_token;

`ifdef USE_VENDOR_ROM
    // One unchanged real reader with its 56 physical lanes; gates only delay handshakes.
    assign reader_request_enable = !stall_mode || lfsr[5:3] != 3'b000;
    assign reader_response_enable = !hold_rom_response && (!stall_mode || lfsr[4:2] != 3'b000);
    assign rom_request_ready = reader_request_ready && reader_request_enable;
    assign rom_response_valid = reader_response_valid && reader_response_enable;
    assign rom_response_data = reader_response_data;
    road_numeric_rom_reader reader(
        .i_clk(i_clk), .i_rstn(i_rstn),
        .i_request_valid(rom_request_valid && reader_request_enable),
        .i_request_addr(rom_request_addr), .o_request_ready(reader_request_ready),
        .o_response_valid(reader_response_valid), .o_response_data(reader_response_data),
        .i_response_ready(rom_response_ready && reader_response_enable), .o_fault(vendor_rom_fault)
    );
`else
    assign vendor_rom_fault = 1'b0;
    assign rom_request_ready = i_rstn && !rom_pending && !rom_response_valid &&
                               (!stall_mode || lfsr[5:3] != 3'b000);
`endif
    assign injected_response_error = late_error_arm && !late_error_used &&
                                     (output_seen != 0) && read_rsp_valid;

    road_head_decode_topk c2(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_abort(pipeline_cancel),
        .i_start_valid(pipeline_start_valid), .i_start_frame_token(pipeline_frame_token),
        .i_start_model_id(pipeline_model_id), .i_cell_valid(cell_valid),
        .i_cell_data(cell_data), .i_cell_id(cell_id), .i_cell_frame_token(cell_frame_token),
        .i_lut_req_ready(lut_req_ready), .i_lut_rsp_valid(lut_rsp_valid),
        .i_lut_rsp_kind(lut_rsp_kind), .i_lut_rsp_address(lut_rsp_address),
        .i_lut_rsp_tag(lut_rsp_tag), .i_lut_rsp_frame_token(lut_rsp_frame_token),
        .i_lut_rsp_model_id(lut_rsp_model_id), .i_lut_rsp_data(lut_rsp_data),
        .i_lut_rsp_error(lut_rsp_error), .i_sealed_ready(nms_sealed_ready),
        .i_read_req_valid(nms_read_valid), .i_read_req_class(nms_read_class),
        .i_read_req_index(nms_read_index), .i_read_rsp_ready(nms_response_ready),
        .i_finish_valid(nms_done), .i_finish_frame_token(nms_frame_token),
        .o_start_ready(c2_start_ready), .o_cell_ready(cell_ready),
        .o_lut_req_valid(lut_req_valid), .o_lut_req_kind(lut_req_kind),
        .o_lut_req_address(lut_req_address), .o_lut_req_tag(lut_req_tag),
        .o_lut_req_frame_token(lut_req_frame_token), .o_lut_req_model_id(lut_req_model_id),
        .o_lut_rsp_ready(lut_rsp_ready), .o_lut_cancel(lut_cancel),
        .o_sealed_valid(sealed_valid), .o_sealed_frame_token(sealed_frame_token),
        .o_count_person(count_person), .o_count_vehicle(count_vehicle),
        .o_read_req_ready(read_req_ready), .o_read_rsp_valid(read_rsp_valid),
        .o_read_rsp_class(read_rsp_class), .o_read_rsp_index(read_rsp_index),
        .o_read_rsp_data(read_rsp_data), .o_read_rsp_error(read_rsp_error),
        .o_finish_ready(finish_ready), .o_fault(c2_fault), .o_error_code(c2_error_code),
        .o_phase(c2_phase), .o_scan_cycles(c2_scan_cycles),
        .o_sort_cycles(c2_sort_cycles), .o_decode_cycles(c2_decode_cycles),
        .o_input_wait_cycles(c2_input_wait_cycles), .o_lut_wait_cycles(c2_lut_wait_cycles),
        .o_ram_wait_cycles(c2_ram_wait_cycles), .o_ram_read_words(c2_ram_read_words),
        .o_ram_write_words(c2_ram_write_words)
    );

    // Frozen real adapter owns lookup identity and byte extraction; no direct LUT oracle.
    road_shared_lut_service service(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(pipeline_cancel | lut_cancel),
        .i_lut_req_valid(lut_req_valid), .i_lut_req_kind(lut_req_kind),
        .i_lut_req_address(lut_req_address), .i_lut_req_tag(lut_req_tag),
        .i_lut_req_frame_token(lut_req_frame_token), .i_lut_req_model_id(lut_req_model_id),
        .o_lut_req_ready(lut_req_ready), .o_lut_rsp_valid(lut_rsp_valid),
        .o_lut_rsp_kind(lut_rsp_kind), .o_lut_rsp_address(lut_rsp_address),
        .o_lut_rsp_tag(lut_rsp_tag), .o_lut_rsp_frame_token(lut_rsp_frame_token),
        .o_lut_rsp_model_id(lut_rsp_model_id), .o_lut_rsp_data(lut_rsp_data),
        .o_lut_rsp_error(lut_rsp_error), .i_lut_rsp_ready(lut_rsp_ready),
        .o_rom_request_valid(rom_request_valid), .o_rom_request_addr(rom_request_addr),
        .i_rom_request_ready(rom_request_ready), .i_rom_response_valid(rom_response_valid),
        .i_rom_response_data(rom_response_data), .o_rom_response_ready(rom_response_ready),
        .i_rom_fault(rom_fault | vendor_rom_fault), .o_fault(service_fault)
    );

    road_nms_serial c9(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(pipeline_cancel),
        .i_sealed_valid(sealed_valid), .i_frame_token(sealed_frame_token),
        .i_count_person(count_person), .i_count_vehicle(count_vehicle),
        .i_read_ready(read_req_ready), .i_response_valid(read_rsp_valid),
        .i_response_class(read_rsp_class), .i_response_index(read_rsp_index),
        .i_response_data(read_rsp_data),
        .i_response_error(read_rsp_error | injected_response_error),
        .i_entry_ready(publisher_entry_ready), .o_sealed_ready(nms_sealed_ready),
        .o_read_valid(nms_read_valid), .o_read_class(nms_read_class),
        .o_read_index(nms_read_index), .o_response_ready(nms_response_ready),
        .o_entry_valid(nms_entry_valid), .o_entry_data(nms_entry_data),
        .o_frame_token(nms_frame_token), .o_output_count(nms_output_count),
        .o_done(nms_done), .o_fault(nms_fault)
    );

    always #5 i_clk = ~i_clk;

    initial begin
        #2.3;
        // Three rounded half-periods total20ns, yielding exactly75MHz on average.
        forever begin
            #6.667 dst_clk = ~dst_clk;
            #6.666 dst_clk = ~dst_clk;
            #6.667 dst_clk = ~dst_clk;
        end
    end

    assign start_ready = publisher_start_ready;
    assign start_valid = dispatch_job_valid && dispatch_job_enable;
    tb_road_dispatch_fixture dispatch_link(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_job_ready(publisher_start_ready&&dispatch_job_enable),
        .i_external_done(nms_done),.i_external_done_id(nms_frame_token),
        .o_job_valid(dispatch_job_valid),.o_job_descriptor(dispatch_job_descriptor),
        .o_timestamp_mismatch(dispatch_timestamp_mismatch),.o_busy(dispatch_busy),.o_error(dispatch_error),
        .o_wrap_fault(),.o_free_mask(dispatch_free),.o_ready_mask(),.o_reading_mask(dispatch_reading),
        .o_quarantine_mask()
    );
    assign source_now_ms = controlled_time ? controlled_src_now : real_src_now_ms;
    assign destination_now_ms = controlled_time ? controlled_dst_now : real_dst_now_ms;
    assign destination_epoch = controlled_time ? 32'h10203040 : real_dst_epoch;
    assign destination_time_valid = controlled_time ? controlled_time_valid : real_dst_time_valid;

    road_result_publisher publisher(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(common_cancel),
        .i_start_valid(start_valid), .i_start_epoch(context_epoch),
        .i_start_task_id(context_task), .i_start_source_frame_id(context_source_frame),
        .i_start_model_id(start_model_id), .i_start_capture_ms(context_capture_ms),
        .i_now_ms(source_now_ms), .i_pipeline_start_ready(c2_start_ready),
        .i_entry_valid(nms_entry_valid), .i_entry(nms_entry_data),
        .i_result_frame_token(nms_frame_token), .i_result_count(nms_output_count),
        .i_result_done(nms_done),
        .i_pipeline_fault(c2_fault || nms_fault || service_fault || vendor_rom_fault),
        .i_table_entry_ready(table_entry_ready && entry_ready),
        .i_table_meta_ready(table_meta_ready && meta_enable),
        .i_table_copy_ack(table_copy_ack), .i_table_busy(table_busy), .i_table_error(table_error),
        .o_start_ready(publisher_start_ready), .o_pipeline_start_valid(pipeline_start_valid),
        .o_pipeline_frame_token(pipeline_frame_token), .o_pipeline_model_id(pipeline_model_id),
        .o_pipeline_cancel(pipeline_cancel), .o_entry_ready(publisher_entry_ready),
        .o_table_entry_valid(publisher_entry_valid), .o_table_entry(publisher_entry),
        .o_table_meta_valid(publisher_meta_valid), .o_table_metadata(publisher_metadata),
        .o_table_abort(publisher_abort), .o_busy(publisher_busy), .o_error(publisher_fault)
    );

    road_time_snapshot timestamp_source(
        .i_src_clk(i_clk && time_clock_enable), .i_dst_clk(dst_clk), .i_rstn(i_rstn),
        .i_src_epoch(32'h10203040), .o_src_now_ms(real_src_now_ms), .o_src_tick(),
        .o_src_busy(), .o_dst_now_ms(real_dst_now_ms), .o_dst_epoch(real_dst_epoch),
        .o_dst_time_valid(real_dst_time_valid), .o_dst_update()
    );

    road_detection_table_cdc #(.AGE_LIMIT_MS(2000), .EXPECTED_MODEL_ID(MODEL_ID)) table_cdc(
        .i_src_clk(i_clk), .i_dst_clk(dst_clk), .i_rstn(i_rstn),
        .i_src_entry_valid(publisher_entry_valid && entry_ready), .i_src_entry(publisher_entry),
        .o_src_entry_ready(table_entry_ready),
        .i_src_meta_valid(publisher_meta_valid && meta_enable), .i_src_metadata(publisher_metadata),
        .o_src_meta_ready(table_meta_ready), .i_src_abort(publisher_abort),
        .o_src_copy_ack(table_copy_ack), .o_src_busy(table_busy), .o_src_error(table_error),
        .i_dst_copy_enable(dst_copy_enable), .i_dst_sof(dst_sof),
        .i_dst_now_ms(destination_now_ms), .i_dst_time_epoch(destination_epoch),
        .i_dst_time_valid(destination_time_valid), .i_dst_read_index(dst_read_index),
        .o_dst_entry(dst_entry), .o_dst_metadata(dst_metadata), .o_dst_active_valid(dst_active_valid),
        .o_dst_draw_valid(dst_draw_valid), .o_dst_pending_valid(dst_pending_valid),
        .o_dst_copy_busy(dst_copy_busy), .o_dst_update(dst_update),
        .o_dst_age_upper_ms(dst_age_upper_ms), .o_dst_error(dst_error)
    );

    always @(negedge dst_clk) begin
        if (!i_rstn) begin
            dst_pixel_count = 0;
            dst_sof = 1'b0;
        end else if (dst_pixel_count == sof_period_cycles-1) begin
            dst_pixel_count = 0;
            dst_sof = 1'b1;
        end else begin
            dst_pixel_count = dst_pixel_count + 1;
            dst_sof = 1'b0;
        end
    end

    task mark_error;
        input integer error_id;
        begin
            fail_count = fail_count + 1;
            $display("TB_ERROR id=%0d cycle=%0d c2_phase=%0d c2_code=%0d nms_state=%0d",
                     error_id, cycle_count, c2_phase, c2_error_code, c9.state_current);
        end
    endtask

    task clear_drives;
        begin
            common_cancel = 1'b0;
            dispatch_job_enable = 1'b0;
            dispatch_link.clear_drives;
            start_frame_token = 32'd0;
            start_model_id = 32'd0;
            cell_valid = 1'b0;
            cell_data = 112'd0;
            cell_id = 14'd0;
            cell_frame_token = 32'd0;
            force_output_stall = 1'b0;
            late_error_arm = 1'b0;
            meta_enable = 1'b1;
            dst_copy_enable = 1'b1;
        end
    endtask

    task clear_frame_metrics;
        begin
            rom_words_accepted = 0;
            rom_words_consumed = 0;
            frame_drain_words = 0;
            rom_request_wait = 0;
            rom_response_wait = 0;
            adapter_queries = 0;
            adapter_latency_total = 0;
            adapter_latency_max = 0;
            adapter_accept_cycle = -1;
            output_seen = 0;
            done_seen = 0;
            start_accept_cycle = -1;
            seal_accept_cycle = -1;
            seal_ram_write_words = -1;
            last_output_cycle = -1;
            done_cycle = -1;
            nms_cycle_total = 0;
            nms_request_phase = 0;
            nms_response_phase = 0;
            nms_output_phase = 0;
            nms_multiply_phase = 0;
            nms_other_phase = 0;
            nms_request_stall = 0;
            nms_response_stall = 0;
            nms_output_stall = 0;
            late_error_used = 1'b0;
            accepted_cells = 0;
            meta_accept_cycle = -1;
            copy_ack_cycle = -1;
            start_accept_time = -1;
            meta_accept_time = -1;
            copy_ack_time = -1;
            active_time = -1;
            entry_wait_cycles = 0;
            metadata_wait_cycles = 0;
            copy_wait_dst_cycles = 0;
        end
    endtask

    task reset_dut;
        begin
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            clear_drives;
            i_rstn = 1'b0;
            repeat (4) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(negedge i_clk);
            if (!c2_start_ready || publisher_busy || c2_phase !== PHASE_FREE || c2_fault || nms_fault ||
                sealed_valid || read_rsp_valid || nms_entry_valid || nms_done)
                mark_error(100);
        end
    endtask

    task load_expected;
        input [4095:0] path_value;
        integer clear_index;
        begin
            for (clear_index = 0; clear_index < 64; clear_index = clear_index + 1)
                expected_words[clear_index] = 97'd0;
            if (expect_outputs > 0)
                $readmemh(path_value, expected_words, 0, expect_outputs - 1);
        end
    endtask

    task start_frame;
        integer watchdog;
        begin
            clear_frame_metrics;
            frame_number = frame_number + 1;
            watchdog = 0;
            @(negedge i_clk);
            // Capture, visibility, identity and image last-consumption are controlled services.
            dispatch_link.allocate(32'hca000000+frame_number,source_now_ms+64'd7,1'b0);
            dispatch_link.send_identity(32'h10203040,32'hca000000+frame_number,source_now_ms);
            dispatch_link.finish_capture(19'd442368);
            dispatch_link.write_visible(1'b0,32'hca000000+frame_number);
            while(!dispatch_job_valid&&watchdog<1000) begin @(negedge i_clk);watchdog=watchdog+1;end
            if(!dispatch_job_valid||!dispatch_timestamp_mismatch||dispatch_job_descriptor[0]!==1'b0||
                dispatch_job_descriptor[32:1]!==32'h03400000||
                dispatch_job_descriptor[96:65]===dispatch_job_descriptor[128:97])
                $fatal(1,"dispatcher context/base/task-source distinction failed");
            accepted_dispatch_context=dispatch_job_descriptor;
            start_frame_token = dispatch_job_descriptor[96:65];
            start_model_id = dispatch_job_descriptor[160:129];
            context_epoch = dispatch_job_descriptor[64:33];
            context_task = dispatch_job_descriptor[96:65];
            context_source_frame = dispatch_job_descriptor[128:97];
            context_capture_ms = dispatch_job_descriptor[224:161];
            expected_capture_ms = context_capture_ms;
            expected_source_frame = context_source_frame;
            expected_task = start_frame_token;
            dispatch_job_enable = 1'b1;
            frame_monitor = 1'b1;
            // Admission is determined at a rising edge; the random ready gate can change at negedge.
            @(posedge i_clk);
            while (!start_ready && watchdog < 10000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!start_ready)
                mark_error(110);
            @(negedge i_clk);
            dispatch_job_enable = 1'b0;
            if(dispatch_link.accepted_job!==accepted_dispatch_context||dispatch_error)
                $fatal(1,"dispatcher/publisher did not accept same225bit context");
            // Busy-time mutations prove the publisher uses the accepted context.
            context_epoch = 32'hdeadbeef;
            context_task = 32'hffffffff;
            start_model_id = 32'hdeadbeef;
            context_source_frame = 32'hbad00000;
            context_capture_ms = 64'hffffffffffffffff;
        end
    endtask

    task send_cells;
        input [4095:0] path_value;
        input integer limit;
        integer cell_number;
        integer watchdog;
        begin
            if(mode==7) $display("FAULT_PROBE_SEND_BEGIN frame=%0d limit=%0d cycle=%0d",frame_number,limit,cycle_count);
            head_handle = $fopen(path_value, "r");
            if (head_handle == 0)
                mark_error(120);
            for (cell_number = 0; cell_number < limit; cell_number = cell_number + 1) begin
                scan_result = $fscanf(head_handle, "%h\n", streamed_head);
                if (scan_result != 1) begin
                    mark_error(121);
                    cell_number = limit;
                end
                if (cell_number < limit) begin
                    if (stall_mode && (cell_number == 7 || (cell_number % 997) == 0)) begin
                        cell_valid = 1'b0;
                        repeat (cell_number == 7 ? 17 : 2) @(posedge i_clk);
                    end
                    watchdog = 0;
                    @(negedge i_clk);
                    cell_id = cell_number[13:0];
                    cell_frame_token = start_frame_token;
                    cell_data = streamed_head;
                    cell_valid = 1'b1;
                    while (!cell_ready && watchdog < 100000) begin
                        @(posedge i_clk);
                        watchdog = watchdog + 1;
                    end
                    if (!cell_ready) begin
                        mark_error(122);
                        $fatal(1,"CELL_WAIT_TIMEOUT frame=%0d cell_loop=%0d cell_id=%0d accepted_cells=%0d publisher_state=%0d c2_phase=%0d start_ready=%0d cancel=%0d pipeline_cancel=%0d late_arm=%0d late_used=%0d",frame_number,cell_number,cell_id,accepted_cells,publisher.state_current,c2_phase,start_ready,common_cancel,pipeline_cancel,late_error_arm,late_error_used);
                    end
                    @(posedge i_clk);
                    @(negedge i_clk);
                    cell_valid = 1'b0;
                end
            end
            if (head_handle != 0)
                $fclose(head_handle);
            if(mode==7) $display("FAULT_PROBE_SEND_END frame=%0d accepted=%0d cycle=%0d",frame_number,accepted_cells,cycle_count);
        end
    endtask

    task wait_for_done;
        integer watchdog;
        begin
            watchdog = 0;
            while (!nms_done && !nms_fault && !c2_fault && watchdog < 2000000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!nms_done || nms_fault || c2_fault)
                mark_error(130);
            repeat (4) @(posedge i_clk);
            if (c2_phase !== PHASE_FREE || !c2_start_ready)
                mark_error(131);
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            if (output_seen != expect_outputs || nms_output_count != expect_outputs[6:0])
                mark_error(132);
            if (done_seen != 1)
                mark_error(133);
            if (rom_words_accepted != rom_words_consumed - frame_drain_words ||
                rom_words_accepted != adapter_queries)
                mark_error(137);
            if (done_cycle - start_accept_cycle > 2000000) begin
                budget_fail_count = budget_fail_count + 1;
                $display("TB_BUDGET_FAIL cycles=%0d allowance=2000000", done_cycle - start_accept_cycle);
            end
            if (nms_cycle_total != nms_request_phase + nms_response_phase + nms_output_phase +
                                    nms_multiply_phase + nms_other_phase)
                mark_error(135);
            if (nms_cycle_total != done_cycle - seal_accept_cycle)
                mark_error(136);
        end
    endtask

    task print_metrics;
        begin
            $display("JOINT_RESULT frame=%0d outputs=%0d start_to_seal=%0d seal_to_last=%0d seal_to_done=%0d start_to_last=%0d start_to_done=%0d",
                     frame_number, output_seen, seal_accept_cycle - start_accept_cycle,
                     (last_output_cycle < 0) ? -1 : last_output_cycle - seal_accept_cycle,
                     done_cycle - seal_accept_cycle,
                     (last_output_cycle < 0) ? -1 : last_output_cycle - start_accept_cycle,
                     done_cycle - start_accept_cycle);
            $display("ROM_RESULT accepted_words=%0d consumed_words=%0d request_wait=%0d response_wait=%0d adapter_queries=%0d adapter_accept_to_rsp_handshake_total=%0d adapter_accept_to_rsp_handshake_max=%0d drain_words=%0d frame_carried_drain_words=%0d",
                     rom_words_accepted, rom_words_consumed, rom_request_wait, rom_response_wait,
                     adapter_queries, adapter_latency_total, adapter_latency_max, drain_words, frame_drain_words);
            $display("C2_RESULT scan=%0d sort=%0d decode=%0d input_wait=%0d lut_wait=%0d ram_wait=%0d ram_read_words=%0d ram_write_words=%0d",
                     c2_scan_cycles, c2_sort_cycles, c2_decode_cycles, c2_input_wait_cycles,
                     c2_lut_wait_cycles, c2_ram_wait_cycles, c2_ram_read_words, c2_ram_write_words);
            $display("NMS_RESULT cycles=%0d request_phase=%0d response_phase=%0d multiply=%0d output_phase=%0d other=%0d request_stall=%0d response_stall=%0d output_stall=%0d",
                     nms_cycle_total, nms_request_phase, nms_response_phase, nms_multiply_phase,
                     nms_output_phase, nms_other_phase, nms_request_stall,
                     nms_response_stall, nms_output_stall);
        end
    endtask

    task run_complete;
        input [4095:0] active_head;
        begin
            start_frame;
            send_cells(active_head, 12096);
            // Explicit controlled last image response consumption, not NNdone or result copy_ack.
            dispatch_link.last_read(accepted_dispatch_context[0],accepted_dispatch_context[64:33],
                accepted_dispatch_context[128:97]);
            if(!dispatch_free[accepted_dispatch_context[0]]||!dispatch_busy)
                $fatal(1,"controlled last-read-first did not free slot while retaining task context");
            wait_for_done;
            wait_for_publication;
            print_metrics;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    task wait_for_publication;
        integer watchdog;
        integer item;
        integer active_before;
        begin
            watchdog = 0;
            while (copy_ack_cycle < 0 && watchdog < 2000000) begin
                @(negedge i_clk);
                watchdog = watchdog + 1;
            end
            if (copy_ack_cycle < 0 || meta_accept_cycle <= last_output_cycle ||
                meta_accept_cycle <= done_cycle || table_meta_seen != table_ack_seen)
                mark_error(300);
            active_before = active_seen;
            while (active_time < 0 && watchdog < 4000000) begin
                @(negedge dst_clk);
                watchdog = watchdog + 1;
            end
            if (active_time < 0 || !dst_active_valid || dst_metadata !== expected_metadata)
                mark_error(301);
            if ((expect_outputs != 0) && !dst_draw_valid)
                mark_error(302);
            if ((expect_outputs == 0) && dst_draw_valid)
                mark_error(303);
            for (item=0; item<64; item=item+1) begin
                dst_read_index = item[5:0];
                #1;
                if (dst_entry !== ((item < expect_outputs) ? expected_words[item] : 97'd0))
                    mark_error(304);
            end
            if (!c2_start_ready || publisher_busy || table_busy)
                mark_error(305);
            $display("PUBLISH_RESULT task=%0d source=%0d count=%0d capture_ms=%0d completion_ms=%0d start_ns=%0.3f meta_ns=%0.3f ack_ns=%0.3f active_ns=%0.3f start_to_meta_ns=%0.3f meta_to_ack_ns=%0.3f ack_to_active_ns=%0.3f start_to_active_ns=%0.3f contained_entry_wait_src=%0d contained_meta_wait_src=%0d contained_copy_wait_dst=%0d sof_period_dst=%0d time_controlled=%0d",
                expected_task,expected_source_frame,expect_outputs,expected_capture_ms,
                expected_metadata[264:201],start_accept_time,meta_accept_time,copy_ack_time,active_time,
                meta_accept_time-start_accept_time,copy_ack_time-meta_accept_time,active_time-copy_ack_time,
                active_time-start_accept_time,entry_wait_cycles,metadata_wait_cycles,copy_wait_dst_cycles,
                sof_period_cycles,controlled_time);
        end
    endtask

    task pulse_reset;
        begin
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            @(negedge i_clk);
            i_rstn = 1'b0;
            #1;
            if (sealed_valid || read_rsp_valid || nms_entry_valid || nms_done ||
                nms_sealed_ready || nms_read_valid || nms_response_ready)
                mark_error(140);
            repeat (3) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(negedge i_clk);
            if (!c2_start_ready || publisher_busy || c2_phase !== PHASE_FREE || c2_fault || nms_fault)
                mark_error(141);
        end
    endtask

    task pulse_cancel;
        begin
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            @(negedge i_clk);
            common_cancel = 1'b1;
            @(posedge i_clk);
            #1;
            if (sealed_valid || read_rsp_valid || nms_entry_valid || nms_done ||
                nms_sealed_ready || nms_read_valid || nms_response_ready)
                mark_error(142);
            @(negedge i_clk);
            common_cancel = 1'b0;
            repeat (3) @(negedge i_clk);
            if (!c2_start_ready || publisher_busy || c2_phase !== PHASE_FREE || c2_fault || nms_fault)
                mark_error(143);
        end
    endtask

    task recover_after_reset;
        begin
            pulse_reset;
            force_output_stall = 1'b0;
            late_error_arm = 1'b0;
            load_expected(expected_path);
            run_complete(head_path);
        end
    endtask

    task run_reset_case;
        begin
            start_frame;
            if (mode == 2) begin
                send_cells(head_path, 64);
                if (c2_phase !== PHASE_SCAN)
                    mark_error(150);
            end else begin
                if (mode == 6)
                    force_output_stall = 1'b1;
                send_cells(head_path, 12096);
                if (mode == 3) begin
                    while (c2_phase !== PHASE_SORT && !c2_fault) @(posedge i_clk);
                end else if (mode == 4) begin
                    while (c2_phase !== PHASE_DECODE && !c2_fault) @(posedge i_clk);
                end else if (mode == 5) begin
                    while (c9.state_current != c9.ST_MULTIPLY_CURRENT &&
                           c9.state_current != c9.ST_MULTIPLY_PREVIOUS &&
                           c9.state_current != c9.ST_MULTIPLY_INTERSECTION && !nms_fault) @(posedge i_clk);
                    repeat (7) @(posedge i_clk);
                end else begin
                    while (!nms_entry_valid && !nms_fault) @(posedge i_clk);
                    repeat (8) @(posedge i_clk);
                    if (!nms_entry_valid)
                        mark_error(151);
                end
            end
            recover_after_reset;
        end
    endtask

    task run_late_error;
        integer watchdog;
        begin
            late_error_arm = 1'b1;
            start_frame;
            send_cells(head_path, 12096);
            watchdog = 0;
            while (!publisher_fault && watchdog < 2000000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!publisher_fault || output_seen == 0 || !late_error_used)
                mark_error(160);
            if (nms_done || nms_output_count != 0 || nms_entry_valid)
                mark_error(161);
            repeat (4) @(negedge i_clk);
            if (table_busy || dst_pending_valid || dst_active_valid || table_meta_seen != 0 ||
                c2_phase !== PHASE_FREE)
                mark_error(162);
            pulse_cancel;
            late_error_arm = 1'b0;
            load_expected(expected_path);
            run_complete(head_path);
        end
    endtask

    task run_long_output_stall;
        begin
            start_frame;
            force_output_stall = 1'b1;
            send_cells(head_path, 12096);
            while (!nms_entry_valid && !nms_fault) @(posedge i_clk);
            repeat (128) @(posedge i_clk);
            if (!nms_entry_valid)
                mark_error(170);
            force_output_stall = 1'b0;
            wait_for_done;
            wait_for_publication;
            print_metrics;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    // Common cancel deliberately does not clear the endpoint: accepted reads must drain.
`ifdef USE_VENDOR_ROM
    // Counter ownership follows actual reader handshakes; no cancel reset is allowed.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn)
            rom_pending <= 1'b0;
        else if (rom_request_valid && rom_request_ready)
            rom_pending <= 1'b1;
        else if (rom_response_valid && rom_response_ready)
            rom_pending <= 1'b0;
    end
`else
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            rom_pending <= 1'b0;
            rom_delay <= 0;
            rom_response_valid <= 1'b0;
            rom_response_data <= 160'd0;
            rom_pending_address <= 13'd0;
        end else begin
            if (rom_response_valid && rom_response_ready)
                rom_response_valid <= 1'b0;
            if (rom_request_valid && rom_request_ready) begin
                if (rom_request_addr >= 7168)
                    mark_error(180);
                rom_pending <= 1'b1;
                rom_pending_address <= rom_request_addr;
                rom_delay <= stall_mode ? (1 + (lfsr[4:2] % 13)) : 1;
            end else if (rom_pending && rom_delay != 0) begin
                rom_delay <= rom_delay - 1;
            end else if (rom_pending && !rom_response_valid && !hold_rom_response) begin
                rom_pending <= 1'b0;
                rom_response_valid <= 1'b1;
                rom_response_data <= physical_words[rom_pending_address];
            end
        end
    end
`endif

    // Verify both physical-word holds and adapter identity, including canceled late returns.
    always @(posedge i_clk) begin
        if(mode==7 && i_rstn && publisher.state_current!=previous_publisher_state) begin
            $display("FAULT_PROBE_STATE frame=%0d cycle=%0d publisher=%0d c2=%0d accepted_cells=%0d cell_valid=%0d cell_id=%0d output_seen=%0d nms_fault=%0d c2_fault=%0d code=%0d cancel=%0d pipeline_cancel=%0d late_arm=%0d late_used=%0d",frame_number,cycle_count,publisher.state_current,c2_phase,accepted_cells,cell_valid,cell_id,output_seen,nms_fault,c2_fault,c2_error_code,common_cancel,pipeline_cancel,late_error_arm,late_error_used);
            previous_publisher_state=publisher.state_current;
        end
        if(i_rstn && cell_valid && cell_ready) begin
            accepted_cells=accepted_cells+1;
            if(mode==7 && cell_id>=12088) $display("FAULT_PROBE_CELL frame=%0d cycle=%0d id=%0d accepted=%0d",frame_number,cycle_count,cell_id,accepted_cells);
        end
        if (!i_rstn) begin
            hold_rom_request <= 1'b0;
            hold_rom_word <= 1'b0;
        end else begin
            if (hold_rom_request && !common_cancel && !lut_cancel &&
                (!rom_request_valid || rom_request_addr !== held_rom_address))
                mark_error(181);
            if (hold_rom_word && (!rom_response_valid || rom_response_data !== held_rom_word))
                mark_error(182);
            hold_rom_request <= rom_request_valid && !rom_request_ready;
            held_rom_address <= rom_request_addr;
            hold_rom_word <= rom_response_valid && !rom_response_ready;
            held_rom_word <= rom_response_data;
            if (rom_response_valid && rom_response_ready && service.state_current == service.ST_DRAIN)
                drain_words = drain_words + 1;
        end
    end

    task run_owned_rom_boundary;
        integer watchdog;
        integer before_drain;
        begin
            hold_rom_response = 1'b1;
            before_drain = drain_words;
            start_frame;
            send_cells(head_path, 1);
            watchdog = 0;
            while (!rom_pending && watchdog < 1000) begin
                @(negedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!rom_pending)
                mark_error(210);
            if (mode == 9) begin
                pulse_cancel;
                if (!rom_pending || lut_req_ready || lut_rsp_valid)
                    mark_error(211);
                hold_rom_response = 1'b0;
                load_expected(expected_path);
                run_complete(head_path);
                if (drain_words != before_drain + 1)
                    mark_error(212);
            end else if (mode == 10) begin
                pulse_reset;
                hold_rom_response = 1'b0;
                if (rom_pending || rom_response_valid)
                    mark_error(213);
                load_expected(expected_path);
                run_complete(head_path);
            end else begin
                // Fault injection is at the controlled reader fault boundary, never a PH1P claim.
                rom_fault = 1'b1;
                repeat (6) @(negedge i_clk);
                if (!service_fault || !c2_fault)
                    mark_error(214);
                pulse_cancel;
                if (!service_fault)
                    mark_error(215);
                rom_fault = 1'b0;
                hold_rom_response = 1'b0;
                recover_after_reset;
            end
        end
    endtask

    always @(negedge i_clk) begin
        lfsr = {lfsr[30:0], lfsr[31] ^ lfsr[21] ^ lfsr[1] ^ lfsr[0]};
        if (!i_rstn || common_cancel)
            entry_ready = 1'b0;
        else if (force_output_stall)
            entry_ready = 1'b0;
        else
            entry_ready = !stall_mode || lfsr[2:0] != 3'b000;
    end

    always @(posedge i_clk) begin
        cycle_count = cycle_count + 1;
        if (frame_monitor && i_rstn) begin
            if (rom_request_valid && rom_request_ready)
                rom_words_accepted = rom_words_accepted + 1;
            if (rom_response_valid && rom_response_ready)
                rom_words_consumed = rom_words_consumed + 1;
            if (rom_response_valid && rom_response_ready && service.state_current == service.ST_DRAIN)
                frame_drain_words = frame_drain_words + 1;
            if (rom_request_valid && !rom_request_ready)
                rom_request_wait = rom_request_wait + 1;
            if (rom_pending && !rom_response_valid)
                rom_response_wait = rom_response_wait + 1;
            if (lut_req_valid && lut_req_ready) begin
                adapter_queries = adapter_queries + 1;
                adapter_accept_cycle = cycle_count;
            end
            if (lut_rsp_valid && lut_rsp_ready) begin
                if (lut_rsp_frame_token !== start_frame_token || lut_rsp_model_id !== MODEL_ID)
                    mark_error(183);
                adapter_latency_total = adapter_latency_total + cycle_count - adapter_accept_cycle;
                if (cycle_count - adapter_accept_cycle > adapter_latency_max)
                    adapter_latency_max = cycle_count - adapter_accept_cycle;
            end
        end
        if (cycle_count > max_cycles) begin
            mark_error(900);
            $fatal(1, "joint watchdog");
        end
        if (!i_rstn || pipeline_cancel) begin
            hold_lut_request <= 1'b0;
            hold_seal <= 1'b0;
            hold_entry <= 1'b0;
        end else begin
            if (hold_lut_request && (!lut_req_valid || lut_req_kind !== hold_lut_kind ||
                lut_req_address !== hold_lut_address || lut_req_tag !== hold_lut_tag ||
                lut_req_frame_token !== hold_lut_frame || lut_req_model_id !== hold_lut_model))
                mark_error(190);
            hold_lut_request <= lut_req_valid && !lut_req_ready;
            hold_lut_kind <= lut_req_kind;
            hold_lut_address <= lut_req_address;
            hold_lut_tag <= lut_req_tag;
            hold_lut_frame <= lut_req_frame_token;
            hold_lut_model <= lut_req_model_id;
            if (hold_seal && (!sealed_valid || sealed_frame_token !== hold_seal_token ||
                count_person !== hold_seal_person || count_vehicle !== hold_seal_vehicle))
                mark_error(191);
            hold_seal <= sealed_valid && !nms_sealed_ready;
            hold_seal_token <= sealed_frame_token;
            hold_seal_person <= count_person;
            hold_seal_vehicle <= count_vehicle;
            if (hold_entry && (!nms_entry_valid || nms_entry_data !== hold_entry_data ||
                nms_frame_token !== hold_entry_token))
                mark_error(192);
            hold_entry <= nms_entry_valid && !publisher_entry_ready;
            hold_entry_data <= nms_entry_data;
            hold_entry_token <= nms_frame_token;
        end

        // Seal is excluded and done is included, so this occupancy interval is
        // exactly done_cycle - seal_accept_cycle cycles.
        if (nms_cycle_enable && i_rstn && !pipeline_cancel) begin
            nms_cycle_total = nms_cycle_total + 1;
            if (c9.state_current == c9.ST_CURRENT_REQUEST || c9.state_current == c9.ST_PREVIOUS_REQUEST)
                nms_request_phase = nms_request_phase + 1;
            else if (c9.state_current == c9.ST_CURRENT_WAIT || c9.state_current == c9.ST_PREVIOUS_WAIT)
                nms_response_phase = nms_response_phase + 1;
            else if (c9.state_current == c9.ST_OUTPUT)
                nms_output_phase = nms_output_phase + 1;
            else if (c9.state_current == c9.ST_MULTIPLY_CURRENT ||
                     c9.state_current == c9.ST_MULTIPLY_PREVIOUS ||
                     c9.state_current == c9.ST_MULTIPLY_INTERSECTION)
                nms_multiply_phase = nms_multiply_phase + 1;
            else
                nms_other_phase = nms_other_phase + 1;
            if ((c9.state_current == c9.ST_CURRENT_REQUEST || c9.state_current == c9.ST_PREVIOUS_REQUEST) &&
                nms_read_valid && !read_req_ready)
                nms_request_stall = nms_request_stall + 1;
            if ((c9.state_current == c9.ST_CURRENT_WAIT || c9.state_current == c9.ST_PREVIOUS_WAIT) &&
                !read_rsp_valid)
                nms_response_stall = nms_response_stall + 1;
            if (c9.state_current == c9.ST_OUTPUT && nms_entry_valid && !publisher_entry_ready)
                nms_output_stall = nms_output_stall + 1;
        end

        if (frame_monitor && i_rstn && !pipeline_cancel) begin
            if (start_valid && start_ready && start_accept_cycle < 0) begin
                start_accept_cycle = cycle_count;
                start_accept_time = $realtime;
            end
            if (sealed_valid && nms_sealed_ready) begin
                seal_accept_cycle = cycle_count;
                seal_ram_write_words = c2_ram_write_words;
                nms_cycle_enable = 1'b1;
                if (sealed_frame_token !== start_frame_token || count_person !== expect_person[7:0] ||
                    count_vehicle !== expect_vehicle[7:0])
                    mark_error(200);
            end
            if (seal_ram_write_words >= 0 && !nms_done &&
                c2_ram_write_words != seal_ram_write_words)
                mark_error(203);
            if (nms_entry_valid && publisher_entry_ready) begin
                if (output_seen >= expect_outputs || nms_entry_data !== expected_words[output_seen] ||
                    nms_frame_token !== start_frame_token)
                    mark_error(201);
                output_seen = output_seen + 1;
                last_output_cycle = cycle_count;
            end
            if (injected_response_error && read_rsp_valid && nms_response_ready)
                late_error_used <= 1'b1;
            if (nms_done) begin
                done_seen = done_seen + 1;
                done_cycle = cycle_count;
                expected_metadata = {source_now_ms, expected_capture_ms, 2'd0,
                    expect_outputs[6:0], MODEL_ID, expected_source_frame, expected_task,32'h10203040};
                if (output_seen != expect_outputs || !finish_ready ||
                    nms_frame_token !== start_frame_token)
                    mark_error(202);
                nms_cycle_enable = 1'b0;
            end
        end
    end

    always @(posedge i_clk) begin
        if (!i_rstn) begin
            held_metadata_valid <= 1'b0;
        end else begin
            if (table_error || dst_error)
                mark_error(310);
            if (nms_entry_valid && !publisher_entry_ready)
                entry_wait_cycles = entry_wait_cycles + 1;
            if (publisher_meta_valid && !(table_meta_ready && meta_enable))
                metadata_wait_cycles = metadata_wait_cycles + 1;
            if (held_metadata_valid && (!publisher_meta_valid || publisher_metadata !== held_metadata))
                mark_error(311);
            held_metadata_valid <= publisher_meta_valid && !(table_meta_ready && meta_enable);
            held_metadata <= publisher_metadata;
            if (publisher_meta_valid && meta_enable && table_meta_ready) begin
                if (publisher_entry_valid && entry_ready || publisher_metadata !== expected_metadata ||
                    output_seen != expect_outputs || nms_fault || c2_fault)
                    mark_error(312);
                meta_accept_cycle = cycle_count;
                meta_accept_time = $realtime;
                table_meta_seen = table_meta_seen + 1;
            end
            if (table_copy_ack) begin
                if (meta_accept_cycle < 0 || !dst_pending_valid)
                    mark_error(313);
                copy_ack_cycle = cycle_count;
                copy_ack_time = $realtime;
                table_ack_seen = table_ack_seen + 1;
            end
            if (publisher_busy && start_ready)
                mark_error(314);
            if (mode==19 && check_pending_source_hold && !table_copy_ack) begin
                if (!publisher_busy || !table_busy || start_ready || !table_cdc.flag_source_sealed ||
                    table_cdc.cnt_source_entry !== 7'd0 ||
                    table_cdc.reg_source_metadata !== expected_metadata ||
                    publisher_metadata !== expected_metadata)
                    mark_error(352);
            end
            if (mode==19 && check_pending_source_hold && table_copy_ack) begin
                if (expect_first_pending_active || active_seen!=1 || $realtime<=first_pending_active_time)
                    mark_error(353);
                check_pending_source_hold=1'b0;
            end
        end
    end

    always @(posedge dst_clk) begin
        if (!i_rstn) begin
            previous_active_metadata = 265'd0;
        end else begin
            if (dst_copy_busy && !dst_copy_enable)
                copy_wait_dst_cycles = copy_wait_dst_cycles + 1;
            #0.001;
            if (dst_update) begin
                if (mode==19 && expect_first_pending_active) begin
                    if (!dst_sof || first_pending_ack_time < 0 ||
                        dst_metadata !== first_pending_expected_metadata || dst_draw_valid || dst_entry!==97'd0)
                        mark_error(354);
                    first_pending_active_time=$realtime;
                    expect_first_pending_active=1'b0;
                    $display("PENDING_FIRST_ACTIVE task=%0d source=%0d active_ns=%0.3f metadata=%h",
                        dst_metadata[63:32],dst_metadata[95:64],$realtime,dst_metadata);
                end else begin
                    if (!dst_sof || copy_ack_time < 0 || dst_metadata !== expected_metadata)
                        mark_error(315);
                    active_time = $realtime;
                end
                active_seen = active_seen + 1;
                if (dst_metadata[95:64] != last_counted_source) begin
                    source_identity_results = source_identity_results + 1;
                    last_counted_source = dst_metadata[95:64];
                end
            end else if (dst_metadata !== previous_active_metadata) begin
                mark_error(316);
            end
            previous_active_metadata = dst_metadata;
        end
    end

    task run_metadata_hold;
        begin
            meta_enable = 1'b0;
            start_frame;
            send_cells(head_path,12096);
            wait_for_done;
            wait(publisher_meta_valid);
            repeat(512) @(negedge i_clk);
            if (table_meta_seen != 0 || table_ack_seen != 0 || dst_pending_valid || dst_active_valid)
                mark_error(320);
            meta_enable = 1'b1;
            wait_for_publication;
            print_metrics;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    task run_copy_hold_and_cancel;
        integer count_before;
        begin
            dst_copy_enable = 1'b0;
            start_frame;
            send_cells(head_path,12096);
            wait_for_done;
            wait(dst_copy_busy);
            @(negedge i_clk);
            common_cancel = 1'b1;
            repeat(512) @(negedge i_clk);
            if (publisher_abort || !publisher_busy || start_ready || copy_ack_cycle >= 0 ||
                dst_pending_valid || dst_active_valid || table_meta_seen != 1)
                mark_error(321);
            common_cancel = 1'b0;
            dst_copy_enable = 1'b1;
            wait_for_publication;
            print_metrics;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    task run_table_reset;
        begin
            if (mode == 17)
                dst_copy_enable = 1'b0;
            start_frame;
            send_cells(head_path,12096);
            if (mode == 16) begin
                wait(output_seen >= 2);
                if (!table_busy || publisher_meta_valid || dst_pending_valid || dst_active_valid)
                    mark_error(322);
            end else begin
                wait_for_done;
                wait(dst_copy_busy);
            end
            pulse_reset;
            if (table_busy || dst_copy_busy || dst_pending_valid || dst_active_valid || publisher_busy)
                mark_error(323);
            table_meta_seen = 0;
            table_ack_seen = 0;
            dst_copy_enable = 1'b1;
            run_complete(head_path);
        end
    endtask

    task run_held_metadata_reset;
        begin
            meta_enable=1'b0;
            start_frame;
            send_cells(head_path,12096);
            wait_for_done;
            wait(publisher_meta_valid);
            repeat(128) @(negedge i_clk);
            if(!publisher_busy || table_meta_seen!=0 || table_ack_seen!=0 ||
                dst_pending_valid || dst_active_valid)
                mark_error(350);
            pulse_reset;
            if(table_busy || publisher_busy || publisher_meta_valid || dst_pending_valid || dst_active_valid)
                mark_error(351);
            meta_enable=1'b1;
            run_complete(head_path);
        end
    endtask

    task run_pending_full_empty;
        integer watchdog;
        begin
            if(expect_outputs!=0) $fatal(1,"pending-full supplement requires complete empty fixture");
            start_frame;
            send_cells(head_path,12096);
            wait_for_done;
            watchdog=0;
            while(copy_ack_cycle<0 && watchdog<1000) begin
                @(negedge i_clk);watchdog=watchdog+1;
            end
            if(copy_ack_cycle<0 || !dst_pending_valid || dst_active_valid || publisher_busy)
                mark_error(355);
            first_pending_expected_metadata=expected_metadata;
            first_pending_ack_time=copy_ack_time;
            first_pending_active_time=-1;
            expect_first_pending_active=1'b1;
            $display("PENDING_FIRST_RESULT task=%0d source=%0d meta_ns=%0.3f ack_ns=%0.3f awaiting_sof=1 metadata=%h",
                expected_task,expected_source_frame,meta_accept_time,copy_ack_time,first_pending_expected_metadata);
            start_frame;
            send_cells(head_path,12096);
            wait_for_done;
            watchdog=0;
            while(meta_accept_cycle<0 && watchdog<1000) begin
                @(negedge i_clk);watchdog=watchdog+1;
            end
            if(meta_accept_cycle<0 || !dst_pending_valid || dst_active_valid ||
                copy_ack_cycle>=0 || !publisher_busy || table_meta_seen!=2 || table_ack_seen!=1)
                mark_error(356);
            check_pending_source_hold=1'b1;
            repeat(512) @(negedge i_clk);
            if(!check_pending_source_hold || !expect_first_pending_active || copy_ack_cycle>=0)
                mark_error(357);
            wait_for_publication;
            if(active_seen!=2 || source_identity_results!=2 || check_pending_source_hold ||
                dst_metadata[95:64]===first_pending_expected_metadata[95:64])
                mark_error(358);
            print_metrics;
            recovery_runs=recovery_runs+2;
            $display("PENDING_FULL_RESULT metadata=2 acks=2 active=2 unique_sources=2 first_active_ns=%0.3f second_ack_ns=%0.3f second_active_ns=%0.3f source_held_until_ack=1",
                first_pending_active_time,copy_ack_time,active_time);
        end
    endtask

    task check_age;
        input [63:0] age;
        input draw;
        begin
            #1;
            if (dst_age_upper_ms !== age || dst_draw_valid !== draw)
                mark_error(330);
        end
    endtask

    task run_age_controlled;
        integer old_results;
        begin
            controlled_time = 1'b1;
            controlled_src_now = 64'd1000;
            controlled_dst_now = 64'd1000;
            $display("TIME_BOUNDARY_GROUP controlled_coherent_time_not_FPS_evidence");
            run_complete(head_path);
            old_results = source_identity_results;
            controlled_dst_now = 64'd2996; check_age(64'd2000,1'b1);
            controlled_dst_now = 64'd2997; check_age(64'd2001,1'b0);
            controlled_time_valid = 1'b0; check_age(64'hffffffffffffffff,1'b0);
            controlled_time_valid = 1'b1;
            controlled_dst_now = 64'd2000; check_age(64'd1004,1'b1);
            if (source_identity_results != old_results)
                mark_error(331);
            controlled_src_now = 64'd2000;
            run_complete(head_path);
            if (source_identity_results != old_results+1)
                mark_error(332);
            controlled_dst_now = 64'd3000;
            controlled_src_now = 64'd3000;
            run_complete(head_path);
            if (source_identity_results != old_results+2)
                mark_error(333);
            $display("TIME_BOUNDARY_RESULT raw1996_allowed raw1997_rejected unknown_invalid retained_table_no_FPS_increment one_second_distinct_source_updates=%0d",source_identity_results-old_results);
        end
    endtask

    task run_real_time_loss;
        begin
            if (dst_age_upper_ms !== 64'hffffffffffffffff || dst_draw_valid)
                mark_error(340);
            run_complete(head_path);
            if (!real_dst_time_valid)
                mark_error(341);
            @(negedge i_clk); time_clock_enable = 1'b0;
            repeat(150010) @(negedge dst_clk);
            if (real_dst_time_valid || dst_draw_valid || dst_age_upper_ms !== 64'hffffffffffffffff)
                mark_error(342);
            $display("TIME_LOSS_RESULT real_snapshot_source_clock_stopped_dst_watchdog_expired");
        end
    endtask

    initial begin
        i_clk = 1'b0;
        i_rstn = 1'b0;
        fail_count = 0;
        cycle_count = 0;
        frame_number = 0;
        recovery_runs = 0;
        frame_monitor = 1'b0;
        nms_cycle_enable = 1'b0;
        rom_fault = 1'b0;
        rom_pending = 1'b0;
`ifndef USE_VENDOR_ROM
        rom_response_valid = 1'b0;
`endif
        hold_rom_response = 1'b0;
        hold_rom_request = 1'b0;
        hold_rom_word = 1'b0;
        drain_words = 0;
        budget_fail_count = 0;
        entry_ready = 1'b0;
        lfsr = 32'h7254a19d;
        hold_lut_request = 1'b0;
        hold_seal = 1'b0;
        hold_entry = 1'b0;
        clear_drives;
        if (!$value$plusargs("MODE=%d", mode) || !$value$plusargs("HEAD=%s", head_path) ||
            !$value$plusargs("EXPECTED=%s", expected_path) ||
            !$value$plusargs("EXPECT_PERSON=%d", expect_person) ||
            !$value$plusargs("EXPECT_VEHICLE=%d", expect_vehicle) ||
            !$value$plusargs("EXPECT_OUTPUTS=%d", expect_outputs) ||
            !$value$plusargs("PHYSICAL=%s", physical_path))
            $fatal(1, "missing joint plusargs");
        if (!$value$plusargs("STALL=%d", stall_mode)) stall_mode = 0;
        if (!$value$plusargs("MAX_CYCLES=%d", max_cycles)) max_cycles = 30000000;
        if (!$value$plusargs("SOF_PERIOD=%d", sof_period_cycles)) sof_period_cycles = 1237500;
        if (!$value$plusargs("HEAD2=%s", head2_path)) head2_path = head_path;
        if (!$value$plusargs("EXPECTED2=%s", expected2_path)) expected2_path = expected_path;
        if (!$value$plusargs("EXPECT2_PERSON=%d", expect2_person)) expect2_person = expect_person;
        if (!$value$plusargs("EXPECT2_VEHICLE=%d", expect2_vehicle)) expect2_vehicle = expect_vehicle;
        if (!$value$plusargs("EXPECT2_OUTPUTS=%d", expect2_outputs)) expect2_outputs = expect_outputs;
`ifndef USE_VENDOR_ROM
        $readmemh(physical_path, physical_words);
`endif
        load_expected(expected_path);
        reset_dut;
        if (mode == 0) begin
            run_complete(head_path);
        end else if (mode == 1) begin
            run_complete(head_path);
            expect_person = expect2_person;
            expect_vehicle = expect2_vehicle;
            expect_outputs = expect2_outputs;
            load_expected(expected2_path);
            run_complete(head2_path);
        end else if (mode >= 2 && mode <= 6) begin
            run_reset_case;
        end else if (mode == 7) begin
            run_late_error;
        end else if (mode == 8) begin
            run_long_output_stall;
        end else if (mode >= 9 && mode <= 11) begin
            run_owned_rom_boundary;
        end else if (mode == 12) begin
            run_copy_hold_and_cancel;
        end else if (mode == 13) begin
            run_age_controlled;
        end else if (mode == 14) begin
            run_real_time_loss;
        end else if (mode == 15) begin
            run_metadata_hold;
        end else if (mode == 16 || mode == 17) begin
            run_table_reset;
        end else if (mode == 18) begin
            run_held_metadata_reset;
        end else if (mode == 19) begin
            run_pending_full_empty;
        end else begin
            mark_error(901);
        end
        frame_monitor = 1'b0;
        if (fail_count != 0)
            $fatal(1, "TB_FAIL failures=%0d mode=%0d", fail_count, mode);
        if(mode!=1||dispatch_link.jobs!=2||dispatch_link.releases!=2||dispatch_error||dispatch_busy)
            $fatal(1,"dispatcher joint must complete exactly7thenempty with2jobs and2last-consume releases");
        $display("TB_PASS_DISPATCH_PUBLISH mode=%0d frames=%0d jobs=%0d releases=%0d metadata=%0d acks=%0d active=%0d unique_sources=%0d controlled_head_NN_visibility_lastread=1",mode,frame_number,dispatch_link.jobs,dispatch_link.releases,table_meta_seen,table_ack_seen,active_seen,source_identity_results);
        $finish;
    end

endmodule


