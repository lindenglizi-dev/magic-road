module color_traffic_runtime #(parameter DEBOUNCE_CYCLES=2100000)(
 input wire I_clk,I_rst_n,input wire [3:0] I_keys_n,
 input wire [95:0] I_rgb,input wire I_valid,I_user,I_last,
 output wire [127:0] O_data,output wire O_valid,O_last,O_done,
 output reg O_early,output wire O_error,output wire [2:0] result
);
 reg [3:0] sync0,sync1,stable;
 reg [21:0] count[0:3];
 reg traffic,strict,mask;integer k;
 // Use the detector's single frame snapshot; do not duplicate voting/reset logic.
 wire frame_traffic;wire [2:0] display_result;
 always @(posedge I_clk or negedge I_rst_n)begin
 if(!I_rst_n)begin
 sync0<=15;sync1<=15;stable<=15;traffic<=1;strict<=0;mask<=0;O_early<=0;
 for(k=0;k<4;k=k+1)count[k]<=0;
 end else begin
 sync0<=I_keys_n;sync1<=sync0;O_early<=I_user;
 for(k=0;k<4;k=k+1)begin
 if(sync1[k]==stable[k])count[k]<=0;
 else if(count[k]==DEBOUNCE_CYCLES-1)begin
 count[k]<=0;stable[k]<=sync1[k];
 if(!sync1[k])case(k)
 0:traffic<=~traffic;1:mask<=~mask;2:strict<=~strict;
 3:begin traffic<=1;mask<=0;strict<=0;end
 endcase
 end else count[k]<=count[k]+1'b1;
 end end end
 wire [95:0] rgb;wire v,u,l,d,core_error,pack_error;
 color_traffic_core u_core(.clk(I_clk),.rst_n(I_rst_n),.rgb(I_rgb),.valid(I_valid),.early(I_user),
 .traffic(traffic),.strict(strict),.mask(mask),.out_rgb(rgb),.out_valid(v),.out_user(u),.out_last(l),.out_done(d),
 .result(result),.frame_result(),.O_display_result(display_result),.O_display_traffic(frame_traffic),
 .red_count(),.yellow_count(),.green_count(),.blue_count(),.error(core_error));
 wire [95:0] osd_rgb;wire osd_v,osd_u,osd_l,osd_d;
 color_mode_osd u_osd(.clk(I_clk),.rst_n(I_rst_n),.I_rgb(rgb),
 .I_valid(v),.I_user(u),.I_last(l),.I_done(d),.I_mode({3'b0,frame_traffic}),.I_result(display_result),
 .O_rgb(osd_rgb),.O_valid(osd_v),.O_user(osd_u),.O_last(osd_l),.O_done(osd_d));
 rgb96_pack128_valid u_pack(.I_clk(I_clk),.I_rst_n(I_rst_n),.I_rgb(osd_rgb),.I_valid(osd_v),.I_user(osd_u),.I_last(osd_l),.I_done(osd_d),
 .O_data(O_data),.O_valid(O_valid),.O_last(O_last),.O_done(O_done),.O_error(pack_error));
 assign O_error=core_error|pack_error;
endmodule
