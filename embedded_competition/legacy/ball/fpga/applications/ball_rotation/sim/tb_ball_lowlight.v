`timescale 1ns / 1ps
// Actual gamma plus complete runtime: dim shaded balls, cyan rejection and video alignment.
module tb_ball_lowlight;
    localparam WIDTH=240, HEIGHT=224, RADIUS=85, CENTER_Y=112;
    localparam WORDS_PER_FRAME=WIDTH*HEIGHT*3/16;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0, scene_phase=0;
    reg valid=0, early=0, last=0;
    reg [95:0] rgb=0;
    wire [95:0] gamma_rgb;
    wire gamma_valid,gamma_early,gamma_last;
    wire [127:0] data;
    wire out_valid,out_last,out_done,out_early,error;
    wire [1:0] track_status;
    wire [33:0] total;
    integer tone,lane,channel,value,previous;
    integer color,frame,x,y,cx=120;
    integer words,lines,frames,scans,labels_checked;
    integer monitor_lane,expected_label,got_label,support_lane,support_count;
    reg [7:0] sample;

    // Use the existing ISP module, including its actual registered marker path.
    axis_gamma_rgb96 gamma_Inst(
        .I_clk(clk),.I_rst_n(rstn),.I_tlast(last),.I_tuser(early),
        .I_tdata(rgb),.I_tvalid(valid),.O_tlast(gamma_last),.O_tuser(gamma_early),
        .O_tdata(gamma_rgb),.O_tvalid(gamma_valid));
    ball_runtime #(.C_FACE_GATE(0),.C_WIDTH(WIDTH),.C_HEIGHT(HEIGHT),
        .C_X_MIN(0),.C_Y_MIN(0),.C_X_END(WIDTH),.C_Y_END(HEIGHT),
        .C_GATE_MIN(80),.C_GATE_END(160),.C_LINE(120),.C_HYST(8),.C_DEBOUNCE(2)) runtime_Inst(
        .I_clk(clk),.I_rst_n(rstn && scene_phase),.I_camera_status(48'd0),.I_keys_n(4'b1111),
        .I_rgb(gamma_rgb),.I_valid(gamma_valid),.I_user(gamma_early),.I_last(gamma_last),
        .O_data(data),.O_valid(out_valid),.O_last(out_last),.O_done(out_done),
        .O_early(out_early),.O_error(error),.O_red(),.O_green(),.O_yellow(),
        .O_total(total),.O_count_mode(),.O_gate_state(),.O_track_status(track_status));

    // Ground-truth geometry is supplied only to stimulus and the checker.
    function [1:0] geometry_label;
        input integer pixel_x,pixel_y,center_x,ball_color;
        integer dx,dy,hx,hy;
        begin
            dx=pixel_x-center_x; dy=pixel_y-CENTER_Y;
            hx=dx+20; hy=dy+20;
            geometry_label=0;
            if(dx*dx+dy*dy <= RADIUS*RADIUS && hx*hx+hy*hy > 64)
                geometry_label=ball_color;
        end
    endfunction

    function [23:0] scene_pixel;
        input integer pixel_x,pixel_y,center_x,ball_color;
        integer dx,dy,hx,hy,shade,red,green,blue;
        begin
            dx=pixel_x-center_x; dy=pixel_y-CENTER_Y;
            hx=dx+20; hy=dy+20;
            // Textured cyan background must never contribute a green candidate.
            red=60; green=120+(pixel_x+pixel_y)%7; blue=130+(pixel_x*3+pixel_y)%7;
            if(dx*dx+dy*dy <= RADIUS*RADIUS)begin
                shade=dx+RADIUS;
                case(ball_color)
                    1:begin red=45+40*shade/(2*RADIUS); green=22+23*shade/(2*RADIUS); blue=18+12*shade/(2*RADIUS); end
                    3:begin green=45+40*shade/(2*RADIUS); red=22+23*shade/(2*RADIUS); blue=18+12*shade/(2*RADIUS); end
                    default:begin red=45+40*shade/(2*RADIUS); green=43+38*shade/(2*RADIUS); blue=8+12*shade/(2*RADIUS); end
                endcase
                if(hx*hx+hy*hy <= 64)begin red=245; green=245; blue=245; end
            end
            scene_pixel={red[7:0],green[7:0],blue[7:0]};
        end
    endfunction

    task check_gamma;
        input [95:0] input_rgb;
        input input_valid,input_early,input_last;
        integer check_lane,check_channel,raw_value,corrected;
        begin
            @(negedge clk); rgb=input_rgb; valid=input_valid; early=input_early; last=input_last;
            @(posedge clk); #1;
            if(gamma_valid !== input_valid || gamma_early !== input_early || gamma_last !== input_last)
                $fatal(1,"gamma valid/early/last lost alignment");
            if(!input_valid && gamma_rgb !== 96'd0)$fatal(1,"gamma invalid bubble data");
            if(input_valid)begin
                for(check_lane=0;check_lane<4;check_lane=check_lane+1)begin
                    for(check_channel=0;check_channel<3;check_channel=check_channel+1)begin
                        raw_value=input_rgb[95-check_lane*24-check_channel*8 -: 8];
                        corrected=gamma_rgb[95-check_lane*24-check_channel*8 -: 8];
                        if(raw_value==0 && corrected!=0)$fatal(1,"gamma black endpoint");
                        if(raw_value==255 && corrected!=255)$fatal(1,"gamma white endpoint");
                        if(raw_value>0 && raw_value<192 && corrected<=raw_value)$fatal(1,"gamma did not lift shadow/midtone");
                        if(corrected<raw_value)$fatal(1,"gamma darkened a channel");
                    end
                end
            end
        end
    endtask

    // Pixel labels are compared with the known object, not a copy of classifier logic.
    always @(posedge clk)begin
        #1;
        if(!rstn || !scene_phase)begin words=0; lines=0; frames=0; scans=0; labels_checked=0; end
        else begin
            if(error)$fatal(1,"runtime video/RAM/packer error");
            if(out_valid)words=words+1;
            if(out_last)begin
                if(!out_valid)$fatal(1,"line marker without valid word");
                lines=lines+1;
            end
            if(out_done)begin
                if(!out_valid || !out_last)$fatal(1,"frame tail markers misaligned");
                frames=frames+1;
            end
            if(runtime_Inst.scan_done)scans=scans+1;
            if(runtime_Inst.front_valid)begin
                for(monitor_lane=0;monitor_lane<4;monitor_lane=monitor_lane+1)begin
                    expected_label=geometry_label(runtime_Inst.front_x+monitor_lane,runtime_Inst.front_y,cx,color);
                    support_count=0;
                    for(support_lane=0;support_lane<4;support_lane=support_lane+1)begin
                        if(geometry_label(runtime_Inst.front_x+support_lane,runtime_Inst.front_y,cx,color)==expected_label)
                            support_count=support_count+1;
                    end
                    if(support_count<2)expected_label=0;
                    got_label=runtime_Inst.front_labels[monitor_lane*2 +: 2];
                    if(got_label!=expected_label)
                        $fatal(1,"dim/cyan/white pixel label color=%0d xy=%0d,%0d expected=%0d got=%0d",color,
                            runtime_Inst.front_x+monitor_lane,runtime_Inst.front_y,expected_label,got_label);
                    labels_checked=labels_checked+1;
                end
            end
        end
    end

    initial begin
        repeat(4)@(negedge clk); rstn=1; previous=0;
        // All256 inputs on every channel/lane, with independently tagged bubbles.
        for(tone=0;tone<256;tone=tone+1)begin
            rgb=0;
            for(lane=0;lane<4;lane=lane+1)begin
                for(channel=0;channel<3;channel=channel+1)begin
                    value=(tone+lane*43+channel*29)%256;
                    rgb[95-lane*24-channel*8 -: 8]=value[7:0];
                end
            end
            check_gamma(rgb,1,tone==0,tone==255);
            sample=gamma_rgb[95:88];
            if(tone>0 && sample<previous)$fatal(1,"gamma nonmonotonic at%0d",tone);
            previous=sample;
            if(tone%17==0)check_gamma(96'h123456789abcdef012345678,0,1,1);
        end
        check_gamma({4{24'h001eff}},1,0,1);
        if(gamma_rgb !== {4{24'h0039ff}})$fatal(1,"gamma exact multichannel/lane anchor");

        for(color=1;color<=3;color=color+1)begin
            @(negedge clk); rstn=0; scene_phase=1; valid=0; early=0; last=0; rgb=0;
            repeat(4)@(negedge clk); rstn=1;
            for(frame=0;frame<3;frame=frame+1)begin
                cx=120+frame;
                @(negedge clk); early=1; valid=0; last=0;
                @(negedge clk); early=0;
                for(y=0;y<HEIGHT;y=y+1)begin
                    for(x=0;x<WIDTH;x=x+4)begin
                        rgb={scene_pixel(x,y,cx,color),scene_pixel(x+1,y,cx,color),
                             scene_pixel(x+2,y,cx,color),scene_pixel(x+3,y,cx,color)};
                        valid=1; last=(x==WIDTH-4);
                        @(negedge clk);
                        if(x==80 && y%19==0)begin valid=0; last=0; @(negedge clk); end
                    end
                end
                valid=0; early=0; last=0;
                repeat(1500)@(negedge clk);
            end
            if(track_status!==2 || !runtime_Inst.track_valid || runtime_Inst.track_color!=color)
                $fatal(1,"shaded color%0d did not acquire track: status=%0d",color,track_status);
            if(runtime_Inst.track_right-runtime_Inst.track_left+1<=160 ||
               runtime_Inst.track_bottom-runtime_Inst.track_top+1<=160)
                $fatal(1,"large ball bbox was clipped/filtered to160");
            if(runtime_Inst.track_x<cx-5 || runtime_Inst.track_x>cx+5 ||
               runtime_Inst.track_y<CENTER_Y-5 || runtime_Inst.track_y>CENTER_Y+5)
                $fatal(1,"shaded ball centroid drift");
            if(words!=3*WORDS_PER_FRAME || lines!=3*HEIGHT || frames!=3 || scans!=3 || labels_checked!=3*WIDTH*HEIGHT)
                $fatal(1,"frame/line/pixel conservation words=%0d lines=%0d frames=%0d scans=%0d labels=%0d",words,lines,frames,scans,labels_checked);
            if(total!==0)$fatal(1,"tracking mode unexpectedly counted a ball");
            $display("PASS shaded color%0d: bbox%0d,%0d-%0d,%0d center%0d,%0d labels%0d words%0d",color,
                runtime_Inst.track_left,runtime_Inst.track_top,runtime_Inst.track_right,runtime_Inst.track_bottom,
                runtime_Inst.track_x,runtime_Inst.track_y,labels_checked,words);
        end
        $display("PASS lowlight: gamma256x12 channels monotonic/lift/endpoints, bubbles/markers, three dim shaded large balls, cyan/white rejection, full RGB-to-packed-video conservation");
        $finish;
    end
    initial begin #3000000; $fatal(1,"lowlight simulation timeout"); end
endmodule
