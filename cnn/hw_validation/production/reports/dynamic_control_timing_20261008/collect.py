"""Partition actual routed timing; external diagnostic failures remain visible."""
import json
import re
import sys
from prepare import HERE, check

ROW = re.compile(r'^Slack\s*:\s*([-+\d.]+)ns\s*\nBegin Point\s*:\s*([^\n]+)\nEnd Point\s*:\s*([^\n]+)\nCheck Type\s*:\s*(\w+)\s*\nProcess\s*:\s*([^\n]+)', re.M)

def main(which):
    folder=HERE/which/'physical'
    text=(folder/'coverage_100000_all_paths.timing').read_text(encoding='utf-8')
    assert 'Confidence          : Routed' in text
    rows=[dict(slack_ns=float(s),begin=b.split(' (')[0].strip(),end=e.split(' (')[0].strip(),kind=k,corner=c.strip())
          for s,b,e,k,c in ROW.findall(text)]
    assert rows
    partition={}
    for label in ('internal','external'):
        subset=[r for r in rows if (r['begin'].startswith('i_') or r['end'].startswith('o_')) == (label=='external')]
        partition[label]={}
        for kind in ('setup','hold','recovery','removal'):
            group=[r for r in subset if r['kind']==kind]
            partition[label][kind]={'rows':len(group),'negative':sum(r['slack_ns']<0 for r in group),
                                    'worst':min(group,key=lambda r:r['slack_ns']) if group else None}
    area=(folder/'shell_route.area').read_text(encoding='utf-8')
    resources={k:int(re.search(r'^#'+k+r'\s+(\d+)',area,re.M)[1]) for k in ('slice','lut6','reg','dsp','eram','IO')}
    log=(folder/'td_actual.log').read_text(encoding='utf-8')
    warnings=[line for line in log.splitlines() if 'SYN-5025' in line]
    reset_paths={}
    for name in ('external_reset_entry.timing','reset_sync_interstage.timing','functional_reset_distribution.timing','internal_reg_to_reg.timing'):
        source=(folder/name).read_text(encoding='utf-8')
        parsed=[dict(slack_ns=float(s),begin=b.split(' (')[0].strip(),end=e.split(' (')[0].strip(),kind=k,corner=c.strip())
                for s,b,e,k,c in ROW.findall(source)]
        reset_paths[name]={}
        for kind in ('setup','hold','recovery','removal'):
            group=[r for r in parsed if r['kind']==kind]
            reset_paths[name][kind]={'rows':len(group),'negative':sum(r['slack_ns']<0 for r in group),
                                    'worst':min(group,key=lambda r:r['slack_ns']) if group else None}
    report={'scope':'Dynamic serial requant/round/SiLU/cache INCLUDING shell, NOT MAC/DW/PW/full CNN',
            'resources':resources,'timing':partition,
            'coverage_lines':[l.strip() for l in text.splitlines() if 'coverage' in l.lower() or 'Confidence' in l],
            'dedicated_paths':reset_paths,
            'constant_endpoints':warnings,'new_timing_exceptions':False,'bitstream_generated':False}
    (folder/'status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
    check()

if __name__=='__main__': main(sys.argv[1])
