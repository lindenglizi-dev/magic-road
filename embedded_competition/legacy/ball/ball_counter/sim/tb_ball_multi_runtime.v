`timescale 1ns / 1ps
module tb_ball_multi_runtime;
    reg clk=0,rstn=0,user=0,valid=0;
    always #5 clk=!clk;
    reg [3:0] keys=15;
    reg [95:0] rgb=0;
    wire [127:0] data;
    wire out_valid,last,done,early,error,mode;
    wire [31:0] red,green,yellow;
    wire [33:0] total;
    ball_runtime #(.C_WIDTH(320),.C_HEIGHT(384),.C_X_MIN(0),.C_Y_MIN(144),.C_X_END(320),.C_Y_END(368),
        .C_GATE_MIN(136),.C_GATE_END(184),.C_LINE(160),.C_HYST(4),.C_MIN_AREA(128),
        .C_COUNT_MIN_SIZE(24),.C_COUNT_MAX_SIZE(96),.C_MAX_MOVE(32),.C_DEBOUNCE(3)) dut(
        .I_clk(clk),.I_rst_n(rstn),.I_keys_n(keys),.I_camera_status(48'd0),.I_rgb(rgb),.I_valid(valid),.I_user(user),.I_last(1'b0),
        .O_data(data),.O_valid(out_valid),.O_last(last),.O_done(done),.O_early(early),.O_error(error),
        .O_red(red),.O_green(green),.O_yellow(yellow),.O_total(total),.O_count_mode(mode));
    reg [255:0] queue=0;
    reg [127:0] expected_word;
    reg expected_early;
    integer nbytes=0,words=0,lines=0,frames=0,captures=0,fd;
    always @(posedge clk)begin
        expected_early=user;
        if(dut.osd_valid)begin queue=(queue<<96)|dut.osd_rgb;nbytes=nbytes+12;end
        #1;
        if(rstn && early!==expected_early)$fatal(1,"early changed");
        if(rstn && error)$fatal(1,"runtime video error");
        if(out_valid)begin
            expected_word=queue>>((nbytes-16)*8);
            if(nbytes<16 || data!==expected_word)$fatal(1,"DDR packing mismatch");
            nbytes=nbytes-16;queue=queue&((256'b1<<(nbytes*8))-1);
            words=words+1;if(last)lines=lines+1;if(done)frames=frames+1;
            if(captures)begin $fdisplay(fd,"%032h",data);end
        end
    end
    integer frame_index,row,group_index,lane,x,y,index,dx,dy,center;
    reg [23:0] pixel;
    initial begin
        fd=$fopen("sim/multi_runtime_frame.hex","w");
        repeat(5)@(negedge clk);rstn=1;
        keys[0]=0;repeat(12)@(negedge clk);keys[0]=1;repeat(12)@(negedge clk);
        for(frame_index=0;frame_index<8;frame_index=frame_index+1)begin
            case(frame_index)
                0:center=80;1:center=100;2:center=120;3:center=140;4:center=164;
                5:center=184;default:center=204;
            endcase
            captures=frame_index==7;
            user=1;@(negedge clk);user=0;repeat(8)@(negedge clk);
            for(row=0;row<384;row=row+1)begin
                for(group_index=0;group_index<80;group_index=group_index+1)begin
                    for(lane=0;lane<4;lane=lane+1)begin
                        x=group_index*4+lane;y=row;pixel=24'h202020;
                        // 门内静态同色正方形必须排除，不能长期占门或成为第五条轨迹。
                        if(x>=144 && x<176 && y>=336 && y<368)pixel=24'h20c820;
                        for(index=0;index<4;index=index+1)begin
                            dx=x-center;dy=y-(164+44*index);
                            if(dx*dx+dy*dy<=225)begin
                                case(index)
                                    0,1:pixel=24'hc82820;
                                    2:pixel=24'hc8b420;
                                    3:pixel=24'h20c820;
                                endcase
                            end
                        end
                        rgb[95-lane*24 -:24]=pixel;
                    end
                    valid=1;@(negedge clk);
                end
                valid=0;repeat(2)@(negedge clk);
            end
            repeat(50000)@(negedge clk);
            if(!mode || dut.scan_diag_count!==4 || dut.multi_live!==4 || dut.multi_valid!==4'hf)
                $fatal(1,"missing multi candidates frame %d N%0d LIVE%0d",frame_index,dut.scan_diag_count,dut.multi_live);
        end
        $fclose(fd);
        if(red!==2 || yellow!==1 || green!==1 || total!==4)$fatal(1,"multi count wrong R%0d Y%0d G%0d T%0d",red,yellow,green,total);
        if(dut.reg_display_valid!==8'h0f || dut.reg_display_live!==4)$fatal(1,"display snapshot missing four tracks");
        if(words!=8*23040 || lines!=8*384 || frames!=8 || nbytes!=0)$fatal(1,"video length changed");
        $display("PASS multi runtime:8 RGB frames; four circles, excluded square in gate, red2/yellow1/green1; 184320 DDR words and actual ID image capture");
        $finish;
    end
endmodule
