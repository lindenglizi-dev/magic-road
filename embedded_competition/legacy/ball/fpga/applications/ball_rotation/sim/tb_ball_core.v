`timescale 1ns / 1ps
module tb_ball_core;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0, valid=0, early=0, clear=0, clear_counts=0;
    reg [95:0] rgb=0;
    wire [95:0] front_rgb;
    wire fv, fs, fl, fe, ferr;
    wire [11:0] fx,fy;
    wire [7:0] labels;
    wire [2:0] gate_hits;
    wire [15:0] front_epoch;
    wire ps,pv,pd,overflow,fault,error;
    wire [1:0] color,event_color;
    wire [19:0] area,gate_pixels;
    wire [11:0] xmin,xmax,ymin,ymax;
    wire [15:0] epoch;
    wire [31:0] red,yellow,green;
    wire [33:0] total;
    wire [2:0] gate_state, reason;
    wire [1:0] empty,track_status;
    wire track_valid;
    wire [11:0] track_x,track_y;
    integer frame_done_count=0,candidates=0,last_candidates=0,frames=0;
    integer words=0,lines=0,pixels=0,sof_count=0;
    wire [127:0] pack_data;
    wire pack_valid,pack_last,pack_done,pack_error;
    reg bcd_load=0;
    reg [33:0] binary_value=0;
    wire [43:0] decimal_value;
    wire decimal_done;
    reg [11:0] last_xmax=0;
    reg force_many=0;
    integer input_file,candidate_file,frame_file;
    reg frame_completed;
    ball_stream_front #(.C_WIDTH(160),.C_HEIGHT(96),.C_X_MIN(0),.C_Y_MIN(0),
        .C_X_END(160),.C_Y_END(96),.C_GATE_MIN(56),.C_GATE_END(104)) front_Inst(
        .i_clk(clk),.i_rstn(rstn),.i_rgb(rgb),.i_valid(valid),.i_early(early),.i_strict(1'b0),.i_epoch(16'd0),
        .o_rgb(front_rgb),.o_valid(fv),.o_sof(fs),.o_eol(fl),.o_eof(fe),.o_x(fx),.o_y(fy),
        .o_labels(labels),.o_gate_hits(gate_hits),.o_epoch(front_epoch),.o_error(ferr));
    ball_projection #(.C_WIDTH(160),.C_HEIGHT(96),.C_MIN_AREA(16),.C_MIN_SIZE(3),.C_MAX_SIZE(64)) projection_Inst(
        .i_clk(clk),.i_rstn(rstn),.i_valid(fv),.i_sof(fs),.i_eof(fe),.i_x(fx),.i_y(fy),
        .i_labels(labels),.i_gate_hits(gate_hits),.i_epoch(front_epoch),
        .o_frame_start(ps),.o_candidate_valid(pv),.o_color(color),.o_area(area),
        .o_x_min(xmin),.o_x_max(xmax),.o_y_min(ymin),.o_y_max(ymax),.o_frame_done(pd),
        .o_gate_pixels(gate_pixels),.o_epoch(epoch),.o_overflow(overflow),.o_fault(fault),.o_error(error));
    ball_gate_counter #(.C_GATE_MIN(56),.C_GATE_END(104),.C_GATE_TOP(0),.C_GATE_BOTTOM(96),.C_LINE(80),.C_HYST(4)) counter_Inst(
        .i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_clear_counts(clear_counts),.i_fault(fault),
        .i_frame_start(ps),.i_candidate_valid(pv),.i_color(color),.i_x_min(xmin),.i_x_max(xmax),.i_y_min(ymin),.i_y_max(ymax),
        .i_frame_done(pd),.i_overflow(overflow),.i_gate_pixels(gate_pixels),.o_red(red),.o_yellow(yellow),.o_green(green),
        .o_total(total),.o_state(gate_state),.o_empty(empty),.o_event(event_color),.o_reason(reason),.o_center_x(),.o_center_y());
    ball_target_tracker #(.C_MAX_MOVE(12)) tracker_Inst(
        .i_clk(clk),.i_rstn(rstn),.i_clear(clear),.i_frame_start(ps),.i_candidate_valid(pv),.i_color(color),.i_area(area),
        .i_x_min(xmin),.i_x_max(xmax),.i_y_min(ymin),.i_y_max(ymax),.i_frame_done(pd),.i_overflow(overflow),
        .o_valid(track_valid),.o_status(track_status),.o_color(),.o_x_min(),.o_x_max(),.o_y_min(),.o_y_max(),
        .o_center_x(track_x),.o_center_y(track_y));
    rgb96_pack128_valid pack_Inst(.I_clk(clk),.I_rst_n(rstn),.I_rgb(front_rgb),.I_valid(fv),.I_user(fs),.I_last(fl),.I_done(fe),
        .O_data(pack_data),.O_valid(pack_valid),.O_last(pack_last),.O_done(pack_done),.O_error(pack_error));
    ball_decimal_format #(.C_BITS(34),.C_DIGITS(11)) decimal_Inst(
        .i_clk(clk),.i_rstn(rstn),.i_load(bcd_load),.i_binary(binary_value),.o_bcd(decimal_value),.o_done(decimal_done),.o_busy());
    reg [255:0] pending_bytes=0;
    reg [127:0] expected_word;
    integer pending_size=0;
    always @(posedge clk)begin
        frame_completed=pd;
        if(fv)begin
            pending_bytes=(pending_bytes<<96)|front_rgb;
            pending_size=pending_size+12;
            pixels=pixels+4;
            if(fs)begin sof_count=sof_count+1; end
        end
        if(ps)begin candidates=0; end
        if(pv)begin
            candidates=candidates+1;
            last_xmax=xmax;
            if(area == 0 || xmin > xmax || ymin > ymax)begin $fatal(1,"invalid candidate"); end
            if(!force_many && area !== (xmax == 159 ? 20'd204 : 20'd289))begin $fatal(1,"exact pixel area"); end
            $fwrite(candidate_file,"%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",frames,color,area,xmin,ymin,xmax,ymax);
        end
        if(pd)begin frame_done_count=frame_done_count+1; last_candidates=candidates; end
        #1;
        if(frame_completed)begin $fwrite(frame_file,"%0d,%0d,%0d\n",frames,gate_pixels,overflow); end
        if(pack_valid)begin
            expected_word=pending_bytes >> ((pending_size-16)*8);
            if(pending_size < 16 || pack_data !== expected_word)begin $fatal(1,"DDR byte order"); end
            pending_size=pending_size-16;
            pending_bytes=pending_bytes & ((256'b1 << (pending_size*8))-1);
            words=words+1;
            if(pack_last)begin lines=lines+1; end
        end
    end
    function [23:0] palette;
        input integer index;
        begin
            case(index)
                1:begin palette=24'hff2020; end
                2:begin palette=24'hffff00; end
                3:begin palette=24'h00ff40; end
                default:begin palette=24'h181818; end
            endcase
        end
    endfunction
    task send_frame;
        input integer center_first, color_first, center_second, color_second;
        integer row,col,lane,x,done_before,word_before,line_before,pixel_before,sof_before;
        reg [23:0] pixel;
        begin
            done_before=frame_done_count; word_before=words; line_before=lines; pixel_before=pixels; sof_before=sof_count;
            $fwrite(input_file,"%0d,%0d,%0d,%0d,%0d,%0d\n",frames,center_first,color_first,center_second,color_second,force_many);
            @(negedge clk); early=1;
            @(negedge clk); early=0;
            repeat(8)@(negedge clk);
            for(row=0;row<96;row=row+1)begin
                for(col=0;col<40;col=col+1)begin
                    for(lane=0;lane<4;lane=lane+1)begin
                        x=col*4+lane; pixel=palette(0);
                        if(row >= 40 && row <= 56)begin
                            if(color_first != 0 && x >= center_first-8 && x <= center_first+8)begin pixel=palette(color_first); end
                            if(color_second != 0 && x >= center_second-8 && x <= center_second+8)begin pixel=palette(color_second); end
                            if(force_many && x % 16 >= 4 && x % 16 <= 12)begin pixel=palette(1); end
                        end
                        rgb[95-lane*24 -:24]=pixel;
                    end
                    valid=1; @(negedge clk);
                    if(col == 13)begin valid=0; repeat(2)@(negedge clk); end
                end
                valid=0; repeat(3)@(negedge clk);
            end
            repeat(1100)@(negedge clk);
            if(frame_done_count != done_before+1)begin $fatal(1,"missing frame scan done %0d",frames); end
            if(words-word_before != 2880 || lines-line_before != 96 || pixels-pixel_before != 15360 || sof_count-sof_before != 1)begin
                $fatal(1,"stream count mismatch");
            end
            if(ferr || error || pack_error || (overflow != force_many) || fault)begin $fatal(1,"unexpected streaming error"); end
            frames=frames+1;
        end
    endtask
    task empty_gate;
        begin send_frame(0,0,0,0); send_frame(0,0,0,0); send_frame(0,0,0,0); end
    endtask
    integer hold_frame;
    initial begin
        input_file=$fopen("sim/core_input.csv","w"); candidate_file=$fopen("sim/core_candidates.csv","w"); frame_file=$fopen("sim/core_frames.csv","w");
        repeat(5)@(negedge clk); rstn=1;
        empty_gate();
        if(gate_state != 1)begin $fatal(1,"gate not ready"); end
        send_frame(65,1,20,1); send_frame(65,1,20,1);
        if(last_candidates != 2 || gate_state != 2)begin $fatal(1,"same-color split/upstream arm"); end
        send_frame(87,1,20,1);
        if(red != 1 || total != 1)begin $fatal(1,"first red count"); end
        for(hold_frame=0;hold_frame<100;hold_frame=hold_frame+1)begin send_frame(87,1,20,1); end
        send_frame(0,0,20,1); send_frame(0,0,20,1);
        if(gate_state != 3 || empty != 2)begin $fatal(1,"lost frames released gate"); end
        send_frame(87,1,20,1);
        if(red != 1)begin $fatal(1,"duplicate count after dropout"); end
        send_frame(0,0,20,1); send_frame(0,0,20,1); send_frame(0,0,20,1);
        send_frame(65,1,135,1); send_frame(65,1,135,1); send_frame(87,1,135,1);
        if(red != 2 || last_candidates != 2)begin $fatal(1,"second same-color ball"); end
        send_frame(0,0,0,0); send_frame(0,0,0,0); send_frame(65,1,0,0); send_frame(65,1,0,0);
        if(gate_state != 4 || reason != 4 || red != 2)begin $fatal(1,"short-gap re-entry not blocked"); end
        empty_gate();
        send_frame(65,3,0,0); send_frame(65,3,0,0); send_frame(87,3,0,0);
        empty_gate();
        send_frame(65,2,0,0); send_frame(65,2,0,0); send_frame(87,2,0,0);
        if(red != 2 || green != 1 || yellow != 1 || total != 4)begin $fatal(1,"per-color totals"); end
        empty_gate(); send_frame(87,1,0,0);
        if(total != 4 || gate_state != 4)begin $fatal(1,"downstream startup counted"); end
        empty_gate(); send_frame(63,1,97,3);
        if(gate_state != 4 || reason != 2)begin $fatal(1,"multi-ball gate not blocked"); end
        empty_gate(); send_frame(156,3,0,0);
        if(last_candidates != 1 || last_xmax != 159)begin $fatal(1,"last-column flush"); end
        @(negedge clk); clear=1; clear_counts=1;
        @(negedge clk); clear=0; clear_counts=0;
        send_frame(35,1,0,0); send_frame(39,1,0,0);
        if(!track_valid || track_status != 2 || track_x != 39 || track_y != 48)begin $fatal(1,"tracker position"); end
        send_frame(0,0,0,0); send_frame(0,0,0,0);
        if(track_status != 3)begin $fatal(1,"tracker lost hold"); end
        send_frame(43,1,0,0);
        if(track_status != 2 || track_x != 43)begin $fatal(1,"tracker reacquire"); end
        send_frame(0,0,0,0); send_frame(0,0,0,0); send_frame(0,0,0,0);
        if(track_valid || track_status != 0)begin $fatal(1,"tracker search timeout"); end
        force_many=1; send_frame(0,0,0,0);
        if(!overflow || last_candidates != 8 || gate_state != 4 || reason != 1)begin $fatal(1,"candidate overflow not blocked"); end
        @(negedge clk); binary_value=34'd12884901885; bcd_load=1;
        @(negedge clk); bcd_load=0;
        repeat(36)@(negedge clk);
        if(decimal_value !== 44'h12884901885)begin $fatal(1,"BCD 34-bit total"); end
        $fclose(input_file); $fclose(candidate_file); $fclose(frame_file);
        $display("PASS ball core: %0d frames, split, tracking, pause100, dropout2, shortgap, overflow, DDR bytes, BCD",frames);
        $finish;
    end
    initial begin #200000000; $fatal(1,"timeout"); end
endmodule
