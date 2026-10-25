// 原厂控制器启动观察；无 DDR2 器件模型时不进行数据正确性验收。
`timescale 1ps / 1ps
module tb_ddr_vendor_startup;
    reg ref_clk = 1'b0;
    reg sys_rst_n = 1'b0;
    wire dhi_clk, cfg_clk, cfg_rst_n, ddrphy_rst_n, ddrphy_rdy;
    wire apb_pready, awready, wready, arready, rvalid, rlast;
    wire [31:0] apb_prdata;
    wire [127:0] rdata;
    wire ddr_ck_p, ddr_ck_n, ddr_cke, ddr_odt, ddr_cs_n, ddr_ras_n, ddr_cas_n, ddr_we_n;
    wire [1:0] ddr_ba, ddr_dqs_p, ddr_dqs_n, ddr_dm;
    wire [12:0] ddr_addr;
    wire [15:0] ddr_dq;
    integer ref_edges = 0, cfg_edges = 0, dhi_edges = 0, ddr_edges = 0;
    integer commands = 0, mrs_count = 0, refresh_count = 0, precharge_count = 0;
    integer unsolicited_reads = 0, snapshots = 0;
    time last_ref = 0;
    time ready_time = 0;

    // ponytail: 只观察原厂启动；取得匹配器件模型后才增加读写scoreboard。
    ddr2 dut (
        .ref_clk(ref_clk), .sys_rst_n(sys_rst_n),
        .apb_pclk(ref_clk), .apb_prst_n(sys_rst_n), .apb_pready(apb_pready),
        .apb_psel(1'b0), .apb_penable(1'b0), .apb_pwrite(1'b0),
        .apb_paddr(16'd0), .apb_pwdata(32'd0), .apb_prdata(apb_prdata),
        .dhi_clk(dhi_clk), .cfg_clk(cfg_clk), .cfg_rst_n(cfg_rst_n),
        .ddrphy_rst_n(ddrphy_rst_n), .ddrphy_rdy(ddrphy_rdy),
        .paxi_awaddr(25'd0), .paxi_awvalid(1'b0), .paxi_awready(awready),
        .paxi_wdata(128'd0), .paxi_wstrb(16'd0), .paxi_wvalid(1'b0), .paxi_wlast(1'b0), .paxi_wready(wready),
        .paxi_araddr(25'd0), .paxi_arvalid(1'b0), .paxi_arready(arready),
        .paxi_rdata(rdata), .paxi_rlast(rlast), .paxi_rvalid(rvalid), .paxi_rready(1'b1),
        .ddr_ck_p(ddr_ck_p), .ddr_ck_n(ddr_ck_n), .ddr_cke(ddr_cke), .ddr_odt(ddr_odt),
        .ddr_cs_n(ddr_cs_n), .ddr_ras_n(ddr_ras_n), .ddr_cas_n(ddr_cas_n), .ddr_we_n(ddr_we_n),
        .ddr_ba(ddr_ba), .ddr_addr(ddr_addr), .ddr_dqs_p(ddr_dqs_p), .ddr_dqs_n(ddr_dqs_n),
        .ddr_dq(ddr_dq), .ddr_dm(ddr_dm)
    );

    always #5000 ref_clk = ~ref_clk;
    always @(posedge ref_clk) begin
        if (ref_edges != 0 && $time-last_ref != 10000) $fatal(1,"Reference clock period");
        last_ref = $time;
        ref_edges = ref_edges+1;
    end
    always @(posedge cfg_clk) cfg_edges = cfg_edges+1;
    always @(posedge dhi_clk) begin
        dhi_edges = dhi_edges+1;
        if (sys_rst_n && rvalid === 1'b1) unsolicited_reads = unsolicited_reads+1;
    end
    always @(posedge ddrphy_rdy) begin
        if (ddrphy_rdy === 1'b1) begin
            ready_time = $time;
            $display("PHY_READY_WITHOUT_CHIP time_ps=%0t",$time);
        end
    end
    always @(posedge ddr_ck_p) begin
        ddr_edges = ddr_edges+1;
        if ({ddr_cke,ddr_cs_n} === 2'b10) begin
            case ({ddr_ras_n,ddr_cas_n,ddr_we_n})
                3'b000: mrs_count = mrs_count+1;
                3'b001: refresh_count = refresh_count+1;
                3'b010: precharge_count = precharge_count+1;
                default: begin end
            endcase
            if ({ddr_ras_n,ddr_cas_n,ddr_we_n} !== 3'b111) begin
                commands = commands+1;
                if (commands <= 20) $display("DRAM_COMMAND time_ps=%0t command=%b bank=%h address=%h",$time,
                    {ddr_ras_n,ddr_cas_n,ddr_we_n},ddr_ba,ddr_addr);
            end
        end
    end
    initial begin
        #2000000 sys_rst_n = 1'b1;
        for (snapshots=0;snapshots<10;snapshots=snapshots+1) begin
            #100000000;
            $display("STARTUP_SAMPLE time_ps=%0t cfg_edges=%0d dhi_edges=%0d ddr_edges=%0d cfg_reset=%b phy_reset=%b ready=%b",
                $time,cfg_edges,dhi_edges,ddr_edges,cfg_rst_n,ddrphy_rst_n,ddrphy_rdy);
        end
        $display("STARTUP_SUMMARY chip_model=ABSENT ref=%0d cfg=%0d dhi=%0d ddr=%0d ready=%b ready_time_ps=%0t commands=%0d mrs=%0d refresh=%0d precharge=%0d unsolicited=%0d",
            ref_edges,cfg_edges,dhi_edges,ddr_edges,ddrphy_rdy,ready_time,commands,mrs_count,refresh_count,precharge_count,unsolicited_reads);
        if (unsolicited_reads != 0) $fatal(1,"Read valid without request");
        if (cfg_edges==0 || dhi_edges==0 || ddr_edges==0) $display("STARTUP_BLOCKED_CLOCK");
        else if (ddrphy_rdy !== 1'b1) $display("STARTUP_BLOCKED_NOT_READY");
        else $display("STARTUP_OBSERVED_NOT_MEMORY_PASS");
        $finish;
    end
endmodule
