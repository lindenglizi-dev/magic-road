`timescale 1ns / 1ps

// Forced read-cone enumeration supplements, but does not replace, legal full-tensor tests.
module tb_scheduler_storage(output reg o_test_done);
    reg clk=0; always #5 clk=~clk;
    reg rstn=0;
    reg dw_valid=0, stem_valid=0, stem_start=0, stem_export=0;
    reg [10:0]dw_addr=0;
    reg signed [31:0]dw_data=0;
    reg [2:0]stem_kind=0;
    reg [8:0]stem_addr=0;
    reg signed [31:0]stem_data=0;
    wire dw_ready, stem_ready, stem_fault, stem_busy;
    reg [4:0]forced_channel=0;
    reg [3:0]forced_position=0;
    reg [1:0]forced_group=0;
    reg [7:0]weights[0:143];
    reg [7:0]expected_weight;
    integer index, position, channel, group_index, lane, spatial, kernel, row, column, checks=0;
    road_down2_tile_scheduler dw(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b0),
        .i_load_valid(dw_valid),.i_load_kind(3'd2),.i_load_addr(dw_addr),.i_load_data(dw_data),.o_load_ready(dw_ready),
        .i_start(1'b0),.i_pw_only(1'b0),.i_commit_ready(1'b1),.i_export_start(1'b0),.i_output_ready(1'b1),
        .i_mac_ready(1'b0),.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
        .i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),
        .i_pp_result_queue_count(2'd0),.i_pp_meta_count(4'd0),.i_pp_pre_busy(1'b0),.i_pp_silu_busy(1'b0),
        .i_pp_post_busy(1'b0),.i_pp_pre_accept(1'b0),.i_pp_silu_accept(1'b0),.i_pp_post_accept(1'b0));
    road_stem_tile_scheduler stem(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b1),
        .i_load_valid(stem_valid),.i_load_kind(stem_kind),.i_load_addr(stem_addr),.i_load_data(stem_data),
        .o_load_ready(stem_ready),.i_start(stem_start),.o_fault(stem_fault),.o_busy(stem_busy),
        .i_mac_ready(1'b0),.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
        .i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),
        .i_commit_ready(1'b1),.i_export_start(stem_export),.i_output_ready(1'b1));
    always @(posedge clk) begin
        #1;
        if(stem.flag_load_state_ready !== (stem.state_current==4'd0)) $fatal(1,"Stem state eligibility mismatch");
        if(stem_ready !== (rstn && stem.state_current==4'd0 && !stem_start && !stem_export && !stem_fault))
            $fatal(1,"Stem ready changed from baseline expression");
    end
    task stem_load;
        input [2:0]kind;
        input integer count;
        begin
            for(index=0;index<count;index=index+1)begin
                @(negedge clk);stem_valid=1;stem_kind=kind;stem_addr=index;
                stem_data=(kind==3'd1) ? 0 : (kind==3'd2) ? ((index*73+19)%256)-128 : 1;
                if(!stem_ready) $fatal(1,"Unexpected gap in back-to-back Stem preload");
                @(posedge clk);#1;
                if(stem_fault) $fatal(1,"Legal Stem preload fault");
                if(kind==3'd1 && stem.reg_halo[index] !== 8'd0) $fatal(1,"Stem halo commit mismatch");
                if(kind==3'd2 && stem.reg_weight[index] !== stem_data[7:0]) $fatal(1,"Stem weight commit mismatch");
            end
        end
    endtask
    initial begin
        o_test_done=0;
        repeat(2) @(negedge clk);rstn=1;
        for(index=0;index<144;index=index+1)begin
            @(negedge clk);dw_valid=1;dw_addr=index;dw_data=((index*73+19)%256)-128;weights[index]=dw_data[7:0];
            if(!dw_ready) $fatal(1,"DW preload unexpectedly blocked");
            @(posedge clk);#1;
            if(dw.reg_dw_weight_write_address !== (index%9)*16+index/9) $fatal(1,"DW transposed address mismatch");
        end
        @(negedge clk);dw_valid=0;
        @(posedge clk);#1;
        force dw.flag_layer_pw=1'b0;
        force dw.cnt_output=forced_channel;
        force dw.cnt_position=forced_position;
        force dw.cnt_mac_group=forced_group;
        for(channel=0;channel<16;channel=channel+1)
            for(position=0;position<16;position=position+1)
                for(group_index=0;group_index<3;group_index=group_index+1)begin
                    forced_channel=channel;forced_position=position;forced_group=group_index;#1;
                    if(dw.next_mac_mask !== ((group_index==2) ? 8'h1f : 8'hff)) $fatal(1,"DW tail mask changed");
                    for(lane=0;lane<8;lane=lane+1)
                        for(spatial=0;spatial<3;spatial=spatial+1)begin
                            kernel=group_index*8+lane;row=kernel/7;column=kernel%7;expected_weight=0;
                            if(kernel<21 && spatial<((position%4==0)?3:1) && column>=spatial*2 && column<spatial*2+3)
                                expected_weight=weights[channel*9+row*3+column-spatial*2];
                            if(dw.next_mac_weight[(spatial*8+lane)*8+:8] !== expected_weight)
                                $fatal(1,"DW bank read mismatch channel=%0d position=%0d group=%0d",channel,position,group_index);
                            checks=checks+1;
                        end
                end
        release dw.flag_layer_pw;release dw.cnt_output;release dw.cnt_position;release dw.cnt_mac_group;
        stem_load(3'd1,243);stem_load(3'd2,432);stem_load(3'd3,16);
        stem_load(3'd4,16);stem_load(3'd5,16);stem_load(3'd6,2);
        @(negedge clk);stem_valid=0;stem_start=1;#1;
        if(stem_ready) $fatal(1,"Start did not block loader immediately");
        @(posedge clk);#1;if(!stem_busy || stem.flag_load_state_ready) $fatal(1,"Last load to start added a bubble");
        @(negedge clk);stem_start=0;repeat(4) @(negedge clk);
        #2;rstn=0;#1;if(stem_ready || stem_busy || stem.state_current!==4'd0) $fatal(1,"Reset cancellation delayed");
        @(negedge clk);rstn=1;stem_export=1;#1;if(stem_ready) $fatal(1,"Export did not block loader");
        @(negedge clk);stem_export=0;stem_valid=1;stem_kind=3'd7;
        @(posedge clk);#1;if(!stem_fault || stem_ready) $fatal(1,"Illegal load did not close loader");
        repeat(5)begin @(negedge clk);if(stem_ready) $fatal(1,"Sticky loader fault reopened");end
        $display("TB_PASS_SCHEDULER_STORAGE selected_bytes=%0d stem_loads=725",checks);
        o_test_done=1;$finish;
    end
    initial begin #5000000;$fatal(1,"Storage test timeout");end
endmodule
