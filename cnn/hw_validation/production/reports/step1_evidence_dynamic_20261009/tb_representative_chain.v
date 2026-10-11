`timescale 1ns / 1ps

// Verify frozen MAC and dynamic postprocess connected through their original interfaces.
module tb_representative_chain();
    reg clk = 0;
    reg rstn = 0;
    reg valid = 0;
    reg first = 0;
    reg last = 0;
    reg [7:0] mask = 0;
    reg [63:0] activations = 0;
    reg [191:0] weights = 0;
    reg [95:0] bias = 0;
    reg [95:0] pre_mul = 0;
    reg [17:0] pre_shift = 0;
    reg [31:0] post_mul = 0;
    reg [5:0] post_shift = 0;
    reg activate = 0;
    reg [2:0] output_mask = 0;
    reg [47:0] tags = 0;
    reg table_valid = 0;
    reg [9:0] table_addr = 0;
    reg [15:0] table_data = 0;
    reg output_ready = 0;
    wire input_ready, mac_valid, mac_fault, pp_ready;
    wire [95:0] mac_data;
    wire result_valid, result_mode, fault, table_ready, table_loaded;
    wire [15:0] result_data, result_tag;
    reg [15:0] table_words [0:1023];
    reg [95:0] expected_mac;
    reg [47:0] expected_output;
    reg [4095:0] path;
    reg [32:0] held_payload;
    reg held = 0;
    integer fd, fields, groups, group_index, lane, table_index;
    integer cycle = 0, tasks = 0, results = 0, mac_results = 0;
    integer start_cycle, mac_end;

    always #5 clk = !clk;
    road_mac_probe u_mac(
        .i_clk(clk), .i_rstn(rstn), .i_input_valid(valid), .i_first(first), .i_last(last),
        .i_lane_mask(mask), .i_activation_data(activations), .i_weight_data(weights),
        .i_bias_data(bias), .i_result_ready(pp_ready), .o_input_ready(input_ready),
        .o_result_valid(mac_valid), .o_result_data(mac_data), .o_fault(mac_fault)
    );
    road_dynamic_postprocess u_post(
        .i_clk(clk), .i_rstn(rstn), .i_table_valid(table_valid), .i_table_addr(table_addr),
        .i_table_data(table_data), .o_table_ready(table_ready), .o_table_loaded(table_loaded),
        .i_input_valid(mac_valid), .o_input_ready(pp_ready), .i_accumulators(mac_data),
        .i_pre_multipliers(pre_mul), .i_pre_shifts(pre_shift), .i_post_multiplier(post_mul),
        .i_post_shift(post_shift), .i_activate(activate), .i_lane_mask(output_mask),
        .i_tags(tags), .i_input_fault(mac_fault), .i_output_ready(output_ready),
        .o_output_valid(result_valid), .o_output_data(result_data), .o_output_tag(result_tag),
        .o_output_int16(result_mode), .o_fault(fault), .o_queue_count(), .o_pending_count(),
        .o_meta_count(), .o_pre_busy(), .o_silu_busy(), .o_post_busy(),
        .o_pre_accept(), .o_silu_accept(), .o_post_accept()
    );
    always @(posedge clk) begin
        cycle = cycle + 1;
        if (cycle > 200000) $fatal(1, "representative watchdog");
        if (rstn && fault) $fatal(1, "unexpected operator fault");
        if (rstn && mac_valid && pp_ready) begin
            if (mac_fault || mac_data !== expected_mac) $fatal(1, "MAC mismatch task=%0d", tasks);
            mac_results = mac_results + 1;
            mac_end = cycle;
        end
        if (rstn && held && (!result_valid || {result_mode,result_tag,result_data} !== held_payload))
            $fatal(1, "result changed under stall");
        held = rstn && result_valid && !output_ready;
        if (held) held_payload = {result_mode,result_tag,result_data};
    end
    initial begin
        if (!$value$plusargs("VECTORS=%s", path)) $fatal(1, "missing vectors");
        $readmemh({path,"/table.hex"}, table_words);
        fd = $fopen({path,"/representative.txt"}, "r");
        if (!fd) $fatal(1, "cannot open representative vectors");
        repeat (10) @(negedge clk);
        rstn = 1;
        for (table_index = 0; table_index < 1024; table_index = table_index + 1) begin
            @(negedge clk);
            table_valid = 1; table_addr = table_index; table_data = table_words[table_index];
            @(posedge clk);
            while (!table_ready) @(posedge clk);
        end
        @(negedge clk); table_valid = 0;
        if (!table_loaded) $fatal(1, "table not loaded");
        while (!$feof(fd)) begin
            fields = $fscanf(fd, "%h %h %h %h %h %h %h %h %h %h\n", groups,
                expected_mac, expected_output, pre_mul, pre_shift, post_mul, post_shift,
                activate, output_mask, tags);
            if (fields != 10 || groups < 1 || groups > 24) $fatal(1, "bad descriptor");
            start_cycle = cycle;
            for (group_index = 0; group_index < groups; group_index = group_index + 1) begin
                @(negedge clk);
                fields = $fscanf(fd, "%h %h %h %h\n", activations, weights, mask, bias);
                if (fields != 4) $fatal(1, "bad group");
                first = group_index == 0; last = group_index == groups-1;
                valid = 1;
                @(posedge clk);
                while (!input_ready) @(posedge clk);
                @(negedge clk); valid = 0;
            end
            for (lane = 0; lane < 3; lane = lane + 1) begin
                if (output_mask[lane]) begin
                    while (!result_valid) @(negedge clk);
                    repeat (tasks % 5) @(negedge clk);
                    output_ready = 1;
                    @(posedge clk);
                    if (!result_valid || result_data !== expected_output[lane*16+:16] ||
                        result_tag !== tags[lane*16+:16] || result_mode !== !activate)
                        $fatal(1, "post mismatch task=%0d lane=%0d", tasks, lane);
                    results = results + 1;
                    @(negedge clk); output_ready = 0;
                end
            end
            $display("REP_TASK %0d %0d %0d %0d", tasks, groups, mac_end-start_cycle, cycle-start_cycle);
            tasks = tasks + 1;
        end
        $fclose(fd);
        if (tasks != 1040 || results != 2544 || mac_results != tasks)
            $fatal(1, "coverage mismatch tasks=%0d results=%0d mac=%0d", tasks, results, mac_results);
        $display("TB_PASS_REPRESENTATIVE tasks=%0d outputs=%0d", tasks, results);
        $finish;
    end
endmodule
