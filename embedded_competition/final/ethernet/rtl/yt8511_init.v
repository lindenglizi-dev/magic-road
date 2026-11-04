module eth_mdio_master(
 input clk,rst_n,start,read,input [4:0] phy,register,input [15:0] wdata,
 output reg busy,done,output reg [15:0] rdata,output reg mdc,inout mdio);
 reg [63:0] bits;reg [6:0] index;reg [3:0] divider;reg reading;
 assign mdio=busy&&!(reading&&index>=46)?bits[63-index]:1'bz;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin busy<=0;done<=0;rdata<=0;mdc<=0;bits<=0;index<=0;divider<=0;reading<=0;end
 else begin
 done<=0;
 if(start&&!busy)begin
 bits<={32'hffffffff,2'b01,(read?2'b10:2'b01),phy,register,2'b10,wdata};
 reading<=read;index<=0;divider<=0;mdc<=0;busy<=1;rdata<=0;
 end else if(busy)begin
 if(divider==9)begin
 divider<=0;mdc<=~mdc;
 if(!mdc)begin if(reading&&index>=48)rdata<={rdata[14:0],mdio};end
 else if(index==63)begin busy<=0;done<=1;mdc<=0;end
 else index<=index+1'b1;
 end else divider<=divider+1'b1;
 end
 end end
endmodule

                                                                                     
                                                                            
                                                                              
module yt8511_init #(parameter RESET_CYCLES=500000,STARTUP_CYCLES=3000000,POLL_CYCLES=2500000)(
 input clk,rst_n,output phy_rst_n,output mdc,inout mdio,
 output ready,output [31:0] status);
 reg [4:0] state,phy,regaddr;reg [21:0] timer;
 reg start,read,configured,fault;reg [15:0] wdata,link;
 wire busy,done;wire [15:0] rdata;
 assign phy_rst_n=timer>=RESET_CYCLES||state!=0;
 assign ready=configured&&link[10]&&link[11]&&link[13]&&link[15:14]==2'b10;
 assign status={configured,fault,ready,phy,8'd0,link};
 eth_mdio_master u_mdio(.clk(clk),.rst_n(rst_n),.start(start),.read(read),.phy(phy),.register(regaddr),
 .wdata(wdata),.busy(busy),.done(done),.rdata(rdata),.mdc(mdc),.mdio(mdio));
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin state<=0;phy<=0;regaddr<=0;timer<=0;start<=0;read<=1;configured<=0;fault<=0;wdata<=0;link<=0;end
 else begin
 start<=0;
 case(state)
 0:if(timer==STARTUP_CYCLES-1)begin timer<=0;state<=1;end else timer<=timer+1'b1;
 1:begin regaddr<=3;read<=1;start<=1;state<=2;end
 2:if(done)begin
 if((rdata&16'hfff0)==16'h0100)begin state<=3;fault<=0;end
 else if(phy==31)begin phy<=0;fault<=1;state<=20;timer<=0;end
 else begin phy<=phy+1'b1;state<=1;end
 end
 3:begin regaddr<=5'h1e;wdata<=16'h000c;read<=0;start<=1;state<=4;end
 4:if(done)begin regaddr<=5'h1f;read<=1;start<=1;state<=5;end
 5:if(done)begin wdata<=(rdata&16'hff0e)|16'h00f1;read<=0;start<=1;state<=6;end
 6:if(done)begin read<=1;start<=1;state<=7;end
 7:if(done)begin
 if((rdata&16'h00f1)!=16'h00f1)begin fault<=1;timer<=0;state<=20;end
 else begin regaddr<=4;read<=1;start<=1;state<=8;end
 end
 8:if(done)begin wdata<=rdata&16'hfe1f;read<=0;start<=1;state<=9;end
 9:if(done)begin regaddr<=9;read<=1;start<=1;state<=10;end
 10:if(done)begin wdata<=(rdata&16'hfcff)|16'h0200;read<=0;start<=1;state<=11;end
 11:if(done)begin regaddr<=0;wdata<=16'h1200;read<=0;start<=1;state<=12;end
 12:if(done)begin configured<=1;timer<=0;state<=13;end
 13:if(timer==POLL_CYCLES-1)begin timer<=0;regaddr<=5'h11;read<=1;start<=1;state<=14;end else timer<=timer+1'b1;
 14:if(done)begin link<=rdata;state<=13;end
 20:if(timer==STARTUP_CYCLES-1)begin timer<=0;state<=1;end else timer<=timer+1'b1;
 default:state<=0;
 endcase
 end end
endmodule
