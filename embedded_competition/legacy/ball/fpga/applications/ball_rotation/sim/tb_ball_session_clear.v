`timescale 1ns / 1ps
module tb_ball_session_clear;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,clear=0,valid=0,sof=0,eof=0;reg [11:0] x=0,y=0;reg [7:0] labels=0;reg [15:0] epoch=0;
    wire start,candidate,done,fault,error;wire [15:0] result_epoch;
    integer row,col,seen=0,finished=0;
    ball_components #(.C_WIDTH(64),.C_HEIGHT(64),.C_X_MIN(0),.C_X_END(64),.C_Y_MIN(0),.C_Y_END(64),
        .C_GATE_MIN(24),.C_GATE_END(40),.C_MIN_AREA(16),.C_MIN_SIZE(4),.C_MAX_SIZE(32)) dut(
        .i_clk(clk),.i_rstn(rstn),.i_session_clear(clear),.i_valid(valid),.i_sof(sof),.i_eof(eof),.i_x(x),.i_y(y),
        .i_labels(labels),.i_gate_hits(3'd0),.i_epoch(epoch),.o_frame_start(start),.o_candidate_valid(candidate),
        .o_color(),.o_area(),.o_x_min(),.o_x_max(),.o_y_min(),.o_y_max(),.o_frame_done(done),.o_gate_pixels(),
        .o_gate_occupied(),.o_epoch(result_epoch),.o_overflow(),.o_fault(fault),.o_error(error),
        .o_diag_count(),.o_diag_width(),.o_diag_height(),.o_diag_area(),.o_diag_fill(),.o_diag_reject());
    always @(negedge clk)begin
        if(candidate)begin if(result_epoch != 9)$fatal(1,"stale candidate");seen=seen+1;end
        if(done)begin if(result_epoch != 9)$fatal(1,"stale done");finished=finished+1;end
    end
    task frame;
        begin
            for(row=0;row<64;row=row+1)for(col=0;col<64;col=col+4)begin
                valid=1;x=col;y=row;sof=row == 0 && col == 0;eof=row == 63 && col == 60;
                labels=(row>=12 && row<28 && col>=12 && col<28) ? 8'h55 : 8'd0;
                @(negedge clk);
            end
            valid=0;sof=0;eof=0;
        end
    endtask
    initial begin
        repeat(3)@(negedge clk);rstn=1;frame;
        wait(start);repeat(10)@(negedge clk);clear=1;
        @(negedge clk);clear=0;epoch=9;repeat(10)@(negedge clk);
        if(dut.state_current != 0 || error || fault || candidate || done)$fatal(1,"clear did not abort");
        frame;wait(done);repeat(2)@(negedge clk);
        if(seen != 1 || finished != 1 || fault || error)$fatal(1,"restart frame seen%0d done%0d fault%0d error%0d",seen,finished,fault,error);
        $display("PASS CCL busy synchronous abort and fresh frame restart");$finish;
    end
    initial begin #1000000;$fatal(1,"CCL clear timeout");end
endmodule
