module isp_top #(parameter C_PREDECODE_MODE_CHANGE=0) (
    input wire [191:0] I_application_config,
    input wire I_application_commit,I_view_target,
    input wire I_application_mode_change,
    output wire O_view_actual,O_view_commit,
    output wire [13:0] O_view_revision,
    input wire I_gamma_we,I_editor_we,I_gamma_commit,I_editor_commit,
    input wire [7:0] I_curve_address,I_curve_value,
    output wire O_pipeline_busy,
    output wire [7:0] O_seg_select_n,
    output wire [7:0] O_seg_segments_n,
    input wire [3:0] I_keys_n,
    input wire [47:0] I_camera_status,
    output wire [1:0] O_camera_step,                                       
    output wire [1535:0] O_status_snapshot,
    output wire O_status_valid,
    input wire [191:0] I_panel_settings,
    input wire I_panel_clear,
    output wire O_panel_early,
    output wire [31:0] O_good,
    output wire [31:0] O_bad,
    input 			axi4s_video_aclk,
    input 			I_rst_n			,
    input 			I_tlast			,
    input 			I_tuser			,
    input [39:0] 	I_tdata			,
    input 			I_tvalid		,
    input [9:0] 	I_tdest			,
    input 			O_tready		,
    output [127:0] 	O_tdata			,
    output 			O_tlast			,
    output 			O_tuser			,
    output 			O_tvalid		,
    output 			I_tready
);
wire app_last, app_done, app_error;
    wire gamma_valid,gamma_early,gamma_last,core_done,core_early,core_error;
wire awb_ready;
wire [47:0] application_camera_status={I_camera_status[47:40],awb_ready,I_camera_status[38:0]};
 
wire         m_aixs_tvalid;  //synthesis keep 
  wire [127:0] m_aixs_tdata;  //synthesis keep 
  wire         m_aixs_tuser;  //synthesis keep 
  wire         m_aixs_tlast;  //synthesis keep 
  wire         m_aixs_tready;  //synthesis keep 
  
  wire [ 95:0] m_aixs_tdata_96;  //synthesis keep 


  wire         awb_O_tlast;  //synthesis keep 
  wire         awb_O_tuser;  //synthesis keep 
  wire [95:0] awb_raw_rgb;
  wire [ 95:0] awb_O_tdata;  //synthesis keep 
  wire         awb_O_tvalid;  //synthesis keep 
  wire         awb_O_tready;  //synthesis keep 

  wire         awb_O_tuser_128;  //synthesis keep 
  wire         awb_O_tvalid_128;  //synthesis keep 
  wire [127:0] awb_O_tdata_128;  //synthesis keep 

  assign awb_O_tready = O_tready;
  assign O_tdata  = awb_O_tdata_128;
  assign O_tlast  = app_last    ;
  assign O_tuser  = core_early    ;
  assign O_tvalid = awb_O_tvalid_128   ;
  
                                    
                                   
                                       
                                       
                                       
 
 
demosaic #(
    .IMG_HEIGHT          (720 ),  // 图像高度
    .IMG_WIDTH           (1280),  // 图像宽度
    .data_complete_delay (50  ),
    .BAYER_MODE          ("BGGR")
)
u_demosaic
(
    .I_clk   			(axi4s_video_aclk)	,   // 时钟信号
    .I_rst_n 			(I_rst_n)	,   // 复位信号，低有效
    .axi4s_video_tdata 	(I_tdata)	,  // AXI4-Stream视频数据
    .axi4s_video_tdest 	(I_tdest)	,
    .axi4s_video_tlast 	(I_tlast)	,  // 行结束信号
    .axi4s_video_tvalid	(I_tvalid)	,  // 数据有效信号
    .axi4s_video_tuser 	(I_tuser)	,  // 帧开始信号
    .axi4s_video_tready	(I_tready)	,  // 从模块准备好接受数据
    .O_tlast  			(m_aixs_tlast)	,  // 输出行结束信号
    .O_tuser  			(m_aixs_tuser)	,  // 输出帧开始信号
    .O_tdata  			(m_aixs_tdata)	,  // 输出数据
    .O_tvalid 			(m_aixs_tvalid)	,  // 输出数据有效信号
    .O_tready   		(m_aixs_tready)	   // 输出数据准备好信号
);
 
data128_96 u_data128_96 (
    .I_tdata(m_aixs_tdata),
    .O_tdata(m_aixs_tdata_96)
);

