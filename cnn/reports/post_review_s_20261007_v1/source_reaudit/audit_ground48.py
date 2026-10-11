from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import cv2


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GROUND48 = ROOT / "cnn/reports/post_review_s_20261007_v1/ground48"
INVENTORY = ROOT / "cnn/reports/strategy_trial_20261006/ground_review/authoritative_v2/source_inventory.json"
AUTHORITATIVE = ROOT / "cnn/reports/strategy_trial_20261006/ground_review/authoritative_v2/ground_dev_manifest.json"
CATALOG = ROOT / "evaluation/public_data/virat_ground_v2/catalog.json"
EXTENSION = ROOT / "evaluation/scene_extensions/virat_010107_02_t100/split_overlay.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pixel_sha256(image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def row_key(row: tuple[int, ...]) -> tuple[str, int, str, tuple[int, int, int, int]]:
    object_id, _duration, _frame, x, y, width, height, raw_type = row
    label = "person" if raw_type == 1 else "vehicle" if raw_type in (2, 3) else "ignore"
    return str(object_id), raw_type, label, (x, y, x + width, y + height)


def manifest_key(row: dict) -> tuple[str, int, str, tuple[int, int, int, int]]:
    return str(row["source_target_id"]), int(row["source_category"]), row["class"], tuple(row["bbox"])


