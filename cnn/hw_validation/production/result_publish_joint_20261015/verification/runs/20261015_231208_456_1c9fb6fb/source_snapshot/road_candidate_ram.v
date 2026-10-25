`timescale 1ns / 1ps
// 两类候选共享存储：每条记录四个连续40bit词，响应消费前不接新请求。
module road_candidate_ram(
    input i_clk, // 统一候选存储时钟
    input i_rstn, // 低有效控制复位，不清除存储内容
    input i_cancel, // 与调用方共同取消旧片上事务
    input i_clear_counters, // 新帧只清统计计数
    input i_req_valid, // 完整记录请求有效
    input i_req_write, // 一为写入记录，零为读取
    input i_req_class, // 两类各占512个词
    input [6:0] i_req_index, // 类内候选记录槽
    input [159:0] i_req_data, // 写入四词期间锁定的载荷
    input i_rsp_ready, // 调用方消费整条响应
    output o_req_ready, // 空闲且未取消时允许请求
    output o_rsp_valid, // 四词操作全部完成后保持
    output o_rsp_class, // 响应归属类别
    output [6:0] o_rsp_index, // 响应归属槽位
    output [159:0] o_rsp_data, // 已聚合的完整读取记录
    output o_rsp_error, // 本地受控RAM没有外设错误返回
    output [31:0] o_read_words, // 实际同步读发射次数
    output [31:0] o_write_words // 实际词写入次数
);
    //-------------状态参数区域-------------//
    localparam ST_IDLE=3'd0; // 等待独占记录请求
    localparam ST_WRITE=3'd1; // 每拍写入一个词
    localparam ST_READ=3'd2; // 发射同步存储读取
    localparam ST_CAPTURE=3'd3; // 捕获前拍读取结果
    localparam ST_RESPONSE=3'd4; // 保持响应直至消费
    //--------------状态机信号--------------//
    reg [2:0] state_current=0; // 当前存储服务阶段
    reg [2:0] state_next=0; // 独立组合状态转移
    //--------------寄存器信号--------------//
    reg reg_class=0; // 接收后冻结类别
    reg [6:0] reg_index=0; // 接收后冻结槽号
    reg [1:0] reg_word=0; // 记录内部词序号
    reg [159:0] reg_write_data=0; // 持有完整待写入记录
    reg [159:0] reg_response=0; // 聚合读取响应并保持
    reg [39:0] reg_read_data=0; // 同步读原始返回寄存器
    reg [39:0] reg_memory [0:1023]; // 40960bit唯一候选存储，不作数组复位
    reg [31:0] cnt_read=0; // 已接受的物理词读
    reg [31:0] cnt_write=0; // 已执行的物理词写
    wire [9:0] memory_address; // 类别、记录、词偏移拼成地址
    reg [39:0] reg_word_data=0; // 当前待写入的40bit切片
    //-------------其他信号连线-------------//
    assign memory_address={reg_class,reg_index,reg_word}; // 各类512词不重叠
    //-------------输出信号连线-------------//
    assign o_req_ready=(state_current==ST_IDLE)&&!i_cancel; // 事务排空后才能重用服务
    assign o_rsp_valid=(state_current==ST_RESPONSE)&&!i_cancel; // 取消优先于旧响应
    assign o_rsp_class=reg_class; // 响应类别保持到消费
    assign o_rsp_index=reg_index; // 响应地址保持到消费
    assign o_rsp_data=reg_response; // 完整四词载荷保持
    assign o_rsp_error=1'b0; // 真实错误由上层身份与范围检查发现
    assign o_read_words=cnt_read; // 不把请求数冒充物理读次数
    assign o_write_words=cnt_write; // 记录真实词写入次数
    //--------------状态机区域--------------//
    // 控制复位或共同取消只撤销valid和游标。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE; end
        else if(i_cancel)begin state_current<=ST_IDLE; end
        else begin state_current<=state_next; end
    end
    // 独立状态转移确保同步读先发射再捕获。
    always@(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin
                if(i_req_valid&&o_req_ready)begin
                    if(i_req_write)begin state_next=ST_WRITE; end
                    else begin state_next=ST_READ; end
                end
            end
            ST_WRITE:begin if(reg_word==2'd3)begin state_next=ST_RESPONSE; end end
            ST_READ:begin state_next=ST_CAPTURE; end
            ST_CAPTURE:begin
                if(reg_word==2'd3)begin state_next=ST_RESPONSE; end
                else begin state_next=ST_READ; end
            end
            ST_RESPONSE:begin if(i_rsp_ready)begin state_next=ST_IDLE; end end
            default:begin state_next=ST_IDLE; end
        endcase
    end
    // 写切片固定为四个case，不使用大动态移位器。
    always@(*)begin
        case(reg_word)
            2'd0:begin reg_word_data=reg_write_data[39:0]; end
            2'd1:begin reg_word_data=reg_write_data[79:40]; end
            2'd2:begin reg_word_data=reg_write_data[119:80]; end
            default:begin reg_word_data=reg_write_data[159:120]; end
        endcase
    end
    //-----------状态任务处理区域-----------//
    // 记录请求、词游标及完整响应缓冲。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_class<=0; reg_index<=0; reg_word<=0; reg_write_data<=0; reg_response<=0;
        end else if(i_cancel)begin
            reg_word<=0; reg_response<=0;
        end else begin
            if(state_current==ST_IDLE&&i_req_valid&&o_req_ready)begin
                reg_class<=i_req_class; reg_index<=i_req_index; reg_word<=0;
                reg_write_data<=i_req_data; reg_response<=0;
            end
            if(state_current==ST_WRITE&&reg_word!=2'd3)begin reg_word<=reg_word+1'b1; end
            if(state_current==ST_CAPTURE)begin
                case(reg_word)
                    2'd0:begin reg_response[39:0]<=reg_read_data; end
                    2'd1:begin reg_response[79:40]<=reg_read_data; end
                    2'd2:begin reg_response[119:80]<=reg_read_data; end
                    default:begin reg_response[159:120]<=reg_read_data; end
                endcase
                if(reg_word!=2'd3)begin reg_word<=reg_word+1'b1; end
            end
        end
    end
    // 同步存储端口没有整阵列复位或上电内容假设。
    always@(posedge i_clk)begin
        if(i_rstn&&!i_cancel)begin
            if(state_current==ST_WRITE)begin reg_memory[memory_address]<=reg_word_data; end
            if(state_current==ST_READ)begin reg_read_data<=reg_memory[memory_address]; end
        end
    end
    // 每帧统计与控制复位独立于存储内容。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin cnt_read<=0; cnt_write<=0; end
        else if(i_clear_counters)begin cnt_read<=0; cnt_write<=0; end
        else if(!i_cancel)begin
            if(state_current==ST_READ)begin cnt_read<=cnt_read+1'b1; end
            if(state_current==ST_WRITE)begin cnt_write<=cnt_write+1'b1; end
        end
    end
endmodule
