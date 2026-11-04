                                                                 
                                                                               
module eth_video_queue #(parameter W=1280,H=720,CHUNK_PIXELS=640,FRAME_DIV=2)(
 input pclk,tclk,rst_n,enable,vsync,de,input [23:0] rgb,
 input [15:0] view_tag,
 output available,input pop,input [10:0] byte_index,
 output [7:0] byte_data,output reg [31:0] dropped);
 (* ASYNC_REG="TRUE" *) reg [1:0] pixel_reset;
 always @(posedge pclk or negedge rst_n)if(!rst_n)pixel_reset<=0;else pixel_reset<={pixel_reset[0],1'b1};
 wire pixel_rst_n=pixel_reset[1];
 localparam CHUNKS=W/CHUNK_PIXELS*H;
 localparam [15:0] WIDTH=W,HEIGHT=H,COUNT=CHUNKS,BYTES=CHUNK_PIXELS*2;
                                                                           
                                                                          
 /* fehdl force_ram=1, ram_style="bram" */ reg [15:0] block_pixels[0:2047];
 /* fehdl force_ram=1, ram_style="bram" */ reg [15:0] tail_pixels[0:4*CHUNK_PIXELS-2049];
 reg [31:0] ids[0:3];reg [15:0] chunks[0:3];
 reg [15:0] tags[0:3];reg [15:0] frame_tag;
 reg [2:0] wp,wg,rp,rg;
 (* ASYNC_REG="TRUE" *) reg [2:0] rm,rs,wm,ws;
 (* ASYNC_REG="TRUE" *) reg em,es;
 reg vsd,capture,skip_chunk;reg [11:0] x,y;reg [10:0] cp;
 reg [31:0] frame;reg [15:0] chunk;reg [7:0] divider;
 wire full=wg=={~rs[2:1],rs[0]};
 wire [2:0] wp_next=wp+1'b1,rp_next=rp+1'b1;
 wire [15:0] rgb565={rgb[23:19],rgb[15:10],rgb[7:3]};
 wire [11:0] write_address=wp[1:0]*CHUNK_PIXELS+cp;
                                                                    
 always @(posedge pclk)
   if(pixel_rst_n&&de&&capture&&!(cp==0?full:skip_chunk))
     if(write_address<2048)block_pixels[write_address[10:0]]<=rgb565;
     else tail_pixels[write_address[8:0]]<=rgb565;
 always @(posedge pclk or negedge pixel_rst_n)begin
 if(!pixel_rst_n)begin wp<=0;wg<=0;rm<=0;rs<=0;em<=0;es<=0;vsd<=0;
 frame_tag<=0;capture<=0;skip_chunk<=0;x<=0;y<=0;cp<=0;frame<=0;chunk<=0;divider<=0;dropped<=0;end
 else begin
 rm<=rg;rs<=rm;em<=enable;es<=em;vsd<=vsync;
 if(vsync&&!vsd)begin
 x<=0;y<=0;cp<=0;chunk<=0;frame<=frame+1'b1;
 capture<=es&&(divider==0);divider<=divider==FRAME_DIV-1?0:divider+1'b1;
 end else if(de)begin
 if(x==0 && y==0)frame_tag<=view_tag;
 if(cp==0)begin skip_chunk<=full;if(capture&&full)dropped<=dropped+1'b1;end
 if(cp==CHUNK_PIXELS-1)begin
 cp<=0;chunk<=chunk+1'b1;
 if(capture&&!skip_chunk)begin
 ids[wp[1:0]]<=frame;chunks[wp[1:0]]<=chunk;tags[wp[1:0]]<=frame_tag;
 wp<=wp_next;wg<=(wp_next>>1)^wp_next;
 end
 end else cp<=cp+1'b1;
 if(x==W-1)begin x<=0;if(y==H-1)begin y<=0;capture<=0;end else y<=y+1'b1;end
 else x<=x+1'b1;
 end
 end end
 assign available=rg!=ws;
 always @(posedge tclk or negedge rst_n)begin
 if(!rst_n)begin rp<=0;rg<=0;wm<=0;ws<=0;end
 else begin wm<=wg;ws<=wm;if(pop&&available)begin rp<=rp_next;rg<=(rp_next>>1)^rp_next;end end end
                                                                                    
                                                                               
 wire [10:0] pixel_index=byte_index<22?0:{1'b0,(byte_index[10:1]-10'd11)};
 wire [11:0] read_target=rp[1:0]*CHUNK_PIXELS+(pixel_index<CHUNK_PIXELS?pixel_index:0);
 reg [15:0] block_pixel,tail_pixel;reg tail_select;reg [11:0] read_address;
 always @(posedge tclk)begin
 read_address<=read_target;
 block_pixel<=block_pixels[read_address[10:0]];
 tail_pixel<=tail_pixels[read_address[8:0]];
 tail_select<=read_address>=2048;
 end
 wire [15:0] pixel=tail_select?tail_pixel:block_pixel;
 wire [191:0] header={tags[rp[1:0]],BYTES,COUNT,chunks[rp[1:0]],
                       HEIGHT,WIDTH,ids[rp[1:0]],16'd24,8'd1,8'd2,32'h4d495848};
 assign byte_data=byte_index<24?header[byte_index*8+:8]:(byte_index[0]?pixel[15:8]:pixel[7:0]);
endmodule
