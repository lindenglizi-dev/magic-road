"""Fetch verified official TRAIN GT only; retain source classes, never publish training labels."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import tarfile
import urllib.request

from PIL import Image
from .prepare_ground48 import ROOT, read_json, sha256_file, write_json

OUT = ROOT / 'cnn/reports/mio_train_gt_lookup_20261010_v1'
URL = 'https://tcd.miovision.com/static/dataset/MIO-TCD-Localization-Code.tar'
ETAG = '"9ae15b42e3f39d297de603cab4d5ee25-4"'
TOTAL, OFFSET, SIZE = 26089472, 14807040, 11278610
MEMBER = 'MIO-TCD-Localization-Code/gt_train.csv'
CLASSES = {'articulated_truck', 'bicycle', 'bus', 'car', 'motorcycle',
           'motorized_vehicle', 'non-motorized_vehicle', 'pedestrian',
           'pickup_truck', 'single_unit_truck', 'work_van'}


def read_range(offset, size):
    assert 0 < size <= SIZE and 0 <= offset < offset + size <= TOTAL
    end = offset + size - 1
    req = urllib.request.Request(URL, headers={'Range': f'bytes={offset}-{end}', 'If-Match': ETAG})
    with urllib.request.urlopen(req, timeout=30) as response:
        assert response.status == 206 and response.headers.get('ETag') == ETAG
        assert response.headers.get('Content-Range') == f'bytes {offset}-{end}/{TOTAL}'
        data = response.read(size + 1)
        assert len(data) == size
    return data


def selected_labels(data):
    receipt = read_json(ROOT / 'cnn/data/mio_ac_screen_20261010_v2/receipt.json')
    selected = {}
    for source in receipt['members']:
        path = ROOT / 'cnn/data/mio_ac_screen_20261010_v2' / source['name'].split('/')[-1]
        assert sha256_file(path) == source['sha256']
        with Image.open(path) as image:
            width, height = image.size
        selected[path.stem] = dict(image_id=path.stem, raw_file=str(path),
            source_sha256=source['sha256'], width=width, height=height, source_labels=[])
    assert len(selected) == 48
    for row in csv.reader(io.StringIO(data.decode('utf-8-sig'))):
        assert len(row) == 6 and len(row[0]) == 8 and row[0].isdigit() and row[1] in CLASSES
        box = [int(v) for v in row[2:]]
        if row[0] not in selected:
            continue
        image = selected[row[0]]
        x1, y1, x2, y2 = box
        assert 0 <= x1 <= x2 < image['width'] and 0 <= y1 <= y2 < image['height'], row
        image['source_labels'].append(dict(source_class=row[1], bbox_xyxy_inclusive=box))
    images = list(selected.values())
    counts = Counter(label['source_class'] for image in images for label in image['source_labels'])
    return dict(images=images, source_class_counts=dict(sorted(counts.items())),
        images_with_pedestrian=sum(any(a['source_class'] == 'pedestrian' for a in image['source_labels'])
                                   for image in images),
        source_coordinate_contract='integer XYXY inclusive; official IoU uses +1 width/height',
        source_classes_preserved=True, project_class_mapping_applied=False,
        static_vehicle_coverage_verified=False, physical_camera_mapping_verified=False,
        training_eligible=False, dataset_frozen=False, G_ready=False, training_started=False)


def check():
    data = (OUT / 'gt_train.csv').read_bytes()
    receipt = read_json(OUT / 'receipt.json')
    assert len(data) == SIZE and hashlib.sha256(data).hexdigest() == receipt['member_sha256']
    assert selected_labels(data) == read_json(OUT / 'selected48_source_labels.json')
    assert receipt['member'] == MEMBER and receipt['test_payload_read'] is False
    print('PASS: verified TRAIN member, 48 original-image hashes, source coordinates/classes, not training-ready')


def fetch():
    if OUT.exists():
        raise FileExistsError('Preserve existing output; run check')
    header = read_range(OFFSET - 512, 512)
    member = tarfile.TarInfo.frombuf(header, 'utf-8', 'strict')
    assert member.name == MEMBER and member.isfile() and member.size == SIZE
    data = read_range(OFFSET, SIZE)
    result = selected_labels(data)
    OUT.mkdir(parents=True)
    with (OUT / 'gt_train.csv').open('xb') as stream:
        stream.write(data)
    write_json(OUT / 'selected48_source_labels.json', result)
    write_json(OUT / 'receipt.json', dict(url=URL, etag=ETAG, archive_bytes=TOTAL,
        member=MEMBER, offset=OFFSET, member_bytes=SIZE,
        member_sha256=hashlib.sha256(data).hexdigest(),
        header_sha256=hashlib.sha256(header).hexdigest(), payload_bytes=SIZE + 512,
        archive_fully_downloaded=False, downloaded_code_executed=False, test_payload_read=False,
        source_page='https://tcd.miovision.com/challenge/dataset.html',
        source_class_counts=result['source_class_counts'], images_with_pedestrian=result['images_with_pedestrian'],
        unsigned_images_not_promoted=True, manual_labels_overwritten=False, training_started=False))
    check()
    print(result['source_class_counts'], 'person-bearing images:', result['images_with_pedestrian'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('fetch', 'check'))
    {'fetch': fetch, 'check': check}[parser.parse_args().action]()
