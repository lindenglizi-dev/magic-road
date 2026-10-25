"""将同一自检的WIF1行为驱动替为合格C4模块；只生成验证快照，不改任何DUT。"""
import re


def connect_physical(text):
    signals=('i_byte_req_ready','i_byte_rsp_valid','i_byte_rsp_data','i_byte_rsp_error',
             'i_weight_req_ready','i_weight_rsp_valid','i_weight_rsp_data','i_weight_rsp_error','i_work_fault')
    for signal in signals:
        text,count=re.subn(r'^    reg (.*?)\b'+signal+r' = 0;',r'    wire \1'+signal+';',text,flags=re.M)
        if count!=1:
            raise ValueError('backend declaration is not unique: '+signal)
    for signal in ('i_byte_req_ready','i_weight_req_ready'):
        text,count=re.subn(r'^        '+signal+r' <=[^\n]*\n','',text,flags=re.M)
        if count!=1:
            raise ValueError('backend readiness driver is not unique: '+signal)
    text=text.replace('i_byte_rsp_valid <= 0; i_weight_rsp_valid <= 0; ','')
    for channel in ('byte','weight'):
        old=f'            if(i_{channel}_rsp_valid && o_{channel}_rsp_ready) i_{channel}_rsp_valid <= 0;'
        new=f'''            if(i_{channel}_rsp_valid && o_{channel}_rsp_ready) begin
                if(!{channel}_pending || i_{channel}_rsp_error || i_{channel}_rsp_data !== saved_{channel}_data)
                    $fatal(1,"PHYSICAL_{channel.upper()}_RESPONSE");
                {channel}_pending <= 0;
            end'''
        if text.count(old)!=1:
            raise ValueError('backend retirement driver is not unique: '+channel)
        text=text.replace(old,new)
        pattern=(r'            if\('+channel+r'_pending\) begin\n'
                 r'                if\('+channel+r'_delay != 0\)[^\n]*\n'
                 r'                else begin[^\n]*\n'
                 r'            end\n')
        text,count=re.subn(pattern,'',text)
        if count!=1:
            raise ValueError('backend response driver is not unique: '+channel)
    instance='''    // 真实C4 WIF1端点；原行为数组只作为独立期望记分板，不驱动客户端。
    road_feature_workstore physical_workstore_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),
        .i_byte_req_valid(o_byte_req_valid),.i_byte_req_write(o_byte_req_write),
        .i_byte_req_addr(o_byte_req_addr),.i_byte_req_data(o_byte_req_data),.i_byte_rsp_ready(o_byte_rsp_ready),
        .i_weight_req_valid(o_weight_req_valid),.i_weight_req_write(o_weight_req_write),
        .i_weight_req_group(o_weight_req_group),.i_weight_req_data(o_weight_req_data),.i_weight_rsp_ready(o_weight_rsp_ready),
        .o_byte_req_ready(i_byte_req_ready),.o_byte_rsp_valid(i_byte_rsp_valid),
        .o_byte_rsp_data(i_byte_rsp_data),.o_byte_rsp_error(i_byte_rsp_error),
        .o_weight_req_ready(i_weight_req_ready),.o_weight_rsp_valid(i_weight_rsp_valid),
        .o_weight_rsp_data(i_weight_rsp_data),.o_weight_rsp_error(i_weight_rsp_error),.o_fault(i_work_fault)
    );
'''
    anchor='    always #5 i_clk = !i_clk;'
    if text.count(anchor)!=1:
        raise ValueError('backend insertion anchor is not unique')
    text=text.replace(anchor,instance+anchor)
    for signal in signals:
        if re.search(r'\b'+signal+r'\s*(?:<=|=(?!=))',text):
            raise ValueError('behavior driver survives physical adapter: '+signal)
    return text


if __name__=='__main__':
    from pathlib import Path
    source=(Path(__file__).parent / 'tb_standard_tile_client.v').read_text(encoding='utf-8')
    converted=connect_physical(source)
    assert converted.count('road_feature_workstore physical_workstore_Inst(')==1
    assert 'PHYSICAL_BYTE_RESPONSE' in converted and 'PHYSICAL_WEIGHT_RESPONSE' in converted
    assert 'gold_partial[partials]' in converted and 'gold_pre[accs-1]' in converted
    print('PHYSICAL_ADAPTER_SELF_CHECK_PASS; no actual WIF1 simulation executed')
