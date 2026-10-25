`timescale 1ns / 1ps
// Full Python-golden trace: inputs and expected outputs are packed in spec port order.
module tb_road_result_publisher_trace;
    reg i_clk = 0;
    reg i_rstn = 0;
    reg i_cancel = 0;
    reg i_start_valid = 0;
    reg [31:0] i_start_epoch = 0;
    reg [31:0] i_start_task_id = 0;
    reg [31:0] i_start_source_frame_id = 0;
    reg [31:0] i_start_model_id = 0;
    reg [63:0] i_start_capture_ms = 0;
    reg [63:0] i_now_ms = 0;
    reg i_pipeline_start_ready = 0;
    reg i_entry_valid = 0;
    reg [96:0] i_entry = 0;
    reg [31:0] i_result_frame_token = 0;
    reg [6:0] i_result_count = 0;
    reg i_result_done = 0;
    reg i_pipeline_fault = 0;
    reg i_table_entry_ready = 0;
    reg i_table_meta_ready = 0;
    reg i_table_copy_ack = 0;
    reg i_table_busy = 0;
    reg i_table_error = 0;
    wire o_start_ready;
    wire o_pipeline_start_valid;
    wire [31:0] o_pipeline_frame_token;
    wire [31:0] o_pipeline_model_id;
    wire o_pipeline_cancel;
    wire o_entry_ready;
    wire o_table_entry_valid;
    wire [96:0] o_table_entry;
    wire o_table_meta_valid;
    wire [264:0] o_table_metadata;
    wire o_table_abort;
    wire o_busy;
    wire o_error;
    reg [849:0] vectors [0:499];
    reg [434:0] expected_outputs;
    reg [2:0] expected_state;
    reg [6:0] expected_count;
    reg new_case;
    reg [8191:0] vector_path;
    integer cycle_index;
    integer case_count;

    road_result_publisher dut (
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .i_cancel(i_cancel),
        .i_start_valid(i_start_valid),
        .i_start_epoch(i_start_epoch),
        .i_start_task_id(i_start_task_id),
        .i_start_source_frame_id(i_start_source_frame_id),
        .i_start_model_id(i_start_model_id),
        .i_start_capture_ms(i_start_capture_ms),
        .i_now_ms(i_now_ms),
        .i_pipeline_start_ready(i_pipeline_start_ready),
        .i_entry_valid(i_entry_valid),
        .i_entry(i_entry),
        .i_result_frame_token(i_result_frame_token),
        .i_result_count(i_result_count),
        .i_result_done(i_result_done),
        .i_pipeline_fault(i_pipeline_fault),
        .i_table_entry_ready(i_table_entry_ready),
        .i_table_meta_ready(i_table_meta_ready),
        .i_table_copy_ack(i_table_copy_ack),
        .i_table_busy(i_table_busy),
        .i_table_error(i_table_error),
        .o_start_ready(o_start_ready),
        .o_pipeline_start_valid(o_pipeline_start_valid),
        .o_pipeline_frame_token(o_pipeline_frame_token),
        .o_pipeline_model_id(o_pipeline_model_id),
        .o_pipeline_cancel(o_pipeline_cancel),
        .o_entry_ready(o_entry_ready),
        .o_table_entry_valid(o_table_entry_valid),
        .o_table_entry(o_table_entry),
        .o_table_meta_valid(o_table_meta_valid),
        .o_table_metadata(o_table_metadata),
        .o_table_abort(o_table_abort),
        .o_busy(o_busy),
        .o_error(o_error)
    );

    initial begin
        if (!$value$plusargs("vectors=%s", vector_path)) begin
            $display("TRACE_ERROR missing vectors plusarg");
            $finish;
        end
        $readmemh(vector_path, vectors);
        case_count = 0;
        for (cycle_index = 0; cycle_index < 500; cycle_index = cycle_index + 1) begin
            // Each label starts a new Python instance, so apply the shared reset first.
            if (vectors[cycle_index][849]) begin
                i_rstn = 0;
                #1;
                case_count = case_count + 1;
            end
            {new_case, i_rstn, i_cancel, i_start_valid, i_start_epoch, i_start_task_id, i_start_source_frame_id, i_start_model_id, i_start_capture_ms, i_now_ms, i_pipeline_start_ready, i_entry_valid, i_entry, i_result_frame_token, i_result_count, i_result_done, i_pipeline_fault, i_table_entry_ready, i_table_meta_ready, i_table_copy_ack, i_table_busy, i_table_error, expected_outputs, expected_state, expected_count} = vectors[cycle_index];
            #2;
            if ({o_start_ready, o_pipeline_start_valid, o_pipeline_frame_token, o_pipeline_model_id, o_pipeline_cancel, o_entry_ready, o_table_entry_valid, o_table_entry, o_table_meta_valid, o_table_metadata, o_table_abort, o_busy, o_error} !== expected_outputs) begin
                $display("TRACE_ERROR preedge cycle=%0d expected=%h actual=%h", cycle_index, expected_outputs, {o_start_ready, o_pipeline_start_valid, o_pipeline_frame_token, o_pipeline_model_id, o_pipeline_cancel, o_entry_ready, o_table_entry_valid, o_table_entry, o_table_meta_valid, o_table_metadata, o_table_abort, o_busy, o_error});
                $finish;
            end
            #3;
            i_clk = 1;
            #1;
            if ((dut.state_current !== expected_state) || (dut.cnt_entry !== expected_count)) begin
                $display("TRACE_ERROR postedge cycle=%0d expected_state=%0d actual_state=%0d expected_count=%0d actual_count=%0d", cycle_index, expected_state, dut.state_current, expected_count, dut.cnt_entry);
                $finish;
            end
            #4;
            i_clk = 0;
        end
        $display("TRACE_PASS cycles=500 cases=%0d preedge_outputs=13 postedge_state_count=2", case_count);
        $finish;
    end
endmodule

