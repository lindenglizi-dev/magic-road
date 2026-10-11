# Public video ground-truth source check

Checked 2026-10-02.  No source below is promoted to a complete formal
RoadYOLO road dataset.  In particular, missing categories are not background,
and frames from one source sequence are one indivisible scene group.

## VID train expansion check (2026-10-03)

The official VisDrone dataset page publishes the Task 2 VID train set as 7.53
GB at Google file ID `1NSNapZQHar22OYzQYuXCugA3QlMndzvw`.  An anonymous HEAD
request to the fixed direct URL returned HTTP 200, `application/octet-stream`,
and exactly 8,080,572,990 bytes:

`https://drive.usercontent.google.com/download?id=1NSNapZQHar22OYzQYuXCugA3QlMndzvw&export=download&confirm=t`

The official VID toolkit says training and validation do not overlap, lists 56
training clips and 24,201 frames, states that training annotations are public,
and says different objects and ignored regions are manually annotated in every
frame.  It names the same ten categories and the same GT score/ignore format as
the already checked validation set, so the existing person/vehicle/ignore
mapping applies without a new adapter.

These 56 clips enlarge the development train/validation pool and should improve
coverage of bus, truck, bicycle, and motor compared with the seven-clip pool.
They do not create a blind test set.  Also, 56 clips must not be reported as 56
independent cameras: the official metadata describes multiple drone platforms
and scenarios but supplies no stable camera ID.  Whole clips remain the minimum
split unit, and camera/source-family duplication still requires manual review.

The fixed downloader refuses arbitrary URLs, uses one lock per archive, safely
resumes only when the server honors the exact byte range, verifies the declared
size and every ZIP CRC, and preserves 20 GiB of free disk.  Train data is kept
under `cnn/data/visdrone_vid_train`; it does not overwrite the validation archive
or its frozen seven-clip split.

### Local train acquisition, audit, and raw manifest

The completed train archive is 8,080,572,990 bytes with SHA-256
`3d7ddd2216524c5a12dcb55cee5bedf99f4625f7093bbf446072f40b8d9c1ea6`.
All 24,316 ZIP entries passed CRC and path/symlink checks; their total extracted
size is 8,128,351,664 bytes.  Extraction used a new staging directory and did
not overwrite the validation data.

The source audit found the officially listed 56 clips and 24,201 frames,
1,169,359 annotation rows, no duplicate rows, three frames with no annotation
rows, and 31 partially out-of-frame source boxes across seven clips.  Every one
of those boxes intersects the image and is clipped by the existing half-open
coordinate transform; none is deleted.  Actual active target counts are
pedestrian 234,305, people 94,396, bicycle 40,255, car 505,301, van 46,940,
truck 30,498, bus 9,653, and motor 102,819.  Tricycle 28,338 and
awning-tricycle 13,011 remain ignore, as do 62,369 ignored-region rows and
1,474 others rows with score zero.

The source-family proxy is the sequence prefix before the second underscore;
it yields 48 groups, not verified camera identities.  Sorting those groups and
assigning every fifth group starting at index four to validation gives a fixed,
model-independent 46-clip/19,050-frame train split and 10-clip/5,151-frame val
split.  No proxy crosses splits, and all eight selected original categories
occur in both.  No clip is assigned to `newtest`.

The density audit keeps every dense frame and every box.  Train has 249,955
person boxes (max 108/frame, 1,758 frames over 32, cap32 oracle recall 0.86334)
and 519,362 vehicle boxes (max 107/frame, 6,561 frames over 32, oracle 0.74494).
Val has 78,746 person boxes (max 64/frame, 103 frames over 32, oracle 0.98364)
and 216,104 vehicle boxes (max 136/frame, 2,966 frames over 32, oracle 0.64678).
These are postprocessing capacity ceilings only: dense training supervision is
unchanged.  In particular, this validation pool cannot support an 85% vehicle
end-to-end recall claim while the fixed 32/class output cap remains.

For comparison, the unchanged seven-clip validation split has a person cap32
oracle recall of 0.86544 (15,153 boxes, max 66/frame, 123 over-cap frames), only
1.54 percentage points above 85%; its vehicle oracle is 1.0 because its maximum
is 25/frame.  The unchanged seven-clip train split has person/vehicle oracles
0.74103/0.76114.  These limits do not alter dense training supervision and were
not used to select easier clips.

The raw manifest is
`cnn/data/visdrone_vid_train/raw_manifest/dataset.json`, SHA-256
`ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4`.
It references all 24,201 original JPEGs by absolute path, records their actual
hashes, sets `preprocess.raw_image=true`, retains the identical 1280x720
letterbox geometry and boxes, and creates no duplicate PNG directory.  The
normal data audit passes with `--no-formal-gate`; the formal gate remains false
because no independent `newtest` was opened or assigned.

