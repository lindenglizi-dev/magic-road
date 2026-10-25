`timescale 1ns / 1ps

module tb_road_box_overlay_joint;
    // Geometry injections enter the actual publisher; real mode enters HEAD112.
    reg inject_mode = 0, inject_valid = 0, inject_done = 0;
    reg [96:0] inject_entry = 0;
    reg [6:0] inject_count = 0;
    reg video_vs=0, video_hs=0, video_de=0;
    reg [23:0] video_rgb=24'h123456;
    wire out_vs,out_hs,out_de,line_ready,prepare_busy,renderer_fault;
    wire [23:0] out_rgb;
    wire [8:0] prepare_cycles;
    integer raster=-1, position, horizontal, vertical;
    integer capture_pixels=0, output_handle=0, rom_requests=0;
    integer max_prepare=0, source_cycles=0, real_start_cycle=0;
    reg capture_arm=0,capturing=0,capture_done=0;
    reg [2:0] expected_sync=0, previous_sync=0;
    reg [264:0] previous_metadata=0;
    reg [4095:0] boxes_path,rgb_path;
    integer inject_delay, index, watchdog, withdraw_pixel=-1;
    integer age_value=123;
    reg [63:0] requested_age=123;
    integer fault_expected=0;
    reg [31:0] random_seed=32'h6715ae31;
    reg [96:0] inject_words[0:63];
    integer poison_index;
    integer withdraw_invalid=0;

    localparam [31:0] MODEL_ID = 32'hB35D4A66;
    localparam [2:0] PHASE_FREE = 3'd0;
    localparam [2:0] PHASE_SCAN = 3'd1;
    localparam [2:0] PHASE_SORT = 3'd2;
    localparam [2:0] PHASE_DECODE = 3'd3;
    localparam [2:0] PHASE_NMS = 3'd4;

    reg i_clk;
    reg i_rstn;
    reg common_cancel;
    reg start_valid;
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
    wire [5:0] dst_read_index;
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
        .i_start_valid(pipeline_start_valid && !inject_mode), .i_start_frame_token(pipeline_frame_token),
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
    assign source_now_ms = controlled_time ? controlled_src_now : real_src_now_ms;
    assign destination_now_ms = controlled_time ? controlled_dst_now : real_dst_now_ms;
    assign destination_epoch = controlled_time ? 32'h10203040 : real_dst_epoch;
    assign destination_time_valid = controlled_time ? controlled_time_valid : real_dst_time_valid;

    road_result_publisher publisher(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(common_cancel),
        .i_start_valid(start_valid), .i_start_epoch(context_epoch),
        .i_start_task_id(context_task), .i_start_source_frame_id(context_source_frame),
        .i_start_model_id(start_model_id), .i_start_capture_ms(context_capture_ms),
        .i_now_ms(source_now_ms), .i_pipeline_start_ready(inject_mode || c2_start_ready),
        .i_entry_valid(inject_mode ? inject_valid : nms_entry_valid), .i_entry(inject_mode ? inject_entry : nms_entry_data),
        .i_result_frame_token(inject_mode ? start_frame_token : nms_frame_token), .i_result_count(inject_mode ? inject_count : nms_output_count),
        .i_result_done(inject_mode ? inject_done : nms_done),
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



    road_box_age_overlay overlay(
        .i_clk(dst_clk),.i_rstn(i_rstn),.i_sof(dst_sof),
        .i_vsync(video_vs),.i_hsync(video_hs),.i_de(video_de),.i_rgb(video_rgb),
        .i_table_active_valid(dst_active_valid),.i_table_count(dst_metadata[134:128]),
        .i_table_entry(dst_entry),.i_table_draw_valid(dst_draw_valid),
        .i_age_upper_ms(inject_mode ? requested_age : dst_age_upper_ms),.o_table_read_index(dst_read_index),
        .o_vsync(out_vs),.o_hsync(out_hs),.o_de(out_de),.o_rgb(out_rgb),
        .o_line_ready(line_ready),.o_prepare_busy(prepare_busy),
        .o_last_prepare_cycles(prepare_cycles),.o_fault(renderer_fault)
    );

    // Exact1650x750 mixer-output-equivalent raster. SOF is consumed in blank,
    //39970pixel periods before DE; this bench does not instantiate official VTC.
    always @(negedge dst_clk) begin
        if (!i_rstn) begin
            raster=-1;dst_sof=0;video_vs=0;video_hs=0;video_de=0;
        end else begin
            raster=(raster==1237499)?0:raster+1;
            dst_sof=(raster==0);
            if(dst_sof) begin
                for(poison_index=0;poison_index<1280;poison_index=poison_index+1)
                    overlay.BoxLine_Inst.PH1P_LOGIC_DRAM_Inst_line_events.memory[poison_index]=$random;
            end
            video_vs=(raster<8250);
            position=raster-39970;
            horizontal=(position>=0)?position%1650:0;
            vertical=(position>=0)?position/1650:0;
            video_de=(position>=0 && vertical<720 && horizontal<1280);
            video_hs=(horizontal>=1390 && horizontal<1430);
            if(capture_arm && dst_sof) begin
                capturing=1;capture_arm=0;capture_pixels=0;
            end
        end
    end

    always @(posedge i_clk) begin
        source_cycles=source_cycles+1;
        if(i_rstn && rom_request_valid && rom_request_ready) rom_requests=rom_requests+1;
        if(i_rstn && !inject_mode && nms_entry_valid && publisher_entry_ready) begin
            if(output_seen>=7 || nms_entry_data!==expected_words[output_seen])
                $fatal(1,"REAL_FINAL97_MISMATCH index=%0d got=%h",output_seen,nms_entry_data);
            output_seen=output_seen+1;
        end
        if(i_rstn && (publisher_fault||table_error||c2_fault||nms_fault||service_fault||vendor_rom_fault))
            $fatal(1,"PIPELINE_FAULT");
    end

    always @(posedge dst_clk) begin
        if(!i_rstn) begin expected_sync=0;previous_sync=0;previous_metadata=0;end
        else begin
            if(overlay.BoxLine_Inst.reg_map_write_enable &&
               overlay.BoxLine_Inst.reg_map_read_address===overlay.BoxLine_Inst.reg_map_write_address)
                $fatal(1,"NATIVE_MAP_READ_WRITE_COLLISION");
            if(capturing && raster==2)
                $display("FRAME_AGE_INPUT age=%0d actual_time=%0d time_valid=%0d injection=%0d",dst_age_upper_ms,destination_now_ms,destination_time_valid,inject_mode);
            expected_sync=previous_sync;
            previous_sync={video_vs,video_hs,video_de};
            if(!dst_sof && dst_metadata!==previous_metadata) $fatal(1,"TABLE_CHANGED_WITHOUT_SOF");
            #0.001;
            if({out_vs,out_hs,out_de}!==expected_sync)
                $fatal(1,"SYNC_NOT_TWO_REGISTERS raster=%0d got=%b expected=%b",raster,{out_vs,out_hs,out_de},expected_sync);
            if(dst_error) $fatal(1,"DST_TABLE_FAULT");
            if(renderer_fault && !fault_expected) $fatal(1,"RENDERER_FAULT raster=%0d",raster);
            if(prepare_cycles>max_prepare) max_prepare=prepare_cycles;
            if(prepare_cycles>330) $fatal(1,"PREP_BUDGET cycles=%0d",prepare_cycles);
            previous_metadata=dst_metadata;
            if(capturing && out_de) begin
                $fwrite(output_handle,"%c%c%c",out_rgb[23:16],out_rgb[15:8],out_rgb[7:0]);
                capture_pixels=capture_pixels+1;
                if(capture_pixels==921600) begin
                    capturing=0;capture_done=1;$fclose(output_handle);
                end
            end
        end
    end

    task begin_result;
        begin
            @(negedge i_clk);
            start_frame_token=start_frame_token+1;
            context_task=start_frame_token;context_source_frame=start_frame_token;
            context_epoch=32'h10203040;context_capture_ms=source_now_ms;start_model_id=MODEL_ID;
            start_valid=1;
            @(posedge i_clk);
            while(!start_ready) @(posedge i_clk);
            @(negedge i_clk);start_valid=0;
        end
    endtask

    task send_real_heads;
        begin
            head_handle=$fopen(head_path,"r");
            if(!head_handle) $fatal(1,"HEAD_OPEN");
            for(index=0;index<12096;index=index+1) begin
                scan_result=$fscanf(head_handle,"%h\n",streamed_head);
                if(scan_result!=1) $fatal(1,"HEAD_LENGTH");
                @(negedge i_clk);cell_id=index;cell_frame_token=start_frame_token;
                cell_data=streamed_head;cell_valid=1;
                @(posedge i_clk);while(!cell_ready) @(posedge i_clk);
                @(negedge i_clk);cell_valid=0;
            end
            $fclose(head_handle);
            wait(nms_done);
            if(output_seen!=7 || nms_output_count!=7 || rom_requests==0)
                $fatal(1,"REAL_PIPELINE_NOT_SEVEN");
            $display("REAL_HEAD_ROM_NMS_PASS heads=12096 results=7 rom_requests=%0d source_cycles=%0d",
                     rom_requests,source_cycles-real_start_cycle);
        end
    endtask

    initial begin
        i_clk=0;i_rstn=0;common_cancel=0;start_valid=0;start_frame_token=32'h92000000;
        start_model_id=MODEL_ID;cell_valid=0;cell_data=0;cell_id=0;cell_frame_token=0;
        entry_ready=1;stall_mode=0;hold_rom_response=0;rom_fault=0;
        lfsr=32'h7254a19d;late_error_arm=0;late_error_used=0;output_seen=0;
        controlled_time=1;controlled_src_now=1000;controlled_dst_now=1119;
        if(!$value$plusargs("BOXES=%s",boxes_path) || !$value$plusargs("RGB=%s",rgb_path) ||
           !$value$plusargs("COUNT=%d",expect_outputs) || !$value$plusargs("MODE=%d",mode))
            $fatal(1,"MISSING_ARGS");
        if(!$value$plusargs("AGE=%d",requested_age)) requested_age=123;
        if(!$value$plusargs("WITHDRAW=%d",withdraw_pixel)) withdraw_pixel=-1;
        if(!$value$plusargs("INVALID_WITHDRAW=%d",withdraw_invalid)) withdraw_invalid=0;
        if(!$value$plusargs("HEAD=%s",head_path)) head_path=0;
        inject_mode=(mode!=0);
        controlled_time=inject_mode;
        inject_count=expect_outputs;
        if(expect_outputs>0) $readmemh(boxes_path,inject_words,0,expect_outputs-1);
        if(!inject_mode) $readmemh(boxes_path,expected_words,0,6);
        repeat(10) @(negedge i_clk);
        i_rstn=1;repeat(10) @(negedge i_clk);
        begin_result;
        real_start_cycle=source_cycles;
        if(!inject_mode) send_real_heads;
        else begin
            for(index=0;index<expect_outputs;index=index+1) begin
                random_seed={random_seed[30:0],random_seed[31]^random_seed[21]^random_seed[1]^random_seed[0]};
                inject_delay=random_seed[2:0];
                repeat(inject_delay) @(negedge i_clk);
                inject_entry=inject_words[index];inject_valid=1;
                @(posedge i_clk);while(!publisher_entry_ready) @(posedge i_clk);
                @(negedge i_clk);inject_valid=0;
            end
            inject_done=1;@(negedge i_clk);inject_done=0;
        end
        wait(table_copy_ack);wait(dst_pending_valid);
        // Known finite age may expire while its table remains active.
        controlled_dst_now=2996;
        if(requested_age==2001) controlled_dst_now=2997;
        if(requested_age==64'hffffffffffffffff) controlled_time_valid=0;
        output_handle=$fopen(rgb_path,"wb");
        if(!output_handle) $fatal(1,"RGB_OPEN");
        capture_arm=1;
        wait(dst_update);@(negedge dst_clk);
        if(dst_metadata[134:128]!==expect_outputs[6:0]) $fatal(1,"TABLE_COUNT");
        if(inject_mode) begin
            controlled_dst_now=2996;controlled_time_valid=1;#1;
            if(dst_age_upper_ms!==2000 || dst_draw_valid!==(expect_outputs!=0)) $fatal(1,"RAW1996_BOUNDARY");
            controlled_dst_now=2997;#1;
            if(dst_age_upper_ms!==2001 || dst_draw_valid) $fatal(1,"RAW1997_BOUNDARY");
            controlled_time_valid=0;#1;
            if(dst_age_upper_ms!==64'hffffffffffffffff || dst_draw_valid) $fatal(1,"INVALID_TIME_BOUNDARY");
            controlled_time_valid=(requested_age!=64'hffffffffffffffff);
            controlled_dst_now=(requested_age==2001)?2997:2996;
            $display("TABLE_AGE_BOUNDARY_PASS raw1996_allow raw1997_reject unknown_invalid");
        end
        if(withdraw_pixel>=0) begin
            wait(capturing && video_de && vertical*1280+horizontal==withdraw_pixel);
            @(negedge dst_clk);
            if(withdraw_invalid) controlled_time_valid=0;
            else controlled_dst_now=2997;
        end
        wait(capture_done);
        if(max_prepare>330) $fatal(1,"FINAL_PREP_BUDGET");
        $display("TB_PASS_BOX_OVERLAY_JOINT mode=%0d count=%0d pixels=%0d max_prepare=%0d exact_two_video_registers=1",
                 mode,expect_outputs,capture_pixels,max_prepare);
        $finish;
    end
    initial begin #150000000; $fatal(1,"GLOBAL_TIMEOUT"); end
endmodule

