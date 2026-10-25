"""独立读取合格C4端点收据及封存闭包；不运行或改动C4实现。"""
from run_standard_tile import ROOT, PACKAGE, read, save, sha
from pathlib import Path


def main():
    c4=PACKAGE.parent / 'workstore_feature_20261016'
    frozen=c4 / 'storage_frozen'
    binding=read(frozen / 'input_binding.json')
    checked={}
    for section in ('original_sha256','staged_sha256'):
        checked[section]={path:sha(Path(path))==digest for path,digest in binding[section].items()}
        assert all(checked[section].values()),checked[section]
    statuses={}
    receipts={}
    for case in (0,1,99):
        folder=frozen / f'workstore_case{case}'
        status=read(folder / 'status.json')
        assert status['status']==('PASS_REAL_CHECKER_NEGATIVE' if case==99 else 'PASS_FUNCTION_CASE')
        assert status['physical_resource_mapping'] is False
        statuses[case]=status
        receipts[case]=sha(folder / 'receipt.json')
        if case!=99:
            fields=read(folder / 'receipt.json')['fields']
            assert fields['accepted_byte']==fields['retired_byte']+fields['aborted_byte']
            assert fields['accepted_weight']==fields['retired_weight']+fields['aborted_weight']
            assert 'FEATURE_WORKSTORE_PASS case='+str(case) in (folder / 'simulation.log').read_text(encoding='utf-8')
        else:
            assert 'FEATURE_WORKSTORE_PASS' not in (folder / 'simulation.log').read_text(encoding='utf-8')
    rtl=frozen / 'rtl/road_feature_workstore.v'
    assert sha(rtl)=='0d9f78544ce6e726a8ff042d7be0f5a2aee7d717bfbde0495a98a78dea25eb1c'
    observation=read(c4 / 'native_endpoint_observation_attempt3/receipt.json')
    assert observation['byte_request_to_response_valid_cycles']==[2]
    assert observation['weight_request_to_response_valid_cycles']==[4]
    assert observation['complete_case_pass'] is False
    assert observation['input_binding_sha256']==sha(frozen / 'input_binding.json')
    result=dict(status='PASS_READ_ONLY_C4_FUNCTIONAL_QUALIFICATION',rtl_sha256=sha(rtl),checked=checked,
                statuses=statuses,receipt_sha256=receipts,native_observation=observation,
                physical_resource_mapping_proven=False,synthesis_run=False)
    save(ROOT / 'c4_qualification.json',result)
    print(result['status'],len(checked['original_sha256']),len(checked['staged_sha256']))


if __name__=='__main__':
    main()
