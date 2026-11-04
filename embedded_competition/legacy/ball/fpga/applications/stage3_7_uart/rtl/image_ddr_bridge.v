// Bundled-data toggle mailbox. Request/data remain stable until the response.
// DDR accesses are single 128-bit beats; no unacknowledged multi-bit CDC bus.
module image_ddr_bridge(
 input sclk,dclk,rst_n,input start,input write,input [24:0] address,input [127:0] data,
 output busy,output reg done,output reg [127:0] result,
 output request,output write_d,output [24:0] address_d,output [127:0] data_d,
 input accepted,input read_valid,input [127:0] read_data);
 reg toggle,ack;reg held_write;reg [24:0] held_address;reg [127:0] held_data,response;
 (* ASYNC_REG="TRUE" *) reg am,asyn,rm,rs;
 reg waiting;
 assign busy=toggle!=asyn;
 assign request=rs!=ack&&!waiting;
 assign write_d=held_write;assign address_d=held_address;assign data_d=held_data;
 always @(posedge sclk or negedge rst_n)begin
 if(!rst_n)begin toggle<=0;am<=0;asyn<=0;done<=0;held_write<=0;held_address<=0;held_data<=0;result<=0;end
 else begin
 am<=ack;asyn<=am;done<=0;
 if(start&&!busy)begin held_write<=write;held_address<=address;held_data<=data;toggle<=~toggle;end
 if(busy&&am==toggle)begin result<=response;done<=1;end
 end end
 always @(posedge dclk or negedge rst_n)begin
 if(!rst_n)begin rm<=0;rs<=0;ack<=0;waiting<=0;response<=0;end
 else begin
 rm<=toggle;rs<=rm;
 if(request&&accepted)begin
 if(held_write)begin response<=0;ack<=rs;end else waiting<=1;
 end
 if(waiting&&read_valid)begin response<=read_data;ack<=rs;waiting<=0;end
 end end
endmodule

// Keep the original VI/VO burst arbitration. Auxiliary clients use idle slots.
// Each queued read has an owner tag, including reads still in the MC FIFO.
module image_ddr_arbiter(
 input clk,rst_n,input vi_busy,vo_busy,input vi_wr,input [24:0] vi_addr,input [127:0] vi_data,
 input vo_rd,input [24:0] vo_addr,output video_ready,
 input up_req,up_write,input [24:0] up_addr,input [127:0] up_data,output up_accept,up_valid,
 input pc_req,input [24:0] pc_addr,output pc_accept,pc_valid,
 output mem_wr,mem_rd,output [24:0] mem_addr,output [127:0] mem_data,input mem_ready,
 input mem_valid,input [127:0] mem_result,output video_valid,output [127:0] aux_result,
 output reg error);
 reg [1:0] owners[0:1023];reg [9:0] head,tail;reg [10:0] count;
 wire idle=!vi_busy&&!vo_busy&&!vi_wr&&!vo_rd;
 wire room=count<1000;
 wire up=idle&&up_req&&mem_ready&&room;
 wire pc=idle&&!up_req&&pc_req&&mem_ready&&room;
 assign video_ready=mem_ready&&room;
 assign up_accept=up;assign pc_accept=pc;
 assign mem_wr=vi_wr||(up&&up_write);
 assign mem_rd=vo_rd||(up&&!up_write)||pc;
 assign mem_addr=vi_wr?vi_addr:vo_rd?vo_addr:up?up_addr:pc_addr;
 assign mem_data=vi_wr?vi_data:up_data;
 wire pop=mem_valid&&count!=0;
 wire [1:0] owner=owners[head];
 assign video_valid=pop&&owner==0;
 assign up_valid=pop&&owner==1;assign pc_valid=pop&&owner==2;
 assign aux_result=mem_result;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin head<=0;tail<=0;count<=0;error<=0;end
 else begin
 if(mem_rd)begin owners[tail]<=vo_rd?0:up?1:2;tail<=tail+1'b1;end
 if(pop)head<=head+1'b1;
 case({mem_rd,pop})2'b10:count<=count+1'b1;2'b01:count<=count-1'b1;default:begin end endcase
 if((mem_valid&&count==0)||(mem_rd&&count==1024)||(mem_wr&&mem_rd))error<=1;
 end end
endmodule