awb #(
    .IMG_HEIGHT(720 ),
    .IMG_WIDTH (1280)
) u_awb (
    .I_clk   (axi4s_video_aclk),
    .I_rst_n (I_rst_n),
    .I_tlast (m_aixs_tlast),
    .I_tuser (m_aixs_tuser),
    .I_tdata (m_aixs_tdata_96),
    .I_tvalid(m_aixs_tvalid),
    .I_tready(m_aixs_tready),
    .O_tlast (awb_O_tlast ),
    .O_tuser (awb_O_tuser ),
    .O_tdata (awb_O_tdata ),
    .O_tvalid(awb_O_tvalid),
    .O_tready(awb_O_tready),
    .O_wb_ready(awb_ready),.O_raw_rgb(awb_raw_rgb)
);

    wire [1535:0] application_snapshot;
                                                                              
    wire [95:0] gamma_data;
    wire [3:0] active_application_mode;
    assign O_panel_early=awb_O_tuser;
                                                                             
                                                                                    
    reg [95:0] fence_rgb,fence_raw;
    reg [47:0] fence_camera_status;
    reg fence_valid,fence_early,fence_last,fence_view,fence_commit,fence_clear;
    (* max_fanout = 20 *) reg fence_mode_change;
    reg fence_gamma_we,fence_editor_we,fence_gamma_commit,fence_editor_commit;
    reg [7:0] fence_curve_address,fence_curve_value;
    always @(posedge axi4s_video_aclk or negedge I_rst_n)begin
        if(!I_rst_n)begin
            fence_rgb<=0;fence_raw<=0;fence_camera_status<=0;
            fence_valid<=0;fence_early<=0;fence_last<=0;fence_view<=0;fence_commit<=0;fence_clear<=0;fence_mode_change<=0;
            fence_gamma_we<=0;fence_editor_we<=0;fence_gamma_commit<=0;fence_editor_commit<=0;
            fence_curve_address<=0;fence_curve_value<=0;
        end else begin
            fence_rgb<=awb_O_tdata;fence_raw<=awb_raw_rgb;fence_camera_status<=application_camera_status;
            fence_valid<=awb_O_tvalid;fence_early<=awb_O_tuser;fence_last<=awb_O_tlast;
            fence_view<=I_view_target;fence_commit<=I_application_commit;fence_clear<=I_panel_clear;
            fence_mode_change<=I_application_mode_change;
            fence_gamma_we<=I_gamma_we;fence_editor_we<=I_editor_we;
            fence_gamma_commit<=I_gamma_commit;fence_editor_commit<=I_editor_commit;
            fence_curve_address<=I_curve_address;fence_curve_value<=I_curve_value;
        end
    end

    combined_video_core #(.C_SHARED_INSPECTION_GAMMA(1)) u_combined(
        .I_clk(axi4s_video_aclk),.I_rst_n(I_rst_n),
        .I_rgb(fence_raw),.I_wb_rgb(fence_rgb),
        .I_valid(fence_valid),.I_user(fence_early),.I_last(fence_last),
        .I_uart_valid(1'b1),.I_uart_mode(I_application_config[3:0]),
        .I_editor_saturation(I_application_config[57:48]),
        .I_tone_contrast(I_application_config[25:16]),.I_tone_brightness(I_application_config[40:32]),
        .I_gamma_we(fence_gamma_we),.I_gamma_address(fence_curve_address),.I_gamma_value(fence_curve_value),.I_gamma_commit(fence_gamma_commit),
        .I_editor_we(fence_editor_we),.I_editor_address(fence_curve_address),.I_editor_value(fence_curve_value),.I_editor_commit(fence_editor_commit),
        .O_rgb(gamma_data),.O_valid(gamma_valid),.O_user(gamma_early),.O_last(gamma_last),.O_done(core_done),
        .O_early(core_early),.O_error(core_error),.O_busy(O_pipeline_busy),.active_mode(active_application_mode));
    ball_runtime #(.C_PREDECODE_MODE_CHANGE(C_PREDECODE_MODE_CHANGE),.C_FACE_GATE(0),.C_PANEL_CONFIG(1),.C_COMBINED(1),.C_VIEW_SWITCH(1),.C_SHARED_INSPECTION_GAMMA(1),.C_SERIAL_RENDER(1)) u_application(
 .I_raw_rgb(fence_raw),.I_view_target(fence_view),.I_application_commit(fence_commit),
 .I_application_mode_change(fence_mode_change),
 .O_view_actual(O_view_actual),.O_view_commit(O_view_commit),.O_view_revision(O_view_revision),
 .I_application_mode(I_application_config[3:0]),.I_settings(I_panel_settings),.I_panel_clear(fence_clear),.O_good(O_good),.O_bad(O_bad),
 .I_clk(axi4s_video_aclk),.I_rst_n(I_rst_n),.I_keys_n(I_keys_n),.I_camera_status(fence_camera_status),
                                                                             
                                                                                  
 .I_rgb(gamma_data),.I_valid(gamma_valid),.I_user(fence_early),.I_last(gamma_last),
 .O_data(awb_O_tdata_128),.O_valid(awb_O_tvalid_128),.O_early(awb_O_tuser_128),
 .O_last(app_last),.O_done(app_done),.O_error(app_error),
 .O_seg_select_n(O_seg_select_n),.O_seg_segments_n(O_seg_segments_n),
 .O_red(),.O_green(),.O_yellow(),.O_total(),.O_count_mode(),.O_gate_state(),.O_track_status(),.O_camera_step(O_camera_step),
 .O_status_snapshot(application_snapshot),.O_status_valid(O_status_valid));



                           
                          
                               
    
	
    assign O_status_snapshot=core_error ?
        {application_snapshot[1535:424],8'd7,application_snapshot[415:0]} : application_snapshot;
endmodule


