"""发布候选复位说明与规定周期图，不改变RTL。"""
import json
import sys
from execute import HERE, OLD, TOP, run, write


def main():
    contract = json.loads((OLD/'shell.contract.json').read_text(encoding='utf-8'))
    m = contract['modules'][0]
    m['feature'] = 'reset_direct_distribution'
    m['behavior'] += [
        'Only reg_release_done drives the internal async reset tree. Raw i_rstn still immediately masks RX ready and TX valid.',
        'Two synchronizer DFFs, clock, ports, numeric core and load protocol remain unchanged. No attributes or timing exceptions.',
        'Raw ASR recovery/removal still checked; a positive diagnostic result cannot establish asynchronous external signoff.']
    m['verification_cases'] += ['Near-edge release before/on/after edge; TABLE, PACKET, SUBMIT, WAIT and stalled TX reset; 1024-word reload; no stale output.']
    m['timing_diagrams'] = [dict(id='release',title='异步取消、两级同步释放',scenario='reset_release',
        description='数字契约示意：释放后两个有效沿；第三沿最早接收，随后必须装满表。不能模拟亚稳态。',
        wavejson={'signal':[{'name':'i_clk','wave':'p.......'},
                           {'name':'i_rstn','wave':'01......'},
                           {'name':'reg_release_meta','wave':'0.1.....'},
                           {'name':'reg_release_done','wave':'0..1....'},
                           {'name':'RX permitted','wave':'0..1....'},
                           {'name':'table_loaded','wave':'0.......'}]})]
    write(HERE/'candidate/shell.contract.json',contract)
    d = HERE/'candidate'
    run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
         '--spec',d/'shell.contract.json','--out-dir',d,
         '--source',d/'rtl'/TOP,'--language','zh'],d,'spec.log')
    print('CANDIDATE_SPEC_AND_WAVEDROM_PASS')


if __name__ == '__main__':
    main()
