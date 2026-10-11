"""Build small, auditable FP32 YOLOX-S dense-teacher caches.

The official teacher runs at 1024x576.  Its stride-8/16/32 raw heads have the
same grids as the student's stride-4/8/16 heads after the 0.5 coordinate map.
Only raw final-convolution outputs are cached; decoded detections are rejected.
"""

from __future__ import annotations

import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path
import sys
import urllib.request
import zipfile

import cv2
import numpy as np
import torch
from torch import Tensor

try:
    from .dataset import _letterbox_720, _refuse_blind
    from .model import RoadYOLOS4
    from .train import (CLASS_CONTRACT, PREPROCESS_CONTRACT, dataset_content_hash,
                        load_dataset_manifest, sha256)
except ImportError:  # python cnn/teacher.py
    from dataset import _letterbox_720, _refuse_blind
    from model import RoadYOLOS4
    from train import (CLASS_CONTRACT, PREPROCESS_CONTRACT, dataset_content_hash,
                       load_dataset_manifest, sha256)


SOURCE_URL = "https://github.com/Megvii-BaseDetection/YOLOX/archive/refs/tags/0.3.0.zip"
WEIGHT_URL = (
    "https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth"
)
SOURCE_VERSION = "0.3.0"
SOURCE_COMMIT_SHORT = "4197784"
COCO_PERSON = 0
COCO_VEHICLE = (1, 2, 3, 5, 7)
EXPECTED_HEADS = ((72, 128), (36, 64), (18, 32))
TEACHER_PREPROCESS = {
    "source": "original image bytes, never prepared 512x288 pixels",
    "color": "BGR (official non-legacy YOLOX convention)",
    "geometry": "center letterbox to 1280x720, then cv2.INTER_AREA to 1024x576",
    "range": "float32 0..255, no mean/std normalization",
    "teacher_strides": [8, 16, 32],
    "source_to_student_coordinate_factor": 0.5,
}


def json_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*.py") if path.is_file())
    if not files:
        raise ValueError(f"no YOLOX Python source under {root}")
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest()


def _download(url: str, destination: Path) -> None:
    if destination.is_file() and destination.stat().st_size:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "RoadYOLO-teacher/1"})
    with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
        while chunk := response.read(1 << 20):
            output.write(chunk)
    if not temporary.stat().st_size:
        raise ValueError(f"empty download: {url}")
    temporary.replace(destination)


