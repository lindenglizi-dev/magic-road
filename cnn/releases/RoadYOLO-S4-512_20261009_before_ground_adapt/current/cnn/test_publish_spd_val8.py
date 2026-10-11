"""Small conversion check: preserve native labels and prohibit training rows."""
from .publish_spd_val8 import convert

sample = dict(width=1920, height=1080, sample_id='spd_inf_010721',
    image_sha256='0'*64, source_group='SPD:scene', frame_id='010721',
    camera_id='1', sequence_id='0058')
review = dict(boxes=[dict(id='manual_1', source_id=None, **{'class': 'person'},
    bbox=[0, 0, 1920, 1080])])
result = convert(sample, review)
assert result['boxes'] == [[0, 0, 512, 288]]
assert result['labels'] == [0] and result['split'] == 'val'
assert result['ignore_boxes'] == []
assert result['native_labels'] == review['boxes']
result['native_labels'][0]['bbox'][0] = 1
assert review['boxes'][0]['bbox'][0] == 0
print('PASS: coordinates, class, validation-only split, independent native labels')
