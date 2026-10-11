"""Tiny no-network checks for source geometry, pairing, density and safety."""
from .prepare_spd_pilot import inspect_objects, paired_member, safe_member, select_pilot

for path in ('../escape', '/absolute', 'C:/bad', 'a\\b'):
    try:
        safe_member(path)
    except ValueError:
        pass
    else:
        raise AssertionError(path)
assert paired_member('label/camera/1.json', 'label/camera').endswith('label/camera/1.json')
try:
    paired_member('label/virtuallidar/1.json', 'label/camera')
except ValueError:
    pass
else:
    raise AssertionError('lidar mispaired as camera')
def obj(kind, box):
    return {'type':kind, '2d_box':dict(zip(('xmin','ymin','xmax','ymax'),box))}
objects, issues = inspect_objects([obj('Pedestrian',[0,0,10,10]),obj('Cyclist',[1,2,8,9]),
                                 obj('Van',[0,0,20.000001,10]),obj('Car',[0,0,float('nan'),1]),
                                 obj('Car',[2,2,2,3])],20,10)
assert objects[0]['proposed_class']=='person' and objects[0]['in_bounds']
assert objects[1]['proposed_class'] is None
assert objects[2]['bbox_xyxy'][2]==20.000001 and not objects[2]['in_bounds']
assert not objects[3]['geometry_valid'] and not objects[4]['geometry_valid']
rows=[{'frame_id':i,'estimated_split_count':19,'objects':[objects[0]]} for i in range(16)]
rows += [{'frame_id':99,'estimated_split_count':20,'objects':[objects[0]]}]
assert len(select_pilot(rows))==8 and len({r['frame_id'] for r in select_pilot(rows)})==8
assert all(r['frame_id']!=99 for r in select_pilot(rows))
print('PASS: safe paths, camera pairing, finite/nonzero/bounds geometry, rider/Van pending, unique density selection')
