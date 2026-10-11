"""Select development road frames for cache QA, never for accuracy acceptance.

Keep original splits and all annotations. No source image is decoded here.
"""
import argparse
import json
from pathlib import Path

from .dataset import audit
from .train import sha256


def select_pilot(document, source, train_count=96, val_count=32):
    if (train_count < 1 or val_count < 1 or train_count + val_count > 128
            or document.get('training_eligible') is not True
            or any(row['split'] not in ('train', 'val') for row in document['images'])):
        raise ValueError('requires an eligible development-only source and at most128 frames')
    if audit(document)['incomplete_frames']:
        raise ValueError('incomplete source annotations')
    scene_splits = {}
    for row in document['images']:
        if scene_splits.setdefault(row['scene_id'], row['split']) != row['split']:
            raise ValueError('source scene leaks across splits')
    selected = []
    for split, count in (('train', train_count), ('val', val_count)):
        candidates = sorted((row for row in document['images'] if row['split'] == split),
                            key=lambda row: row['image'])
        if len(candidates) < count:
            raise ValueError('not enough development frames')
        for index in range(count):
            row = dict(candidates[index * len(candidates) // count])
            if not row.get('preprocess', {}).get('raw_image'):
                raise ValueError('road cache pilot requires original raw images')
            image = Path(row['image'])
            row['teacher_key'] = str(row.get('teacher_key', row['image'])).replace('\\', '/')
            row['image'] = str(image if image.is_absolute() else (source.parent / image).resolve())
            selected.append(row)
    result = dict(document)
    result.update(images=selected, purpose='CPU_disk_cache_QA_only_not_accuracy_or_training',
                  manifest_status='development_cache_pilot', formal_road_eligible=False)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    if sha256(args.source) != args.source_sha256:
        raise ValueError('source manifest identity mismatch')
    original = json.loads(args.source.read_text(encoding='utf-8'))
    selected = select_pilot(original, args.source)
    if sha256(args.source) != args.source_sha256:
        raise ValueError('source manifest changed during selection')
    selected['cache_pilot_provenance'] = dict(
        source_manifest=str(args.source.resolve()), source_manifest_sha256=args.source_sha256,
        selection='floor(i*N/K)_over_sorted_image_names_separately_in_original_splits',
        selected_by_labels_or_model_scores=False, source_pixels_read=False,
        all_selected_annotations_preserved=True, accuracy_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(selected, stream, indent=2)
    print(json.dumps(dict(output=str(args.output), sha256=sha256(args.output),
                          images=len(selected['images']),
                          positive_boxes=sum(len(row['boxes']) for row in selected['images']),
                          ignore_boxes=sum(len(row['ignore_boxes']) for row in selected['images']),
                          scenes=len({row['scene_id'] for row in selected['images']}))), flush=True)


if __name__ == '__main__':
    main()
