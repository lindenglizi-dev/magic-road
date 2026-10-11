`timescale 1ns / 1ps

module tb_road_round_internal_probe;
    reg i_clk = 1'b0;
    reg i_rstn = 1'b0;
    wire o_result_valid;
    wire [15:0] o_result_data;
    wire [15:0] o_result_tag;
    wire o_result_fault;
    wire [63:0] o_checksum;
    wire o_error;
    wire [15:0] o_result_count;

    reg [127:0] vectors [0:191];
    reg [127:0] current_vector;
    reg [63:0] held_prbs;
    reg [63:0] held_product;
    reg [5:0] held_shift;
    reg [15:0] held_source_tag;
    reg held_source_valid;
    reg [7:0] held_core_valid;
    reg [127:0] held_core_tag;
    reg held_advance;
    reg [191:0] seen = 192'd0;
    integer generated = 0;
    integer checked = 0;
    integer stalls = 0;
    integer faults = 0;

    road_round_internal_probe Probe_Inst (
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .o_result_valid(o_result_valid),
        .o_result_data(o_result_data),
        .o_result_tag(o_result_tag),
        .o_result_fault(o_result_fault),
        .o_checksum(o_checksum),
        .o_error(o_error),
        .o_result_count(o_result_count)
    );

    always #5 i_clk = ~i_clk;

    initial begin
        #100000;
        $display("FAIL timeout");
        $finish_and_return(1);
    end

    initial begin
        $readmemh("vectors.dath", vectors, 0, 191);

        // Prove two-edge synchronous release before placing live tokens in flight.
        repeat (2) @(negedge i_clk);
        i_rstn = 1'b1;
        @(posedge i_clk);
        #1;
        if (Probe_Inst.road_round_reset_gen_Inst_release.reg_reset_meta !== 1'b1
            || Probe_Inst.road_round_reset_gen_Inst_release.reg_reset_release !== 1'b0) begin
            $display("FAIL reset release stage one");
            $finish_and_return(1);
        end
        @(posedge i_clk);
        #1;
        if (Probe_Inst.road_round_reset_gen_Inst_release.reg_reset_release !== 1'b1) begin
            $display("FAIL reset release stage two");
            $finish_and_return(1);
        end

        // Cancel an active pipeline asynchronously, then require a clean restart.
        while (Probe_Inst.road_round_internal_probe_core_Inst_datapath.road_round_shift_Inst_core.flag_valid_pipe == 8'd0) @(posedge i_clk);
        #2;
        i_rstn = 1'b0;
        #1;
        if (Probe_Inst.road_round_reset_gen_Inst_release.reg_reset_meta !== 1'b0
            || Probe_Inst.road_round_reset_gen_Inst_release.reg_reset_release !== 1'b0
            || Probe_Inst.road_round_internal_probe_core_Inst_datapath.road_round_shift_Inst_core.flag_valid_pipe !== 8'd0
            || {o_result_valid, o_result_data, o_result_tag, o_result_fault} !== 34'd0
            || o_checksum !== 64'd0 || o_result_count !== 16'd0) begin
            $display("FAIL asynchronous reset cancellation");
            $finish_and_return(1);
        end
        @(negedge i_clk);
        i_rstn = 1'b1;
        repeat (2) @(posedge i_clk);
        #1;
        if (Probe_Inst.road_round_reset_gen_Inst_release.reg_reset_release !== 1'b1) begin
            $display("FAIL reset restart release");
            $finish_and_return(1);
        end

        // Compare every generated payload and every registered result.
        while (o_result_count < 16'd168) begin
            @(negedge i_clk);
			held_advance = Probe_Inst.road_round_internal_probe_core_Inst_datapath.flag_advance;
            held_prbs = Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_prbs;
            held_product = Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_product_source;
            held_shift = Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_shift_source;
            held_source_tag = Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_tag_source;
            held_source_valid = Probe_Inst.road_round_internal_probe_core_Inst_datapath.flag_source_valid;
            held_core_valid = Probe_Inst.road_round_internal_probe_core_Inst_datapath.road_round_shift_Inst_core.flag_valid_pipe;
            held_core_tag = Probe_Inst.road_round_internal_probe_core_Inst_datapath.road_round_shift_Inst_core.reg_tag_pipe;
            @(posedge i_clk);
            #1;

            if (held_advance) begin
                if (generated < 192) begin
                    current_vector = vectors[generated];
                    if (Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_product_source !== current_vector[63:0]
                        || Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_shift_source !== current_vector[69:64]
                        || Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_tag_source !== current_vector[102:87]
                        || Probe_Inst.road_round_internal_probe_core_Inst_datapath.flag_source_valid !== current_vector[103]) begin
                        $display("FAIL source sequence generated=%0d", generated);
                        $finish_and_return(1);
                    end
                    generated = generated + 1;
                end
            end else begin
                stalls = stalls + 1;
                if (Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_prbs !== held_prbs
                    || Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_product_source !== held_product
                    || Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_shift_source !== held_shift
                    || Probe_Inst.road_round_internal_probe_core_Inst_datapath.reg_tag_source !== held_source_tag
                    || Probe_Inst.road_round_internal_probe_core_Inst_datapath.flag_source_valid !== held_source_valid
                    || Probe_Inst.road_round_internal_probe_core_Inst_datapath.road_round_shift_Inst_core.flag_valid_pipe !== held_core_valid
                    || Probe_Inst.road_round_internal_probe_core_Inst_datapath.road_round_shift_Inst_core.reg_tag_pipe !== held_core_tag) begin
                    $display("FAIL common stall changed source or core");
                    $finish_and_return(1);
                end
            end

            if (o_result_valid) begin
                if (o_result_tag >= 16'd192 || seen[o_result_tag]) begin
                    $display("FAIL duplicate or out-of-range tag=%0d", o_result_tag);
                    $finish_and_return(1);
                end
                current_vector = vectors[o_result_tag];
                if (!current_vector[103]
                    || o_result_fault !== current_vector[86]
                    || (!o_result_fault && o_result_data !== current_vector[85:70])) begin
                    $display("FAIL result tag=%0d data=%h fault=%b expected=%h/%b",
                             o_result_tag, o_result_data, o_result_fault,
                             current_vector[85:70], current_vector[86]);
                    $finish_and_return(1);
                end
                seen[o_result_tag] = 1'b1;
                checked = checked + 1;
                if (o_result_fault) faults = faults + 1;
            end
        end

        if (generated != 192 || checked != 168 || stalls == 0 || faults != 3
            || o_checksum !== 64'h0000000100001486 || o_error !== 1'b0) begin
            $display("FAIL final generated=%0d checked=%0d stalls=%0d faults=%0d checksum=%h error=%b",
                     generated, checked, stalls, faults, o_checksum, o_error);
            $finish_and_return(1);
        end
        $display("PASS probe generated=%0d results=%0d stalls=%0d faults=%0d checksum=%h",
                 generated, checked, stalls, faults, o_checksum);
        $finish;
    end
endmodule
