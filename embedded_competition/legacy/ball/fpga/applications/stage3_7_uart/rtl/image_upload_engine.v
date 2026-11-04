// Native 1920x1080 RGB565, two banks in unused 16-bit-word DDR address space.
// Bank0 [25165824,27239424), bank1 [27239424,29313024); DDR limit33554432.
module image_upload_engine #(parameter WIDTH=1920,HEIGHT=1080,
 parameter BASE0=25165824,BASE1=27239424)(
 input clk,rst_n,ready,input start,input [7:0] command,length,input [255:0] header,input [15:0] signature,
 output reg [7:0] payload_addr,input [7:0] payload_data,
 output reg done,output reg [7:0] error,reply_length,output reg [63:0] reply,
 output reg mem_start,output reg mem_write,output reg [24:0] mem_address,output reg [127:0] mem_data,
 input mem_busy,mem_done,input [127:0] mem_result,
 output reg publish,output reg publish_bank,input publish_ack,
 output reg valid_image,output reg [31:0] uploaded);
 localparam BYTES=WIDTH*HEIGHT*2;
 reg [3:0] state;reg active,bank,committed_bank;
 reg [31:0] id,expected_crc,running_crc,offset,next_offset;
 reg [31:0] last_offset;reg [15:0] last_signature;reg [7:0] last_length;
 reg [7:0] data_length,index;reg [3:0] lane;reg [127:0] word_data,last_word;
 reg [24:0] address,last_address;
 (* ASYNC_REG="TRUE" *) reg pm,ps;
 function [31:0] crc_add;
 input [31:0] old;input [7:0] b;reg [31:0] c;integer k;
 begin c=old^b;for(k=0;k<8;k=k+1)c=c[0]?(c>>1)^32'hedb88320:c>>1;crc_add=c;end endfunction
 task finish;
 input [7:0] code;input [7:0] size;input [63:0] value;
 begin error<=code;reply_length<=size;reply<=value;done<=1;state<=0;end endtask
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin
 state<=0;active<=0;bank<=0;committed_bank<=1;id<=0;expected_crc<=0;running_crc<=32'hffffffff;
 offset<=0;uploaded<=0;last_offset<=32'hffffffff;last_signature<=0;last_length<=0;
 data_length<=0;index<=0;lane<=0;word_data<=0;last_word<=0;address<=0;last_address<=0;
 payload_addr<=0;done<=0;error<=0;reply_length<=0;reply<=0;
 mem_start<=0;mem_write<=0;mem_address<=0;mem_data<=0;publish<=0;publish_bank<=0;pm<=0;ps<=0;valid_image<=0;
 end else begin
 pm<=publish_ack;ps<=pm;done<=0;mem_start<=0;
 case(state)
 0:if(start)begin
 case(command)
 8'h30:if(length!=17)finish(2,0,0);
 else if(!ready)finish(8,0,0);
 else if(header[47:32]!=WIDTH||header[63:48]!=HEIGHT||header[71:64]!=1||header[103:72]!=BYTES)finish(3,0,0);
 else if(active&&header[31:0]==id)begin
 if(header[135:104]!=expected_crc)finish(4,0,0);else finish(0,4,{32'd0,id});
 end else begin
 id<=header[31:0];expected_crc<=header[135:104];active<=1;bank<=~committed_bank;
 offset<=0;uploaded<=0;running_crc<=32'hffffffff;last_offset<=32'hffffffff;
 finish(0,4,{32'd0,header[31:0]});
 end
 8'h31:if(length<24||length>232||(length-8)%16!=0)finish(2,0,0);
 else if(!active||header[31:0]!=id)finish(8,0,0);
 else if(header[63:32]==last_offset&&length==last_length&&signature==last_signature)finish(0,8,{offset,id});
 else if(header[63:32]!=offset||offset+(length-8)>BYTES)finish(6,0,0);
 else begin
 data_length<=length-8;next_offset<=offset+(length-8);index<=0;lane<=0;word_data<=0;payload_addr<=8;
 address<=(bank?BASE1:BASE0)+(offset>>1);state<=1;
 last_offset<=offset;last_length<=length;last_signature<=signature;
 end
 8'h32:if(length!=8)finish(2,0,0);
 else if(!active||header[31:0]!=id)finish(8,0,0);
 else if(offset!=BYTES)finish(6,0,0);
 else if((running_crc^32'hffffffff)!=expected_crc||header[63:32]!=expected_crc)begin active<=0;finish(7,0,0);end
 else if(!mem_busy)begin
 // Ordered readback fences the queued writes before bank publication.
 mem_address<=last_address;mem_write<=0;mem_start<=1;state<=5;
 end
 8'h33:if(length!=4)finish(2,0,0);
 else if(active&&header[31:0]!=id)finish(8,0,0);
 else begin active<=0;finish(0,4,{32'd0,header[31:0]});end
 default:finish(1,0,0);
 endcase end
 1:begin
 word_data[lane*8+:8]<=payload_data;running_crc<=crc_add(running_crc,payload_data);
 index<=index+1'b1;payload_addr<=payload_addr+1'b1;lane<=lane+1'b1;
 if(lane==15)state<=2;
 end
 2:if(!mem_busy)begin mem_address<=address;mem_data<=word_data;mem_write<=1;mem_start<=1;state<=3;end
 3:if(mem_done)begin
 last_word<=word_data;last_address<=address;address<=address+8;word_data<=0;
 if(index==data_length)begin offset<=next_offset;uploaded<=next_offset;finish(0,8,{next_offset,id});end else state<=1;
 end
 5:if(mem_done)begin
 if(mem_result!=last_word)begin active<=0;finish(7,0,0);end
 else begin publish_bank<=bank;publish<=~publish;state<=6;end
 end
 6:if(ps==publish)begin committed_bank<=bank;active<=0;valid_image<=1;finish(0,8,{expected_crc,id});end
 default:state<=0;
 endcase
 end end
endmodule
