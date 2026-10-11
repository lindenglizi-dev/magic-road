"""Selection is deterministic, keeps complete targets and fails closed before image IO."""
import copy

from .prepare_tiny_fit import select_rows, training_arguments
from .train import build_parser, protocol_for
from pathlib import Path


def main():
    rows = []
    for index in range(48):
        image_id = index + 1
        rows.append(dict(image=f"/coco/{image_id:012d}.jpg", source_frame=image_id,
            scene_id=f"coco-{image_id}", source_sha256=f"{image_id:064x}",
            split="train" if index < 32 else "val",
            boxes=[[10, 10, 50, 70], [60, 40, 120, 80]], labels=[0, 1], ignore_boxes=[],
            incomplete_frame=False, annotation_complete=True, preprocess={"raw_image": True}))
    document = dict(schema_version=1, task="detection", input_size=[512, 288],
                    classes=["person", "vehicle"], training_eligible=True, images=rows)
    original = copy.deepcopy(document)
    selected, pools = select_rows(document)
    assert len(selected) == 48 and pools == {"train": 32, "val": 16}
    assert document == original and selected[0]["boxes"] == original["images"][0]["boxes"]
    document["images"].reverse()
    assert select_rows(document)[0] == selected
    for field, value in (("split", "newtest"), ("image", "/blind/file.jpg"),
                         ("scene_id", "SPD:yizhuang09:1:0058"),
                         ("camera_id", "SPD:yizhuang09:1"),
                         ("source_sha256", original["images"][0]["source_sha256"])):
        bad = copy.deepcopy(original)
        bad["images"][-1][field] = value
        try:
            select_rows(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe/overlapping row accepted: {field}")
    bad = copy.deepcopy(original)
    bad["images"][0]["boxes"].append([0, 0, 2, 2])
    bad["images"][0]["labels"].append(0)
    try:
        select_rows(bad)
    except ValueError as error:
        assert "not enough" in str(error)
    else:
        raise AssertionError("small extra target was dropped instead of excluding whole frame")
    args = build_parser().parse_args(training_arguments(Path("manifest"), Path("cache"), "a" * 64))
    assert args.epochs == 75 and args.max_steps == 300 and args.checkpoint_kind == "diagnostic"
    assert not args.mosaic and not args.amp and args.resume is None
    assert args.batch_size == 8 and args.accum_steps == 1
    protocol = protocol_for(args, 4, None)
    assert protocol["optimizer_steps_per_epoch"] * protocol["epochs"] == 300
    assert protocol["warmup_epochs"] == 0 and protocol["base_lr"] == .001
    print("PASS tiny-fit selection/isolation/full-target-preservation/protocol")


if __name__ == "__main__":
    main()