def fetch_assets(assets: Path) -> dict[str, object]:
    source_zip = assets / "YOLOX-0.3.0.zip"
    checkpoint = assets / "yolox_s.pth"
    _download(SOURCE_URL, source_zip)
    _download(WEIGHT_URL, checkpoint)
    source_root = assets / "source" / "YOLOX-0.3.0"
    if not (source_root / "yolox" / "models" / "yolox.py").is_file():
        with zipfile.ZipFile(source_zip) as archive:
            prefix = "YOLOX-0.3.0/"
            selected = [name for name in archive.namelist()
                        if name.startswith(prefix + "yolox/")
                        or name in {prefix + "LICENSE", prefix + "README.md"}]
            if not selected:
                raise ValueError("official archive lacks the YOLOX source tree")
            destination_root = (assets / "source").resolve()
            for name in selected:
                destination = (assets / "source" / name).resolve()
                if destination_root not in destination.parents and destination != destination_root:
                    raise ValueError(f"unsafe archive member: {name}")
                if name.endswith("/"):
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    continue
                with archive.open(name) as source, destination.open("xb") as output:
                    while chunk := source.read(1 << 20):
                        output.write(chunk)
    receipt = {
        "format": "road-yolo-official-teacher-assets-v1",
        "source": {"url": SOURCE_URL, "version": SOURCE_VERSION,
                   "commit_short": SOURCE_COMMIT_SHORT, "sha256": sha256(source_zip)},
        "weights": {"url": WEIGHT_URL, "benchmark": "YOLOX-S 40.5 COCO AP",
                    "dtype": "FP32", "sha256": sha256(checkpoint)},
        "license": {"name": "Apache-2.0", "path": str(source_root / "LICENSE")},
        "source_tree_sha256": tree_hash(source_root / "yolox"),
        "runtime_dependencies": {
            "torch": torch.__version__, "loguru": metadata.version("loguru"),
            "thop": metadata.version("thop"),
        },
    }
    receipt_path = assets / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def load_official_model(source_root: Path, checkpoint_path: Path,
                        device: torch.device) -> torch.nn.Module:
    if not (source_root / "yolox" / "models").is_dir():
        raise ValueError(f"not a YOLOX source checkout: {source_root}")
    sys.path.insert(0, str(source_root.resolve()))
    try:
        from yolox.models import YOLOPAFPN, YOLOX, YOLOXHead
    finally:
        sys.path.pop(0)
    backbone = YOLOPAFPN(0.33, 0.50, in_channels=[256, 512, 1024], act="silu")
    head = YOLOXHead(80, 0.50, in_channels=[256, 512, 1024], act="silu")
    model = YOLOX(backbone, head)
    # No unsafe pickle fallback: incompatible checkpoints fail here.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    state = checkpoint.get("model") if isinstance(checkpoint, dict) else None
    if not isinstance(state, dict):
        raise ValueError("official checkpoint has no tensor model state")
    model.load_state_dict(state, strict=True)
    model.float().eval().to(device)
    if any(parameter.dtype != torch.float32 for parameter in model.parameters()):
        raise ValueError("teacher parameters are not FP32")
    return model


def merge_class_logits(class_logits: Tensor) -> Tensor:
    if class_logits.ndim != 4 or class_logits.shape[1] != 80:
        raise ValueError("teacher classification head must be BCHW with 80 COCO classes")
    person = class_logits[:, COCO_PERSON:COCO_PERSON + 1].float()
    vehicle_probability = class_logits[:, COCO_VEHICLE].float().sigmoid().amax(
        dim=1, keepdim=True)
    vehicle = torch.logit(vehicle_probability.clamp(1e-6, 1.0 - 1e-6))
    return torch.cat((person, vehicle), dim=1)


def adapt_raw_head(regression: Tensor, objectness: Tensor,
                   classification: Tensor) -> Tensor:
    if (regression.ndim != 4 or regression.shape[1] != 4
            or objectness.ndim != 4 or objectness.shape[1] != 1
            or classification.ndim != 4
            or not (regression.shape[0] == objectness.shape[0] == classification.shape[0])
            or regression.shape[2:] != objectness.shape[2:]
            or regression.shape[2:] != classification.shape[2:]):
        raise ValueError("raw teacher heads have incompatible BCHW shapes")
    regression = regression.float().clone()
    regression[:, 2:4].clamp_(-4.0, 3.5)
    return torch.cat((regression, objectness.float(), merge_class_logits(classification)), dim=1)


def capture_raw_heads(model: torch.nn.Module, inputs: Tensor) -> list[Tensor]:
    head = getattr(model, "head", None)
    families = (getattr(head, "reg_preds", None), getattr(head, "obj_preds", None),
                getattr(head, "cls_preds", None))
    if any(not isinstance(family, torch.nn.ModuleList) or len(family) != 3
           for family in families):
        raise ValueError("official YOLOX head layout changed; raw final heads unavailable")
    captured: list[list[Tensor | None]] = [[None] * 3 for _ in range(3)]
    handles = []
    for family_index, family in enumerate(families):
        for scale, module in enumerate(family):
            def hook(_module: torch.nn.Module, _args: tuple[Tensor, ...], output: Tensor,
                     family_index: int = family_index, scale: int = scale) -> None:
                captured[family_index][scale] = output.detach()
            handles.append(module.register_forward_hook(hook))
    try:
        with torch.inference_mode():
            model(inputs.float())
    finally:
        for handle in handles:
            handle.remove()
    result = []
    for scale, expected_hw in enumerate(EXPECTED_HEADS):
        reg, obj, cls = (captured[index][scale] for index in range(3))
        if reg is None or obj is None or cls is None:
            raise ValueError(f"teacher scale {scale} raw hooks did not fire")
        adapted = adapt_raw_head(reg, obj, cls)
        if tuple(adapted.shape) != (inputs.shape[0], 7, *expected_hw):
            raise ValueError(f"teacher scale {scale} shape {tuple(adapted.shape)}")
        result.append(adapted)
    return result