## Immediate choice: VisDrone2019-VID validation

The official [VisDrone dataset page](https://github.com/VisDrone/VisDrone-Dataset)
publishes the VID validation archive as 1.49 GB.  Its Google file ID is
`1xuG7Z3IhVfGGKMe3Yj6RnrFHqo_d2a1B`; an anonymous HEAD request to the direct
download URL returned HTTP 200, `application/octet-stream`, and 1,602,397,759
bytes:

`https://drive.usercontent.google.com/download?id=1xuG7Z3IhVfGGKMe3Yj6RnrFHqo_d2a1B&export=download&confirm=t`

The official [VID toolkit documentation](https://github.com/VisDrone/VisDrone2018-VID-toolkit)
defines ten columns, 1-based frame indices, target IDs, a GT score/ignore bit,
and category IDs 0 through 11.  The project mapping is deliberately narrow:

| Official category | RoadYOLO result |
|---|---|
| pedestrian (1), people (2) | person |
| bicycle (3), car (4), van (5), truck (6), bus (9), motor (10) | vehicle |
| ignored region (0), tricycle (7), awning-tricycle (8), others (11) | ignore |
| any row with GT score 0 | ignore, regardless of category |

This is the checked anonymous video download whose taxonomy names every
requested target class.  The official toolkit says all ten categories are in
scope and that different objects and ignored regions are manually annotated in
every frame.  The official
[VID2019 paper](https://openaccess.thecvf.com/content_ICCVW_2019/papers/VISDrone/Zhu_VisDrone-VID2019_The_Vision_Meets_Drone_Object_Detection_in_Video_Challenge_ICCVW_2019_paper.pdf)
also reports evaluation over all ten categories, 56/7/16 train/validation/test
clips, and 24,198/2,846/6,322 frames.  This is sufficient to mark score-1 labels
as source-declared complete for **development training**, but not as formal
RoadYOLO road-camera acceptance:

- GT score 0 is an explicit ignore signal and is never promoted to a positive,
  even when its category name otherwise maps to person or vehicle.
- The repository publishes download links and citation instructions and says
  researchers may use the labelled test-dev set for papers.  The toolkit says
  its **code library** is research-purpose only.  There is no dataset LICENSE or
  explicit grant covering copying, modification, commercial use, or
  redistribution.  Local, non-redistributed research matches the stated intent,
  but that is an operational boundary, not a reconstructed legal licence.
- The source uses drone-mounted cameras and explicitly spans different platforms
  and scenarios.  Fixed/hovering status must be reviewed per sequence; it cannot
  be inferred from the dataset name.
- The official format does not state that a rider always has one human box and
  one separate bicycle/motor box.  The adapter never synthesizes either box.

### Local acquisition and full-sequence trial

The official validation ZIP was acquired anonymously and verified before
extraction: 1,602,397,759 bytes, SHA-256
`0e1b44481ad701cec088089ab9630b957b2bf247a759c62eba1bec9a887d3865`,
2,863 ZIP entries, 1,640,875,379 uncompressed bytes, and a successful CRC scan.
Extraction rejected absolute paths, parent traversal, drive-qualified paths,
and symlinks and did not overwrite an existing destination.  Download and
extraction receipts are stored next to `cnn/data/visdrone_vid_val/raw.zip`.

The corrected first/middle/last source audit is
`public_video_visdrone_vid_val_source_audit_first_mid_last.json`.  It found seven
sequences, 2,846 frames, 118,127 annotation rows, no frame without annotation
rows, no exact duplicate rows, and no box outside the sampled sequence
dimensions.  Actual `(category, score)` totals are:

| Category | score 1 | score 0 |
|---|---:|---:|
| pedestrian | 32,404 | 0 |
| people | 17,908 | 0 |
| bicycle | 6,022 | 0 |
| car | 31,821 | 0 |
| van | 6,842 | 0 |
| truck | 1,359 | 0 |
| bus | 264 | 0 |
| motor | 12,025 | 0 |
| tricycle | 3,769 | 0 |
| awning-tricycle | 1,718 | 0 |
| ignored region | 0 | 3,994 |
| others | 0 | 1 |

The frozen sequence-level split assigns five clips/2,222 frames to train and
two clips/624 frames to val.  Both project classes occur in both splits.  Bus
occurs only in `uav0000305_00000_v`; whole-video isolation therefore makes bus
coverage in both splits impossible.  That sequence remains in train, so the
original-category validation split has no bus.  This limitation is recorded,
not converted into background evidence.

The complete 2,846-frame conversion passed `cnn.dataset audit
--no-formal-gate`.  It contains 35,159 train person boxes, 46,639 train vehicle
boxes, 15,153 val person boxes, and 11,694 val vehicle boxes.  Its manifest
SHA-256 is
`d75d2848d939d7f2718ffcbbc1c0a07cc3b047c29e5207bf92f1eb9e150a953c`;
the integrity receipt also records every converted image SHA-256.  The normal
formal audit intentionally fails the 6-train/3-val/3-newtest scene gate.  This
is development data, not a substitute for the frozen formal road set.

`cnn.public_video` converts an extracted archive to the existing
`cnn.dataset` JSON shape and preserves category, target ID, score, truncation,
and occlusion in per-box metadata.  `--task vid` records
`manifest_status=source_declared_complete_development` and
`training_eligible=true`, while `formal_road_eligible=false` remains explicit.
`--task mot` remains fail-closed/incomplete because the official MOT task only
evaluates five categories.

```powershell
python -m cnn.public_video `
  --root cnn/data/visdrone_vid_val/extracted/VisDrone2019-VID-val `
  --output cnn/data/visdrone_vid_val/converted `
  --split-map cnn/reports/public_video_visdrone_vid_val_split.json `
  --task vid
```

The split-map is one JSON object whose keys are all seven extracted `uav...`
sequence directory names and whose values are `train` or `val`.  This produces
one dataset containing both development splits without dividing adjacent frames.
The adapter rejects missing, extra, or duplicated sequence assignments.  Freeze
the map before model fitting; it is provenance, not a parameter to tune.

Do not assign `newtest` merely because the official archive says `val`.
Downloading or visually inspecting it makes it development data for this
project.  Keep every `uav...` sequence wholly within one project split.

## KITTI tracking

The official [tracking page](https://www.cvlibs.net/datasets/kitti/eval_tracking.php)
lists 21 training and 29 test sequences and advertises 15 GB left-camera images
and 9 MB uncompressed training labels.  Anonymous direct URLs were verified:

- labels: `https://s3.eu-central-1.amazonaws.com/avg-kitti/data_tracking_label_2.zip`
  — HTTP 200, 2,259,128 compressed bytes;
- left images: `https://s3.eu-central-1.amazonaws.com/avg-kitti/data_tracking_image_2.zip`
  — HTTP 200, 15,813,146,295 bytes.

KITTI has the clearest licence of the three: its official home page states
[CC BY-NC-SA 3.0](https://www.cvlibs.net/datasets/kitti/).  It does not satisfy
the frozen taxonomy.  Official labels are Car, Van, Truck, Pedestrian,
Person_sitting, Cyclist, Tram, Misc, and DontCare.  Bus and motorcycle are not
separate classes, and Cyclist does not provide the contract's independent
person plus bicycle boxes.  The tracking page also says only Car and Pedestrian
have enough labelled instances for comprehensive evaluation.  Missing target
classes must remain unknown/ignore, never background.  The camera is mounted on
a moving car, so this is cross-view pretraining rather than fixed-camera
acceptance data.

## BDD100K box tracking

Official [format documentation](https://github.com/bdd100k/bdd100k/blob/master/doc/source/format.rst)
lists pedestrian, rider, car, truck, bus, train, motorcycle, and bicycle for box
tracking.  The official paper reports 2,000 videos, about 400k labelled frames,
and 1,400/200/400 train/validation/test videos.  It covers the requested names,
but rider is its own category and must not be silently split into independent
person and vehicle boxes.

The [data licence](https://github.com/bdd100k/bdd100k/blob/master/doc/source/license.rst)
allows educational, research, and non-profit use without a signed agreement,
subject to its notice terms.  The current official download page says
"Download at User portal".  No anonymous first-party object URL or primary-page
file size was available in this check, so BDD100K does not meet the requested
no-account acquisition condition.  It is ego-vehicle footage, not fixed-camera
data.

## Required review before any promotion

For each imported sequence record and sign off:

1. archive URL, byte count, SHA-256, extraction root, annotation SHA-256, frame
   count, and exact source/project split;
2. counts by `(category_id, GT score)`, missing referenced frames, invalid or
   clipped boxes, duplicate rows, and target-ID continuity;
3. `camera_motion = fixed | hover_drift | pan_tilt | moving | uncertain`, scene
   family, source/derivative family, and whether the scene resembles the board
   camera;
4. sampled raw-frame overlay checks for coordinate convention, score-zero rows,
   ignored regions, crowd/occlusion handling, and unlabelled target-class
   objects;
5. sampled riders: whether human and bicycle/motor have independent boxes.  If
   not demonstrated, keep affected objects/frames ignored for the frozen rider
   policy;
6. per-sequence presence of person, car/van, bus, truck, bicycle, and motor.
   Absence is a missing class, not evidence that the frame is a negative;
7. split at whole-sequence/source-family granularity.  Adjacent frames,
   transcodes, and crops of one original may not cross train/val/test.

VID development completeness is source-declared, not manually re-proven.  Only
the listed review and fixed-camera road data can support formal acceptance;
counts or model performance cannot manufacture formal annotation completeness.