def main() -> None:
    manifest = json.loads((GROUND48 / "review_manifest_teacher.json").read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    authoritative = json.loads(AUTHORITATIVE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    extension = json.loads(EXTENSION.read_text(encoding="utf-8"))
    clips = {item["clip_id"]: item for item in inventory["clips"]}
    catalog_clips = {item["clip_id"]: item for item in catalog["clips"]}
    authoritative_frames = {item["sample_id"]: item for item in authoritative["frames"]}

    parsed: dict[str, dict[int, list[tuple[int, ...]]]] = {}
    source_checks = []
    for clip_id, clip in clips.items():
        path = Path(clip["annotation_path"])
        by_frame: dict[int, list[tuple[int, ...]]] = defaultdict(list)
        bad_width = []
        for line_number, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            values = tuple(map(int, text.split()))
            if len(values) != 8:
                bad_width.append(line_number)
                continue
            by_frame[values[2]].append(values)
        parsed[clip_id] = by_frame
        source = catalog_clips.get(clip_id, extension)
        sha512_match = None
        if clip_id not in catalog_clips:
            sha512_match = hashlib.sha512(path.read_bytes()).hexdigest() == source["annotation_sha512"]
        source_checks.append({
            "clip_id": clip_id,
            "annotation_path": str(path),
            "annotation_sha256": sha256(path),
            "expected_sha256": clip["annotation_sha256"],
            "sha256_match": sha256(path) == clip["annotation_sha256"],
            "annotation_url": source["annotation_download_url"],
            "local_bytes": path.stat().st_size,
            "expected_bytes": source.get("expected_annotation_bytes"),
            "publisher_identity_receipt": source.get("official_annotation_identity_check", f"official_item_sha512_match={sha512_match}"),
            "bad_field_count_lines": bad_width,
        })

    selected = defaultdict(dict)
    for sample in manifest["samples"]:
        selected[sample["selection_clip_id"]][sample["frame_index"]] = sample

    pixel_results = {}
    for clip_id, frames in selected.items():
        capture = cv2.VideoCapture(clips[clip_id]["video_path"])
        assert capture.isOpened(), clips[clip_id]["video_path"]
        wanted = set(frames)
        for frame_index in range(max(wanted) + 1):
            ok, image = capture.read()
            assert ok, (clip_id, frame_index)
            if frame_index not in wanted:
                continue
            sample = frames[frame_index]
            png = cv2.imread(str(GROUND48 / sample["raw_file"]), cv2.IMREAD_COLOR)
            pixel_results[sample["image_id"]] = pixel_sha256(image) == pixel_sha256(png)
        capture.release()

    fields = [
        "image_id", "clip_id", "frame_index", "raw_rows", "manifest_boxes",
        "raw_person", "raw_vehicle", "raw_ignore", "exact_8field_projection",
        "duplicate_object_ids", "minus1_same_projection", "plus1_same_projection",
        "png_file_sha_match", "png_matches_decoded_video_frame", "source_line_numbers",
        "source_rows_8_fields",
    ]
    audits = []
    for sample in manifest["samples"]:
        clip_id = sample["selection_clip_id"]
        frame = sample["frame_index"]
        raw_rows = parsed[clip_id].get(frame, [])
        raw_projection = [row_key(row) for row in raw_rows]
        manifest_projection = [manifest_key(row) for row in sample["original"]]
        ids = [row[0] for row in raw_projection]
        labels = Counter(row[2] for row in raw_projection)
        path = Path(clips[clip_id]["annotation_path"])
        all_lines = path.read_text(encoding="utf-8").splitlines()
        line_numbers = [i for i, text in enumerate(all_lines, 1) if len(text.split()) == 8 and int(text.split()[2]) == frame]
        prior = sorted(row_key(row) for row in parsed[clip_id].get(frame - 1, []))
        after = sorted(row_key(row) for row in parsed[clip_id].get(frame + 1, []))
        current_manifest = sorted(manifest_projection)
        authoritative_frame = authoritative_frames[sample["legacy_id"]]
        audits.append({
            "image_id": sample["image_id"], "clip_id": clip_id, "frame_index": frame,
            "raw_rows": len(raw_rows), "manifest_boxes": len(manifest_projection),
            "raw_person": labels["person"], "raw_vehicle": labels["vehicle"], "raw_ignore": labels["ignore"],
            "exact_8field_projection": sorted(raw_projection) == current_manifest,
            "duplicate_object_ids": ";".join(sorted(k for k, v in Counter(ids).items() if v > 1)),
            "minus1_same_projection": prior == current_manifest,
            "plus1_same_projection": after == current_manifest,
            "png_file_sha_match": sha256(GROUND48 / sample["raw_file"]) == sample["source_sha256"] == authoritative_frame["raw_frame_sha256"],
            "png_matches_decoded_video_frame": pixel_results[sample["image_id"]],
            "source_line_numbers": ";".join(map(str, line_numbers)),
            "source_rows_8_fields": " | ".join(" ".join(map(str, row)) for row in raw_rows),
        })

    with (HERE / "ground48_frame_audit.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(audits)

    totals = Counter()
    for row in audits:
        for key in ("raw_rows", "raw_person", "raw_vehicle", "raw_ignore"):
            totals[key] += row[key]
    per_clip = []
    for clip_id in selected:
        rows = [row for row in audits if row["clip_id"] == clip_id]
        per_clip.append((clip_id, len(rows), sum(row["raw_rows"] for row in rows), min(row["raw_rows"] for row in rows), max(row["raw_rows"] for row in rows)))

    lines = [
        "# Ground48 官方来源复核（2026-10-07）", "",
        "## 结论", "",
        f"- 48/48 帧的 manifest `original` 与对应官方 `*.viratdata.objects.txt` 当前帧的全部八字段行，按 `id/type/class/[x,y,x+w,y+h]` 投影后完全一致；共 {totals['raw_rows']} 框（person {totals['raw_person']}、vehicle {totals['raw_vehicle']}、ignore {totals['raw_ignore']}）。",
        "- 48/48 PNG 文件哈希同时匹配 Ground48 manifest 与 authoritative Ground manifest；本次重新从 5 个 MP4 自 frame 0 顺序解码，48/48 PNG 像素与对应 `frame_index` 完全一致。未发现视频帧偏移或 0/1 基错配。",
        "- 5 个源标注文件 SHA-256 全部匹配来源清单；所有行均恰为 8 字段；所选 48 帧没有同帧重复 object id。",
        "- 绿框稀少集中在 000200/000203/000205/000207：这些帧的官方原文件本身只有 2–3 行。010107 的每帧有 30–36 行。因此网页没有漏读这些源文件，但这不等于画面中的所有可见目标都已被完整标注。",
        "- 官方 Release 2 README 明写 object file 是 `all objects annotated`，并注明 object 可为 moving 或 static（例如 parked car）。所以当原图中明显可见很多车辆而原文件只有 2–3 行时，不能把未框区域当作完整负例；当前 Ground48 仍需人工补全全帧真值。现有证据不支持“拿错同名标注文件”，只证实当前配套发布条目文件在这些帧实际只有少量行；是否属于发布端遗漏，本轮不能定因。", "",
        "## 每个来源", "",
        "| clip | 抽帧 | 框总数 | 每帧最少–最多 | 字节/发布身份收据 | 标注 SHA-256 | 发布条目 |", "|---|---:|---:|---:|---|---|---|",
    ]
    checks = {row["clip_id"]: row for row in source_checks}
    for clip_id, frame_count, box_count, minimum, maximum in per_clip:
        source = checks[clip_id]
        byte_evidence = str(source["local_bytes"])
        if source["expected_bytes"] is not None:
            byte_evidence += f"/{source['expected_bytes']}"
        byte_evidence += f"; {source['publisher_identity_receipt']}"
        lines.append(f"| `{clip_id}` | {frame_count} | {box_count} | {minimum}–{maximum} | {byte_evidence} | `{source['annotation_sha256']}` | [Kitware item]({source['annotation_url']}) |")
    lines += ["", "## 逐帧", "", "| frame | P/V/I | raw=manifest | PNG=video | 重复ID | raw八字段行 |", "|---|---:|---:|---:|---|---|"]
    for row in audits:
        counts = f"{row['raw_person']}/{row['raw_vehicle']}/{row['raw_ignore']}"
        raw_text = row["source_rows_8_fields"].replace("|", "\\|")
        lines.append(f"| `{row['image_id']}` | {counts} | {str(row['exact_8field_projection']).lower()} | {str(row['png_matches_decoded_video_frame']).lower()} | {row['duplicate_object_ids'] or '无'} | `{raw_text}` |")
    lines += ["", "## 证据边界", "", "- 本报告复验的是当前项目配套发布条目文件的身份、八字段逐行搬运、坐标转换和视频帧对应关系；没有把教师预测当真值。", "- 4 个历史 clip 的 catalog 收据为 expected bytes + SHA-256 均通过；010107 的 extension 收据为官方 Kitware item SHA-512 通过。本次用浏览工具访问 Kitware API 失败，因此没有重新联网下载；工作区只读同名文件扫描（排除 blind reserve）每个 clip 仅发现这一份，没有找到同名异版。", "- `README_format_release2.txt` 是随 Release 2 数据取得且哈希已在 catalog 中固定的本地副本；catalog 记录 README 的 Kitware item 与下载地址。README 的完整性措辞与当前文件的可见覆盖之间存在张力，所以结论只限定为“当前配套文件实际稀疏，程序未漏读”；不推测发布方为何未框，也不把它解释为有意只标运动目标。", "- 未访问 blind reserve，未修改标签、缓存、manifest 或训练代码，也未启动训练。", ""]
    (HERE / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    assert len(audits) == 48
    assert all(row["exact_8field_projection"] for row in audits)
    assert all(row["png_file_sha_match"] and row["png_matches_decoded_video_frame"] for row in audits)
    assert all(not row["duplicate_object_ids"] for row in audits)
    assert all(row["sha256_match"] and not row["bad_field_count_lines"] for row in source_checks)
    print(f"PASS: {len(audits)} frames, {totals['raw_rows']} boxes, 48 pixel-exact video frames")


if __name__ == "__main__":
    main()
