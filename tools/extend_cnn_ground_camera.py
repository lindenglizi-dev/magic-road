"""Acquire one bounded official development candidate, never training or blind data."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import urllib.request

import cv2

from tools.prepare_cnn_ground_review import (
    ROOT, LICENSE_RECEIPT, CATALOG, sha256, write_json, extension_rows,
    validate_boxes, evenly_spaced, assign_time_groups, decode_clip,
)

CLIP = "VIRAT_S_010000_02_000388_000421"
API = "https://data.kitware.com/api/v1/"
FILES = [("56f5877b8d777f753209cad4", CLIP + ".mp4"),
         ("56f57ebb8d777f753209c05b", CLIP + ".viratdata.objects.txt")]
OUT = ROOT / "cnn/reports/strategy_trial_20261006/third_camera_candidate"


def get_json(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def download(item_id, name, folder):
    metadata = get_json(API + "item/" + item_id + "/files")
    if len(metadata) != 1 or metadata[0]["name"] != name:
        raise ValueError("official file identity mismatch")
    info = metadata[0]
    if not 0 < info["size"] <= 8 * 1024 * 1024 or not info.get("sha512"):
        raise ValueError("candidate exceeds bounded budget or lacks official SHA512")
    destination = folder / name
    digest, size = hashlib.sha512(), 0
    with urllib.request.urlopen(API + "item/" + item_id + "/download", timeout=45) as response:
        with destination.open("xb") as stream:
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                if size > info["size"]:
                    raise ValueError("download exceeds official size")
                digest.update(chunk)
                stream.write(chunk)
    if size != info["size"] or digest.hexdigest() != info["sha512"]:
        raise ValueError("official size/SHA512 verification failed")
    return dict(path=str(destination), sha256=sha256(destination),
                official_file=info, download_url=API + "item/" + item_id + "/download")


def build():
    acceptance = json.loads(LICENSE_RECEIPT.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if not acceptance.get("accepted") or sha256(LICENSE_RECEIPT) != catalog["user_acceptance_receipt"]["receipt_sha256"]:
        raise ValueError("accepted official usage receipt required")
    if OUT.exists():
        raise FileExistsError("preserve prior candidate; do not overwrite or redownload")
    OUT.mkdir()
    sources = OUT / "sources"
    sources.mkdir()
    acquired = [download(item_id, name, sources) for item_id, name in FILES]
    write_json(OUT / "official_sources.json", acquired)
    capture = cv2.VideoCapture(acquired[0]["path"])
    if not capture.isOpened():
        raise RuntimeError("candidate video cannot be opened")
    clip = dict(clip_id=CLIP, scene_id="virat-ground-010000",
                video_path=acquired[0]["path"],
                frame_count=int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
                width=int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                height=int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                fps=float(capture.get(cv2.CAP_PROP_FPS)))
    capture.release()
    if clip["frame_count"] <= 0 or clip["fps"] <= 0:
        raise ValueError("invalid video timing metadata")
    source_rows = extension_rows(Path(acquired[1]["path"]), CLIP, clip["scene_id"])
    excluded = [row for row in source_rows if row["frame_index"] == clip["frame_count"]]
    rows = [row for row in source_rows if row["frame_index"] != clip["frame_count"]]
    validate_boxes(rows, clip["frame_count"], clip["width"], clip["height"])
    by_frame = defaultdict(list)
    for row in rows:
        by_frame[row["frame_index"]].append(row)
    eligible = sorted(frame for frame, boxes in by_frame.items()
                      if {row["label"] for row in boxes} >= {"ped", "vehicle"})
    if len(eligible) < 24:
        write_json(OUT / "failure.json", dict(status="insufficient_source_cooccurrence_frames",
                   eligible_frames=len(eligible), required_frames=24, clip=clip,
                   source_types=dict(Counter(row["original_type"] for row in rows)),
                   source_integrity_verified=True, training_started=False))
    chosen = evenly_spaced(eligible, 24)
    samples = [dict(sample_id=f"tc{index:03d}", clip_id=CLIP,
                    frame_index=frame, timestamp_ms=1000 * frame / clip["fps"],
                    camera_identity="pending_visual_verification",
                    annotation_complete=False, training_eligible=False,
                    human_review=None)
               for index, frame in enumerate(chosen)]
    for name in ("raw_frames", "official_overlays"):
        (OUT / name).mkdir()
    decode = decode_clip(clip, samples, {frame: by_frame[frame] for frame in chosen}, OUT)
    selected_rows = [row for frame in chosen for row in by_frame[frame]]
    groups = assign_time_groups(selected_rows, {CLIP: clip["fps"]})
    write_json(OUT / "review_manifest.json", dict(clip=clip, frames=samples,
               source_boxes=selected_rows, excluded_terminal_rows=excluded,
               source_time_groups=groups, source_box_counts=dict(Counter(row["label"] for row in selected_rows)),
               selection_fixed_before_predictions=True, annotation_complete=False,
               training_eligible=False, formal_acceptance=False))
    hashes = {path.relative_to(OUT).as_posix(): sha256(path)
              for path in sorted(OUT.rglob("*")) if path.is_file()}
    write_json(OUT / "artifact_hashes.json", hashes)
    result = dict(status="candidate_prepared_camera_identity_and_annotations_pending",
                  frames=len(samples), decode=decode, source_time_groups=groups,
                  camera_count_claimed=False, training_started=False,
                  blind_reserve_accessed=False, human_signed_frames=0,
                  license_receipt_sha256=sha256(LICENSE_RECEIPT),
                  script_sha256=sha256(Path(__file__)),
                  artifact_hashes_sha256=sha256(OUT / "artifact_hashes.json"))
    write_json(OUT / "receipt.json", result)
    print(json.dumps(result, ensure_ascii=False))


def verify():
    receipt = json.loads((OUT / "receipt.json").read_text(encoding="utf-8"))
    assert sha256(OUT / "artifact_hashes.json") == receipt["artifact_hashes_sha256"]
    artifacts = json.loads((OUT / "artifact_hashes.json").read_text(encoding="utf-8"))
    for name, digest in artifacts.items():
        path = (OUT / name).resolve()
        assert OUT.resolve() in path.parents
        assert sha256(path) == digest, name
    print(json.dumps(dict(status="verified", artifacts=len(artifacts))))


def prepare_person_review():
    """Reuse the second verified download; do not claim missing vehicle GT complete."""
    global OUT
    prior = OUT
    acquired = json.loads((prior / "official_sources.json").read_text(encoding="utf-8"))
    failure = json.loads((prior / "failure.json").read_text(encoding="utf-8"))
    for item in acquired:
        assert sha256(Path(item["path"])) == item["sha256"]
        assert Path(item["path"]).stat().st_size == item["official_file"]["size"]
    OUT = prior.parent / "third_camera_person_review"
    if OUT.exists():
        raise FileExistsError("preserve existing person-only review")
    clip = failure["clip"]
    clip["scene_id"] = "virat-ground-010001"
    rows = extension_rows(Path(acquired[1]["path"]), CLIP, clip["scene_id"])
    excluded = [row for row in rows if row["frame_index"] == clip["frame_count"]]
    rows = [row for row in rows if row["frame_index"] != clip["frame_count"]]
    validate_boxes(rows, clip["frame_count"], clip["width"], clip["height"])
    by_frame = defaultdict(list)
    for row in rows:
        by_frame[row["frame_index"]].append(row)
    chosen = evenly_spaced(sorted(frame for frame, boxes in by_frame.items()
                                  if any(row["label"] == "ped" for row in boxes)), 24)
    samples = [dict(sample_id=f"tc{index:03d}", clip_id=CLIP, frame_index=frame,
                    timestamp_ms=1000 * frame / clip["fps"], human_review=None,
                    annotation_complete=False, training_eligible=False)
               for index, frame in enumerate(chosen)]
    OUT.mkdir()
    for name in ("raw_frames", "official_overlays"):
        (OUT / name).mkdir()
    decode = decode_clip(clip, samples, {frame: by_frame[frame] for frame in chosen}, OUT)
    selected = [row for frame in chosen for row in by_frame[frame]]
    groups = assign_time_groups(selected, {CLIP: clip["fps"]})
    write_json(OUT / "review_manifest.json", dict(clip=clip, frames=samples,
               source_boxes=selected, excluded_terminal_rows=excluded, sources=acquired,
               selection="24 evenly spaced source-person frames, fixed before prediction",
               source_vehicle_boxes=0, unannotated_regions_are_background=False,
               source_time_groups=groups, annotation_complete=False,
               training_eligible=False, formal_acceptance=False))
    hashes = {path.relative_to(OUT).as_posix(): sha256(path)
              for path in sorted(OUT.rglob("*")) if path.is_file()}
    write_json(OUT / "artifact_hashes.json", hashes)
    write_json(OUT / "receipt.json", dict(status="review_material_only",
               frames=24, decode=decode, source_time_groups=groups,
               source_integrity_verified=True, human_signed_frames=0,
               camera_identity_verified=False, training_started=False,
               minimum_frame_gap_ms=min((b-a)*1000/clip["fps"] for a,b in zip(chosen,chosen[1:])),
               artifact_hashes_sha256=sha256(OUT / "artifact_hashes.json")))
    verify()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--second-candidate", action="store_true")
    parser.add_argument("--prepare-person-review", action="store_true")
    args = parser.parse_args()
    if args.second_candidate or args.prepare_person_review:
        CLIP = "VIRAT_S_010001_00_000019_000065"
        FILES = [("56f587848d777f753209cae9", CLIP + ".mp4"),
                 ("56f57ebf8d777f753209c09a", CLIP + ".viratdata.objects.txt")]
        OUT = OUT.parent / "third_camera_candidate_2"
    if args.prepare_person_review:
        prepare_person_review()
    else:
        verify() if args.verify else build()
