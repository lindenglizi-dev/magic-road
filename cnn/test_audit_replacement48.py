"""No files/models/network: inventory must preserve draft and ignore semantics."""
from copy import deepcopy
from .audit_replacement48 import effective_boxes, recommendation

sample = {'original': [{'target_id':'o1', 'class':'person', 'bbox':[0,0,5,5]},
                       {'target_id':'o2', 'class':'vehicle', 'bbox':[5,5,10,10]}]}
review = {'actions': [{'target_id':'o1', 'action':'D', 'class':'person', 'bbox':[0,0,5,5]},
                     {'target_id':'o2', 'action':'I', 'class':'ignore', 'bbox':[5,5,10,10]},
                     {'target_id':'teacher_t1', 'action':'N', 'class':'person', 'bbox':[1,1,6,6]}]}
before = deepcopy((sample, review))
assert [item['class'] for item in effective_boxes(sample, review)] == ['ignore', 'person']
assert (sample, review) == before
assert len(effective_boxes(sample, {})) == 2
assert recommendation(True, 19) == 'KEEP_CANDIDATE_SIGNED'
assert recommendation(False, 19) == 'UNRESOLVED_COMPLETENESS'
assert recommendation(True, 20) == 'REPLACE_CANDIDATE_DENSITY'
print('PASS: draft actions/ignore retained, no mutation, signed/pending/density proposals separated')
