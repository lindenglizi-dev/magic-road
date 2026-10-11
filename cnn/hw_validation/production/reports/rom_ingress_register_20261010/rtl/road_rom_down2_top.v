`timescale 1ns / 1ps
// Fixed down2 ROM consumer. External narrow port supplies only the 9x9x16 halo.
module road_rom_down2_top(
    input i_clk,
    input i_rstn,
    input i_load_valid,
    input [10:0]i_load_addr,
    input signed [7:0]i_load_data,
    output o_load_ready,
    input i_start,
    input i_commit_ready,
    input i_export_start,
    input i_output_ready,
    output o_parameters_ready,
    output o_busy,
    output o_done,
    output o_fault,
    output o_output_valid,
    output signed [7:0]o_output_data,
    output [8:0]o_output_index,
    output o_export_done
);
    reg reg_release_meta, reg_release_done;
    reg flag_load_fault;
    // One registered parameter entry; external halo remains unbuffered.
    reg flag_pref_pending;
    reg [2:0]reg_pref_kind;
    reg [10:0]reg_pref_address;
    reg signed [31:0]reg_pref_data;
    // Ownership is granted only after the parameter entry has drained.
    reg flag_external_owner;
    wire domain_rstn;
    wire rom_request_valid, rom_request_ready, rom_response_valid, rom_response_ready, rom_fault;
    wire [12:0]rom_address;
    wire [159:0]rom_data;
    wire pref_load_valid, pref_table_valid, pref_done, pref_fault;
    wire [2:0]pref_load_kind;
    wire [10:0]pref_load_address;
    wire signed [31:0]pref_load_data;
    wire [9:0]pref_table_address;
    wire signed [15:0]pref_table_data;
    wire [31:0]pref_cycles;
    wire runner_load_ready, runner_table_ready, runner_table_loaded, runner_table_fault;
    wire runner_busy, runner_done, runner_fault, runner_output_valid, runner_export_done;
    wire signed [7:0]runner_output_data;
    wire [8:0]runner_output_index;
    wire [31:0]runner_core_cycles;
    wire [31:0]runner_export_cycles;
    wire runner_load_valid;
    wire [2:0]runner_load_kind;
    wire [10:0]runner_load_address;
    wire signed [31:0]runner_load_data;
    wire flag_external_open;
    wire flag_fault_any;
    wire pref_load_ready;
    wire flag_pref_capture, flag_pref_consume;
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) reg_release_meta<=1'b0;
        else reg_release_meta<=1'b1;
    end
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) reg_release_done<=1'b0;
        else reg_release_done<=reg_release_meta;
    end
    assign domain_rstn=i_rstn && reg_release_done;
    assign flag_fault_any=pref_fault || rom_fault || flag_load_fault || runner_fault || runner_table_fault;
    assign flag_external_open=domain_rstn && flag_external_owner && (~flag_fault_any);
    // No same-cycle replacement: a full entry cannot accept another word.
    assign pref_load_ready=domain_rstn && (~flag_external_owner) && (~flag_pref_pending) && (~flag_fault_any);
    assign flag_pref_capture=pref_load_valid && pref_load_ready;
    assign flag_pref_consume=flag_pref_pending && runner_load_ready &&
                             (~flag_external_owner) && (~flag_fault_any) && domain_rstn;
    assign runner_load_valid=flag_external_owner ?
                             (i_load_valid && flag_external_open && (i_load_addr < 11'd1296)) :
                             (flag_pref_pending && (~flag_fault_any) && domain_rstn);
    assign runner_load_kind=flag_external_owner ? 3'd0 : reg_pref_kind;
    assign runner_load_address=flag_external_owner ? i_load_addr : reg_pref_address;
    assign runner_load_data=flag_external_owner ? {{24{i_load_data[7]}}, i_load_data} : reg_pref_data;
    assign o_load_ready=flag_external_open && runner_load_ready && (i_load_addr < 11'd1296);
    assign o_parameters_ready=flag_external_open;
    assign o_busy=runner_busy && domain_rstn;
    assign o_done=runner_done && domain_rstn;
    assign o_fault=flag_fault_any && domain_rstn;
    assign o_output_valid=runner_output_valid && flag_external_open;
    assign o_output_data=runner_output_data;
    assign o_output_index=runner_output_index;
    assign o_export_done=runner_export_done && flag_external_open;
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) flag_load_fault<=1'b0;
        else if(flag_external_owner && i_load_valid && (i_load_addr >= 11'd1296)) flag_load_fault<=1'b1;
    end
    // Fault/reset cancel the queued word; a consumed word is never reissued.
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) flag_pref_pending<=1'b0;
        else if(flag_fault_any) flag_pref_pending<=1'b0;
        else if(flag_pref_consume) flag_pref_pending<=1'b0;
        else if(flag_pref_capture) flag_pref_pending<=1'b1;
    end
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) reg_pref_kind<=3'd0;
        else if(flag_pref_capture) reg_pref_kind<=pref_load_kind;
    end
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) reg_pref_address<=11'd0;
        else if(flag_pref_capture) reg_pref_address<=pref_load_address;
    end
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) reg_pref_data<=32'sd0;
        else if(flag_pref_capture) reg_pref_data<=pref_load_data;
    end
    // Use the pre-edge empty state: never hand over on the final consume edge.
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) flag_external_owner<=1'b0;
        else if(flag_fault_any) flag_external_owner<=1'b0;
        else if(pref_done && runner_table_loaded && (~flag_pref_pending)) flag_external_owner<=1'b1;
    end
    road_numeric_rom_reader road_numeric_rom_reader_Inst_parameters(
        .i_clk(i_clk), .i_rstn(domain_rstn), .i_request_valid(rom_request_valid),
        .i_request_addr(rom_address), .o_request_ready(rom_request_ready),
        .o_response_valid(rom_response_valid), .o_response_data(rom_data),
        .i_response_ready(rom_response_ready), .o_fault(rom_fault)
    );
    road_down2_parameter_prefetch road_down2_parameter_prefetch_Inst_parameters(
        .i_clk(i_clk), .i_rstn(domain_rstn), .o_rom_valid(rom_request_valid),
        .o_rom_addr(rom_address), .i_rom_ready(rom_request_ready),
        .i_rom_valid(rom_response_valid), .i_rom_data(rom_data), .o_rom_ready(rom_response_ready),
        .o_load_valid(pref_load_valid), .o_load_kind(pref_load_kind),
        .o_load_addr(pref_load_address), .o_load_data(pref_load_data), .i_load_ready(pref_load_ready),
        .o_table_valid(pref_table_valid), .o_table_addr(pref_table_address),
        .o_table_data(pref_table_data), .i_table_ready(runner_table_ready),
        .o_done(pref_done), .o_fault(pref_fault), .o_cycles(pref_cycles)
    );
    down2_dynamic_tile_runner down2_dynamic_tile_runner_Inst_compute(
        .i_clk(i_clk), .i_rstn(domain_rstn),
        .i_table_valid(pref_table_valid), .i_table_addr(pref_table_address), .i_table_data(pref_table_data),
        .o_table_ready(runner_table_ready), .o_table_loaded(runner_table_loaded), .o_table_fault(runner_table_fault),
        .i_load_valid(runner_load_valid), .i_load_kind(runner_load_kind),
        .i_load_addr(runner_load_address), .i_load_data(runner_load_data), .o_load_ready(runner_load_ready),
        .i_start(i_start && flag_external_open), .i_pw_only(1'b0),
        .i_commit_ready(i_commit_ready && flag_external_open),
        .o_busy(runner_busy), .o_done(runner_done), .o_fault(runner_fault),
        .i_export_start(i_export_start && flag_external_open), .i_output_ready(i_output_ready && flag_external_open),
        .o_output_valid(runner_output_valid), .o_output_data(runner_output_data),
        .o_output_index(runner_output_index), .o_export_done(runner_export_done),
        .o_core_cycles(runner_core_cycles), .o_export_cycles(runner_export_cycles),
        .o_debug_valid(),
        .o_debug_phase(),
        .o_debug_layer(),
        .o_debug_position(),
        .o_debug_channel(),
        .o_debug_value(),
        .o_preload_writes(),
        .o_mac_cycles(),
        .o_pre_cycles(),
        .o_silu_cycles(),
        .o_post_cycles(),
        .o_writeback_cycles(),
        .o_storage_wait_cycles(),
        .o_scheduler_idle_cycles(),
        .o_result_queue_count(),
        .o_result_reserved(),
        .o_meta_count(),
        .o_mac_result_count(),
        .o_pre_accept_count(),
        .o_silu_accept_count(),
        .o_post_accept_count(),
        .o_writeback_count()
    );
endmodule

