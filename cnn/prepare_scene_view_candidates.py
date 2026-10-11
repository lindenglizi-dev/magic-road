"""Build the bounded scene-view candidate booklet; never reads labels or held-out data."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cnn/reports/scene_view_choice_20261009_v1/candidates"
INTERSECTION = ROOT / "cnn/data/intersection_flow_5k/raw_v4/Intersection-Flow-5K/images/train"
GROUND = ROOT / "cnn/reports/post_review_s_20261007_v1/ground48/images"
SPD = ROOT / "cnn/reports/replacement48_spd_draft8_20261008_v2/raw"
CDNET = ROOT / "public_data/raw/cdnet_pedestrian/dataset/pedestrian detection dataset"
VISDRONE = ROOT / "cnn/data/visdrone_vid_train/extracted/VisDrone2019-VID-train/sequences"

PROBE_PATHS = [
    *(INTERSECTION / name for name in (
        "10110065.jpg", "10117923.jpg", "1662001262.927308083.jpg", "1662004131.477492809.jpg",
        "1662028917.566905499.jpg", "1662033278.316426277.jpg", "1662273395.572103977.jpg",
        "1662425101.199633837.jpg", "1662428430.356881142.jpg", "1662439960.051561117.jpg",
        "1697250696.164180994.jpg", "1697256599.958851576.jpg", "1697263705.821557522.jpg",
        "1697269090.905438423.jpg", "20216884.jpg", "2029305.jpg",
    )),
    *(GROUND / image_id / "raw.png" for image_id in (
        "VIRAT_S_000200_00_000100_000171_f0001376", "VIRAT_S_000203_03_000736_000785_f0000951",
        "VIRAT_S_000205_00_000065_000149_f0001227", "VIRAT_S_000207_02_000498_000530_f0000253",
        "VIRAT_S_010107_02_000282_000312_f0000249",
    )),
    *(SPD / name for name in (
        "spd_inf_010721.jpg", "spd_inf_010868.jpg", "spd_inf_010881.jpg", "spd_inf_010883.jpg",
        "spd_inf_010887.jpg", "spd_inf_010898.jpg", "spd_inf_010900.jpg", "spd_inf_010907.jpg",
    )),
    CDNET / "busStation/input/in000626.jpg",
    CDNET / "pedestrians/input/in000551.jpg",
    VISDRONE / "uav0000013_00000_v/0000135.jpg",
    VISDRONE / "uav0000020_00406_v/0000251.jpg",
]


def candidate(candidate_id: str, path: Path, source: str, split_role: str,
              visual_class: str, scene_type: str, uncertainty: str,
              *, sequence_id: str | None = None, camera_id: str | None = None,
              source_frame: int | None = None, note: str = "") -> dict:
    return {
        "candidate_id": candidate_id,
        "path": path,
        "source": source,
        "split_role": split_role,
        "known_source": {
            "sequence_id": sequence_id,
            "camera_id": camera_id,
            "source_frame": source_frame,
        },
        "visual_class": visual_class,
        "scene_type": scene_type,
        "uncertainty": uncertainty,
        "note": note,
    }


CANDIDATES = [
    candidate("if_train_10110065", INTERSECTION / "10110065.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "雨夜城市路口", "中；无已知 camera_id，视觉相似不等于同机位"),
    candidate("if_train_1662001262", INTERSECTION / "1662001262.927308083.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "白天多车道大路口", "中；无已知 camera_id"),
    candidate("if_train_1662028917", INTERSECTION / "1662028917.566905499.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "夜间多车道大路口", "中；无已知 camera_id"),
    candidate("if_train_1662273395", INTERSECTION / "1662273395.572103977.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "雨雾多车道大路口", "中；无已知 camera_id"),
    candidate("if_train_1662425101", INTERSECTION / "1662425101.199633837.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "白天拥挤多车道路口", "中；无已知 camera_id"),
    candidate("if_train_1697250696", INTERSECTION / "1697250696.164180994.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "白天宽幅空旷路口", "中；无已知 camera_id"),
    candidate("if_train_1697263705", INTERSECTION / "1697263705.821557522.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "白天宽幅路口", "中；与相邻候选视觉近似但未认定同机位"),
    candidate("if_train_20216884", INTERSECTION / "20216884.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "雨夜近端停止线", "中；无已知 camera_id"),
    candidate("if_train_2029305", INTERSECTION / "2029305.jpg", "Intersection-Flow-5K", "train",
              "中高位斜视", "夜间稀疏交通路口", "中；无已知 camera_id"),
    candidate("ground48_a_f1376", GROUND / "VIRAT_S_000200_00_000100_000171_f0001376/raw.png",
              "Ground48/VIRAT", "development-reviewed",
              "中高位斜视", "停车场", "低；camera_id 与 frame 来自 selection.json",
              sequence_id="VIRAT_S_000200_00_000100_000171", camera_id="virat-parking-lot-camera-a", source_frame=1376),
    candidate("ground48_b_f249", GROUND / "VIRAT_S_010107_02_000282_000312_f0000249/raw.png",
              "Ground48/VIRAT", "development-reviewed",
              "中高位斜视", "停车场与邻接道路", "低；camera_id 与 frame 来自 selection.json",
              sequence_id="VIRAT_S_010107_02_000282_000312", camera_id="virat-010107-camera-b", source_frame=249),
    candidate("spd8_010721", SPD / "spd_inf_010721.jpg", "SPD8", "development-reviewed",
              "中高位斜视", "白天大型十字路口", "中；文件名保留，未从标签推断 frame/camera",
              note="仅复用已审核/验证原图；未读取同名 JSON 标签"),
    candidate("cdnet_busstation_f626", CDNET / "busStation/input/in000626.jpg", "CDnet 2014 pedestrian", "train-view-example",
              "低至中位斜视", "公交站/建筑入口", "中；非道路严格平视，且不是完整人车训练 GT",
              sequence_id="busStation", source_frame=626, note="仅作视角示例"),
    candidate("cdnet_pedestrians_f551", CDNET / "pedestrians/input/in000551.jpg", "CDnet 2014 pedestrian", "train-view-example",
              "低至中位斜视", "人行步道", "中；非道路严格平视，且不是完整人车训练 GT",
              sequence_id="pedestrians", source_frame=551, note="仅作视角示例"),
    candidate("visdrone_0013_f135", VISDRONE / "uav0000013_00000_v/0000135.jpg", "VisDrone2019-VID", "train-development-view",
              "无人机高位斜视", "滨水步道", "低；不是严格正俯视",
              sequence_id="uav0000013_00000_v", source_frame=135),
    candidate("visdrone_0020_f251", VISDRONE / "uav0000020_00406_v/0000251.jpg", "VisDrone2019-VID", "train-development-view",
              "无人机高位斜视", "滨水道路", "低；不是严格正俯视",
              sequence_id="uav0000020_00406_v", source_frame=251),
]

CHOICE_CLASS = {
    "if_train_10110065": "A 固定斜俯视通道",
    "if_train_1662001262": "D 高位斜视密集大路口",
    "if_train_1662028917": "D 高位斜视密集大路口",
    "if_train_1662273395": "D 高位斜视密集大路口",
    "if_train_1662425101": "D 高位斜视密集大路口",
    "if_train_1697250696": "A 固定斜俯视通道",
    "if_train_1697263705": "A 固定斜俯视通道",
    "if_train_20216884": "A 固定斜俯视通道",
    "if_train_2029305": "A 固定斜俯视通道",
    "ground48_a_f1376": "C 固定斜俯视停车场园区",
    "ground48_b_f249": "C 固定斜俯视停车场园区",
    "spd8_010721": "D 高位斜视密集大路口",
    "cdnet_busstation_f626": "B 低机位/近地斜视",
    "cdnet_pedestrians_f551": "B 低机位/近地斜视",
    "visdrone_0013_f135": "E 无人机高空",
    "visdrone_0020_f251": "E 无人机高空",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_thumbnail(source: Path, destination: Path, size: tuple[int, int] = (320, 200)) -> tuple[int, int]:
    with Image.open(source) as image:
        image.load()
        original_size = image.size
        image.thumbnail(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", size, "#111827")
        canvas.paste(image.convert("RGB"), ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
        canvas.save(destination, quality=88)
    return original_size


def build_contact_sheet(rows: list[dict], destination: Path, cols: int = 4) -> None:
    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 14)
    cell_w, cell_h = 340, 255
    sheet = Image.new("RGB", (cell_w * cols, cell_h * ((len(rows) + cols - 1) // cols)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(rows):
        x, y = (index % cols) * cell_w, (index // cols) * cell_h
        with Image.open(row["thumbnail_path"]) as thumb:
            sheet.paste(thumb.convert("RGB"), (x + 10, y + 8))
        draw.text((x + 10, y + 211), f"{index + 1:02d} {row['candidate_id']}", fill="black", font=font)
        draw.text((x + 10, y + 231), f"{row['visual_class']} · {row.get('scene_type', '')}", fill="#374151", font=font)
    sheet.save(destination, quality=90)


def build_candidates() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in CANDIDATES:
        source = item["path"].resolve()
        assert source.is_file(), source
        thumb = (OUT / f"thumb_{item['candidate_id']}.jpg").resolve()
        width, height = build_thumbnail(source, thumb)
        rows.append({
            key: value for key, value in item.items() if key != "path"
        } | {
            "choice_class": CHOICE_CLASS[item["candidate_id"]],
            "original_path": str(source),
            "thumbnail_path": str(thumb),
            "sha256": sha256(source),
            "size": [width, height],
        })
    build_contact_sheet(rows[:8], OUT / "contact_sheet_1.jpg", cols=4)
    build_contact_sheet(rows[8:], OUT / "contact_sheet_2.jpg", cols=4)
    payload = {
        "schema": "scene_view_candidates_v1",
        "purpose": "visual viewpoint/scene choice only; no training or label decisions",
        "candidate_count": len(rows),
        "source_read_boundary": {
            "Intersection-Flow-5K": "train/images only; exactly 16 dispersed source images visually reviewed, 9 retained",
            "Ground48": "selection.json plus five already-reviewed raw.png images visually reviewed, 2 retained",
            "SPD8": "eight already-reviewed raw JPGs visually reviewed, 1 retained; no label JSON read",
            "CDnet": "catalog.json plus one middle train frame from busStation and pedestrians; both retained as view examples only",
            "VisDrone": "two development-split train sequence middle frames visually reviewed and retained",
        },
        "uncovered_views": [
            "严格水平平视道路机位：无可信本地代表",
            "严格正俯视/垂直俯拍：无可信本地代表",
            "明确低机位道路摄像头：无可信本地代表；CDnet 仅是低至中位行人场景对照",
        ],
        "candidates": rows,
    }
    manifest = OUT / "candidates.json"
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validate(rows)
    return payload


def build_probe() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, source in enumerate(PROBE_PATHS, 1):
        assert source.is_file(), source
        thumb = OUT / f"probe_{index:02d}.jpg"
        build_thumbnail(source, thumb)
        rows.append({
            "candidate_id": source.parent.name if source.name == "raw.png" else source.stem,
            "thumbnail_path": str(thumb),
            "visual_class": "bounded review probe",
        })
    destination = OUT / "probe_contact_sheet.jpg"
    build_contact_sheet(rows, destination)
    return destination


def validate(rows: list[dict]) -> None:
    assert 16 <= len(rows) <= 24
    assert sum(row["source"] == "Intersection-Flow-5K" for row in rows) <= 16
    for row in rows:
        source = Path(row["original_path"])
        thumb = Path(row["thumbnail_path"])
        assert not ({part.lower() for part in source.parts} & {"test", "blind", "reserve", "newtest"})
        assert source.is_absolute() and source.is_file()
        assert thumb.is_absolute() and thumb.is_file()
        assert row["sha256"] == sha256(source)
        with Image.open(source) as image:
            assert list(image.size) == row["size"] and min(image.size) > 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true", help="validate existing candidates.json")
    parser.add_argument("--probe", action="store_true", help="render the fixed bounded review set")
    parser.add_argument("--build", action="store_true", help="build final candidates, thumbnails, and contact sheets")
    args = parser.parse_args()
    manifest_path = OUT / "candidates.json"
    if args.validate:
        validate(json.loads(manifest_path.read_text(encoding="utf-8"))["candidates"])
        print(f"PASS: {manifest_path}")
        return 0
    if args.probe:
        print(build_probe())
        return 0
    if args.build:
        payload = build_candidates()
        print(f"PASS: built {payload['candidate_count']} candidates in {OUT}")
        return 0
    parser.error("choose --build, --probe, or --validate")


if __name__ == "__main__":
    raise SystemExit(main())