def teacher_input(row: dict[str, object], device: torch.device) -> Tensor:
    preprocess = row.get("preprocess")
    if not isinstance(preprocess, dict) or preprocess.get("raw_image") is not True:
        raise ValueError("1024x576 teacher requires preprocess.raw_image=true source rows")
    bgr = cv2.imread(str(row["image_path"]), cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError(f"cannot decode raw teacher image: {row['image_path']}")
    letterboxed, transform = _letterbox_720(bgr)
    if preprocess.get("letterbox_1280x720") != transform:
        raise ValueError(f"teacher source geometry mismatch: {row['image_path']}")
    high_resolution = cv2.resize(letterboxed, (1024, 576), interpolation=cv2.INTER_AREA)
    tensor = torch.from_numpy(np.ascontiguousarray(high_resolution)).permute(2, 0, 1)
    return tensor.unsqueeze(0).to(device=device, dtype=torch.float32)


def validate_cache_metadata(payload: dict[str, object], expected: dict[str, object]) -> None:
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(f"teacher cache {key} mismatch")
    if payload.get("inference_dtype") != "float32" or payload.get("storage_dtype") != "float16":
        raise ValueError("teacher cache precision contract mismatch")


def verify_cache(cache: Path, report_path: Path) -> dict[str, object]:
    if report_path.exists():
        raise FileExistsError(f"preserve existing verification report: {report_path}")
    payload = torch.load(cache, map_location="cpu", weights_only=True)
    items = payload.get("items")
    if not isinstance(items, dict) or len(items) != payload.get("item_count"):
        raise ValueError("teacher cache item count mismatch")
    expected_shapes = tuple((7, *shape) for shape in EXPECTED_HEADS)
    for key, item in items.items():
        if not isinstance(item, dict) or set(item) != {"heads"}:
            raise ValueError(f"teacher item {key} contains non-head payload")
        heads = item["heads"]
        if (not isinstance(heads, list) or tuple(tuple(head.shape) for head in heads)
                != expected_shapes or any(head.dtype != torch.float16 for head in heads)):
            raise ValueError(f"teacher item {key} shape/dtype mismatch")
    report = {
        "status": "passed_cache_structure_and_binding_metadata",
        "cache": str(cache.resolve()), "cache_sha256": sha256(cache),
        "cache_bytes": cache.stat().st_size, "item_count": len(items),
        "head_shapes_chw": expected_shapes, "storage_dtype": "float16",
        "inference_dtype": payload.get("inference_dtype"),
        "student_architecture_hash": payload.get("student_architecture_hash"),
        "dataset_sha256": payload.get("dataset_sha256"),
        "dataset_content_sha256": payload.get("dataset_content_sha256"),
        "teacher_source_sha256": payload.get("teacher_source_sha256"),
        "teacher_weight_sha256": payload.get("teacher_weight_sha256"),
        "teacher_preprocess_sha256": payload.get("teacher_preprocess_sha256"),
        "ground_truth_policy": payload.get("ground_truth_policy"),
        "evidence_boundary": "two-image integration cache; not full distillation or accuracy evidence",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def _prepare_cache(dataset_path, source_root, checkpoint_path, split, device):
    _refuse_blind(dataset_path)
    preview = json.loads(dataset_path.read_text(encoding="utf-8"))
    if any(row["split"] not in ("train", "val") for row in preview["images"]):
        raise ValueError("teacher cache requires development-only train/val manifest")
    for row in preview["images"]:
        _refuse_blind(dataset_path.parent / row["image"])
    _manifest, rows = load_dataset_manifest(dataset_path.resolve())
    selected = [row for row in rows if row["split"] == split]
    if not selected:
        raise ValueError(f"dataset has no rows for split {split}")
    if any(row.get("preprocess", {}).get("raw_image") is not True for row in selected):
        raise ValueError("all selected teacher rows must retain original raw images")

    dataset_sha256 = sha256(dataset_path)
    content_sha256 = dataset_content_hash(rows)
    source_sha256 = tree_hash(source_root / "yolox")
    weight_sha256 = sha256(checkpoint_path)
    expected = {
        "contract": "road-yolo-student-dense-v1",
        "student_architecture_hash": RoadYOLOS4().architecture_hash(),
        "strides": [4, 8, 16], "class_contract": CLASS_CONTRACT,
        "dataset_sha256": dataset_sha256,
        "dataset_content_sha256": content_sha256,
        "preprocess_contract": PREPROCESS_CONTRACT,
        "teacher_source_sha256": source_sha256,
        "teacher_weight_sha256": weight_sha256,
        "teacher_preprocess_sha256": json_hash(TEACHER_PREPROCESS),
    }
    payload: dict[str, object] = {
        **expected, "format": "road-yolo-teacher-cache-v1",
        "teacher": "official YOLOX-S FP32 40.5 AP non-legacy",
        "teacher_input": [1024, 576], "teacher_raw_strides": [8, 16, 32],
        "teacher_preprocess": TEACHER_PREPROCESS,
        "class_merge": {"person": "COCO probability index 0",
                        "vehicle": "max sigmoid probability indices 1,2,3,5,7 then logit"},
        "tw_th_clamp": [-4.0, 3.5], "inference_dtype": "float32",
        "storage_dtype": "float16", "storage_note": "converted to float32 by training loader",
        "split": split,
        "ground_truth_policy": "teacher cache contains no GT and never replaces manifest GT",
    }
    keys = [row["teacher_key"] for row in selected]
    if len(set(keys)) != len(keys):
        raise ValueError("duplicate teacher key in selected split")
    return selected, payload, load_official_model(source_root, checkpoint_path, device)


def _write_cache(selected, payload, model, device, output):
    if output.exists():
        raise FileExistsError(f"preserve existing teacher cache: {output}")
    items = {}
    for index, row in enumerate(selected, 1):
        heads = capture_raw_heads(model, teacher_input(row, device))
        if any(not torch.isfinite(head).all() or not torch.isfinite(head.half()).all()
               for head in heads):
            raise FloatingPointError("teacher head cannot be stored as finite float16")
        items[row["teacher_key"]] = {"heads": [head.squeeze(0).half().cpu() for head in heads]}
        print(json.dumps({"cached": index, "total": len(selected), "key": row["teacher_key"]}),
              flush=True)
    payload = {**payload, "item_count": len(items), "items": items}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    torch.save(payload, temporary)
    loaded = torch.load(temporary, map_location="cpu", weights_only=True)
    validate_cache_metadata(loaded, {key: payload[key] for key in (
        "dataset_sha256", "dataset_content_sha256", "teacher_weight_sha256")})
    if set(loaded["items"]) != set(items):
        raise ValueError("written teacher cache key coverage mismatch")
    temporary.replace(output)
    return {key: value for key, value in payload.items() if key != "items"}


def build_cache(dataset_path: Path, output: Path, source_root: Path,
                checkpoint_path: Path, split: str, max_images: int,
                device: torch.device, start_image: int = 0) -> dict[str, object]:
    if not 1 <= max_images <= 512 or start_image < 0:
        raise ValueError("--max-images must be 1..512 and --start-image must be nonnegative")
    if output.exists():
        raise FileExistsError(f"preserve existing teacher cache: {output}")
    rows, payload, model = _prepare_cache(dataset_path, source_root, checkpoint_path, split, device)
    selected = rows[start_image:start_image + max_images]
    if not selected:
        raise ValueError("teacher cache selection is empty")
    return _write_cache(selected, payload, model, device, output)


def build_sharded_cache(dataset_path: Path, output: Path, source_root: Path,
                        checkpoint_path: Path, shard_images: int, device: torch.device):
    """One verification/model load; complete train coverage, bounded 64-image files."""
    if not 1 <= shard_images <= 512 or output.suffix != ".json":
        raise ValueError("shard size must be 1..512 and output must be a JSON index")
    if output.exists() or output.with_suffix("").exists():
        raise FileExistsError("preserve existing teacher index or partial shard directory")
    rows, payload, model = _prepare_cache(dataset_path, source_root, checkpoint_path, "train", device)
    directory = output.with_suffix("")
    directory.mkdir(parents=True, exist_ok=False)
    shards = []
    for offset in range(0, len(rows), shard_images):
        selected = rows[offset:offset + shard_images]
        path = directory / f"shard_{len(shards):04d}.pt"
        _write_cache(selected, payload, model, device, path)
        shards.append(dict(file=path.relative_to(output.parent).as_posix(),
                           sha256=sha256(path), keys=[row["teacher_key"] for row in selected]))
    index = {**payload, "format": "road-yolo-teacher-index-v1", "item_count": len(rows),
             "shard_images": shard_images, "shards": shards}
    with output.open("x", encoding="utf-8") as stream:
        json.dump(index, stream, indent=2)
    return dict(status="complete_train_teacher_shards", item_count=len(rows),
                shards=len(shards), index_sha256=sha256(output))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    fetch = subparsers.add_parser("fetch")
    fetch.add_argument("--assets", type=Path, default=Path("cnn/teacher_assets"))
    cache = subparsers.add_parser("cache")
    cache.add_argument("--dataset", type=Path, required=True)
    cache.add_argument("--output", type=Path, required=True)
    cache.add_argument("--source-root", type=Path,
                       default=Path("cnn/teacher_assets/source/YOLOX-0.3.0"))
    cache.add_argument("--checkpoint", type=Path,
                       default=Path("cnn/teacher_assets/yolox_s.pth"))
    cache.add_argument("--split", choices=("train", "val"), default="train")
    cache.add_argument("--max-images", type=int, default=8)
    cache.add_argument("--start-image", type=int, default=0)
    cache.add_argument("--device", default="cuda")
    shards = subparsers.add_parser("cache-sharded")
    shards.add_argument("--dataset", type=Path, required=True)
    shards.add_argument("--output", type=Path, required=True)
    shards.add_argument("--source-root", type=Path,
                        default=Path("cnn/teacher_assets/source/YOLOX-0.3.0"))
    shards.add_argument("--checkpoint", type=Path, default=Path("cnn/teacher_assets/yolox_s.pth"))
    shards.add_argument("--shard-images", type=int, default=64)
    shards.add_argument("--device", default="cpu")
    verify = subparsers.add_parser("verify-cache")
    verify.add_argument("--cache", type=Path, required=True)
    verify.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "fetch":
        print(json.dumps(fetch_assets(args.assets.resolve()), indent=2))
        return 0
    if args.command == "verify-cache":
        print(json.dumps(verify_cache(args.cache.resolve(), args.output.resolve()), indent=2))
        return 0
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    if args.command == "cache-sharded":
        print(json.dumps(build_sharded_cache(args.dataset.resolve(), args.output.resolve(),
                                           args.source_root.resolve(), args.checkpoint.resolve(),
                                           args.shard_images, device), indent=2))
        return 0
    report = build_cache(args.dataset.resolve(), args.output.resolve(),
                         args.source_root.resolve(), args.checkpoint.resolve(),
                         args.split, args.max_images, device, args.start_image)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
