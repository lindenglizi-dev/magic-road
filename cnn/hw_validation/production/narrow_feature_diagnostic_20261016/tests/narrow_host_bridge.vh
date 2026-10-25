// Host side of the fixed 16-bit protocol; only narrow pins drive DUT inputs.
    reg host_control = 0;
    reg host_control_valid = 0;
    reg [15:0] host_control_data = 0;
    wire rx_ready, tx_valid, tx_ready;
    wire [15:0] tx_data;
    wire rx_valid;
    wire [15:0] rx_data;
    reg [15:0] host_tx_kind = 0;
    integer host_tx_words = 0;
    integer host_tx_index = 0;
    reg [63:0] host_tx_payload = 0;
    wire [63:0] host_tx_complete = host_tx_payload | ({48'd0,tx_data} << (host_tx_index*16));
    wire host_tx_final = host_tx_words!=0 && host_tx_index==host_tx_words-1;
    reg host_barrier_pending = 0;
    reg [6:0] host_barrier_identity = 0;
    reg [15:0] host_rx_kind = 0;
    integer host_rx_words = 0;
    integer host_rx_index = 0;
    reg [463:0] host_rx_payload = 0;
    reg host_rx_header = 0;
    wire host_rx_last = host_rx_words!=0 && !host_rx_header && host_rx_index==host_rx_words-1;
    reg host_tx_held = 0;
    reg [15:0] host_tx_held_data = 0;
    integer host_table_cycles = 0;
    integer host_table_start = 0;
    integer host_export_cycles = 0;
    integer host_service_cycles = 0;
    integer host_rx_cycles = 0;
    integer host_busy_starts = 0;
    assign tx_ready = rstn && (!host_tx_final ||
        (host_tx_kind==16'ha100 ? read_ready :
         host_tx_kind==16'ha101 ? parameter_ready :
         host_tx_kind==16'ha102 ? write_ready : !host_barrier_pending));
    assign read_valid = tx_valid && host_tx_final && host_tx_kind==16'ha100;
    assign read_address = host_tx_complete[31:0];
    assign parameter_valid = tx_valid && host_tx_final && host_tx_kind==16'ha101;
    assign parameter_channel = host_tx_complete[13:7];
    assign parameter_group = host_tx_complete[18:14];
    assign parameter_window = host_tx_complete[21:19];
    assign write_valid = tx_valid && host_tx_final && host_tx_kind==16'ha102;
    assign write_address = host_tx_complete[31:0];
    assign write_data = host_tx_complete[39:32];
    assign write_sum = host_tx_complete[48:40];
    assign barrier_valid = host_barrier_pending;
    assign parameter_response_ready = !host_control && host_rx_kind==16'h8101 && host_rx_last && rx_ready;
    assign read_response_ready = !host_control && host_rx_kind==16'h8100 && host_rx_last && rx_ready;
    assign rx_valid = host_control ? host_control_valid : host_rx_words!=0;
    assign rx_data = host_control ? host_control_data :
        host_rx_header ? host_rx_kind : (host_rx_payload >> (host_rx_index*16));

    road_narrow_feature_top dut(
        .i_clk(clk),.i_rstn(rstn),.i_rx_valid(rx_valid),.i_rx_data(rx_data),.o_rx_ready(rx_ready),
        .o_tx_valid(tx_valid),.o_tx_data(tx_data),.i_tx_ready(tx_ready),
        .o_busy(busy),.o_done(done),.o_fault(fault),.o_table_loaded(table_loaded)
    );

    // Explicit host command ownership prevents interleaving an automatic reply packet.
    task host_begin;
        begin
            wait(host_rx_words==0);
            @(negedge clk); host_control=1;
        end
    endtask
    task host_word;
        input [15:0] value;
        begin
            @(negedge clk); host_control_data=value; host_control_valid=1;
            @(posedge clk);
            while(!rx_ready)@(posedge clk);
            @(negedge clk); host_control_valid=0;
        end
    endtask
    task host_end;
        begin @(negedge clk); host_control_valid=0; host_control=0; end
    endtask

    always @(posedge clk or negedge rstn)begin
        if(!rstn)begin
            host_tx_kind<=0; host_tx_words<=0; host_tx_index<=0; host_tx_payload<=0;
            host_barrier_pending<=0; host_barrier_identity<=0;
            host_rx_kind<=0; host_rx_words<=0; host_rx_index<=0; host_rx_payload<=0; host_rx_header<=0;
            host_tx_held<=0;
        end else begin
            if(host_tx_held && (!tx_valid || tx_data!==host_tx_held_data))
                $fatal(1,"NARROW_TX_STABILITY data changed or valid dropped while stalled");
            host_tx_held<=tx_valid&&!tx_ready;
            host_tx_held_data<=tx_data;
            if(active && tx_valid)begin
                if(host_tx_kind==16'ha102)host_export_cycles=host_export_cycles+1;
                else host_service_cycles=host_service_cycles+1;
            end
            if(active && rx_valid)host_rx_cycles=host_rx_cycles+1;
            if(tx_valid && tx_ready)begin
                if(host_tx_words==0)begin
                    host_tx_kind<=tx_data; host_tx_index<=0; host_tx_payload<=0;
                    case(tx_data)
                        16'ha100,16'ha101:host_tx_words<=2;
                        16'ha102:host_tx_words<=4;
                        16'ha103:host_tx_words<=1;
                        default:$fatal(1,"NARROW_TX unknown header %h",tx_data);
                    endcase
                end else if(host_tx_final)begin
                    if(host_tx_kind==16'ha101 && host_tx_complete[6:0]!=={layer,block_id})
                        $fatal(1,"NARROW_PARAM request identity mismatch");
                    if(host_tx_kind==16'ha103)begin
                        if(host_tx_complete[6:0]!=={layer,block_id})$fatal(1,"NARROW_BARRIER identity mismatch");
                        host_barrier_pending<=1; host_barrier_identity<=host_tx_complete[6:0];
                    end
                    host_tx_words<=0; host_tx_index<=0; host_tx_payload<=0;
                end else begin
                    host_tx_payload<=host_tx_complete;
                    host_tx_index<=host_tx_index+1;
                end
            end
            if(!host_control)begin
                if(host_rx_words!=0)begin
                    if(rx_ready)begin
                        if(host_rx_header)host_rx_header<=0;
                        else if(host_rx_last)begin host_rx_words<=0; host_rx_index<=0; end
                        else host_rx_index<=host_rx_index+1;
                    end
                end else if(read_response_valid)begin
                    host_rx_kind<=16'h8100; host_rx_words<=11; host_rx_index<=0; host_rx_header<=1;
                    host_rx_payload<={303'd0,read_error,read_response_data,read_response_address};
                end else if(parameter_response_valid)begin
                    host_rx_kind<=16'h8101; host_rx_words<=29; host_rx_index<=0; host_rx_header<=1;
                    host_rx_payload<={1'b0,parameter_error,parameter_response_data,parameter_response_weight,
                        parameter_response_window,parameter_response_group,parameter_response_channel,
                        parameter_response_layer,parameter_response_block_id};
                end else if(host_barrier_pending && barrier_ready)begin
                    host_rx_kind<=16'h8102; host_rx_words<=1; host_rx_index<=0; host_rx_header<=1;
                    host_rx_payload<={457'd0,barrier_layer,barrier_block_id};
                    host_barrier_pending<=0;
                end else if(active && busy && !done && !fault && lfsr[7:0]==8'h6d)begin
                    host_rx_kind<=16'h8001; host_rx_words<=1; host_rx_index<=0; host_rx_header<=1;
                    host_rx_payload<={460'd0,lfsr[19:16]};
                    host_busy_starts=host_busy_starts+1;
                end
            end
        end
    end

