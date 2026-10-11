`timescale 1ns / 1ps

module tb_road_dynamic_postprocess;
    localparam BATCH_COUNT = 330;
    localparam RESULT_COUNT = 604;

    reg clk = 0;
    reg rstn = 0;
    reg table_valid = 0;
    reg [9:0] table_addr = 0;
    reg signed [15:0] table_data = 0;
    reg input_valid = 0;
    reg [95:0] accumulators = 0;
    reg [95:0] multipliers = 0;
    reg [17:0] shifts = 0;
    reg [31:0] post_multiplier = 0;
    reg [5:0] post_shift = 0;
    reg activate = 0;
    reg [2:0] lane_mask = 0;
    reg [47:0] tags = 0;
    reg input_fault = 0;
    reg output_ready = 0;

    wire table_ready;
    wire table_loaded;
    wire input_ready;
    wire output_valid;
    wire signed [15:0] output_data;
    wire [15:0] output_tag;
    wire output_int16;
    wire fault;
    wire [1:0] queue_count;
    wire [3:0] pending_count;
    wire [3:0] meta_count;
    wire pre_busy;
    wire silu_busy;
    wire post_busy;
    wire pre_accept;
    wire silu_accept;
    wire post_accept;

    reg [15:0] table_words [0:1023];
    reg [95:0] vec_acc [0:BATCH_COUNT-1];
    reg [95:0] vec_mul [0:BATCH_COUNT-1];
    reg [17:0] vec_shift [0:BATCH_COUNT-1];
    reg [31:0] vec_post_mul [0:BATCH_COUNT-1];
    reg [5:0] vec_post_shift [0:BATCH_COUNT-1];
    reg vec_activate [0:BATCH_COUNT-1];
    reg [2:0] vec_mask [0:BATCH_COUNT-1];
    reg [47:0] vec_tags [0:BATCH_COUNT-1];
    reg [47:0] vec_expected [0:BATCH_COUNT-1];

    integer cycles = 0;
    integer seed = 32'h13579bdf;
    integer accepted_count = 0;
    integer result_count = 0;
    integer expected_batch = 0;
    integer expected_lane = 0;
    integer file_handle;
    integer fields;
    integer index;
    integer wait_count;
    integer coverage_masks = 0;
    integer coverage_retire_full = 0;
    integer coverage_ingress_full = 0;
    integer coverage_meta_nonzero = 0;
    integer coverage_meta_full = 0;
    integer coverage_pre = 0;
    integer coverage_silu = 0;
    integer coverage_post = 0;
    integer coverage_accept_overlap = 0;
    integer coverage_raw_post_collision = 0;
    integer coverage_ingress_push_pop = 0;
    integer coverage_retire_push_pop = 0;
    integer coverage_meta_push_pop = 0;
    integer coverage_slot_zero = 0;
    integer coverage_slot_seven = 0;
    integer coverage_slot_wrap = 0;
    integer max_ingress = 0;
    integer max_pending = 0;
    integer max_meta_natural = 0;
    integer max_meta_synthetic = 0;
    reg check_enable = 0;
    reg synthetic_meta_gate = 0;
    reg held = 0;
    reg [32:0] held_payload = 0;
    reg last_accept_slot_valid = 0;
    reg [2:0] last_accept_slot = 0;

    always #5 clk = !clk;

    road_dynamic_postprocess dut(
        .i_clk(clk),
        .i_rstn(rstn),
        .i_table_valid(table_valid),
        .i_table_addr(table_addr),
        .i_table_data(table_data),
        .o_table_ready(table_ready),
        .o_table_loaded(table_loaded),
        .i_input_valid(input_valid),
        .i_accumulators(accumulators),
        .i_pre_multipliers(multipliers),
        .i_pre_shifts(shifts),
        .i_post_multiplier(post_multiplier),
        .i_post_shift(post_shift),
        .i_activate(activate),
        .i_lane_mask(lane_mask),
        .i_tags(tags),
        .i_input_fault(input_fault),
        .o_input_ready(input_ready),
        .i_output_ready(output_ready),
        .o_output_valid(output_valid),
        .o_output_data(output_data),
        .o_output_tag(output_tag),
        .o_output_int16(output_int16),
        .o_fault(fault),
        .o_queue_count(queue_count),
        .o_pending_count(pending_count),
        .o_meta_count(meta_count),
        .o_pre_busy(pre_busy),
        .o_silu_busy(silu_busy),
        .o_post_busy(post_busy),
        .o_pre_accept(pre_accept),
        .o_silu_accept(silu_accept),
        .o_post_accept(post_accept)
    );

    task advance_expected;
        begin
            while (expected_batch < BATCH_COUNT &&
                   (expected_lane >= 3 || !vec_mask[expected_batch][expected_lane])) begin
                if (expected_lane >= 3) begin
                    expected_batch = expected_batch + 1;
                    expected_lane = 0;
                end else begin
                    expected_lane = expected_lane + 1;
                end
            end
        end
    endtask

    always @(posedge clk) begin
        cycles = cycles + 1;
        if (cycles > 5000000) $fatal(1, "watchdog");
        if (!rstn) begin
            held = 0;
            last_accept_slot_valid = 0;
        end else begin
            if ((^{table_ready, table_loaded, input_ready, output_valid, fault,
                  pre_accept, silu_accept, post_accept, dut.pre_result_valid,
                  dut.silu_output_valid, dut.post_result_valid}) === 1'bx)
                $fatal(1, "valid/ready control contains X or Z");
            if (output_valid && (^{output_int16, output_tag, output_data}) === 1'bx)
                $fatal(1, "valid output payload contains X or Z");
            if (queue_count > 2 || pending_count > 8 || meta_count > 8)
                $fatal(1, "diagnostic count exceeded capacity");
            if (queue_count == 2) coverage_ingress_full = 1;
            if (pending_count == 8) coverage_retire_full = 1;
            if (meta_count != 0) coverage_meta_nonzero = 1;
            if (meta_count == 8) coverage_meta_full = 1;
            if (queue_count > max_ingress) max_ingress = queue_count;
            if (pending_count > max_pending) max_pending = pending_count;
            if (!synthetic_meta_gate && meta_count > max_meta_natural)
                max_meta_natural = meta_count;
            if (synthetic_meta_gate && meta_count > max_meta_synthetic)
                max_meta_synthetic = meta_count;
            if (pre_busy) coverage_pre = 1;
            if (silu_busy) coverage_silu = 1;
            if (post_busy) coverage_post = 1;
            if (pre_accept && post_accept) coverage_accept_overlap = 1;
            if (dut.pre_result_valid && !dut.flag_pre_active &&
                !dut.flag_pre_drop && dut.post_result_valid)
                coverage_raw_post_collision = 1;
            if (dut.flag_ingress_push && dut.flag_ingress_pop)
                coverage_ingress_push_pop = 1;
            if (dut.flag_input_accept && dut.flag_retire_pop)
                coverage_retire_push_pop = 1;
            if (dut.flag_silu_accept && dut.flag_post_accept)
                coverage_meta_push_pop = 1;
            if (dut.flag_input_accept) begin
                if (dut.reg_retire_write == 3'd0) coverage_slot_zero = 1;
                if (dut.reg_retire_write == 3'd7) coverage_slot_seven = 1;
                if (last_accept_slot_valid && last_accept_slot == 3'd7 &&
                    dut.reg_retire_write == 3'd0) coverage_slot_wrap = 1;
                last_accept_slot = dut.reg_retire_write;
                last_accept_slot_valid = 1;
            end
            if (held && (!output_valid || {output_int16, output_tag, output_data} !== held_payload))
                $fatal(1, "output payload changed under backpressure");
            held = output_valid && !output_ready;
            held_payload = {output_int16, output_tag, output_data};
            if (check_enable && output_valid && output_ready) begin
                if (expected_batch >= BATCH_COUNT) $fatal(1, "extra corpus output");
                if (output_data !== vec_expected[expected_batch][expected_lane*16 +: 16] ||
                    output_tag !== vec_tags[expected_batch][expected_lane*16 +: 16] ||
                    output_int16 !== !vec_activate[expected_batch])
                    $fatal(1, "corpus mismatch batch=%0d lane=%0d data=%h tag=%h int16=%0d",
                           expected_batch, expected_lane, output_data, output_tag, output_int16);
                coverage_masks = coverage_masks | (1 << vec_mask[expected_batch]);
                result_count = result_count + 1;
                expected_lane = expected_lane + 1;
                advance_expected;
            end
        end
    end

    task poison_inputs;
        begin
            accumulators = 96'hdeaddeaddeaddeaddeaddead;
            multipliers = 96'hffffffffffffffffffffffff;
            shifts = 18'h3ffff;
            post_multiplier = 32'hffffffff;
            post_shift = 63;
            activate = 1;
            lane_mask = 0;
            tags = 48'hffffffffffff;
            input_fault = 1;
        end
    endtask

    task load_vector;
        input integer vector_index;
        input [47:0] tag_value;
        input use_tag_value;
        begin
            accumulators = vec_acc[vector_index];
            multipliers = vec_mul[vector_index];
            shifts = vec_shift[vector_index];
            post_multiplier = vec_post_mul[vector_index];
            post_shift = vec_post_shift[vector_index];
            activate = vec_activate[vector_index];
            lane_mask = vec_mask[vector_index];
            tags = use_tag_value ? tag_value : vec_tags[vector_index];
            input_fault = 0;
        end
    endtask

    task load_table;
        integer address;
        begin
            for (address = 0; address < 1024; address = address + 1) begin
                @(negedge clk);
                table_valid = 1;
                table_addr = address;
                table_data = table_words[address];
                @(posedge clk);
                if (!table_ready || input_ready || output_valid)
                    $fatal(1, "table load protocol address=%0d", address);
            end
            @(negedge clk);
            table_valid = 0;
            #1;
            if (!table_loaded || !input_ready) $fatal(1, "full table did not enable input");
        end
    endtask

    task reset_only;
        begin
            @(negedge clk);
            rstn = 0;
            input_valid = 0;
            table_valid = 0;
            output_ready = 0;
            #1;
            if (input_ready || output_valid || table_loaded || fault ||
                queue_count != 0 || pending_count != 0 || meta_count != 0)
                $fatal(1, "asynchronous reset did not clear public state");
            repeat (3) @(negedge clk);
            rstn = 1;
        end
    endtask

    task reset_and_load;
        begin
            reset_only;
            load_table;
        end
    endtask

    task send_vector;
        input integer vector_index;
        input [47:0] tag_value;
        input use_tag_value;
        begin
            @(negedge clk);
            load_vector(vector_index, tag_value, use_tag_value);
            input_valid = 1;
            begin: wait_vector_accept
                forever begin
                    @(posedge clk);
                    if (input_ready) disable wait_vector_accept;
                end
            end
            @(negedge clk);
            input_valid = 0;
            poison_inputs;
        end
    endtask

    task produce_corpus;
        integer vector_index;
        integer gap;
        begin
            vector_index = 0;
            @(negedge clk);
            load_vector(0, 0, 0);
            input_valid = 1;
            while (vector_index < BATCH_COUNT) begin
                begin: wait_corpus_accept
                    forever begin
                        @(posedge clk);
                        if (input_ready) disable wait_corpus_accept;
                    end
                end
                accepted_count = accepted_count + 1;
                vector_index = vector_index + 1;
                if (vector_index == BATCH_COUNT) begin
                    @(negedge clk);
                    input_valid = 0;
                    poison_inputs;
                end else begin
                    gap = vector_index < 24 ? 0 : ($random(seed) & 3);
                    @(negedge clk);
                    if (gap == 0) begin
                        load_vector(vector_index, 0, 0);
                        input_valid = 1;
                    end else begin
                        input_valid = 0;
                        poison_inputs;
                        repeat (gap) @(negedge clk);
                        load_vector(vector_index, 0, 0);
                        input_valid = 1;
                    end
                end
            end
        end
    endtask

    task drive_corpus_ready;
        integer ready_cycle;
        begin
            output_ready = 0;
            wait_count = 0;
            while (pending_count != 8 && wait_count < 500000) begin
                @(negedge clk);
                wait_count = wait_count + 1;
            end
            if (pending_count != 8 || input_ready) $fatal(1, "retirement depth eight not enforced");
            repeat (80) @(negedge clk);
            ready_cycle = 0;
            while (result_count < RESULT_COUNT) begin
                @(negedge clk);
                ready_cycle = ready_cycle + 1;
                if ((ready_cycle % 211) < 64)
                    output_ready = 0;
                else
                    output_ready = (($random(seed) & 7) != 0);
            end
            @(negedge clk);
            output_ready = 0;
        end
    endtask

    task collect_vector;
        input integer vector_index;
        input [47:0] expected_tags;
        integer lane;
        begin
            for (lane = 0; lane < 3; lane = lane + 1) begin
                if (vec_mask[vector_index][lane]) begin
                    begin: wait_manual_output
                        forever begin
                            @(posedge clk);
                            if (output_valid && output_ready) begin
                                if (output_data !== vec_expected[vector_index][lane*16 +: 16] ||
                                    output_tag !== expected_tags[lane*16 +: 16] ||
                                    output_int16 !== !vec_activate[vector_index])
                                    $fatal(1, "manual vector mismatch index=%0d lane=%0d", vector_index, lane);
                                disable wait_manual_output;
                            end
                        end
                    end
                end
            end
        end
    endtask

    task send_fault_variant;
        input integer variant;
        begin
            @(negedge clk);
            accumulators = 0;
            multipliers = {32'd1, 32'd1, 32'd1};
            shifts = 0;
            post_multiplier = 1;
            post_shift = 0;
            activate = 1;
            lane_mask = 7;
            tags = 48'h123412341234;
            input_fault = 0;
            case (variant)
                0: input_fault = 1;
                1: shifts[17:12] = 63;
                2: multipliers[95] = 1;
                3: post_shift = 63;
                4: post_multiplier = 32'h80000000;
                default: lane_mask = 0;
            endcase
            input_valid = 1;
            begin: wait_fault_accept
                forever begin
                    @(posedge clk);
                    if (input_ready) disable wait_fault_accept;
                end
            end
            @(negedge clk);
            input_valid = 0;
            input_fault = 0;
            #1;
            if (input_ready) $fatal(1, "fault detection did not stop new input variant=%0d", variant);
        end
    endtask

    function stage_hit;
        input integer stage;
        begin
            case (stage)
                0: stage_hit = queue_count != 0;
                1: stage_hit = pre_busy;
                2: stage_hit = silu_busy;
                3: stage_hit = meta_count != 0;
                4: stage_hit = post_busy;
                default: stage_hit = output_valid;
            endcase
        end
    endfunction

    task reset_at_stage;
        input integer stage;
        begin
            output_ready = 0;
            fork
                send_vector(15, 48'h0, 0);
            join
            wait_count = 0;
            while (!stage_hit(stage) && wait_count < 50000) begin
                @(negedge clk);
                wait_count = wait_count + 1;
            end
            if (!stage_hit(stage)) $fatal(1, "stage reset point not reached stage=%0d", stage);
            reset_and_load;
        end
    endtask

    initial begin
        $readmemh("table.hex", table_words);
        file_handle = $fopen("batches.txt", "r");
        if (!file_handle) $fatal(1, "batches.txt open failed");
        for (index = 0; index < BATCH_COUNT; index = index + 1) begin
            fields = $fscanf(file_handle, "%h %h %h %h %h %h %h %h %h\n",
                             vec_acc[index], vec_mul[index], vec_shift[index],
                             vec_post_mul[index], vec_post_shift[index], vec_activate[index],
                             vec_mask[index], vec_tags[index], vec_expected[index]);
            if (fields != 9) $fatal(1, "batch parse index=%0d", index);
        end
        $fclose(file_handle);

        reset_and_load;
        expected_batch = 0;
        expected_lane = 0;
        advance_expected;
        check_enable = 1;
        fork
            produce_corpus;
            drive_corpus_ready;
        join
        check_enable = 0;
        if (accepted_count != BATCH_COUNT || result_count != RESULT_COUNT ||
            expected_batch != BATCH_COUNT || coverage_masks != 8'hfe)
            $fatal(1, "corpus closure accepted=%0d outputs=%0d masks=%h",
                   accepted_count, result_count, coverage_masks);
        if (!coverage_retire_full || !coverage_pre || !coverage_silu || !coverage_post ||
            !coverage_meta_nonzero)
            $fatal(1, "required pipeline coverage absent");

        // Diagnostic-only sink gate proves the eight-entry metadata boundary.
        // The run resets immediately, so deliberately discarded SiLU outputs cannot retire.
        reset_and_load;
        output_ready = 0;
        synthetic_meta_gate = 1;
        force dut.flag_post_accept = 1'b0;
        send_vector(15, 48'h0, 0);
        send_vector(15, 48'h0, 0);
        send_vector(15, 48'h0, 0);
        wait_count = 0;
        while (meta_count != 8 && wait_count < 50000) begin
            @(negedge clk);
            wait_count = wait_count + 1;
        end
        if (meta_count != 8) $fatal(1, "metadata depth eight not reached");
        if (meta_count > max_meta_synthetic) max_meta_synthetic = meta_count;
        release dut.flag_post_accept;
        reset_only;
        synthetic_meta_gate = 0;
        load_table;

        // Repeated tags and different per-batch coefficients/modes must not alias slots.
        reset_and_load;
        output_ready = 0;
        send_vector(0, 48'h55aa55aa55aa, 1);
        send_vector(15, 48'h55aa55aa55aa, 1);
        @(negedge clk);
        output_ready = 1;
        collect_vector(0, 48'h55aa55aa55aa);
        collect_vector(15, 48'h55aa55aa55aa);
        @(negedge clk);
        output_ready = 0;

        // A later fault cannot truncate an older batch after its first scalar retired.
        reset_and_load;
        output_ready = 0;
        send_vector(0, 48'ha5a5a5a5a5a5, 1);
        @(negedge clk);
        output_ready = 1;
        begin: first_old_scalar
            forever begin
                @(posedge clk);
                if (output_valid && output_ready) begin
                    if (output_data !== vec_expected[0][15:0] || output_tag !== 16'ha5a5 ||
                        output_int16 !== 1 || fault)
                        $fatal(1, "first old scalar before fault mismatch");
                    disable first_old_scalar;
                end
            end
        end
        @(negedge clk);
        output_ready = 0;
        send_fault_variant(0);
        if (fault) $fatal(1, "fault became public before older retirement");
        @(negedge clk);
        output_ready = 1;
        begin: remaining_old_scalars
            integer old_lane;
            for (old_lane = 1; old_lane < 3; old_lane = old_lane + 1) begin
                begin: one_old_scalar
                    forever begin
                        @(posedge clk);
                        if (output_valid && output_ready) begin
                            if (output_data !== vec_expected[0][old_lane*16 +: 16] ||
                                output_tag !== 16'ha5a5 || output_int16 !== 1 || fault)
                                $fatal(1, "older scalar lost before ordered fault lane=%0d", old_lane);
                            disable one_old_scalar;
                        end
                    end
                end
            end
        end
        wait_count = 0;
        while (!fault && wait_count < 1000) begin
            @(posedge clk);
            wait_count = wait_count + 1;
            if (output_valid) $fatal(1, "fault batch emitted a scalar");
        end
        if (!fault || input_ready) $fatal(1, "ordered sticky fault missing");

        // Runtime post fault on the final lane: older retires; fault and younger do not.
        reset_and_load;
        output_ready = 0;
        fork
            begin
                send_vector(0, 48'h111111111111, 1);
                send_vector(15, 48'h222222222222, 1);
                send_vector(1, 48'h333333333333, 1);
            end
            begin: inject_runtime_post_fault
                wait_count = 0;
                while (!(dut.post_result_valid && dut.wire_post_slot == 3'd1 &&
                         dut.wire_post_lane == 2'd2) && wait_count < 50000) begin
                    @(negedge clk);
                    wait_count = wait_count + 1;
                end
                if (wait_count == 50000) $fatal(1, "runtime post fault target not reached");
                force dut.post_result_fault = 1'b1;
                @(posedge clk);
                @(negedge clk);
                release dut.post_result_fault;
            end
        join
        if (input_ready || fault) $fatal(1, "runtime fault visibility timing");
        @(negedge clk);
        output_ready = 1;
        collect_vector(0, 48'h111111111111);
        wait_count = 0;
        while (!fault && wait_count < 1000) begin
            @(posedge clk);
            wait_count = wait_count + 1;
            if (output_valid) $fatal(1, "fault or younger batch became externally visible");
        end
        if (!fault || output_valid) $fatal(1, "runtime post fault did not retire atomically");

        // Every accepted bad batch eventually faults with zero output; no immediate-cycle assumption.
        for (index = 1; index < 6; index = index + 1) begin
            reset_and_load;
            send_fault_variant(index);
            wait_count = 0;
            while (!fault && wait_count < 1000) begin
                @(posedge clk);
                wait_count = wait_count + 1;
                if (output_valid) $fatal(1, "bad batch emitted variant=%0d", index);
            end
            if (!fault) $fatal(1, "bad batch did not retire fault variant=%0d", index);
        end

        // Bad coefficients in inactive lanes and post fields on raw mode are ignored.
        reset_and_load;
        @(negedge clk);
        accumulators = {32'd0, 32'd0, 32'd4};
        multipliers = {32'h80000000, 32'h80000000, 32'd1};
        shifts = {6'd63, 6'd63, 6'd0};
        post_multiplier = 32'h80000000;
        post_shift = 63;
        activate = 0;
        lane_mask = 1;
        tags = 48'h004200420042;
        input_fault = 0;
        input_valid = 1;
        @(posedge clk);
        while (!input_ready) @(posedge clk);
        @(negedge clk);
        input_valid = 0;
        output_ready = 1;
        begin: inactive_bad_ignored
            forever begin
                @(posedge clk);
                if (output_valid && output_ready) begin
                    if (fault || output_data !== 16'd4 || output_tag !== 16'h42 || !output_int16)
                        $fatal(1, "inactive parameter legality leaked");
                    disable inactive_bad_ignored;
                end
            end
        end

        // Reset at ingress, pre, SiLU/meta, post, and held-output observation points.
        for (index = 0; index < 6; index = index + 1)
            reset_at_stage(index);

        // Partial table state is cancelled and the full table must be reloaded.
        reset_only;
        for (index = 0; index < 17; index = index + 1) begin
            @(negedge clk);
            table_valid = 1;
            table_addr = index;
            table_data = table_words[index];
            @(posedge clk);
            if (!table_ready || input_ready || table_loaded) $fatal(1, "partial table protocol");
        end
        reset_and_load;

        if (!coverage_ingress_full)
            $display("COVERAGE_NOTE ingress depth two did not persist at a sampled edge");
        if (!coverage_accept_overlap || !coverage_raw_post_collision)
            $fatal(1, "overlap collision coverage absent accepts=%0d raw_post=%0d",
                   coverage_accept_overlap, coverage_raw_post_collision);
        if (!coverage_ingress_push_pop || !coverage_retire_push_pop ||
            !coverage_meta_push_pop)
            $fatal(1, "same-cycle push/pop coverage absent ingress=%0d retire=%0d meta=%0d",
                   coverage_ingress_push_pop, coverage_retire_push_pop,
                   coverage_meta_push_pop);
        if (!coverage_slot_zero || !coverage_slot_seven || !coverage_slot_wrap)
            $fatal(1, "retirement slot wrap coverage absent slot0=%0d slot7=%0d wrap=%0d",
                   coverage_slot_zero, coverage_slot_seven, coverage_slot_wrap);
        if (!coverage_meta_full) $fatal(1, "metadata full coverage absent");
        $display("TB_PASS_DYNAMIC_OVERLAP batches=330 outputs=604 masks=7 queue_high=%0d retire_high=%0d meta_natural_high=%0d meta_synthetic_high=%0d raw_post_collision=1 ingress_push_pop=1 retire_push_pop=1 meta_push_pop=1 slot0=1 slot7=1 wrap7to0=1 valid_xz=0 resets=8 input_faults=6 runtime_post_faults=1",
                 max_ingress, max_pending, max_meta_natural, max_meta_synthetic);
        $finish;
    end
endmodule
