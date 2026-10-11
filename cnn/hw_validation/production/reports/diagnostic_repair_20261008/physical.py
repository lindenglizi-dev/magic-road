"""只实现独立38位壳；SDC/ADC不变，不导出位流。"""
import json
import xml.etree.ElementTree as ET
from execute import HERE, OLD, CORE, TOP, TD, run, sha, check, write


def main():
    check()
    d = HERE / 'candidate/physical'
    assert not (d / 'td.log').exists()
    original = (OLD / 'candidate/physical/road_dynamic_low_io_top.al').read_text(encoding='utf-8')
    tree = ET.fromstring(original.replace('UsedInP&R', 'UsedInP&amp;R'))
    tree.set('Path', d.as_posix())
    sources = tree.find('Source_Files/Verilog')
    sources.clear()
    for order, name in enumerate((TOP, *CORE), 1):
        info = ET.SubElement(ET.SubElement(sources, 'File', Path='../rtl/' + name), 'FileInfo')
        for key, value in (('UsedInSyn','true'), ('UsedInP&R','true'),
                           ('BelongTo','design_1'), ('CompileOrder', str(order))):
            ET.SubElement(info,'Attr',Name=key,Val=value)
    with (d / 'road_dynamic_low_io_top.al').open('x', encoding='utf-8') as f:
        f.write(ET.tostring(tree,encoding='unicode').replace('UsedInP&amp;R','UsedInP&R'))
    paths = [HERE / 'candidate/rtl' / name for name in (TOP,*CORE)] + [d/'shell.sdc',d/'shell.adc']
    write(d/'input_hashes.json',{str(p.relative_to(HERE)):sha(p) for p in paths})
    run([TD],d,'td.log','source ../../build.tcl\nexit\n')
    assert (d/'pr.db').is_file() and (d/'all_endpoints.timing').is_file()
    log = (d/'td.log').read_text(encoding='utf-8',errors='replace')
    assert 'DIAGNOSTIC_PHYSICAL_COMPLETE' in log and 'ERROR:' not in log, 'Retain TD failure log'
    check()
    write(d/'receipt.json',{'status':'ROUTED_NOT_SIGNOFF','device':'PH1P35MDG324','speed':'-3',
          'period_ns':10, 'no_new_constraints':True, 'no_bitstream':True,
          'sources':{p.name:sha(p) for p in paths}, 'td_sha256':sha(TD)})
    print('PHYSICAL_DATABASE_READY_NOT_SIGNOFF',flush=True)


if __name__ == '__main__':
    main()
