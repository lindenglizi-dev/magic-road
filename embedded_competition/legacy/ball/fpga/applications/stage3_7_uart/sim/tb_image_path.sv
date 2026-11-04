`timescale 1ns/1ps
// Scaled geometry to exercise identical counters/CRC/CDC; not board DDR emulation.
module tb_image_path;
 localparam W=48,H=6,N=W*H*2,B0=1024,B1=1312;
 reg clk=0,dclk=0,vclk=0;always #10 clk=~clk;always #3.5 dclk=~dclk;always #4.83 vclk=~vclk;
 reg [127:0] return_data=0;
 reg rst=0,start=0;reg [7:0] cmd=0,len=0;reg [255:0] header=0;reg [15:0] sig=1;
 wire [7:0] addr;reg [7:0] payload[0:239];wire done;wire [7:0] error,reply_len;wire [63:0] reply;
 wire ms,mw,mb,md;wire [24:0] ma;wire [127:0] mdata,mresult;
 wire pub,pbank,pack;wire valid_sys;wire [31:0] uploaded;
 image_upload_engine #(.WIDTH(W),.HEIGHT(H),.BASE0(B0),.BASE1(B1)) upload(
 .clk(clk),.rst_n(rst),.ready(1'b1),.start(start),.command(cmd),.length(len),.header(header),.signature(sig),
 .payload_addr(addr),.payload_data(payload[addr]),.done(done),.error(error),.reply_length(reply_len),.reply(reply),
 .mem_start(ms),.mem_write(mw),.mem_address(ma),.mem_data(mdata),.mem_busy(mb),.mem_done(md),.mem_result(mresult),
 .publish(pub),.publish_bank(pbank),.publish_ack(pack),.valid_image(valid_sys),.uploaded(uploaded));
 wire uq,uw,ua,uv;wire [24:0] uaddr;wire [127:0] udata;
 image_ddr_bridge ub(.sclk(clk),.dclk(dclk),.rst_n(rst),.start(ms),.write(mw),.address(ma),.data(mdata),.busy(mb),.done(md),.result(mresult),
 .request(uq),.write_d(uw),.address_d(uaddr),.data_d(udata),.accepted(ua),.read_valid(uv),.read_data(return_data));
 wire ps,pb,pd;wire [24:0] pa;wire [127:0] presult;wire pq,paccept,pvalid;wire [24:0] paddr;
 image_ddr_bridge rb(.sclk(vclk),.dclk(dclk),.rst_n(rst),.start(ps),.write(1'b0),.address(pa),.data(128'd0),.busy(pb),.done(pd),.result(presult),
 .request(pq),.write_d(),.address_d(paddr),.data_d(),.accepted(paccept),.read_valid(pvalid),.read_data(return_data));
 wire valid_image,in_frame;wire [95:0] rgb;wire vv,early,last;
 reg select_pc=0;reg runtime_busy=0;integer drain=0;
 pc_image_replay #(.IN_W(W),.IN_H(H),.OUT_W(32),.OUT_H(4),.BASE0(B0),.BASE1(B1),.FRAME_GAP(100)) replay(
 .clk(vclk),.rst_n(rst),.selected(select_pc),.runtime_busy(runtime_busy),.publish(pub),.publish_bank(pbank),.publish_ack(pack),.image_valid(valid_image),.in_frame(in_frame),
 .mem_start(ps),.mem_address(pa),.mem_busy(pb),.mem_done(pd),.mem_result(presult),.rgb(rgb),.valid(vv),.early(early),.last(last));
 wire mem_wr,mem_rd;wire [24:0] mem_addr;wire [127:0] mem_data;wire video_ready,video_valid,arb_error;wire [127:0] aux_data;
 reg vi_busy=0,vo_busy=0,vi_wr=0,vo_rd=0;reg [24:0] vi_addr=0,vo_addr=0;
 reg mem_ready=1,return_valid=0;
 image_ddr_arbiter arb(.clk(dclk),.rst_n(rst),.vi_busy(vi_busy),.vo_busy(vo_busy),.vi_wr(vi_wr),.vi_addr(vi_addr),.vi_data(128'h1234),
 .vo_rd(vo_rd),.vo_addr(vo_addr),.video_ready(video_ready),.up_req(uq),.up_write(uw),.up_addr(uaddr),.up_data(udata),.up_accept(ua),.up_valid(uv),
 .pc_req(pq),.pc_addr(paddr),.pc_accept(paccept),.pc_valid(pvalid),.mem_wr(mem_wr),.mem_rd(mem_rd),.mem_addr(mem_addr),.mem_data(mem_data),.mem_ready(mem_ready),
 .mem_valid(return_valid),.mem_result(return_data),.video_valid(video_valid),.aux_result(aux_data),.error(arb_error));
 reg [127:0] memory[0:2047];reg [24:0] reads[0:31];integer rh=0,rt=0,cycle=0,video_responses=0,write_count=0;
 always @(negedge dclk)begin
 if(rst)begin
 cycle=cycle+1;mem_ready=cycle%9!=0;
 vi_busy=cycle%61<12;vo_busy=cycle%61>=12&&cycle%61<24;
 // Repeated unrelated display reads prove owner tags prevent FIFO contamination.
 vo_rd=cycle%61==14&&video_ready;vo_addr=0;
 end end
 always @(posedge dclk)begin
 return_valid<=0;
 if(rst)begin
 if(mem_wr)begin memory[mem_addr>>3]<=mem_data;write_count=write_count+1;end
 if(mem_rd)begin reads[rt%32]=mem_addr;rt=rt+1;end
 if(cycle%7==0&&rh<rt)begin return_valid<=1;return_data<=memory[reads[rh%32]>>3];rh=rh+1;end
 if(video_valid)begin video_responses=video_responses+1;if(return_data!==128'hdeadbeef)$fatal(1,"read owner routed wrong data");end
 if(arb_error)$fatal(1,"DDR arbiter invariant");
 end end
 function automatic [15:0] pixel(input integer x,input integer y);
 begin pixel={5'(x%32),6'(y*7),5'((x+y)%32)};end endfunction
 function automatic [7:0] image_byte(input integer n);
 reg [15:0] p;begin p=pixel((n/2)%W,(n/2)/W);return n%2?p[15:8]:p[7:0];end endfunction
 function automatic [31:0] add_crc(input [31:0] old,input [7:0] b);
 reg [31:0] c;begin c=old^b;repeat(8)c=c[0]?(c>>1)^32'hedb88320:c>>1;return c;end endfunction
 function automatic [23:0] expand(input [15:0] v);
 return {v[15:11],v[15:13],v[10:5],v[10:9],v[4:0],v[4:2]};endfunction
 task issue(input [7:0] c,l,input [255:0] h,input [7:0] expected);
 begin
 @(negedge clk);cmd=c;len=l;header=h;sig=sig+1;start=1;
 @(negedge clk);start=0;wait(done);if(error!=expected)$fatal(1,"image cmd=%h error=%d expected=%d",c,error,expected);
 @(negedge clk);
 end endtask
 integer groups=0,frames=0,x,y,j;reg checking=0;reg [23:0] expected_rgb;
 always @(posedge vclk)begin
 #1;
 if(early)begin runtime_busy=1;groups=0;end
 if(vv)begin
 for(j=0;j<4;j=j+1)begin
 x=(groups%8)*4+j;y=groups/8;
 expected_rgb=expand(pixel(x*3/2,y*3/2));
 if(rgb[95-j*24-:24]!==expected_rgb)$fatal(1,"replay RGB565/stride/scale x=%d y=%d got=%h expected=%h",x,y,rgb[95-j*24-:24],expected_rgb);
 end
 if(last!==(groups%8==7))$fatal(1,"replay line marker");groups=groups+1;
 if(groups==32)begin frames=frames+1;drain=20;end
 end
 if(drain>0)begin drain=drain-1;if(drain==0)runtime_busy=0;end
 end
 integer i,pos,n;reg [31:0] crc;
 initial begin
 memory[0]=128'hdeadbeef;repeat(5)@(negedge clk);rst=1;
 crc=32'hffffffff;for(i=0;i<N;i=i+1)crc=add_crc(crc,image_byte(i));crc=crc^32'hffffffff;
 issue(8'h30,17,{120'd0,crc,32'(N),8'd1,16'(H),16'(W),32'd123},0);
 // Incomplete END must not expose a new image.
 issue(8'h32,8,{192'd0,crc,32'd123},6);if(valid_image)$fatal(1,"partial image visible");
 for(pos=0;pos<N;pos=pos+n)begin
 n=N-pos>224?224:N-pos;
 for(i=0;i<n;i=i+1)payload[i+8]=image_byte(pos+i);
 issue(8'h31,n+8,{192'd0,32'(pos),32'd123},0);
 if(reply!=={32'(pos+n),32'd123})$fatal(1,"offset ACK");
 end
 sig=sig-1;issue(8'h31,n+8,{192'd0,32'(N-n),32'd123},0);
 if(write_count!=N/16)$fatal(1,"retry wrote duplicate data");
 issue(8'h32,8,{192'd0,crc,32'd123},0);
 if(!valid_image||!valid_sys||uploaded!=N)$fatal(1,"commit before fence/publication");
 select_pc=1;wait(frames==2);select_pc=0;wait(!in_frame);
 // Abort a new upload: the committed image remains available and repeatable.
 issue(8'h30,17,{120'd0,crc,32'(N),8'd1,16'(H),16'(W),32'd124},0);
 issue(8'h33,4,{224'd0,32'd124},0);if(!valid_image)$fatal(1,"abort erased old image");
 // A fully received but corrupt image must never replace the committed bank.
 issue(8'h30,17,{120'd0,crc,32'(N),8'd1,16'(H),16'(W),32'd125},0);
 for(pos=0;pos<N;pos=pos+n)begin
 n=N-pos>224?224:N-pos;
 for(i=0;i<n;i=i+1)payload[i+8]=image_byte(pos+i)^(pos+i==0?8'd1:8'd0);
 issue(8'h31,n+8,{192'd0,32'(pos),32'd125},0);
 end
 issue(8'h32,8,{192'd0,crc,32'd125},7);
 select_pc=1;wait(frames==3);select_pc=0;
 if(video_responses==0||write_count!=N/8)$fatal(1,"DDR coverage");
 $display("PASS image path: native-format bytes, DDR CDC/backpressure, read-owner isolation, CRC commit fence, 3:2 replay/line markers, repeated image and abort preservation");$finish;
 end
 initial begin #20000000;$fatal(1,"image test timeout");end
endmodule
