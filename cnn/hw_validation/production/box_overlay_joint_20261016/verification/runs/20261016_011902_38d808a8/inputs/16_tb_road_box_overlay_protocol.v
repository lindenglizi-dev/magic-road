`timescale 1ns/1ps
// Direct display protocol tests; these injections are not recognition evidence.
module tb_road_box_overlay_protocol;
    reg clk=0,rstn=0,sof=0,de=0;
    reg [6:0] count=64;
    reg [96:0] entry=0;
    wire [5:0] read_index;
    wire vs,hs,ode,ready,busy,fault;
    wire [23:0] rgb;
    wire [8:0] cycles;
    integer pixel,index,seen,max_ready_delay;
    reg check_raw=0;
    reg [2:0] sync_previous=0,sync_expected=0;
    road_box_age_overlay dut(
        .i_clk(clk),.i_rstn(rstn),.i_sof(sof),.i_vsync(1'b0),.i_hsync(1'b0),
        .i_de(de),.i_rgb(24'h123456),.i_table_active_valid(1'b1),
        .i_table_count(count),.i_table_entry(entry),.i_table_draw_valid(1'b1),
        .i_age_upper_ms(64'd2000),.o_table_read_index(read_index),
        .o_vsync(vs),.o_hsync(hs),.o_de(ode),.o_rgb(rgb),
        .o_line_ready(ready),.o_prepare_busy(busy),.o_last_prepare_cycles(cycles),.o_fault(fault));
    always #6.666 clk=~clk;
    always @(posedge clk) begin
        if(rstn) begin
            if(dut.BoxLine_Inst.reg_map_read_address>=1280 || dut.BoxLine_Inst.reg_map_write_address>=1280)
                $fatal(1,"NATIVE_ADDRESS_RANGE read=%0d write=%0d",dut.BoxLine_Inst.reg_map_read_address,dut.BoxLine_Inst.reg_map_write_address);
            if(dut.BoxLine_Inst.reg_map_write_enable && dut.BoxLine_Inst.reg_map_read_address===dut.BoxLine_Inst.reg_map_write_address)
                $fatal(1,"NATIVE_COLLISION");
            sync_expected=sync_previous;sync_previous={2'b0,de};
            #0.001;
            if({vs,hs,ode}!==sync_expected) $fatal(1,"PROTOCOL_SYNC_LATENCY");
            if(check_raw && ode) begin
                seen=seen+1;
                if(rgb!==24'h123456) $fatal(1,"MIDROW_PAINT pixel=%0d rgb=%h",seen,rgb);
            end
        end else begin sync_expected=0;sync_previous=0;end
    end
    task reset_and_poison;
        begin
            @(negedge clk);rstn=0;de=0;sof=0;
            repeat(4) @(negedge clk);
            for(index=0;index<1280;index=index+1)
                dut.BoxLine_Inst.PH1P_LOGIC_DRAM_Inst_line_events.memory[index]=$random;
            rstn=1;
        end
    endtask
    task pulse_sof;
        begin @(negedge clk);sof=1;@(negedge clk);sof=0;end
    endtask
    task raw_line;
        begin
            seen=0;check_raw=1;
            @(negedge clk);de=1;
            repeat(1280) @(negedge clk);
            de=0;repeat(3) @(negedge clk);
            check_raw=0;
            if(seen!=1280) $fatal(1,"PROTOCOL_PIXEL_COUNT %0d",seen);
        end
    endtask
    initial begin
        entry=(97'd1280<<65)|(97'd720<<85);
        reset_and_poison;
        // Cold reset plus normalblank: clear and all64 entries must finish.
        max_ready_delay=0;
        while(!ready && max_ready_delay<39970) begin
            @(negedge clk);max_ready_delay=max_ready_delay+1;
        end
        if(!ready || cycles!=320 || fault) $fatal(1,"COLD_CLEAR_PREP");
        $display("COLD_CLEAR_PREP_PASS blank_cycles=%0d scan=%0d",max_ready_delay,cycles);
        // Force active video before clear completion; no midrow recovery.
        pulse_sof;repeat(100) @(negedge clk);raw_line;
        if(!fault) $fatal(1,"EARLY_CLEAR_DE_NOT_REPORTED");
        reset_and_poison;pulse_sof;repeat(1300) @(negedge clk);raw_line;
        if(!fault) $fatal(1,"EARLY_PREP_DE_NOT_REPORTED");
        // Oversize count must fault and suppress the entire line.
        count=65;reset_and_poison;pulse_sof;repeat(2000) @(negedge clk);raw_line;
        if(!fault) $fatal(1,"COUNT65_NOT_REPORTED");
        // Disabled malformed endpoints must keep even unused nativeaddresses legal.
        count=1;entry=(97'd4095<<25)|(97'd4095<<45)|(97'd4095<<65)|(97'd4095<<85);
        reset_and_poison;pulse_sof;repeat(2000) @(negedge clk);raw_line;
        if(fault) $fatal(1,"COLLAPSE_SHOULD_SKIP_ONLY");
        $display("TB_PASS_BOX_OVERLAY_PROTOCOL cold_clear poisoned_storage early_clear early_prepare count65 collapsed_address");
        $finish;
    end
    initial begin #10000000;$fatal(1,"PROTOCOL_TIMEOUT");end
endmodule
