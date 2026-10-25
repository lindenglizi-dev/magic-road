"""Reuse the board-proven clock/DDR/HDMI shell, replace only its diagnostic."""
from pathlib import Path
import run


def generate():
    source=(run.PREVIOUS/'rtl/road_ddr_selftest_top.v').read_text(encoding='utf-8')
    header=source[:source.index('    //-------------模块实例化信号')]
    header=header.replace('road_ddr_selftest_top','road_stem_ddr_board_top')
    header=header.replace('无摄像头、CNN、Flash控制或其他DDR客户','一次性Stem、DDR和down2共享计算，无其他DDR客户')
    data_wires=source[source.index('    wire clk_ref;'):source.index('    wire [1:0] status;')]
    display_wires=source[source.index('    wire vtc_vs;'):source.index('    //---------------寄存器信号')]
    resets=source[source.index('    // 各域分别异步'):source.index('    //----------------模块实例化')]
    pll_ddr=source[source.index('    PLL u_PLL ('):source.index('    road_ddr_selftest road_ddr_selftest_Inst')]
    display=source[source.index('    uivtc #('):]
    display=display.replace('.i_clk(dhi_clk), .i_rstn(reg_user_release), .i_payload(payload)',
                            '.i_clk(clk_ref), .i_rstn(reg_cnn_release), .i_payload(payload)')
    declarations='''
    wire [1:0] status;
    wire [3:0] error_kind;
    wire [4:0] phase;
    wire [6:0] writes,reads;
    wire [8:0] output_bytes;
    wire [31:0] cycles;
    wire [319:0] cycle_bins;
    wire [24:0] address;
    wire [127:0] expected_data,actual_data;
    wire [255:0] payload;
    wire req_valid,req_ready,req_write,rsp_valid,rsp_ready,mailbox_fault;
    wire [24:0] req_addr;
    wire [127:0] req_data,rsp_data;
    wire [3:0] rsp_error;
    reg reg_ref_meta,reg_ref_release,reg_user_meta,reg_user_release;
    reg reg_pixel_meta,reg_pixel_release,reg_cnn_meta,reg_cnn_release;
    reg reg_phy_meta,reg_phy_sync;
    reg [27:0] cnt_page;
    reg [127:0] reg_page_data;
    assign raw_rstn = i_rstn && pll_locked;
    assign user_raw_rstn = raw_rstn && ddrphy_rst_n;
    assign payload = {status,cnt_page[27:26],phase,error_kind,writes,reads,output_bytes,
                      cycles,60'h535444445232,reg_page_data};
    // 四页观察值均由原有冻结载荷显示机制发布。
    always @(*) begin
        case(cnt_page[27:26])
            2'd0: reg_page_data = expected_data;
            2'd1: reg_page_data = actual_data;
            2'd2: reg_page_data = cycle_bins[127:0];
            default: reg_page_data = {cycle_bins[287:256],cycle_bins[223:192],
                                      cycle_bins[159:128],cycles};
        endcase
    end
    // 计算域释放不早于整个DDR用户接口复位许可。
    always @(posedge clk_ref or negedge user_raw_rstn) begin
        if(!user_raw_rstn) begin
            reg_cnn_meta <= 1'b0;
            reg_cnn_release <= 1'b0;
            reg_phy_meta <= 1'b0;
            reg_phy_sync <= 1'b0;
            cnt_page <= 28'd0;
        end else begin
            reg_cnn_meta <= 1'b1;
            reg_cnn_release <= reg_cnn_meta;
            reg_phy_meta <= ddrphy_ready;
            reg_phy_sync <= reg_phy_meta;
            cnt_page <= cnt_page + 28'd1;
        end
    end
'''
    # Replace the old standalone page process by the CNN-domain one above.
    marker='    always @(posedge dhi_clk or negedge user_raw_rstn) begin\n        if (!user_raw_rstn) begin\n            cnt_page'
    assert marker in resets
    resets=resets[:resets.index(marker)]
    instances='''
    road_stem_ddr_sequence u_sequence(
        .i_clk(clk_ref),.i_rstn(reg_cnn_release),.i_phy_ready(reg_phy_sync),.i_ddr_fault(mailbox_fault),
        .i_req_ready(req_ready),.i_rsp_valid(rsp_valid),.i_rsp_data(rsp_data),.i_rsp_error(rsp_error),
        .o_req_valid(req_valid),.o_req_write(req_write),.o_req_addr(req_addr),.o_req_data(req_data),.o_rsp_ready(rsp_ready),
        .o_status(status),.o_error(error_kind),.o_phase(phase),.o_writes(writes),.o_reads(reads),
        .o_output_bytes(output_bytes),.o_cycles(cycles),.o_cycle_bins(cycle_bins),
        .o_address(address),.o_expected(expected_data),.o_actual(actual_data)
    );
    road_paxi_mailbox u_mailbox(
        .i_clk(clk_ref),.i_rstn(reg_cnn_release),.i_ddr_clk(dhi_clk),.i_ddr_rstn(reg_user_release),
        .i_phy_ready(ddrphy_ready),.i_req_valid(req_valid),.i_req_write(req_write),.i_req_addr(req_addr),.i_req_data(req_data),
        .o_req_ready(req_ready),.o_rsp_valid(rsp_valid),.o_rsp_data(rsp_data),.o_rsp_error(rsp_error),
        .i_rsp_ready(rsp_ready),.o_fault(mailbox_fault),
        .i_awready(awready),.i_wready(wready),.i_arready(arready),.i_rvalid(rvalid),.i_rlast(rlast),.i_rdata(rdata),
        .o_awaddr(awaddr),.o_awvalid(awvalid),.o_wdata(wdata),.o_wstrb(wstrb),.o_wvalid(wvalid),.o_wlast(wlast),
        .o_araddr(araddr),.o_arvalid(arvalid),.o_rready(rready)
    );
'''
    result=header+data_wires+display_wires+declarations+resets+pll_ddr+instances+display
    assert result.count('cnt_page <= 28\'d0')==1
    assert result.count('always @(posedge dhi_clk or negedge user_raw_rstn)')==1
    assert result.count('module road_stem_ddr_board_top')==1
    (run.ROOT/'rtl/road_stem_ddr_board_top.v').write_text(result,encoding='utf-8')
    print('BOARD_SHELL_GENERATED IO=51 CNN=100MHz DDR=133.33MHz')


if __name__=='__main__':
    generate()
