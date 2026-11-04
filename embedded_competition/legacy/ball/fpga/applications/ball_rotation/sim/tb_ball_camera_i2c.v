`timescale 1ns / 1ps
// 真正开漏总线及原uii2c主机；从设备模型保存传感器寄存器并可注入读错/NACK。
module tb_ball_camera_i2c;
    parameter READ_WAIT=5000;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,request=0;
    reg [15:0] exposure=1991,gain=144;
    wire scl;
    tri1 sda;
    reg slave_low=0;
    assign sda=slave_low ? 1'b0 : 1'bz;
    wire configured,ae_done,id_ok,error,read_valid,read_match;
    wire [15:0] sensor_id,read_exposure;
    wire [23:0] read_gain;
    uicfgcs520 #(.CLK_DIV(8),.READ_WAIT_CYCLES(READ_WAIT)) dut(.I_clk(clk),.I_rst_n(rstn),.I_ae_req(request),.I_ae(exposure),.I_ag(gain),
        .O_cam_scl(scl),.IO_cam_sda(sda),.O_cfg_done(configured),.O_ae_cfg_done(ae_done),
        .O_sensor_id(sensor_id),.O_sensor_id_ok(id_ok),.O_iic_error(error),
        .O_read_exposure(read_exposure),.O_read_gain(read_gain),.O_read_valid(read_valid),.O_read_match(read_match));
    reg [7:0] memory[0:65535];
    localparam IDLE=0,RX=1,ACK=2,ACK_END=3,TX=4,TX_END=5,MASTER_ACK=6;
    integer phase=IDLE,bits=0,byte_index=0,tx_bits=0;
    reg [7:0] rx_byte=0,tx_byte=0;
    reg [15:0] address=0;
    reg read_mode=0,nack_address=0,corrupt_read=0;
    integer reads=0,writes=0,starts=0,init_index;
    integer settle_count=0;
    always @(posedge clk)begin if(settle_count>0)settle_count=settle_count-1;end
    always @(negedge sda)begin
        if(rstn && scl===1'b1)begin phase=RX;bits=0;byte_index=0;rx_byte=0;slave_low=0;starts=starts+1;end
    end
    always @(posedge sda)begin
        if(rstn && scl===1'b1)begin phase=IDLE;slave_low=0;end
    end
    always @(posedge scl)begin
        if(rstn)begin
            case(phase)
                RX:begin
                    rx_byte={rx_byte[6:0],sda};bits=bits+1;
                    if(bits==8)begin
                        case(byte_index)
                            0:begin
                                if(rx_byte[7:1]!==7'h36)$fatal(1,"wrong sensor address %h",rx_byte);
                                read_mode=rx_byte[0];
                            end
                            1:address[15:8]=rx_byte;
                            2:address[7:0]=rx_byte;
                            3:begin
                                memory[address]=rx_byte;writes=writes+1;
                                if(address==16'h3812 && rx_byte==8'h30)settle_count=4000;
                            end
                            default:begin end
                        endcase
                    end
                end
                ACK:phase=ACK_END;
                TX:begin tx_bits=tx_bits+1;if(tx_bits==8)begin phase=TX_END;reads=reads+1;end end
                MASTER_ACK:begin
                    if(sda===1'b1)begin phase=IDLE;end
                    else begin address=address+1'b1;tx_byte=memory[address];tx_bits=0;phase=TX;end
                end
                default:begin end
            endcase
        end
    end
    always @(negedge scl)begin
        if(rstn)begin
            case(phase)
                RX:if(bits==8)begin slave_low=!(nack_address && byte_index==0);phase=ACK;end
                ACK_END:begin
                    slave_low=0;
                    if(byte_index==0 && nack_address)begin nack_address=0;phase=IDLE;end
                    else if(byte_index==0 && read_mode)begin
                        tx_byte=memory[address];
                        if(address[15:8]==8'h3e && settle_count>0)tx_byte=tx_byte^8'h01;
                        if(corrupt_read && address==16'h3e01)begin tx_byte=tx_byte^8'h01;end
                        tx_bits=0;slave_low=!tx_byte[7];phase=TX;
                    end else begin byte_index=byte_index+1;bits=0;phase=RX;end
                end
                TX:slave_low=!tx_byte[7-tx_bits];
                TX_END:begin slave_low=0;phase=MASTER_ACK;end
                default:begin end
            endcase
        end
    end
    task configure_ae;
        input [15:0] new_exposure,new_gain;
        begin
            wait(ae_done);@(negedge clk);exposure=new_exposure;gain=new_gain;request=1;
            @(negedge clk);request=0;
            wait(!ae_done);wait(ae_done);repeat(3)@(negedge clk);
        end
    endtask
    initial begin
        for(init_index=0;init_index<65536;init_index=init_index+1)begin memory[init_index]=0;end
        memory[16'h3107]=8'hee;memory[16'h3108]=8'h4b;
        repeat(5)@(negedge clk);rstn=1;
        wait(configured && ae_done);
        if(!id_ok || sensor_id!=16'hee4b || error)$fatal(1,"initial I2C sensor configuration failed");
        configure_ae(1991,144);
        if(!read_valid || !read_match || read_exposure!=1991 || read_gain!=24'h0f0080 || error)$fatal(1,"default AE readback failed");
        configure_ae(480,176);
        if(!read_match || read_exposure!=480 || read_gain!=24'h1f0080)$fatal(1,"short AE readback failed");
        corrupt_read=1;configure_ae(240,80);
        if(read_match || error || !read_valid)$fatal(1,"corrupt read falsely matched or bus error conflated");
        corrupt_read=0;configure_ae(120,112);
        if(!read_match || read_exposure!=120 || read_gain!=24'h0b0080)$fatal(1,"readback recovery failed");
        nack_address=1;configure_ae(480,144);
        if(read_match || !error)$fatal(1,"NACK falsely reported success");
        $display("PASS camera I2C: actual master and open-drain bytes, init ID/table, six-register AE/AG readback, corruption, recovery and NACK; reads=%0d writes=%0d",reads,writes);
        $finish;
    end
    initial begin #100000000;$fatal(1,"I2C timeout phase=%0d state=%0d address=%h",phase,dut.state,address);end
endmodule
