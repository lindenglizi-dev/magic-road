"""Qualitative teacher/student inference on actual raw ground images, WITHOUT GT metrics."""
import argparse
import json
from pathlib import Path

import cv2
import torch

from .dataset import _letterbox_720, _refuse_blind
from .evaluate_teacher import quantize_heads
from .integer import postprocess, resize_area
from .model import RoadYOLOS4
from .teacher import capture_raw_heads, load_official_model, teacher_input, tree_hash
from .train import sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", nargs="+", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    torch.set_num_threads(4)
    device = torch.device("cpu")
    weights = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    student = RoadYOLOS4().eval()
    if student.architecture_hash() != weights["architecture_hash"]:
        raise ValueError("student architecture mismatch")
    student.load_state_dict(weights["model"], strict=True)
    assets = Path("cnn/teacher_assets")
    source = assets / "source/YOLOX-0.3.0"
    receipt = json.loads((assets / "receipt.json").read_text(encoding="utf-8"))
    if (sha256(assets / "yolox_s.pth") != receipt["weights"]["sha256"]
            or tree_hash(source / "yolox") != receipt["source_tree_sha256"]):
        raise ValueError("teacher asset binding changed")
    teacher = load_official_model(source, assets / "yolox_s.pth", device)
    args.output.mkdir(parents=True, exist_ok=False)
    results = []
    for number, path in enumerate(args.images):
        _refuse_blind(path)
        bgr = cv2.imread(str(path))
        if bgr is None:
            raise ValueError(f"cannot decode {path}")
        rgb720, transform = _letterbox_720(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        input512 = torch.from_numpy(resize_area(rgb720)).permute(2, 0, 1).float() - 128
        row = dict(image_path=path, preprocess=dict(raw_image=True, letterbox_1280x720=transform))
        with torch.inference_mode():
            heads = dict(student=student(input512.unsqueeze(0)),
                         teacher=capture_raw_heads(teacher, teacher_input(row, device)))
        entry = dict(image=str(path), image_sha256=sha256(path), transform=transform)
        for name, output in heads.items():
            detections = postprocess(quantize_heads(output), (3276, 3276))
            entry[name] = detections
            canvas = cv2.cvtColor(rgb720, cv2.COLOR_RGB2BGR)
            # Full >=0.05 predictions remain in JSON; presentation uses >=0.5 only.
            for detection in detections:
                if detection["score_uint16"] < 32768:
                    continue
                x0, y0, x1, y1 = [round(v / 256 * 2.5) for v in detection["box_q8"]]
                label = ("person", "vehicle")[detection["label"]]
                color = ((0, 255, 0), (0, 165, 255))[detection["label"]]
                cv2.rectangle(canvas, (x0, y0), (x1, y1), color, 2)
                cv2.putText(canvas, f"{label} {detection['score_uint16']/65536:.2f}",
                            (x0, max(20, y0)), cv2.FONT_HERSHEY_SIMPLEX, .5, color, 1)
            output_image = args.output / f"{number:02d}_{name}.jpg"
            if not cv2.imwrite(str(output_image), canvas):
                raise OSError(output_image)
            entry[name + "_overlay"] = dict(path=str(output_image), sha256=sha256(output_image))
        results.append(entry)
        print(f"qualitative ground inference {number+1}/{len(args.images)}", flush=True)
    report = dict(status="qualitative_raw_ground_inference_not_validated_detection_baseline",
                  checkpoint_sha256=sha256(args.checkpoint), teacher_assets=receipt,
                  preprocessing="raw RGB -> 720p letterbox -> exact 2/5 area -> pixel-128",
                  postprocess=dict(score_floor_uint16=3276, top_k_per_class=128,
                                   max_boxes_per_class=32, nms_iou=.5),
                  images=results, precision=None, recall=None, AP50=None,
                  acceptance_eligible=False, trained=False,
                  limitation="No GT scoring: rider semantics and camera split unresolved; 3 images are source QA, not a representative validation set. FP32 host inference, not INT8 or FPGA FPS.")
    with (args.output / "report.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
