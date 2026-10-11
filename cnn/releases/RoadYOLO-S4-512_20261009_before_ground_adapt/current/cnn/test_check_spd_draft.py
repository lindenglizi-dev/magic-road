from .check_spd_draft import iou, associate, diagnose
assert iou([0,0,10,10],[0,0,10,10])==1
assert iou([0,0,10,10],[10,0,20,10])==0
riders=[{'source_id':'r1','source_type':'Cyclist','bbox_xyxy':[0,0,20,20],'proposed_class':None},
        {'source_id':'r2','source_type':'Cyclist','bbox_xyxy':[30,0,50,20],'proposed_class':None}]
boxes=[{'id':'p1','class':'person','bbox':[0,0,10,10],'source_id':None},
       {'id':'v1','class':'vehicle','bbox':[0,10,20,20],'source_id':None}]
assert set(associate(riders,boxes,'person'))=={'r1'}
s={'sample_id':'fixture','objects':riders}
result=diagnose(s,{'boxes':boxes})
assert result['rider_checks'][0]['person'] and result['rider_checks'][0]['vehicle']
assert result['rider_checks'][1]['person'] is None
assert not result['complete_gt'] and not result['duplicates']
duplicate=dict(boxes[0],id='p2');assert len(diagnose(s,{'boxes':boxes+[duplicate]})['duplicates'])==1
assert diagnose(s,{'boxes':[]})['empty_draft']
print('PASS: overlap, unlinked rider support, missing support, same-class duplicates, empty not GT')
