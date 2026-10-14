`timescale 1ns / 1ps

// 完整数值ROM接入冻结共享前端；本次仅启动其中down2两层。
module road_rom_current_down2_top(
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
    reg reg_release_meta;                      // 复位释放同步首级
    reg reg_release_done;                      // 第二有效沿后释放内部域
    reg flag_load_fault;                       // 非法halo地址粘滞故障
    reg flag_pref_pending;                     // 已保管但尚未提交的单项参数
    reg [2:0]reg_pref_kind;
    reg [10:0]reg_pref_address;
    reg signed [31:0]reg_pref_data;
    reg flag_external_owner;                   // 参数与整表排空后的图像输入许可
    wire domain_rstn;
    wire prefetch_rstn;
    wire selected_down2;
    wire select_ready;
    wire rom_request_valid, rom_request_ready, rom_response_valid, rom_response_ready, rom_fault;
    wire [12:0]rom_address;
    wire [159:0]rom_data;
    wire pref_load_valid, pref_load_ready, pref_table_valid, pref_table_ready, pref_done, pref_fault;
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
    wire runner_load_valid;
    wire [2:0]runner_load_kind;
    wire [10:0]runner_load_address;
    wire signed [31:0]runner_load_data;
    wire flag_fault;
    wire flag_external_open;
    wire flag_pref_push;
    wire flag_pref_pop;

    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) reg_release_meta <= 1'b0;
        else reg_release_meta <= 1'b1;
    end
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) reg_release_done <= 1'b0;
        else reg_release_done <= reg_release_meta;
    end
    assign domain_rstn = i_rstn && reg_release_done;
    // 预取只能在共享前端完成down2选择后运行，不把参数误送给Stem。
    assign prefetch_rstn = domain_rstn && selected_down2;
    assign flag_fault = pref_fault || rom_fault || runner_fault || runner_table_fault || flag_load_fault;
    assign flag_external_open = domain_rstn && flag_external_owner && !flag_fault;
    assign pref_load_ready = prefetch_rstn && !flag_external_owner && !flag_pref_pending && !flag_fault;
    assign pref_table_ready = prefetch_rstn && runner_table_ready && !flag_fault;
    assign flag_pref_push = pref_load_valid && pref_load_ready;
    assign flag_pref_pop = domain_rstn && flag_pref_pending && runner_load_ready && !flag_fault;
    // 来源选择由寄存的owner控制，pref_done不直接进入地址/数据大选择锥。
    assign runner_load_valid = flag_external_owner ?
        (i_load_valid && flag_external_open && i_load_addr < 11'd1296) :
        (flag_pref_pending && domain_rstn && !flag_fault);
    assign runner_load_kind = flag_external_owner ? 3'd0 : reg_pref_kind;
    assign runner_load_address = flag_external_owner ? i_load_addr : reg_pref_address;
    assign runner_load_data = flag_external_owner ? {{24{i_load_data[7]}}, i_load_data} : reg_pref_data;
    assign o_load_ready = flag_external_open && runner_load_ready && i_load_addr < 11'd1296;
    assign o_parameters_ready = flag_external_open;
    assign o_busy = runner_busy && domain_rstn;
    assign o_done = runner_done && domain_rstn;
    assign o_fault = flag_fault && domain_rstn;
    assign o_output_valid = runner_output_valid && flag_external_open;
    assign o_output_data = runner_output_data;
    assign o_output_index = runner_output_index;
    assign o_export_done = runner_export_done && flag_external_open;

    // 单项保管足以覆盖多周期预取源；满时拒收，反压保持全部负载。
    always @(posedge i_clk or negedge domain_rstn) begin
        if(!domain_rstn) begin
            flag_pref_pending <= 1'b0;
            reg_pref_kind <= 3'd0;
            reg_pref_address <= 11'd0;
            reg_pref_data <= 32'sd0;
            flag_external_owner <= 1'b0;
            flag_load_fault <= 1'b0;
        end else if(flag_fault) begin
            flag_pref_pending <= 1'b0;
            flag_external_owner <= 1'b0;
        end else begin
            if(flag_pref_push) begin
                flag_pref_pending <= 1'b1;
                reg_pref_kind <= pref_load_kind;
                reg_pref_address <= pref_load_address;
                reg_pref_data <= pref_load_data;
            end else if(flag_pref_pop) begin
                flag_pref_pending <= 1'b0;
            end
            if(pref_done && !flag_pref_pending && runner_table_loaded && selected_down2)
                flag_external_owner <= 1'b1;
            if(flag_external_open && i_load_valid && i_load_addr >= 11'd1296)
                flag_load_fault <= 1'b1;
        end
    end

    road_numeric_rom_reader u_rom(
        .i_clk(i_clk), .i_rstn(domain_rstn), .i_request_valid(rom_request_valid),
        .i_request_addr(rom_address), .o_request_ready(rom_request_ready),
        .o_response_valid(rom_response_valid), .o_response_data(rom_data),
        .i_response_ready(rom_response_ready), .o_fault(rom_fault)
    );
    road_down2_parameter_prefetch u_prefetch(
        .i_clk(i_clk), .i_rstn(prefetch_rstn), .o_rom_valid(rom_request_valid),
        .o_rom_addr(rom_address), .i_rom_ready(rom_request_ready),
        .i_rom_valid(rom_response_valid), .i_rom_data(rom_data), .o_rom_ready(rom_response_ready),
        .o_load_valid(pref_load_valid), .o_load_kind(pref_load_kind),
        .o_load_addr(pref_load_address), .o_load_data(pref_load_data), .i_load_ready(pref_load_ready),
        .o_table_valid(pref_table_valid), .o_table_addr(pref_table_address),
        .o_table_data(pref_table_data), .i_table_ready(pref_table_ready),
        .o_done(pref_done), .o_fault(pref_fault), .o_cycles(pref_cycles)
    );
    road_frontend_shared_core u_compute(
        .i_clk(i_clk), .i_rstn(domain_rstn),
        .i_select_valid(domain_rstn && !selected_down2 && !flag_fault), .i_select_down2(1'b1),
        .o_select_ready(select_ready), .o_selected_down2(selected_down2),
        .i_table_valid(pref_table_valid && prefetch_rstn && !flag_fault),
        .i_table_addr(pref_table_address), .i_table_data(pref_table_data),
        .o_table_ready(runner_table_ready), .o_table_loaded(runner_table_loaded), .o_table_fault(runner_table_fault),
        .i_load_valid(runner_load_valid), .i_load_kind(runner_load_kind),
        .i_load_addr(runner_load_address), .i_load_data(runner_load_data), .o_load_ready(runner_load_ready),
        .i_start(i_start && flag_external_open), .i_commit_ready(i_commit_ready && flag_external_open),
        .o_busy(runner_busy), .o_done(runner_done), .o_fault(runner_fault), .o_core_cycles(runner_core_cycles),
        .i_export_start(i_export_start && flag_external_open), .i_output_ready(i_output_ready && flag_external_open),
        .o_output_valid(runner_output_valid), .o_output_data(runner_output_data),
        .o_output_index(runner_output_index), .o_export_done(runner_export_done)
    );
endmodule
