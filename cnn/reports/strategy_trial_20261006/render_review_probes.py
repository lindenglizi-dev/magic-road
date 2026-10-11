"""Enlarge a few source-box contexts; never infer or edit ground truth."""
import json
from pathlib import Path

from PIL import Image

from cnn.dataset import _refuse_blind, sha256_file


def main():
    folder = Path(__file__).resolve().parent / "train_review"
    manifest = json.loads((folder / "review_manifest.json").read_text(encoding="utf-8"))
    selected = [("train_001", 20), ("train_001", 26), ("train_033", 10), ("train_034", 8)]
    output = folder / "probes"
    output.mkdir(exist_ok=False)
    records = []
    for sample, target_id in selected:
        row = next(row for row in manifest["samples"] if row["sample_id"] == sample)
        source = Path(row["source_image"])
        _refuse_blind(source)
        assert sha256_file(source) == row["source_sha256"]
        target = next(target for target in row["source_annotations"] if target["target_id"] == target_id)
        x, y, width, height = target["bbox"]
        with Image.open(source) as image:
            rect = [max(0, int(x)-30), max(0, int(y)-30),
                    min(image.width, int(x+width)+30), min(image.height, int(y+height)+30)]
            crop = image.convert("RGB").crop(rect)
        assert crop.width > 0 and crop.height > 0
        crop = crop.resize((crop.width*4, crop.height*4), Image.Resampling.NEAREST)
        name = f"{sample}_target{target_id}.png"
        crop.save(output / name)
        records.append(dict(sample_id=sample, target_id=target_id,
                            source=str(source), source_sha256=row["source_sha256"],
                            crop_xyxy_source=rect, zoom="4x nearest, no generated content",
                            source_label=target["category"], output=name,
                            output_sha256=sha256_file(output / name)))
    with (output / "receipt.json").open("x", encoding="utf-8") as stream:
        json.dump(dict(probes=records, script_sha256=sha256_file(Path(__file__)),
                       labels_changed=False, human_review=False), stream, indent=2)
    print("four source-bound review probes generated")


if __name__ == "__main__":
    main()
