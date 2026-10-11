`timescale 1ns / 1ps
module tb_road_round_shift;
    reg i_clk = 0;
    reg i_rstn = 0;
    reg i_advance = 0;
    reg i_input_valid = 0;
    reg signed [63:0] i_product = 0;
    reg [5:0] i_shift = 0;
    reg [15:0] i_tag = 0;
    wire o_result_valid;
    wire [15:0] o_result_data;
    wire [15:0] o_result_tag;
    wire o_fault;
    reg [127:0] vectors [0:16383];
    reg [127:0] expected_pipe [0:8];
    reg [8:0] expected_valid = 0;
    reg [33:0] held_output;
    reg [63:0] held_quotient;
    reg [63:0] absolute_value;
    reg [127:0] stage_vector;
    integer case_count;
    integer index;
    integer cycle = 0;
    integer cursor = 0;
    integer checked = 0;
    integer stalled = 0;
    integer intermediate_checked = 0;
    integer fault_checked = 0;

    road_round_shift Round_Inst (
        .i_clk(i_clk), .i_rstn(i_rstn), .i_advance(i_advance),
        .i_input_valid(i_input_valid), .i_product(i_product),
        .i_shift(i_shift), .i_tag(i_tag), .o_result_valid(o_result_valid),
        .o_result_data(o_result_data), .o_result_tag(o_result_tag), .o_fault(o_fault)
    );
    always #5 i_clk = ~i_clk;
    initial begin
        #2000000;
        $display("FAIL timeout");
        $finish_and_return(1);
    end
    initial begin
        if (!$value$plusargs("COUNT=%d", case_count)) begin
            $display("FAIL missing COUNT");
            $finish_and_return(1);
        end
        if (case_count <= 0 || case_count > 16384) begin
            $display("FAIL invalid COUNT");
            $finish_and_return(1);
        end
        $readmemh("vectors.dath", vectors, 0, case_count - 1);
        for (index = 0; index < 9; index = index + 1) expected_pipe[index] = 0;

        // Reset cancels tokens already inside the pipeline, not just idle state.
        repeat (2) @(negedge i_clk);
        i_rstn = 1;
        i_advance = 1;
        i_input_valid = 1;
        i_product = 64'sd7;
        i_shift = 6'd1;
        i_tag = 16'hffff;
        repeat (4) @(negedge i_clk);
        i_rstn = 0;
        #1;
        if ({o_result_valid, o_result_data, o_result_tag, o_fault} !== 34'd0) begin
            $display("FAIL asynchronous reset");
            $finish_and_return(1);
        end
        i_input_valid = 0;
        @(negedge i_clk);
        i_rstn = 1;
        repeat (12) begin
            @(posedge i_clk);
            #1;
            if (o_result_valid !== 1'b0) begin
                $display("FAIL late result after reset");
                $finish_and_return(1);
            end
        end

        while (checked < case_count) begin
            @(negedge i_clk);
            cycle = cycle + 1;
            i_advance = ((cycle % 11) != 3) && ((cycle % 11) != 4);
            i_input_valid = (cursor < case_count) && ((cycle % 7) != 2);
            if (cursor < case_count) begin
                i_product = vectors[cursor][63:0];
                i_shift = vectors[cursor][69:64];
                i_tag = vectors[cursor][102:87];
            end
            held_output = {o_result_valid, o_result_data, o_result_tag, o_fault};
            held_quotient = Round_Inst.reg_quotient;
            @(posedge i_clk);
            if (i_advance) begin
                for (index = 8; index > 0; index = index - 1)
                    expected_pipe[index] = expected_pipe[index - 1];
                expected_pipe[0] = vectors[cursor < case_count ? cursor : 0];
                expected_valid = {expected_valid[7:0], i_input_valid};
                if (i_input_valid) cursor = cursor + 1;
            end
            #1;
            if (!i_advance) begin
                stalled = stalled + 1;
                if ({o_result_valid, o_result_data, o_result_tag, o_fault} !== held_output
                    || Round_Inst.reg_quotient !== held_quotient) begin
                    $display("FAIL stall changes payload or intermediate");
                    $finish_and_return(1);
                end
            end else begin
                if (o_result_valid !== expected_valid[8]) begin
                    $display("FAIL latency/bubble cycle=%0d", cycle);
                    $finish_and_return(1);
                end
                if (expected_valid[1]) begin
                    stage_vector = expected_pipe[1];
                    if (stage_vector[63]) absolute_value = -stage_vector[63:0];
                    else absolute_value = stage_vector[63:0];
                    if (Round_Inst.reg_quotient !== (absolute_value >> stage_vector[69:64])) begin
                        $display("FAIL quotient intermediate");
                        $finish_and_return(1);
                    end
                    intermediate_checked = intermediate_checked + 1;
                end
                if (expected_valid[2]) begin
                    stage_vector = expected_pipe[2];
                    if (stage_vector[63]) absolute_value = -stage_vector[63:0];
                    else absolute_value = stage_vector[63:0];
                    if (Round_Inst.reg_remainder !== (absolute_value & ~(64'hffffffffffffffff << stage_vector[69:64]))) begin
                        $display("FAIL remainder intermediate");
                        $finish_and_return(1);
                    end
                    intermediate_checked = intermediate_checked + 1;
                end
                if (o_result_valid) begin
                    if (o_result_tag !== expected_pipe[8][102:87]
                        || o_fault !== expected_pipe[8][86]) begin
                        $display("FAIL tag/fault cursor=%0d", checked);
                        $finish_and_return(1);
                    end
                    if (!o_fault && o_result_data !== expected_pipe[8][85:70]) begin
                        $display("FAIL rounding tag=%0d actual=%h expected=%h", o_result_tag,
                                 o_result_data, expected_pipe[8][85:70]);
                        $finish_and_return(1);
                    end
                    if (o_fault) fault_checked = fault_checked + 1;
                    checked = checked + 1;
                end
            end
        end
        if (cursor != case_count || stalled == 0 || fault_checked != 5
            || intermediate_checked != 2 * case_count) begin
            $display("FAIL insufficient coverage");
            $finish_and_return(1);
        end
        $display("PASS round cases=%0d intermediate=%0d stalls=%0d faults=%0d enabled_latency=8 II=1",
                 checked, intermediate_checked, stalled, fault_checked);
        $finish;
    end
endmodule
