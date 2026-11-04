`timescale 1ns / 1ps
// 复用摄像头功能验收，只增加总线事务记录和三个非同步复位刺激。
module tb_ball_i2c_equivalence;
    parameter CLK_DIV=8;
    parameter RESET_STRESS=0;
    tb_ball_camera_i2c bench();
    defparam bench.dut.CLK_DIV=CLK_DIV;
    reg [2047:0] trace_path;
    integer trace_file,serial_bits=0,bytes=0,starts=0,resets=0;
    reg [7:0] serial_byte=0;
    reg active=0,have_edge=0,previous_scl=0;
    time edge_time;
    initial begin
        if(!$value$plusargs("TRACE=%s",trace_path))$fatal(1,"missing TRACE path");
        trace_file=$fopen(trace_path,"w");
        if(!trace_file)$fatal(1,"cannot open trace");
    end
    always @(negedge bench.sda)begin
        if(bench.rstn && bench.scl===1'b1)begin
            active=1;have_edge=0;serial_bits=0;serial_byte=0;starts=starts+1;
            $fwrite(trace_file,"S %0t\n",$time);
        end
    end
    always @(posedge bench.sda)begin
        if(bench.rstn && bench.scl===1'b1)begin
            $fwrite(trace_file,"T %0t\n",$time);
            active=0;have_edge=0;serial_bits=0;
        end
    end
    always @(posedge bench.scl)begin
        if(bench.rstn && active)begin
            if(serial_bits<8)begin serial_byte={serial_byte[6:0],bench.sda};serial_bits=serial_bits+1;end
            else begin
                if(bench.sda!==1'b0 && bench.sda!==1'b1)$fatal(1,"unknown ACK bit");
                $fwrite(trace_file,"B %02h %0d %0t\n",serial_byte,bench.sda,$time);
                serial_bits=0;bytes=bytes+1;
            end
        end
    end
    always @(posedge bench.scl or negedge bench.scl)begin
        if(bench.rstn && active)begin
            if(have_edge)$fwrite(trace_file,"P %0d %0t\n",previous_scl,$time-edge_time);
            edge_time=$time;previous_scl=bench.scl;have_edge=1;
        end else have_edge=0;
    end
    task interrupt_bus;
        input integer identity,hold_time;
        begin
            bench.rstn=0;
            // 传感器存储继续保留，只释放开漏响应并重新等待START。
            bench.slave_low=0;bench.phase=0;bench.bits=0;bench.byte_index=0;bench.tx_bits=0;
            active=0;have_edge=0;serial_bits=0;resets=resets+1;
            $fwrite(trace_file,"R %0d %0t\n",identity,$time);
            #(hold_time);bench.rstn=1;
        end
    endtask
    initial begin
        if(RESET_STRESS)begin
            wait(bench.rstn);
            wait(bench.phase==1 && bench.bits==3);#3;interrupt_bus(0,17);
            wait(bench.phase==2);#2;interrupt_bus(1,23);
            wait(bench.phase==4 && bench.tx_bits==3);#7;interrupt_bus(2,13);
            $display("PASS I2C RESET STRESS: RX, address ACK and TX interrupted at distinct clock phases; DIV=%0d",CLK_DIV);
        end
    end
endmodule
