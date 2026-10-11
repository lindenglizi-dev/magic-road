"""下载官方COCO标注和可追溯的有限预训练子集；不宣称道路域验收。

仅允许本脚本列出的COCO存储桶对象，不接受任意下载地址。
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import http.client
import json
from pathlib import Path
import shutil
import time
import urllib.request
import urllib.error
import zipfile
import zlib


BASE = "https://s3.amazonaws.com/images.cocodataset.org/"
TARGET_IDS = (1, 2, 3, 4, 6, 8)  # COCO category_id，不是80类数组索引。


def digest(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def fetch(relative: str, destination: Path) -> dict:
    allowed = relative in {"annotations/annotations_trainval2017.zip",
                           "zips/train2017.zip", "zips/val2017.zip"}
    allowed |= (relative.startswith(("train2017/", "val2017/"))
                and len(relative.split("/")) == 2
                and relative.split("/")[-1].removesuffix(".jpg").isdigit()
                and relative.endswith(".jpg"))
    if not allowed:
        raise ValueError("只允许官方COCO2017标注与图片")
    if destination.exists():
        if destination.stat().st_size == 0:
            raise ValueError(f"已有空文件，不覆盖：{destination}")
        return {"path": str(destination), "bytes": destination.stat().st_size,
                "sha256": digest(destination), "url": BASE + relative, "reused": True}
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    for attempt in range(3):
        offset = partial.stat().st_size if partial.exists() else 0
        headers = {"User-Agent": "RoadYOLO-research/1"}
        if offset:
            headers["Range"] = f"bytes={offset}-"
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE + relative, headers=headers),
                                        timeout=60) as response:
                if offset and response.status != 206:
                    raise ValueError("服务器不支持已有部分文件的安全续传，不覆盖")
                if offset and not response.headers.get("Content-Range", "").startswith(f"bytes {offset}-"):
                    raise ValueError("续传起点不一致")
                expected = int(response.headers["Content-Length"]) + offset
                if shutil.disk_usage(destination.parent).free < expected - offset + 256 * 1024**2:
                    raise OSError('insufficient space for remaining download plus 256MiB reserve')
                # A failed first read can leave an empty .part; append safely on retry.
                with partial.open("ab" if partial.exists() else "xb") as stream:
                    reported = offset // (256 * 1024 * 1024)
                    while block := response.read(1024 * 1024):
                        stream.write(block)
                        progress = stream.tell() // (256 * 1024 * 1024)
                        if progress > reported:
                            print(f"{relative}: {stream.tell()}/{expected} bytes", flush=True)
                            reported = progress
            if partial.stat().st_size != expected:
                raise IOError("下载大小与Content-Length不一致")
            # 同目录原子发布；已存在目标绝不覆盖。
            partial.rename(destination)
            return {"path": str(destination), "bytes": expected, "sha256": digest(destination),
                    "url": BASE + relative, "reused": False}
        except (OSError, urllib.error.URLError, http.client.HTTPException):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    raise RuntimeError("下载未完成")


def extract_images(archive: Path, image_root: Path, split: str,
                   expected_count: int | None = None) -> int:
    """Extract only flat official split JPEGs; ZIP CRC checks cover every new file."""
    if split not in ('train2017', 'val2017'):
        raise ValueError('invalid COCO split')
    count = 0
    with zipfile.ZipFile(archive) as source:
        entries = [entry for entry in source.infolist() if not entry.is_dir()]
        # Validate the entire directory before any member is extracted.
        names = set()
        for entry in entries:
            parts = entry.filename.split('/')
            if (len(parts) != 2 or parts[0] != split or
                    not parts[1].endswith('.jpg') or
                    not parts[1][:-4].isdigit() or len(parts[1][:-4]) != 12 or
                    entry.file_size > 64 * 1024 * 1024):
                raise ValueError(f'unsafe or unexpected ZIP member: {entry.filename}')
            if entry.filename in names:
                raise ValueError('duplicate archive member')
            names.add(entry.filename)
        if (len(entries) > 118287 or
                (expected_count is not None and len(entries) != expected_count) or
                sum(entry.file_size for entry in entries) > 40 * 1024**3):
            raise ValueError('archive exceeds COCO image count/size contract')
        missing_bytes = sum(entry.file_size for entry in entries
                            if not (image_root / entry.filename).exists())
        if shutil.disk_usage(archive.parent).free < missing_bytes + 256 * 1024**2:
            raise OSError('insufficient space for remaining extraction plus 256MiB reserve')
        for entry in entries:
            destination = image_root / entry.filename
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                crc = 0
                with destination.open('rb') as handle:
                    for block in iter(lambda: handle.read(1024 * 1024), b''):
                        crc = zlib.crc32(block, crc)
                if destination.stat().st_size != entry.file_size or crc != entry.CRC:
                    raise ValueError(f'existing image differs from official archive: {destination}')
            else:
                partial = destination.with_suffix('.jpg.extracting')
                # Preserve failed extraction for diagnosis rather than overwriting it.
                with source.open(entry) as input_stream, partial.open('xb') as output:
                    shutil.copyfileobj(input_stream, output, 1024 * 1024)
                partial.rename(destination)
            count += 1
            if count % 5000 == 0:
                print(f'{split}: extracted {count}', flush=True)
    return count


def select_images(annotation: dict, count: int) -> list[dict]:
    """六种原类轮流取样；ID哈希顺序固定，不根据模型成绩选图。"""
    if count < 1:
        raise ValueError("图片数量必须为正")
    members = {category: set() for category in TARGET_IDS}
    for row in annotation["annotations"]:
        if row["category_id"] in members and not row.get("iscrowd", 0):
            members[row["category_id"]].add(row["image_id"])
    ordered = {category: iter(sorted(ids, key=lambda value: hashlib.sha256(
        f"42:{value}".encode()).hexdigest())) for category, ids in members.items()}
    selected: set[int] = set()
    active = list(TARGET_IDS)
    while len(selected) < count and active:
        for category in tuple(active):
            try:
                selected.add(next(ordered[category]))
            except StopIteration:
                active.remove(category)
            if len(selected) == count:
                break
    return [image for image in annotation["images"] if image["id"] in selected]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--train-images", type=int, default=96)
    parser.add_argument("--val-images", type=int, default=32)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--full", action="store_true",
                        help="Download official complete train/val image ZIPs, not a subset")
    args = parser.parse_args()
    report = args.root / ('download_receipt_full2017.json' if args.full else
                         f'download_receipt_{args.train_images}_{args.val_images}.json')
    if report.exists():
        raise FileExistsError(f'保留已有收据：{report}')
    if args.full:
        args.root.mkdir(parents=True, exist_ok=True)
        if shutil.disk_usage(args.root).free < 45 * 1024**3:
            raise OSError('完整COCO下载/解压预留45GiB，空间不足；不自动删除文件')
    archive = args.root / "annotations_trainval2017.zip"
    annotation_names = ("instances_train2017.json", "instances_val2017.json")
    annotations = [args.root / "annotations" / name for name in annotation_names]
    receipts = []
    receipts.append(fetch("annotations/annotations_trainval2017.zip", archive))
    with zipfile.ZipFile(archive) as source:
        for path in annotations:
            entry = source.getinfo('annotations/' + path.name)
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                partial = path.with_suffix('.json.extracting')
                with source.open(entry) as input_stream, partial.open('xb') as output:
                    shutil.copyfileobj(input_stream, output, 1024 * 1024)
                partial.rename(path)
            crc = 0
            with path.open('rb') as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b''):
                    crc = zlib.crc32(block, crc)
            if path.stat().st_size != entry.file_size or crc != entry.CRC:
                raise ValueError(f'annotation differs from official archive: {path}')
    full_counts = {}
    if args.full:
        for split in ('train2017', 'val2017'):
            image_archive = args.root / f'{split}.zip'
            receipts.append(fetch(f'zips/{split}.zip', image_archive))
            full_counts[split] = extract_images(image_archive, args.root / 'images', split,
                                                 118287 if split == 'train2017' else 5000)
        if full_counts != {'train2017': 118287, 'val2017': 5000}:
            raise ValueError(f'COCO2017 image count mismatch: {full_counts}')
    subset_sources = () if args.full else zip(annotations, ('train2017', 'val2017'),
                                              (args.train_images, args.val_images), strict=True)
    for path, split, count in subset_sources:
        with path.open(encoding="utf-8") as stream:
            selected = select_images(json.load(stream), count)
        print(f"{split}: 下载{len(selected)}张固定选样图片", flush=True)
        with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as executor:
            jobs = [executor.submit(fetch, split + "/" + image["file_name"],
                                    args.root / "images" / split / image["file_name"])
                    for image in selected]
            for index, job in enumerate(jobs):
                receipts.append(job.result())
                if (index + 1) % 16 == 0:
                    print(f"{split}: {index + 1}/{len(jobs)}", flush=True)
    receipt = {"kind": ('coco_full_pretrain_not_road_acceptance' if args.full else
                        'coco_pretrain_subset_not_road_acceptance'),
               "source": "https://cocodataset.org/#download",
               "terms": "https://cocodataset.org/#termsofuse",
               "annotation_files": [{"path": str(path), "sha256": digest(path)} for path in annotations],
               "image_json_paths": [{"annotation_json": str(path),
                                     "image_root": str(args.root / "images" / split),
                                     "split": split.removesuffix("2017"),
                                     "source_url": "https://cocodataset.org/#download",
                                     "license_url": "https://cocodataset.org/#termsofuse"}
                                    for path, split in zip(annotations, ("train2017", "val2017"), strict=True)],
               "image_selection": 'all_official_2017_images' if args.full else "category_round_robin_sha256_seed42",
               "full_image_counts": full_counts,
               "downloads": receipts, "formal_road_acceptance_eligible": False}
    with report.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(str(report), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
