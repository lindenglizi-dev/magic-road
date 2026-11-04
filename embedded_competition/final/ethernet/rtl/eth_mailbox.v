                                                                                    
module eth_rx_mailbox(
 input eclk,sclk,rst_n,input [7:0] data,input valid,input [15:0] length,
 output reg [7:0] sdata,output reg svalid);
 reg [7:0] mem[0:255]; /* fehdl force_ram=1, ram_style="dram" */
 reg [8:0] count,size,local_size,index;reg [15:0] expected;reg req,ack,vd,accept,bad;
 (* ASYNC_REG="TRUE" *) reg [1:0] reset_e,reset_s;
 always @(posedge eclk or negedge rst_n)if(!rst_n)reset_e<=0;else reset_e<={reset_e[0],1'b1};
 always @(posedge sclk or negedge rst_n)if(!rst_n)reset_s<=0;else reset_s<={reset_s[0],1'b1};
 (* ASYNC_REG="TRUE" *) reg am,as,rm,rs;
 wire start_ok=req==as&&length<=250&&length>=10;
 wire [7:0] write_address=vd?count[7:0]:8'd0;
 always @(posedge eclk)
 if(valid&&(!vd?start_ok:(accept&&count<250)))mem[write_address]<=data;
 wire [7:0] read_address=(rs!=ack&&index<local_size-1)?index[7:0]+1'b1:8'd0;
 reg [7:0] prefetched;
 always @(posedge sclk)prefetched<=mem[read_address];
 always @(posedge eclk or negedge reset_e[1])begin
 if(!reset_e[1])begin expected<=0;count<=0;size<=0;req<=0;vd<=0;accept<=0;bad<=0;am<=0;as<=0;end
 else begin
 am<=ack;as<=am;vd<=valid;
 if(valid&&!vd)begin
 expected<=length;accept<=req==as&&length<=250&&length>=10;bad<=0;count<=1;
 end else if(valid)begin
 if(count<250)count<=count+1'b1;else bad<=1;
 end
 if(!valid&&vd&&accept&&!bad&&count==expected)begin size<=count;req<=~req;end
 end end
 always @(posedge sclk or negedge reset_s[1])begin
 if(!reset_s[1])begin ack<=0;rm<=0;rs<=0;local_size<=0;index<=0;sdata<=0;svalid<=0;end
 else begin
 rm<=req;rs<=rm;svalid<=0;
                                                                     
                                                                   
 if(rm!=rs)local_size<=size;
 if(rs!=ack)begin
 sdata<=prefetched;svalid<=1;
 if(index==local_size-1)begin index<=0;ack<=rs;end else index<=index+1'b1;
 end
 end end
endmodule

                                                                           
module eth_reply_mailbox(
 input sclk,eclk,rst_n,start,input [7:0] command,seq,length,payload_data,output [5:0] payload_index,
 output busy,output available,input pop,
 output [7:0] ecommand,eseq,elength,input [5:0] read_index,output reg [7:0] epayload_byte);
                                                                        
                                                                          
 reg [7:0] payload_bytes[0:63]; /* fehdl force_ram=1, ram_style="dram" */
 reg filling;reg [5:0] write_index;
 reg req,ack;reg [23:0] received;
 (* ASYNC_REG="TRUE" *) reg [1:0] reset_e,reset_s;
 always @(posedge eclk or negedge rst_n)if(!rst_n)reset_e<=0;else reset_e<={reset_e[0],1'b1};
 always @(posedge sclk or negedge rst_n)if(!rst_n)reset_s<=0;else reset_s<={reset_s[0],1'b1};
 (* ASYNC_REG="TRUE" *) reg am,as,rm,rs;
 assign busy=filling || req!=as;assign available=rs!=ack;
 assign {elength,eseq,ecommand}=received[23:0];
 assign payload_index=write_index;
                                                                     
 always @(posedge sclk)if(filling)payload_bytes[write_index]<=payload_data;
 always @(posedge eclk)epayload_byte<=payload_bytes[read_index];
 always @(posedge sclk or negedge reset_s[1])begin
 if(!reset_s[1])begin req<=0;am<=0;as<=0;filling<=0;write_index<=0;end
 else begin
 am<=ack;as<=am;
 if(start&&!busy&&length<=64)begin
  if(length==0)req<=~req;
  else begin filling<=1;write_index<=0;end
 end else if(filling)begin
  if(write_index==length-1'b1)begin filling<=0;req<=~req;end
  else write_index<=write_index+1'b1;
 end
 end end
 always @(posedge eclk or negedge reset_e[1])begin
 if(!reset_e[1])begin ack<=0;rm<=0;rs<=0;received<=0;end
 else begin
 rm<=req;rs<=rm;
                                                                           
 if(rm!=rs)received<={length,seq,command};
 if(pop&&available)ack<=rs;
 end end
endmodule
