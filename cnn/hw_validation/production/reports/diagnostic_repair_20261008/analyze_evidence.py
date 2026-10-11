"""Classify diagnostics and routed paths; manual evidence is not a gate waiver."""
import collections
import csv
import json
import sys
from execute import HERE,A,check,write,sha

sys.path.insert(0,str(A))
from summarize import rows,statistics

check()
d=HERE/'candidate/readback_physical'
assert 'CANDIDATE_READBACK_COMPLETE' in (d/'td.log').read_text()
parsed={p.stem:rows(p) for p in d.glob('*.timing')}
global_rows=rows(HERE/'candidate/physical/all_endpoints.timing')
source_groups=('reg_all','slice_all','dsp_all','eram_all','memory_all')
internal=[r for name in source_groups for r in parsed[name] if not r['end'].startswith('o_')]
assert not any(r['begin'].startswith('i_') for r in internal)
external=[r for name in source_groups for r in parsed[name] if r['end'].startswith('o_')]
external+=parsed['input_all']+parsed['output_all']
def key(r):
    return (r['kind'],'capture:'+r['capture_net'] if r.get('capture_net') else 'pin:'+r['end'])
worst={}
for r in internal:
    k=key(r)
    if k not in worst or r['slack_ns']<worst[k]['slack_ns']:worst[k]=r
missing=[];worse=[]
for r in global_rows:
    if not r['begin'].startswith('i_') and not r['end'].startswith('o_'):
        k=key(r)
        if k not in worst:missing.append(k)
        elif r['slack_ns']<worst[k]['slack_ns']-0.0001:worse.append(r)
assert all(r.get('launch_q')=='reg_release_done_reg_syn_3.oqb' and r['end'] in
    ('reg_release_done_reg_syn_4.ima','reg_release_done_reg_syn_5.ima') for r in parsed['meta_done'])
assert all(r.get('launch_q') in ('reg_release_done_reg_syn_4.oqa','reg_release_done_reg_syn_5.oqa') for r in parsed['done_all'])
assert not missing and not worse,(len(missing),len(worse))
write(HERE/'candidate/timing_comparison.json',{
    'scope':'Dynamic serial postprocess plus 38-bit shell; excludes MAC/tile/DDR/full network',
    'baseline':json.loads((A/'timing_scope_acceptance.json').read_text())['internal_union'],
    'candidate_internal':statistics(internal),'candidate_external':statistics(external),
    'candidate_named_paths':{k:statistics(v) for k,v in parsed.items()},
    'global_capture_keys':len({key(r) for r in global_rows if not r['begin'].startswith('i_') and not r['end'].startswith('o_')}),
    'missing_capture_keys':missing,'unexplained_worse_global_records':worse,
    'coverage':'100 percent reported by TD; real external contract not signed',
    'reset_physical':'One first stage, two tool-replicated final stages; exact pins verified',
    'db_sha256':sha(HERE/'candidate/physical/pr.db'),
    'new_exceptions':False,'signoff':False})
base=HERE/'baseline_sim/modelsim_host';cand=HERE/'candidate_sim/modelsim_host'
assert (base/'results.csv').read_bytes()==(cand/'results.csv').read_bytes()
assert (base/'batch_cycles.csv').read_bytes()==(cand/'batch_cycles.csv').read_bytes()
write(HERE/'simulation_comparison.json',{'simulator':'ModelSim 2020.4 same-simulator comparison',
    'batches':330,'outputs':604,'candidate_equal_baseline':True,
    'core_cycles':15058,'raw_cycles':4564,'activated_cycles':10494,
    'shell_cycles':46151,'new_reset_checks':13,
    'old_icarus_core_cycles':15388,'cross_simulator_cycles_comparable':False,
    'note':'One-cycle-per-batch measurement difference; not claimed as speedup'})
scopes={}
for label in ('original_full','hardware','model','candidate'):
    gate=json.loads((HERE/'gates'/label/'gate.json').read_text())
    scopes[label]={'errors':gate['errors'],'strict_warnings':gate['strict_warnings'],
                   'checks':{k:v['status'] for k,v in gate['checks'].items()}}
write(HERE/'diagnostic_classification.json',{'scope_counts':scopes,'counts_additive':False,
    'semantic_review':[
      {'rule':'VG153','scope':'Original six files','findings':25,'confirmed_real_drivers':25,
       'evidence':'24 named child outputs plus behavioral indexed memory write; no wire-to-reg edits',
       'strict_state':'still failed, not waived'},
      {'rule':'VG155','findings':2,'consumers':['state_current','reg_tx_index'],
       'evidence':'ST_TX makes TX valid; ready-only consumption occurs in that state and reset is guarded',
       'strict_state':'two identities retained; no functional duplicate-transfer observed'},
      {'rule':'VG098','findings':14,'evidence':'Six shell plus eight dynamic non-idle states have input/reset-reachable transitions',
       'limit':'Manual reachable-state reasoning, not unbounded liveness proof'},
      {'rule':'VG138','findings':80,'hardware_unsized':72,'model_defaults':7,'comment_match':1,
       'strict_state':'72 hardware formatting requirements genuinely outstanding; comment match kept'},
      {'rule':'VG097/VG132','evidence':'PH1P governed interface and real ERAM netlist exist; checker clock/primitive recognition still incomplete',
       'action':'No port renaming or global checker relaxation; add narrow positive/negative adapter tests before claiming closure'}],
    'tool_failures':[
      'Icarus unchanged shell compilation access exception 0xC0000005; partial VVP not accepted',
      'ModelSim restricted launch WinError623; host launch and actual regressions passed',
      'First TD readback assumed original logical reset alias; routed tool cloned only final stage',
      'Second readback broad DSP wildcard included nonphysical aliases; exact PH1P physical REF_NAME fixed query only',
      'Spec initial permission failure then nested workspace scope failure; root cwd retry rendered WaveDrom successfully'],
    'delivery_pass':False,'checker_modified':False})
print('INTERNAL', {k:v['worst']['slack_ns'] if v['worst'] else None for k,v in statistics(internal).items()})
print('COVERAGE_CAPTURE_PASS',len(worst))
check()
